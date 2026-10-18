"""Offline only: build, pure-core tests, CLR Harmony probe. No deploy/game boot.
Requires Windows desktop CLR plus the .NET 6 SDK and local licensed game refs in lib/.
No DLL references are downloaded or distributed by this script.
"""
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, subprocess, sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

def decode(raw):
    if raw.startswith(b'\xff\xfe'): return raw.decode('utf-16')
    return raw.decode('utf-8-sig', errors='replace')

def run(command, log):
    result = subprocess.run([str(x) for x in command], cwd=REPO, capture_output=True)
    text = decode(result.stdout) + decode(result.stderr)
    log.write_text(text, encoding='utf-8')
    print(text[-3000:])
    if result.returncode: raise RuntimeError(f'{command[0]} failed: {result.returncode}; {log}')
    return text

def declared_changes():
    """Editorial assertion derived from the shipped manifest, never a hard-coded number."""
    manifest = json.loads((REPO/'BetterPortuguese/Data/manifest.json').read_text(encoding='utf-8-sig'))
    return int(manifest['coverage']['changedKeys'])

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--expected-changes', type=int, default=None, help='Changed-key content assertion; defaults to coverage.changedKeys in BetterPortuguese/Data/manifest.json')
    ap.add_argument('--out', type=Path, default=HERE/'out')
    ap.add_argument('--bepinex-core', type=Path, default=Path.home()/'AppData/Roaming/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/core')
    a = ap.parse_args(); out = a.out.resolve(); out.mkdir(parents=True, exist_ok=True)
    count_source = 'argument' if a.expected_changes is not None else 'Data/manifest.json coverage.changedKeys'
    if a.expected_changes is None: a.expected_changes = declared_changes()
    deps = out/'deps'; deps.mkdir(exist_ok=True)
    hashes = {}
    for name in ['0Harmony.dll', 'Mono.Cecil.dll', 'MonoMod.Utils.dll', 'MonoMod.RuntimeDetour.dll']:
        source = REPO/'lib'/name
        if not source.exists(): source = a.bepinex_core/name
        if not source.is_file(): raise FileNotFoundError(source)
        shutil.copy2(source, deps/name)
        hashes[name] = hashlib.sha256(source.read_bytes()).hexdigest()
    for config in ['Debug', 'Release']:
        run(['dotnet', 'build', REPO/'BetterPortuguese/BetterPortuguese.csproj', '-c', config, '-p:DeployToBepInEx=false', '--no-incremental'], out/f'build-{config.lower()}.log')
    run(['dotnet','build', HERE/'BetterPortuguese.Offline.csproj','-c','Release',f'-p:OfflineDepsDir={deps}'],out/'build-tests.log')
    core = run(['dotnet', HERE/'bin/Release/net6.0/BetterPortuguese.Offline.dll', REPO, str(a.expected_changes)],out/'core-tests.log')
    # Same source core, compiled against desktop CLR, because the local HarmonyX's
    # old MethodInvoker is not compatible with this host's CoreCLR/net6 reflection.
    sdk = subprocess.check_output(['dotnet','--list-sdks']).decode('utf-8').splitlines()[-1]
    match = re.fullmatch(r'([^ ]+) \[(.+)\]', sdk.strip())
    csc = Path(match[2])/match[1]/'Roslyn/bincore/csc.dll'
    framework = Path(os.environ.get('WINDIR','C:/Windows'))/'Microsoft.NET/Framework64/v4.0.30319'
    probe = out/'harmony-clr'; probe.mkdir(exist_ok=True)
    for p in deps.glob('*.dll'): shutil.copy2(p,probe/p.name)
    entry = dict(Value='baseline',Key='key',TranslatorKey=None,Feminine='',Masculine='',Neutral='',LanguageGender=0,CanBeGendered=False,NeedsGenderInfo=False)
    root = dict(schemaVersion=1,locale='pt-BR',variant='Original',source=dict(taskId='t_00000000',artifactSha256='a'*64,resourcePath='SYNTHETIC_OFFLINE_FIXTURE',resourcePathId=1,resourceAssetSha256='b'*64,assemblySha256='c'*64,canonicalMemberSha256='d'*64),records=[dict(id='LANG-00001',key='key',presentInSource=True,entries=[entry])],manualRecords=[])
    (probe/'fixture.original.json').write_text(json.dumps(root),encoding='utf-8')
    entry['Value']='corrected'; root['variant']='Corrigido'
    (probe/'fixture.corrigido.json').write_text(json.dumps(root),encoding='utf-8')
    change=dict(id='LANG-00001',key='key',entryIndex=0,field='Value',before='baseline',after='corrected',approvalTaskId='t_00000000')
    original_root=json.loads((probe/'fixture.original.json').read_text(encoding='utf-8'))
    changes=[change]
    for i,key,absent in [(2,'empty',False),(3,'absent',True)]:
        before=None if absent else []
        original_root['records'].append(dict(id=f'LANG-{i:05d}',key=key,presentInSource=not absent,entries=before))
        added=dict(entry,Key=key,Value='added '+key,Feminine=None,Masculine=None,Neutral=None)
        root['records'].append(dict(id=f'LANG-{i:05d}',key=key,presentInSource=not absent,entries=[added]))
        changes.append(dict(operation='addEntry',id=f'LANG-{i:05d}',key=key,entryIndex=0,before=before,after=added,approvalTaskId='t_00000000'))
    (probe/'fixture.original.json').write_text(json.dumps(original_root),encoding='utf-8')
    (probe/'fixture.corrigido.json').write_text(json.dumps(root),encoding='utf-8')
    (probe/'fixture.diff.json').write_text(json.dumps(changes),encoding='utf-8')
    command=['dotnet',csc,'-nologo','-noconfig','-nostdlib+','-langversion:10','-target:exe',f'-out:{probe / "HarmonyCoreProbe.exe"}']
    command += [f'-r:{framework/name}' for name in ['mscorlib.dll','System.dll','System.Core.dll']]
    command += [f'-r:{deps/"0Harmony.dll"}', HERE/'HarmonyCoreProbe.cs']
    command += sorted((REPO/'BetterPortuguese/Core').glob('*.cs'))
    run(command,out/'build-harmony-clr.log')
    harmony = run([probe/'HarmonyCoreProbe.exe'],out/'harmony-tests.log')
    count = lambda text: tuple(int(n) for n in re.search(r'RESULT passed=(\d+) failed=(\d+)',text).groups())
    cp,cf=count(core); hp,hf=count(harmony)
    report=dict(corePassed=cp,coreFailed=cf,harmonyPassed=hp,harmonyFailed=hf,totalPassed=cp+hp,totalFailed=cf+hf,dependencySha256=hashes,noGameTargetPatched=True,deployment=False,limits=['UI/game/Mono not exercised',f'Expected changed-key count: {a.expected_changes} (source: {count_source})','No approved mod or manual adapters'])
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    return int(report['totalFailed']!=0)
if __name__=='__main__':
    try: sys.exit(main())
    except Exception as e: print(f'ERROR {e}',file=sys.stderr);sys.exit(1)
