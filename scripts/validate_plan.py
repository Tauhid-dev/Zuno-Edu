#!/usr/bin/env python3
"""Validate complete planning references, coverage and contract boundaries without network or writes."""
from pathlib import Path
import argparse,json,re,sys
from reconcile_state import validate_plan,Blocked,Repository,mandatory_witnesses,witness_normalization,plan_digest,safe_path
ROOT=Path(__file__).resolve().parents[1]
EXPECTED={
'product':'PRODUCT_DEFINITION LAUNCH_SCOPE OUT_OF_SCOPE FUNCTIONAL_REQUIREMENTS NON_FUNCTIONAL_REQUIREMENTS ROLE_CAPABILITIES USER_JOURNEYS DATA_REQUIREMENTS LAUNCH_ACCEPTANCE_CRITERIA FUTURE_CONSIDERATIONS SCOPE_LOCK',
'architecture':'SYSTEM_ARCHITECTURE DOMAIN_MODEL AGGREGATES BACKEND_ARCHITECTURE BACKEND_OBJECT_CATALOG BACKEND_SERVICE_CATALOG PORTS_AND_REPOSITORIES DATA_MODEL DATABASE_SCHEMA_PLAN AUTHORIZATION_MODEL PERMISSION_MATRIX DATA_ACCESS_BOUNDARIES API_ARCHITECTURE API_CATALOG API_SCHEMA_CATALOG INTEGRATIONS BILLING_ARCHITECTURE LIVE_CLASS_ARCHITECTURE CALENDAR_ARCHITECTURE COMMUNICATION_ARCHITECTURE FILE_STORAGE_ARCHITECTURE FRONTEND_ARCHITECTURE FRONTEND_ROUTE_MAP FRONTEND_COMPONENT_CATALOG FRONTEND_STATE_AND_API_MODEL FRONTEND_BACKEND_MAPPING CODE_BLUEPRINT SECURITY_ARCHITECTURE DEPLOYMENT_ARCHITECTURE',
'standards':'ENGINEERING_STANDARDS OOP_AND_DOMAIN_STANDARDS BACKEND_STANDARDS FRONTEND_STANDARDS API_STANDARDS DATABASE_STANDARDS TESTING_STANDARDS SECURITY_STANDARDS ACCESSIBILITY_STANDARDS UI_DESIGN_SYSTEM OBSERVABILITY_STANDARDS DOCUMENTATION_STANDARDS',
'planning':'MASTER_PLAN PHASES DEPENDENCY_GRAPH REQUIREMENT_TRACEABILITY CHUNK_REGISTRY STATE_RECONCILIATION SCOPE_CHANGE_PROCESS INDEPENDENT_REVIEW BOOTSTRAP_VALIDATION'}
def require(ok,msg):
 if not ok:raise ValueError(msg)
def read(path):return json.loads((ROOT/path).read_text())
def unique(rows,key,label):
 values=[x[key] for x in rows];require(len(values)==len(set(values)),label+' identifiers duplicate');return set(values)
def validate(bootstrap=False):
 for directory,names in EXPECTED.items():
  for name in names.split():require((ROOT/'docs'/directory/(name+'.md')).is_file(),'Missing required document '+directory+'/'+name)
 req=read('docs/product/requirements.json');ids=unique(req,'id','Requirement')
 for r in req:
  require(all(r.get(k) for k in ['id','description','rationale','roles','priority','acceptance','capability']),'Incomplete requirement '+r['id'])
  require(r['priority']=='REQUIRED FOR LAUNCH','Wrong requirement priority '+r['id'])
  require(isinstance(r['acceptance'],list) and all(isinstance(x,str) and x.strip() for x in r['acceptance']),'Missing observable acceptance '+r['id'])
 chunks=validate_plan(read('docs/planning/chunks.json'));chunk_ids={c['id'] for c in chunks};b=read('docs/architecture/backend-catalog.json');f=read('docs/architecture/frontend-catalog.json')
 objs=unique(b['objects'],'name','Object');svcs=unique(b['services'],'name','Service');ports=unique(b['ports'],'name','Port');apis=unique(b['operations'],'id','API');schemas=unique(b['schemas'],'name','Schema');comps=unique(f['components'],'name','Component')
 require(len({(a['method'],a['route']) for a in b['operations']})==len(apis),'Duplicate API method/route')
 api_map={a['id']:a for a in b['operations']};schema_map={s['name']:s for s in b['schemas']}
 for a in b['operations']:
  require(set(a['requirements'])<=ids and a['requirements'],'API requirement orphan '+a['id'])
  require(a['service'].split('.')[0] in svcs,'Unknown service '+a['id'])
  require(set(a['objects'])<=objs and set(a['ports'])<=ports,'Unknown object/port '+a['id'])
  require(a['request'] in schemas and a['response'] in schemas,'Unknown request/response '+a['id'])
  require(a['ownership'] and a['roles'] and a['consumer'],'Missing authorization/consumer '+a['id'])
  require(a.get('chunk') in chunk_ids,'Unowned API '+a['id'])
  path_fields={x['name'] for x in schema_map[a['request']]['fields'] if x['location']=='path'}
  require(set(re.findall(r'\{([^}]+)\}',a['route']))<=path_fields,'Undeclared path input '+a['id'])
  if a['service'].split('.')[0] in {'BillingService','RefundService','ReportingService'}:
   require(not(set(a['roles'])&{'teacher','student'}),'Forbidden finance API role '+a['id'])
 for s in b['schemas']:
  unique(s['fields'],'name','Field in '+s['name'])
  for field in s['fields']:
   require(all(k in field for k in ['type','required','nullable','location','validation']),'Incomplete field '+s['name'])
   require(type(field['required']) is bool and type(field['nullable']) is bool,'Invalid nullability '+s['name'])
   typ=field['type'];require(typ.count('(')==typ.count(')'),'Malformed enum '+s['name'])
 for kind,names in [('objects',objs),('services',svcs),('ports',ports)]:
  for item in b[kind]:
   require(item.get('requirements') and set(item['requirements'])<=ids,'Untraced '+kind+' '+item['name'])
   require(item.get('chunks') and set(item['chunks'])<=chunk_ids,'Unowned '+kind+' '+item['name'])
   require(item.get('methods'),'Missing public behavior '+item['name'])
 coverage=set()
 for c in chunks:
  require(set(c['requirements'])<=ids,'Unknown chunk requirement '+c['id']);coverage.update(c['requirements'])
  for path in c['required_context']+c['required_skills']+c['optional_skills']:require((ROOT/path).is_file(),'Missing context/skill '+c['id']+': '+path)
  require(set(c['api_operations'])<=apis and set(c['frontend_components'])<=comps,'Unknown chunk contract '+c['id'])
  require(c['required_tests'] and c['acceptance_criteria'],'Untestable chunk '+c['id'])
  text=(ROOT/'docs/planning/chunks'/(c['id']+'.md')).read_text();front=json.loads(text.split('---',2)[1])
  for key in front:require(front[key]==c[key],'Manifest drift '+c['id']+': '+key)
 require(coverage==ids,'Orphan requirements '+str(sorted(ids-coverage)))
 # Mappings are explicit per HTTP API consumer; worker/provider operations have no UI requirement.
 mapping_pairs={(m['component'],m['operation']) for m in f['mappings']}
 mapped=set()
 for comp in f['components']:
  require(comp['chunk'] in chunk_ids and set(comp['requirements'])<=ids,'Untraced component '+comp['name'])
  require(set(comp['operations'])<=apis,'Unknown component API '+comp['name'])
  for oid in comp['operations']:
   require((comp['name'],oid) in mapping_pairs,'Missing frontend/backend mapping '+comp['name']+': '+oid);mapped.add(oid)
 for m in f['mappings']:
  require(m['component'] in comps and m['operation'] in apis,'Orphan frontend mapping')
  a=api_map[m['operation']];require(m['service']==a['service'] and m['objects']==a['objects'] and m['ports']==a['ports'],'Stale frontend backend chain '+m['operation'])
 for a in b['operations']:
  if a['method']!='WORKER' and set(a['consumer'])&{'public','parent','student','teacher','admin'}:require(a['id'] in mapped,'HTTP API has no frontend consumer '+a['id'])
 for route in f['routes']:
  require(route['component'] in comps and set(route['operations'])<=apis,'Orphan frontend route '+route['path'])
 trace=read('docs/planning/traceability.json');require(unique(trace,'requirement','Traceability')==ids,'Traceability IDs differ')
 for t in trace:
  require(set(t['chunks'])<=chunk_ids and t['chunks'] and t['tests'] and t['verification'],'Incomplete trace '+t['requirement'])
  require(set(t['api'])<=apis,'Unknown trace API '+t['requirement'])
 skills=list((ROOT/'skills').glob('*/*/SKILL.md'));require(len(skills)>=46,'Required skill inventory incomplete')
 for p in skills:
  content=p.read_text();require(content.startswith('---\n'),'Skill frontmatter missing '+str(p))
  fm=content.split('---',2)[1];require(re.search(r'^name: [a-z0-9-]+$',fm,re.M) and re.search(r'^description: .+',fm,re.M),'Invalid skill identity '+str(p))
 # No bootstrap business implementation may be smuggled into app/package/infra skeleton.
 for base in ['apps','packages','infra']:
  if bootstrap:
   require(all(p.name=='README.md' for p in (ROOT/base).rglob('*') if p.is_file()),'Draft bootstrap contains application/runtime implementation under '+base)
 lock=read('docs/product/scope-lock.json');require(re.fullmatch(r'[0-9]+\.[0-9]+',lock['scope_version']) and type(lock['architecture_version']) is int and lock['architecture_version']>=1,'Invalid scope/architecture version')
 witnesses=lock['plan_artifacts'];paths=unique(witnesses,'path','Scope witness')
 require('docs/product/scope-lock.json' not in paths,'Scope cannot witness itself')
 require(mandatory_witnesses(Repository(ROOT))<=paths,'Required scope witnesses missing')
 for artifact in witnesses:
  path=safe_path(artifact['path'])
  require(artifact.get('normalization')==witness_normalization(path),'Incorrect witness normalization '+path)
  resolved=(ROOT/path).resolve();require(resolved.is_relative_to(ROOT),'Witness escapes repository')
  require(plan_digest(resolved.read_bytes(),artifact)==artifact['sha256'],'Stale scope witness '+path)
 result={'validation':'PASS','requirements':len(ids),'planned_requirement_coverage':'100%','phases':len({c['id'][3:6] for c in chunks}),'chunks':len(chunks),'objects':len(objs),'services':len(svcs),'ports':len(ports),'api_and_worker_operations':len(apis),'schemas':len(schemas),'frontend_components':len(comps),'frontend_routes':len(f['routes']),'skills':len(skills),'scope_witnesses':len(paths)}
 if bootstrap:result.update(implementation_coverage='0%',application_implementation_started=False)
 return result
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--bootstrap',action='store_true',help='Additionally prove initial planning contains no application implementation')
 args=parser.parse_args()
 try:print(json.dumps(validate(bootstrap=args.bootstrap),indent=2))
 except (ValueError,KeyError,TypeError,OSError,Blocked) as exc:
  print(json.dumps({'validation':'FAIL','reason':str(exc)},indent=2));sys.exit(1)
