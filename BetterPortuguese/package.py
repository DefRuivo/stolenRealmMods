"""Build-free audit package for BP-1: compiled DLL + both embedded and external datasets.
Reuses repo metadata checks; never installs, starts the game, uploads or overwrites ZIPs.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json, re, struct, sys, zipfile, zlib

MOD = Path(__file__).resolve().parent
REPO = MOD.parent

def sha(data): return hashlib.sha256(data).hexdigest()
def unique(pairs):
    obj = {}
    for key,value in pairs:
        if key in obj: raise ValueError('Duplicate JSON member: '+key)
        obj[key]=value
    return obj

def preflight(config='Release'):
    spec=importlib.util.spec_from_file_location('repo_pack',REPO/'tools/pack-thunderstore.py')
    pack=importlib.util.module_from_spec(spec);spec.loader.exec_module(pack)
    manifest,paths=pack.verificar('BetterPortuguese',config=config)
    expected=dict(re.findall(r'\{ "([^"]+)", "([a-f0-9]{64})" \}',(MOD/'Core/ResourceHashes.cs').read_text(encoding='utf-8')))
    data_files={p.name:p for p in (MOD/'Data').glob('*.json')}
    if set(data_files)!=set(expected): raise ValueError('Data/resource hash names mismatch')
    for name,path in data_files.items():
        if sha(path.read_bytes())!=expected[name]: raise ValueError('Data digest mismatch: '+name)
        json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique)
    original=json.loads((MOD/'Data/pt-BR.original.json').read_text(encoding='utf-8'))
    corrected=json.loads((MOD/'Data/pt-BR.corrigido.json').read_text(encoding='utf-8'))
    if len(original['records'])!=9095 or len(corrected['records'])!=9095: raise ValueError('Corpus count mismatch')
    if original['variant']!='Original' or corrected['variant']!='Corrigido': raise ValueError('Wrong variant')
    if sha((REPO/'lib/Assembly-CSharp.dll').read_bytes())!=original['source']['assemblySha256']: raise ValueError('Re-extract snapshots for new game assembly')
    compiled=[p for p in MOD.rglob('*') if p.is_file() and not set(p.relative_to(MOD).parts).intersection({'bin','obj','__pycache__'}) and p.suffix in {'.cs','.csproj','.json'}]
    if Path(paths['dll']).stat().st_mtime<max(p.stat().st_mtime for p in compiled): raise ValueError('DLL older than code/dataset; build again WITHOUT deploy')
    # Validate whole PNG, not just width/height header.
    png=Path(paths['icon']).read_bytes(); at=8; idat=bytearray(); width=height=None; ended=False
    if png[:8]!=b'\x89PNG\r\n\x1a\n': raise ValueError('Not a PNG')
    while at<len(png):
        n=struct.unpack('>I',png[at:at+4])[0]; kind=png[at+4:at+8]; payload=png[at+8:at+8+n]
        if len(payload)!=n or zlib.crc32(kind+payload)&0xffffffff!=struct.unpack('>I',png[at+8+n:at+12+n])[0]: raise ValueError('PNG CRC/truncation')
        if kind==b'IHDR': width,height,depth,color,_,_,interlace=struct.unpack('>IIBBBBB',payload)
        if kind==b'IDAT':idat.extend(payload)
        at+=12+n
        if kind==b'IEND':ended=True;break
    if (width,height,depth,color,interlace)!=(256,256,8,2,0) or not ended or at!=len(png) or len(zlib.decompress(idat))!=256*(1+256*3):raise ValueError('Invalid generated RGB icon')
    files={name:Path(paths[key]) for name,key in [('manifest.json','manifest'),('README.md','readme'),('CHANGELOG.md','changelog'),('icon.png','icon')]}
    files['plugins/BetterPortuguese/BetterPortuguese.dll']=Path(paths['dll'])
    files.update({'plugins/BetterPortuguese/Data/'+name:path for name,path in data_files.items()})
    return manifest,files

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--config',choices=['Debug','Release'],default='Release')
    ap.add_argument('--output',type=Path)
    ap.add_argument('--check-only',action='store_true')
    a=ap.parse_args(); manifest,files=preflight(a.config)
    if a.check_only: print('PREFLIGHT OK',len(files),'members; 4 version mirrors; both snapshots');return 0
    output=(a.output or REPO/f'dist/gumatos-BetterPortuguese-{manifest["version_number"]}-auditado.zip').resolve()
    output.parent.mkdir(parents=True,exist_ok=True)
    if output.exists():raise FileExistsError('Preserved existing package: '+str(output))
    index={name:dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for name,p in sorted(files.items())}
    with zipfile.ZipFile(output,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,path in sorted(files.items()):z.write(path,name)
    with zipfile.ZipFile(output) as z:
        if set(z.namelist())!=set(files) or len(z.namelist())!=len(files):raise ValueError('ZIP count/duplicate mismatch')
        if z.testzip() is not None:raise ValueError('ZIP CRC failure')
        for name,p in files.items():
            if z.read(name)!=p.read_bytes():raise ValueError('ZIP readback differs: '+name)
    report=dict(package=output.name,packageSha256=sha(output.read_bytes()),packageBytes=output.stat().st_size,members=len(index),files=index,noThirdPartyAssemblies=True,deployed=False,published=False,contentState='NO_HUMAN_APPROVALS_NO_TEXT_CHANGES')
    output.with_suffix('.verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))
    print(str(output));return 0
if __name__=='__main__':
    try:sys.exit(main())
    except Exception as e:print('ERROR '+str(e),file=sys.stderr);sys.exit(1)
