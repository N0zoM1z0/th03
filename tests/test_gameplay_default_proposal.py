"""Proposed promoted-default guards; synthetic/mock-only, no native execution."""
import hashlib,sys,tomllib,unittest,tempfile,shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from test_th03_serial_schedule import ScheduleTests,m
ROOT=Path(__file__).resolve().parents[1]
class GameplayDefaultProposal(ScheduleTests):
    def test_promoted_default_uses_unchanged_local_jobs_policy(self):
        cfg=tomllib.loads((ROOT/'config/th03_main_exact_units.toml').read_text())
        for u in cfg['units']:
            self.assertFalse(any(e['path']=='build.bat' for e in u.get('carrier_edits',[])))
        s=m.Schedule(self.execute,self.root,'unique',False)
        for n in (1,2):
            work=self.workspace(n,False);before=(work/'build.bat').read_bytes();self.call(s,work)
            self.assertEqual((work/'build.bat').read_bytes(),before)
            self.assertEqual((work/'.tup/options').read_bytes(),m.OPTIONS)
    def test_promoted_default_pin_rejects_arbitrary_edits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in m.PINS:
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,p)
            m.check_pins(root,None)
            p=root/'config/th03_main_exact_units.toml';p.write_bytes(p.read_bytes()+b'\n# drift\n')
            with self.assertRaises(ValueError):m.check_pins(root,None)
    def test_exact_additive_default_scope(self):
        old=tomllib.loads((ROOT/'tests/fixtures/th03_main_exact_units_pre_gameplay.toml').read_text())
        prop=tomllib.loads((ROOT/'config/th03_main_mima_gameplay_candidate.toml').read_text())
        from test_main_score_candidate import ACCEPTED as new, DEFAULT
        self.assertEqual(len(DEFAULT['functions']),377)
        self.assertEqual(new['functions'],old['functions']+prop['functions'])
        self.assertEqual(new['units'][:len(old['units'])],old['units'])
        self.assertEqual(len(new['functions']),371)
        for u in new['units'][len(old['units']):]:
            self.assertNotIn('stage_round',str(u));self.assertNotIn('round_loop',str(u))
