"""CLI regressions on COPIES of collected evidence. Never launch the game.
Fixtures here are mutations of real outputs, NOT new runtime observations.
"""
from pathlib import Path
import argparse, json, shutil, subprocess, sys, unittest

HERE=Path(__file__).resolve().parent

def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False),encoding='utf-8')

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.case=OUT/self.id().split('.')[-1]
        self.case.mkdir(parents=True)
        parent=self.case/'recorder-on'; parent.mkdir()
        shutil.copy2(EVIDENCE.parent/'inputs.json',parent/'inputs.json')
        shutil.copytree(EVIDENCE.parent/'inputs',parent/'inputs')
        self.boot=parent/'boot01'
        # No production save or registry data copied: only outputs evaluated by the CLI.
        shutil.copytree(EVIDENCE,self.boot,ignore=shutil.ignore_patterns('*.reg','saves-antes','isolamento'))
        self.export=next((self.boot/'preserved/recorder/exports').glob('*.json'))
    def cli(self,expected,failed=None):
        p=subprocess.run([sys.executable,str(HERE/'runner.py'),'evaluate','--out',str(self.boot)],capture_output=True,timeout=30)
        (self.case/'cli.stdout.json').write_bytes(p.stdout)
        (self.case/'cli.stderr.log').write_bytes(p.stderr)
        self.assertEqual(p.returncode,expected,p.stderr.decode(errors='replace'))
        d=json.loads(p.stdout)
        self.assertEqual(d['exit'],expected)
        self.assertEqual(d['kit_verdict'],'NOT_GRANTED')
        if failed:self.assertIn(failed,d['failures'])
        return d
    def mutate(self,rel,fn):
        p=self.boot/rel;d=read(p);fn(d);write(p,d)
    def test_real_export_passes(self): self.cli(0)
    def test_missing_export_fails(self):
        self.export.unlink(); self.cli(1,'export_file_exists')
    def test_missing_debugger_asset_fails(self):
        p=self.boot/'preserved/Player.log';s=p.read_text(encoding='utf-8-sig')
        p.write_text('\n'.join(x for x in s.splitlines() if "[Skill] 'Fireball' |" not in x),encoding='utf-8')
        self.cli(1,'debugger_skill_matches_live_target')
    def test_missing_footer_fails(self):
        p=self.boot/'preserved/Player.log';s=p.read_text(encoding='utf-8-sig')
        p.write_text('\n'.join(x for x in s.splitlines() if 'DBG-PROV-V1 fim |' not in x),encoding='utf-8')
        self.cli(1,'debugger_session_complete')
    def test_wrong_export_session_fails(self):
        d=read(self.export);d['sessao']='NOT_THIS_BOOT';write(self.export,d);self.cli(1,'export_session')
    def test_wrong_runtime_pid_fails(self):
        self.mutate('preserved/recorder/controle-runtime.json',lambda d:d['engine'].update(pid=-1))
        self.cli(1,'engine_identity')
    def test_unrendered_frame_fails(self):
        def change(d):
            e=d['rstv_coleta']['events'];hover=next(x['frame'] for x in e if x['event']=='hover_handler')
            next(x for x in e if x['event']=='tooltip_observed')['frame']=hover
        self.mutate('probe/aut4probe.json',change);self.cli(1,'post_render_frame_order')
    def test_missing_mark_fails(self):
        d=read(self.export);d['marcacoes']=[];write(self.export,d);self.cli(1,'checkpoint_mark_retained')
    def test_offline_flag_fails(self):
        d=read(self.export);d['runtime_exercitado']=False;write(self.export,d);self.cli(1,'export_schema')
    def test_guard_false_fails(self):
        def change(d):d['comandos_auto'][0]['contexto']['foco_no_jogo']=False
        self.mutate('preserved/recorder/controle-runtime.json',change);self.cli(1,'guarded_dispatch')
    def test_input_drift_fails(self):
        p=self.boot.parent/'inputs/AUT4Probe.dll';p.write_bytes(p.read_bytes()+b'OFFLINE_MUTATION')
        self.cli(1,'input_hashes')
    def test_cleanup_failure_fails(self):
        self.mutate('result.json',lambda d:d.update(cleanup_error='OFFLINE_MUTATION'))
        self.cli(1,'driver_completed')
    def test_readback_drift_fails(self):
        def change(d):d['production']['changed']=['Character1.json']
        self.mutate('baseline-after.json',change)
        self.cli(1,'owner_readback_unchanged')
    def test_missing_restore_log_fails(self):
        p=self.boot/'dados-restaurar.stderr.log';s=p.read_text(encoding='utf-8-sig')
        p.write_text('\n'.join(x for x in s.splitlines() if 'BYTE A BYTE identico' not in x),encoding='utf-8')
        self.cli(1,'owner_readback_unchanged')
    def test_missing_log_not_green(self):
        (self.boot/'preserved/Player.log').unlink();self.cli(2,'evidence_unusable')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--evidence',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args(); EVIDENCE=args.evidence.resolve();OUT=args.out.resolve()
    OUT.mkdir(parents=True,exist_ok=False)
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(EvidenceTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    data={'schema':'KIT-AUTO/CLI-tests/1','runtime_boots':0,'evidence':str(EVIDENCE),
        'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
        'exit':0 if result.wasSuccessful() else 1}
    write(OUT/'summary.json',data);print(json.dumps(data));sys.exit(data['exit'])
