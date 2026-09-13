from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]; A=R/'docs/architecture';b=json.loads((A/'backend-catalog.json').read_text())
def put(n,s): (A/(n+'.md')).write_text(s.rstrip()+'\n')
def val(x):return ', '.join(x) if isinstance(x,list) else str(x)
def esc(x):return val(x).replace('|','\\|').replace('\n',' ')
head='Status: DRAFT, scope 1.0 / architecture 1. Canonical structured contracts: [backend-catalog.json](backend-catalog.json). These are design contracts, not implemented classes or endpoints. Implementation ownership and requirement traceability are in CODE_BLUEPRINT.md and docs/planning/REQUIREMENT_TRACEABILITY.md.\n\n'
s='# Backend object catalog\n\n'+head
for o in b['objects']:
 s+='## '+o['name']+'\n\n'
 for k in ['type','module','responsibility','attributes','invariants','authorization','dependencies','collaborators','persistence','requirements','chunks']:
  s+=f'- **{k.replace("_"," ").title()}:** {val(o.get(k,[])) or "See Code Blueprint implementation ownership"}\n'
 s+='\n| Public method | Purpose | Inputs | Output | Domain failures |\n|---|---|---|---|---|\n'
 for m in o['methods']:s+='| '+' | '.join(esc(m.get(k,'')) for k in ['name','purpose','input','output','errors'])+' |\n'
 s+='\n'
put('BACKEND_OBJECT_CATALOG',s)
s='# Backend application services\n\n'+head
for o in b['services']:
 s+='## '+o['name']+'\n\n'
 for k in ['module','responsibility','objects','ports','invariants','persistence','authorization','requirements','chunks']:
  s+=f'- **{k.title()}:** {val(o.get(k,[])) or "See Code Blueprint implementation ownership"}\n'
 s+='\n| Operation | Input → output | Purpose | Authorization | Errors | API/worker |\n|---|---|---|---|---|---|\n'
 for m in o['methods']:s+='| '+' | '.join(esc(x) for x in [m['name'],m['input']+' → '+m['output'],m['purpose'],m['authorization'],m['errors'],m['operation']])+' |\n'
 s+='\n'
put('BACKEND_SERVICE_CATALOG',s)
s='# Ports and aggregate repositories\n\n'+head+'Repositories return domain roots or named scoped projections, never an unscoped ORM session. Every application write uses UnitOfWork. Provider calls execute through durable intent outside database locks; each adapter maps provider errors to the named port failures.\n\n'
for o in b['ports']:
 s+='## '+o['name']+'\n\n'
 for k in ['type','module','responsibility','objects','adapter','persistence','invariants','requirements','chunks']:
  s+=f'- **{k.title()}:** {val(o.get(k,[])) or "See Code Blueprint implementation ownership"}\n'
 s+='\n| Interface signature | Purpose | Inputs | Output | Failures |\n|---|---|---|---|---|\n'
 for m in o['methods']:s+='| '+' | '.join(esc(m.get(k,'')) for k in ['signature','purpose','input','output','errors'])+' |\n'
 s+='\n'
put('PORTS_AND_REPOSITORIES',s)
s='# API operation catalog\n\n'+head+'All HTTP paths are versioned under `/api/v1`. WORKER entries are internal consumers and expose no HTTP route. Field-by-field request/response definitions are in [API_SCHEMA_CATALOG.md](API_SCHEMA_CATALOG.md); every operation refers to a concrete named schema, including path/query inputs. Transport conventions and status codes are in API_ARCHITECTURE.md.\n\n'
for o in b['operations']:
 s+='## '+o['id']+'\n\n'
 for label,x in [('Method/route',o['method']+' '+o['route']),('Purpose',o['purpose']),('Roles',o['roles']),('Ownership / assignment / state',o['ownership']),('Request',o['request']),('Response',o['response']),('Application operation',o['service']),('Domain objects',o['objects']),('Repository / ports',o['ports']),('Success status',o['success_status']),('Transaction',o['transaction']),('Implementation chunk',o.get('chunk','Pending final chunk binding')),('Errors',o['errors']),('Requirements',o['requirements']),('Consumers',o['consumer'])]:s+=f'- **{label}:** {val(x)}\n'
 s+='\n'
put('API_CATALOG',s)
s='# API schema catalog\n\n'+head+'`required` means key presence is mandatory; nullable independently permits null. Optional blank child fields normalize to null. Unknown write properties are rejected. Referenced DTO fields validate recursively. Enum values are closed. Path IDs are opaque UUIDs and never confer access.\n\n'
for o in b['schemas']:
 s+='## '+o['name']+'\n\n'+o['description']+'\n\n| Field | Type | Required | Nullable | Location | Validation |\n|---|---|---|---|---|---|\n'
 for f in o['fields']:s+='| '+' | '.join(esc(f[k]) for k in ['name','type','required','nullable','location','validation'])+' |\n'
 s+='\n'
put('API_SCHEMA_CATALOG',s)
print('Rendered object, service, port, API and schema catalogs')
