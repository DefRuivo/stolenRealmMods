"""Plant a real guard defect in a disposable copy; require harness red then green."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys
W=Path(__file__).resolve().parent
HERE=W
OUT=W/'guard-proof';OUT.mkdir(exist_ok=False)
original=HERE/'candidate/tools/automacao/runtime/KIT04Adapter.SR/PonteControleRSTV.cs'
original_hash=hashlib.sha256(original.read_bytes()).hexdigest()
results={}
for case in ('red','green'):
    root=OUT/case
    shutil.copytree(HERE/'candidate',root,ignore=shutil.ignore_patterns('bin','obj','__pycache__'))
    if case=='red':
        f=root/'tools/automacao/runtime/KIT04Adapter.SR/PonteControleRSTV.cs'
        s=f.read_text(encoding='utf-8-sig')
        before='public Dictionary<string, object> ProcessarAcao(string acao, long agoraMs, string descricao = null)\n        {\n            string motivo = GuardBloqueia();'
        assert s.count(before)==1
        f.write_text(s.replace(before,before.replace('GuardBloqueia()','null')),encoding='utf-8')
    env=dict(os.environ)
    temp=root/'temp';temp.mkdir();env['TEMP']=env['TMP']=str(temp)
    env['USERPROFILE']=str(root/'home');env['APPDATA']=str(root/'roaming');env['LOCALAPPDATA']=str(root/'local')
    project=root/'tools/automacao/runtime/harness-controle/HarnessControle.csproj'
    p=subprocess.run(['dotnet','run','--project',str(project),'-c','Release','-p:DeployToBepInEx=false'],capture_output=True,timeout=180,env=env)
    (OUT/(case+'.stdout.log')).write_bytes(p.stdout);(OUT/(case+'.stderr.log')).write_bytes(p.stderr)
    results[case]={'exit':p.returncode,'failure_lines':[s for s in p.stdout.decode(errors='replace').splitlines() if '[FALHA ' in s]}
assert results['red']['exit']==1 and len(results['red']['failure_lines'])==20,results
assert results['green']['exit']==0 and not results['green']['failure_lines'],results
assert hashlib.sha256(original.read_bytes()).hexdigest()==original_hash
(OUT/'RESULTADO.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
