"""Render human-readable frontend contracts from the canonical planning JSON."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'docs/architecture'
f=json.loads((D/'frontend-catalog.json').read_text(encoding='utf-8'))
def fmt(value):
    if isinstance(value,list):return ', '.join(str(x) for x in value)
    if isinstance(value,dict):return '; '.join(str(k)+': '+fmt(v) for k,v in value.items())
    return str(value)
def cell(value):return fmt(value).replace('|','\\|').replace('\n',' ')
def write(name,text):(D/(name+'.md')).write_text('\n'.join(line.rstrip() for line in text.splitlines()).rstrip()+'\n', encoding='utf-8', newline='\n')
lock=json.loads((ROOT/'docs/product/scope-lock.json').read_text(encoding='utf-8'))
head=f"Status: DRAFT, scope {lock['scope_version']} / architecture {lock['architecture_version']}."+' These are planned contracts, not implemented screens. Canonical data: [frontend-catalog.json](frontend-catalog.json). Backend schemas and authorization are authoritative; navigation and UI guards never confer access.\n\n'
s='# Frontend route map\n\n'+head+'Routes sharing a component retain separate trusted route bindings. Detail/dialog selection uses authorized returned identifiers, never user-entered opaque IDs. Private data is not statically generated or publicly cached. MFA setup routes use their limited setup context.\n\n'
for surface in ['public','parent','student','teacher','admin']:
    s+='## '+surface.title()+'\n\n| Route | Main component | Bindings / parameter sources | Mounted API operations | Guard |\n|---|---|---|---|---|\n'
    for r in f['routes']:
        if r['surface']==surface:s+='| '+' | '.join(cell(v) for v in [r['path'],r['component'],dict(r['parameter_sources'],**r['bindings']),r['operations'],r['guard']])+' |\n'
    s+='\n'
write('FRONTEND_ROUTE_MAP',s)
s='# Frontend component catalog\n\n'+head+'Reusable primitives accept DTOs and explicit callbacks. Feature controllers own their generated API subset and current request state. Composition is explicit and its cross-chunk ownership is included in the dependency graph. A shared renderer does not import a role-feature tree. Every field-level request/response is defined in API_SCHEMA_CATALOG.\n\n'
for name,definition in f.get('presentation_types',{}).items():s+='- **'+name+':** '+fmt(definition)+'\n'
s+='\n'
for c in f['components']:
    s+='## '+c['name']+'\n\n'
    for key in ['kind','surface','responsibility','chunk','expected_module','composition','reuse','input_sources','local_state','states','accessibility','import_boundary','requirements']:
        s+='- **'+key.replace('_',' ').title()+':** '+fmt(c.get(key,''))+'\n'
    s+='\n| Prop | Type | Required | Source |\n|---|---|---|---|\n'
    for p in c['props']:s+='| '+' | '.join(cell(p[k]) for k in ['name','type','required','source'])+' |\n'
    if not c['props']:s+='| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |\n'
    s+='\n| Operation | Request schema | Response schema | Roles | Ownership / state |\n|---|---|---|---|---|\n'
    auth={a['operation']:a for a in c['authorization']}
    for a in c['server_state']:s+='| '+' | '.join(cell(v) for v in [a['operation'],a['request'],a['response'],auth[a['operation']]['roles'],auth[a['operation']]['rule']])+' |\n'
    if not c['server_state']:s+='| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |\n'
    s+='\n'
write('FRONTEND_COMPONENT_CATALOG',s)
s='# Frontend to backend mapping\n\n'+head+f"{len(f['mappings'])} explicit route/component/API mappings cover every user HTTP operation. Internal workers and signed provider webhook ingress have no browser screen. Repeated operations reflect legitimate role-specific consumers, not extra backend implementations.\n\n"
for r in f['routes']:
    s+='## '+r['path']+'\n\nSurface: '+r['surface']+'. Main component: '+r['component']+'. Mounted composition: '+fmt(r['mounted_components'])+'.\n\n'
    s+='| Component / operation | API / schemas | Application operation | Domain objects | Repository / integration ports | Persistence boundary | Requirements |\n|---|---|---|---|---|---|---|\n'
    for m in f['mappings']:
        if m['route']==r['path']:s+='| '+' | '.join(cell(v) for v in [m['component']+' / '+m['operation'],m['method']+' '+m['api_route']+'; '+m['request']+' → '+m['response'],m['service'],m['objects'],m['ports'],m['persistence'],m['requirements']])+' |\n'
    s+='\n'
write('FRONTEND_BACKEND_MAPPING',s)
print('Rendered frontend route, component and backend mapping catalogs')
