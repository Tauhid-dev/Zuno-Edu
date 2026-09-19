"""Adversarial plan checks on isolated copies; never modify the real scope record."""
from pathlib import Path
import json
import shutil
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import validate_plan as validator


class PlanValidationTests(unittest.TestCase):
    def setUp(self):
        self.directory=tempfile.TemporaryDirectory()
        self.root=Path(self.directory.name).resolve()
        for directory in ('docs','skills'):
            shutil.copytree(ROOT/directory,self.root/directory)
        for directory in ('apps/api','packages/contracts','infra'):
            (self.root/directory).mkdir(parents=True)
            (self.root/directory/'README.md').write_text('Bootstrap fixture.\n')
        self.previous=validator.ROOT
        validator.ROOT=self.root

    def tearDown(self):
        validator.ROOT=self.previous
        self.directory.cleanup()

    def mutate_json(self,path,change):
        target=self.root/path
        value=json.loads(target.read_text())
        change(value)
        target.write_text(json.dumps(value))

    def test_complete_bootstrap_is_valid(self):
        result=validator.validate(bootstrap=True)
        self.assertEqual(result['planned_requirement_coverage'],'100%')
        self.assertFalse(result['application_implementation_started'])

    def test_omitted_authority_cannot_escape_approval(self):
        self.mutate_json('docs/product/scope-lock.json',lambda lock:lock['plan_artifacts'].pop())
        with self.assertRaisesRegex(ValueError,'Required scope witnesses missing'):
            validator.validate()

    def test_changed_design_cannot_keep_old_approval(self):
        with (self.root/'docs/product/LAUNCH_SCOPE.md').open('a') as file:
            file.write('\nUnapproved scope alteration.\n')
        with self.assertRaisesRegex(ValueError,'Stale scope witness'):
            validator.validate()

    def test_teacher_finance_contract_is_rejected(self):
        def change(catalog):
            operation=next(a for a in catalog['operations'] if a['service'].startswith('BillingService.'))
            operation['roles'].append('teacher')
        self.mutate_json('docs/architecture/backend-catalog.json',change)
        with self.assertRaisesRegex(ValueError,'Forbidden finance API role'):
            validator.validate()

    def test_missing_frontend_mapping_is_rejected(self):
        self.mutate_json('docs/architecture/frontend-catalog.json',lambda catalog:catalog['mappings'].clear())
        with self.assertRaisesRegex(ValueError,'Missing frontend/backend mapping'):
            validator.validate()

    def test_api_cannot_be_absent_from_its_implementation_chunk(self):
        catalog=json.loads((self.root/'docs/architecture/backend-catalog.json').read_text())
        operation=catalog['operations'][0]
        def change(chunks):
            owner=next(c for c in chunks if c['id']==operation['chunk'])
            owner['api_operations'].remove(operation['id'])
        self.mutate_json('docs/planning/chunks.json',change)
        with self.assertRaisesRegex(ValueError,'API absent from implementation owner'):
            validator.validate()

    def test_component_cannot_be_absent_from_its_implementation_chunk(self):
        def change(chunks):
            owner=next(c for c in chunks if 'AppShell' in c['frontend_components'])
            owner['frontend_components'].remove('AppShell')
        self.mutate_json('docs/planning/chunks.json',change)
        with self.assertRaisesRegex(ValueError,'Component absent from implementation owner'):
            validator.validate()

    def test_consumed_api_requires_its_implementation_prerequisite(self):
        # Removing this chunk's prerequisites must fail before its stale witness can
        # hide the actual readiness error. The matching manifest remains consistent.
        chunks=json.loads((self.root/'docs/planning/chunks.json').read_text())
        owner=next(c for c in chunks if c['id']=='ZE-P09-C02')
        owner['dependencies']=[]
        (self.root/'docs/planning/chunks.json').write_text(json.dumps(chunks))
        path=self.root/'docs/planning/chunks/ZE-P09-C02.md'
        parts=path.read_text().split('---',2)
        metadata=json.loads(parts[1]);metadata['dependencies']=[]
        path.write_text('---\n'+json.dumps(metadata)+'\n---'+parts[2])
        with self.assertRaisesRegex(ValueError,'Missing API prerequisite'):
            validator.validate()

    def test_reused_component_requires_its_implementation_prerequisite(self):
        def change(catalog):
            shared=next(c for c in catalog['components'] if c['name']=='ScheduleView')
            shared['composition'].append('AdminCompletionCertificates')
        self.mutate_json('docs/architecture/frontend-catalog.json',change)
        with self.assertRaisesRegex(ValueError,'Missing reused-component prerequisite'):
            validator.validate()

    def test_same_chunk_component_composition_cycle_is_rejected(self):
        def change(catalog):
            navigation=next(c for c in catalog['components'] if c['name']=='RoleNavigation')
            navigation['composition'].append('AppShell')
        self.mutate_json('docs/architecture/frontend-catalog.json',change)
        with self.assertRaisesRegex(ValueError,'Component composition cycle'):
            validator.validate()

    def test_private_route_must_include_layout_component_and_session_read(self):
        path=self.root/'docs/architecture/frontend-catalog.json'
        original=path.read_text()
        for key,value,message in [('mounted_components','ActorSessionProvider','Stale route component closure'),
                                  ('operations','API-AUTH-ME','Stale route operation closure')]:
            with self.subTest(omitted=key):
                catalog=json.loads(original)
                route=next(r for r in catalog['routes'] if r['layout']=='RoleAppShell')
                route[key].remove(value)
                path.write_text(json.dumps(catalog))
                with self.assertRaisesRegex(ValueError,message):
                    validator.validate()

    def test_mapping_on_another_route_cannot_hide_a_missing_route_mapping(self):
        def change(catalog):
            repeated=next(m for m in catalog['mappings'] if m['operation']=='API-AUTH-ME')
            catalog['mappings'].remove(repeated)
            self.assertTrue(any(m['component']==repeated['component'] and
                                m['operation']==repeated['operation'] for m in catalog['mappings']))
        self.mutate_json('docs/architecture/frontend-catalog.json',change)
        with self.assertRaisesRegex(ValueError,'Missing or stale route frontend/backend mapping'):
            validator.validate()

    def test_mapping_contract_drift_is_rejected(self):
        path=self.root/'docs/architecture/frontend-catalog.json'
        original=path.read_text()
        replacements={'method':'POST','api_route':'/api/v1/unrelated','request':'OtherRequest',
                      'response':'OtherResponse','roles':['teacher'],'authorization':'Another owner',
                      'service':'OtherService.execute','objects':[],'ports':[]}
        for key,value in replacements.items():
            with self.subTest(field=key):
                catalog=json.loads(original)
                self.assertNotEqual(catalog['mappings'][0][key],value)
                catalog['mappings'][0][key]=value
                path.write_text(json.dumps(catalog))
                with self.assertRaisesRegex(ValueError,'Stale frontend backend chain'):
                    validator.validate()

    def test_bootstrap_code_guard_does_not_claim_future_implementation_status(self):
        (self.root/'apps/api/product.py').write_text('FEATURE = True\n')
        with self.assertRaisesRegex(ValueError,'Draft bootstrap contains application'):
            validator.validate(bootstrap=True)
        result=validator.validate()
        self.assertNotIn('implementation_coverage',result)
        self.assertNotIn('application_implementation_started',result)


if __name__=='__main__':unittest.main()
