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
        self.root=Path(self.directory.name)
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

    def test_bootstrap_code_guard_does_not_claim_future_implementation_status(self):
        (self.root/'apps/api/product.py').write_text('FEATURE = True\n')
        with self.assertRaisesRegex(ValueError,'Draft bootstrap contains application'):
            validator.validate(bootstrap=True)
        result=validator.validate()
        self.assertNotIn('implementation_coverage',result)
        self.assertNotIn('application_implementation_started',result)


if __name__=='__main__':unittest.main()
