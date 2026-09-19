#!/usr/bin/env python3
"""Rebind a proposed DRAFT plan to its canonical contracts, without approving scope."""
from pathlib import Path
import json,re
from reconcile_state import Repository,require,validate_plan
ROOT=Path(__file__).resolve().parents[1]

def main():
    require(Repository(ROOT).git('branch','--show-current').startswith('feature/'),'Plan rendering requires a feature branch')
    require(json.loads((ROOT/'docs/product/scope-lock.json').read_text())['status']=='DRAFT','Only an explicitly proposed DRAFT plan may be rebound')
    def read(path):return json.loads((ROOT/path).read_text())
    def put(path,value):
        (ROOT/path).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n' if not isinstance(value,str) else value.rstrip()+'\n')
    b=read('docs/architecture/backend-catalog.json');f=read('docs/architecture/frontend-catalog.json');chunks=read('docs/planning/chunks.json');req=read('docs/product/requirements.json')
    byid={c['id']:c for c in chunks};apis={a['id']:a for a in b['operations']};components={c['name']:c for c in f['components']}
    for c in chunks:
        c['api_operations']=[];c['frontend_components']=[]
        c['domain_objects']=[];c['application_services']=[];c['ports']=[]
    for a in b['operations']:
        require(a.get('chunk') in byid,'Every API/worker needs explicit implementation ownership: '+a['id'])
        byid[a['chunk']]['api_operations'].append(a['id'])
    for component in f['components']:
        c=byid[component['chunk']];c['frontend_components'].append(component['name']);c['api_operations']+=component['operations'];c['requirements']+=component['requirements']
        for oid in component['operations']:
            if apis[oid]['chunk']!=c['id']:c['dependencies'].append(apis[oid]['chunk'])
        for name in component.get('composition',[]):
            require(name in components,'Unknown composition member '+name)
            owner=components[name]['chunk']
            if owner!=c['id']:c['dependencies'].append(owner)
    for c in chunks:
        for oid in c['api_operations']:
            a=apis[oid];c['domain_objects']+=a['objects'];c['application_services'].append(a['service']);c['ports']+=a['ports'];c['requirements']+=a['requirements']
        for key in ['dependencies','requirements','api_operations','frontend_components','domain_objects','application_services','ports']:
            c[key]=sorted(set(c[key]))
    validate_plan(chunks) # Reject cycles before transitive reduction.
    def ancestors(cid,seen=None):
        seen=set() if seen is None else seen
        for dep in byid[cid]['dependencies']:
            if dep not in seen:seen.add(dep);ancestors(dep,seen)
        return seen
    for c in chunks:
        deps=c['dependencies'];c['dependencies']=[d for d in deps if not any(d in ancestors(other) for other in deps if other!=d)]
    validate_plan(chunks)
    for group in ['objects','services','ports']:
        for item in b[group]:
            owners={a['chunk'] for a in b['operations'] if (item['name'] in a['objects'] if group=='objects' else item['name']==a['service'].split('.')[0] if group=='services' else item['name'] in a['ports'])}
            if owners:item['chunks']=sorted(owners)
    put('docs/architecture/backend-catalog.json',b);put('docs/planning/chunks.json',chunks)
    for c in chunks:
        path='docs/planning/chunks/'+c['id']+'.md';raw=(ROOT/path).read_text();parts=raw.split('---',2);metadata=json.loads(parts[1]);metadata={k:c[k] for k in metadata}
        body=parts[2]
        sections={'Requirements Served':', '.join(c['requirements']),'Domain Objects':', '.join(c['domain_objects']) or 'Engineering foundation only; no new product aggregate.','Application Services':', '.join(c['application_services']) or 'Engineering/presentation concern; no duplicate business behavior.','API Contracts':', '.join(c['api_operations']) or 'No feature API authored here.','Frontend Components':', '.join(c['frontend_components']) or 'No role-facing UI authored here.','Acceptance Criteria':'\n'.join('- '+t for t in c['acceptance_criteria']),'Required Tests':'\n'.join('- '+t for t in c['required_tests'])}
        for heading,value in sections.items():
            pattern=r'(## '+re.escape(heading)+r'\n\n).*?(?=\n## |\Z)'
            body,count=re.subn(pattern,lambda m:m.group(1)+value+'\n',body,flags=re.S)
            require(count==1,'Missing/duplicate manifest section '+c['id']+': '+heading)
        put(path,'---\n'+json.dumps(metadata,indent=2,ensure_ascii=False)+'\n---'+body)
    registry='# Chunk registry\n\nCanonical metadata: [chunks.json](chunks.json). All implementation remains PLANNED during bootstrap; sequence selects only eligible work after verified scope approval.\n\n| Sequence | Chunk | Responsibility | Dependencies |\n|---|---|---|---|\n'
    graph='# Dependency graph\n\nImmediate prerequisites after cycle validation and transitive reduction. Phase numbers group capabilities, not a mandatory serial gate. Frontend includes actual API and reused-component dependencies. The final gate requires every other chunk.\n\n```mermaid\nflowchart TD\n'
    blueprint=(ROOT/'docs/architecture/CODE_BLUEPRINT.md').read_text().split('| Chunk | Objects |')[0]+'| Chunk | Objects | Application operations | APIs | Frontend components | Repository / integration ports |\n|---|---|---|---|---|---|\n'
    for c in chunks:
        registry+=f"| {c['sequence']} | [{c['id']}](chunks/{c['id']}.md) | {c['title']} | {', '.join(c['dependencies']) or 'Scope approval only'} |\n"
        if not c['dependencies']:graph+='  '+c['id'].replace('-','_')+'["'+c['id']+'"]\n'
        for d in c['dependencies']:graph+='  '+d.replace('-','_')+' --> '+c['id'].replace('-','_')+'\n'
        blueprint+='| '+' | '.join([c['id']]+[', '.join(c[k]) for k in ['domain_objects','application_services','api_operations','frontend_components','ports']])+' |\n'
    graph+='```\n\n'+'\n'.join('- '+c['id']+': '+(', '.join(c['dependencies']) or 'no chunk prerequisite') for c in chunks)
    put('docs/planning/CHUNK_REGISTRY.md',registry);put('docs/planning/DEPENDENCY_GRAPH.md',graph);put('docs/architecture/CODE_BLUEPRINT.md',blueprint)
    prior={t['requirement']:t for t in read('docs/planning/traceability.json')};trace=[]
    for r in req:
        oid={o['name'] for o in b['objects'] if r['id'] in o['requirements']}
        relevant=[a for a in b['operations'] if r['id'] in a['requirements'] or set(a['objects'])&oid or a['id'] in prior[r['id']]['api']]
        ids={a['id'] for a in relevant};owners=[c for c in chunks if r['id'] in c['requirements']]
        t=prior[r['id']];t.update(objects=sorted(oid|{o for a in relevant for o in a['objects']}),services=sorted({a['service'] for a in relevant}),api=sorted(ids),consumers=sorted({s for a in relevant for s in a['consumer']}) or ['cross-cutting engineering/operations'],chunks=[c['id'] for c in owners],frontend_components=sorted(c['name'] for c in f['components'] if r['id'] in c['requirements'] or set(c['operations'])&ids),design_documents=sorted({p for c in owners for p in c['required_context']}),verification=['docs/planning/verification/'+c['id']+'.md' for c in owners]);trace.append(t)
    put('docs/planning/traceability.json',trace)
    md='# Requirement traceability\n\n100% planned coverage is not implementation completion. Each TEST-ID corresponds in order to acceptance in requirements.json. [traceability.json](traceability.json) supplies full object/service/API/frontend/design/chunk/evidence links; tests remain planned until implemented and executed.\n\n| Requirement | Design / operations | Frontend consumers | Chunks | Planned tests |\n|---|---|---|---|---|\n'
    for t in trace:md+='| '+' | '.join([t['requirement'],', '.join(t['services']) or ', '.join(t['design_documents']),', '.join(t['frontend_components']) or 'Engineering/operations',', '.join(t['chunks']),', '.join(t['tests'])])+' |\n'
    put('docs/planning/REQUIREMENT_TRACEABILITY.md',md)
    print(json.dumps({'chunks':len(chunks),'requirements':len(req),'operations':len(apis),'components':len(components),'scope_status':'DRAFT'}))

if __name__=='__main__':main()
