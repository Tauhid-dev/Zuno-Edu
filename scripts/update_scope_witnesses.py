#!/usr/bin/env python3
"""Capture proposed plan hashes on a feature branch; this never approves scope."""
from pathlib import Path
import json
from reconcile_state import Repository,mandatory_witnesses,witness_normalization,plan_digest,require

def main():
    root=Path(__file__).resolve().parents[1]
    repo=Repository(root)
    require(repo.git('branch','--show-current').startswith('feature/'),
            'Scope witnesses may only be proposed on a feature branch')
    path=root/'docs/product/scope-lock.json'
    lock=json.loads(path.read_text())
    require(lock['status']=='DRAFT','Start an explicitly authorized DRAFT scope proposal before replacing approved witnesses')
    artifacts=[]
    for name in sorted(mandatory_witnesses(repo)):
        artifact={'path':name}
        normalization=witness_normalization(name)
        if normalization:artifact['normalization']=normalization
        artifact['sha256']=plan_digest((root/name).read_bytes(),artifact)
        artifacts.append(artifact)
    lock['plan_artifacts']=artifacts
    path.write_text(json.dumps(lock,indent=2)+'\n')
    print(json.dumps({'status':'DRAFT','captured_witnesses':len(artifacts),'approved':False}))

if __name__=='__main__':main()
