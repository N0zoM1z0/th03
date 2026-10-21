"""Mock-only scheduling tests; no subprocess, Wine or compiler is started."""
import importlib.util
import json
import subprocess
from types import SimpleNamespace
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("schedule_once", HERE.parent / "scripts/lib/th03_serial_schedule.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ScheduleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="th03-schedule-mock-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.output = self.root / ".analysis/th03-main-exact/unique"
        self.events = []
        self.fail = None
        self.options_text = b"Parsed option file: .tup/options\nupdater.num_jobs = '1' from .tup/options\n"
        for key, value in (("BUILD_SHA", m.sha(m.BEFORE)), ("TUP_SHA", m.sha(b"mock tup"))):
            p = patch.object(m,key,value);p.start();self.addCleanup(p.stop)
        # Assert no accidental production subprocess entry can be introduced.
        p = patch("subprocess.Popen",side_effect=AssertionError("native process forbidden"))
        p.start();self.addCleanup(p.stop)
        p = patch.object(m.subprocess, "run", side_effect=self.build)
        self.build_run = p.start();self.addCleanup(p.stop)

    def build(self, argv, *, cwd, env, stdout, stderr, timeout):
        self.assertEqual(argv,m.BUILD_ARGV)
        self.assertEqual(timeout,300)
        self.assertEqual(stdout,m.subprocess.PIPE)
        self.assertEqual(stderr,m.subprocess.STDOUT)
        self.execute(argv,cwd,env,cwd.parent/"cold-build.log")
        return SimpleNamespace(returncode=0,stdout=b"build succeeded")

    def workspace(self, n=1, candidate=False):
        work = self.output / ("round"+str(n)) / "source"
        work.mkdir(parents=True)
        (work/"bin").mkdir()
        (work/"bin/tup.exe").write_bytes(b"mock tup")
        (work/"build.bat").write_bytes(m.AFTER if candidate else m.BEFORE)
        (work/"Tupfile.ini").write_bytes(b"")
        return work

    def execute(self, argv, work, env, log):
        self.events.append((list(argv),work,env,log))
        if self.fail and self.fail in argv[-1]:
            raise ValueError("mock failure")
        if argv[-1] == r"bin\tup init":
            (work/".tup").mkdir()
            (work/".tup/db").write_bytes(b"empty mock database")
        elif argv[-1] == r"bin\tup options":
            log.write_bytes(self.options_text)
        return {"argv":argv,"exit_code":0,"log_sha256":"mock"}

    def call(self, schedule, work):
        return schedule(m.BUILD_ARGV,work,{"WINEPREFIX":"unchanged"},work.parent/"cold-build.log")

    def test_two_rounds_baseline_and_candidate(self):
        for candidate in (False,True):
            with self.subTest(candidate=candidate):
                # Separate IDs/roots preserve all four source directories.
                self.output=self.root/(".analysis/th03-main-exact/candidate" if candidate else ".analysis/th03-main-exact/unique")
                run_id="candidate" if candidate else "unique"
                s=m.Schedule(self.execute,self.root,run_id,candidate)
                for n in (1,2):
                    work=self.workspace(n,candidate)
                    before=(work/"build.bat").read_bytes()
                    result=self.call(s,work)
                    self.assertEqual(result["argv"],m.BUILD_ARGV)
                    self.assertEqual((work/"build.bat").read_bytes(),before)
                    self.assertEqual((work/".tup/options").read_bytes(),m.OPTIONS)
                    self.assertEqual([x[0][-1] for x in self.events[-3:]],
                                     [r"bin\tup init",r"bin\tup options",m.BUILD_ARGV[-1]])
                self.assertEqual(len(s.rounds),2)

    def test_non_cold_passes_through(self):
        s=m.Schedule(self.execute,self.root,"unique")
        work=self.workspace()
        argv=["wine","mock-hud-command"]
        result=s(argv,work,{},work.parent/"hud.log")
        self.assertEqual(result["argv"],argv)
        self.assertEqual(len(self.events),1)
        self.build_run.assert_not_called()
        self.assertFalse((work/".tup").exists())

    def test_timeout_retains_partial_output_and_never_completes(self):
        work=self.workspace();s=m.Schedule(self.execute,self.root,"unique")
        self.build_run.side_effect=subprocess.TimeoutExpired(m.BUILD_ARGV,300,output=b"partial compiler output")
        with self.assertRaises(subprocess.TimeoutExpired):self.call(s,work)
        self.assertEqual((work.parent/"cold-build.log").read_bytes(),b"partial compiler output")
        row=json.loads((work.parent/"scheduling.json").read_text())
        self.assertFalse(row["completed"])
        self.assertEqual(row["original_build_timeout_seconds"],180)
        self.assertEqual(row["effective_build_timeout_seconds"],300)
        self.assertEqual(row["nonbuild_timeout_seconds"],180)
        self.assertEqual(row["outer_supervisor_timeout_seconds"],900)
        self.assertEqual(row["partial_timeout_log_sha256"],m.sha(b"partial compiler output"))
        with self.assertRaises(ValueError):self.call(s,work)
        self.assertEqual(self.build_run.call_count,1)

    def test_timeout_without_output_retains_empty_log(self):
        work=self.workspace()
        self.build_run.side_effect=subprocess.TimeoutExpired(m.BUILD_ARGV,300)
        with self.assertRaises(subprocess.TimeoutExpired):self.call(m.Schedule(self.execute,self.root,"unique"),work)
        self.assertEqual((work.parent/"cold-build.log").read_bytes(),b"")

    def test_nonzero_build_preserves_log_and_fails(self):
        work=self.workspace()
        self.build_run.return_value=SimpleNamespace(returncode=7,stdout=b"failure")
        self.build_run.side_effect=None
        with self.assertRaisesRegex(ValueError,"tool exit 7"):self.call(m.Schedule(self.execute,self.root,"unique"),work)
        self.assertEqual((work.parent/"cold-build.log").read_bytes(),b"failure")

    def test_third_round_never_reaches_executor(self):
        s=m.Schedule(self.execute,self.root,"unique")
        for n in (1,2):self.call(s,self.workspace(n))
        with self.assertRaises(ValueError):self.call(s,self.workspace(3))
        self.assertEqual(self.build_run.call_count,2)

    def test_deceptive_command_never_reaches_executor(self):
        work=self.workspace();s=m.Schedule(self.execute,self.root,"unique")
        with self.assertRaises(ValueError):
            s(m.BUILD_ARGV[:-1]+[m.BUILD_ARGV[-1]+" && extra"],work,{},work.parent/"cold-build.log")
        self.build_run.assert_not_called()

    def test_existing_tup_refused(self):
        work=self.workspace();(work/".tup").mkdir()
        with self.assertRaisesRegex(ValueError,"absent"):
            self.call(m.Schedule(self.execute,self.root,"unique"),work)
        self.assertFalse(self.events)

    def test_tup_symlink_refused(self):
        work=self.workspace();(work/".tup").symlink_to(self.root)
        with self.assertRaises(ValueError):
            self.call(m.Schedule(self.execute,self.root,"unique"),work)
        self.assertFalse(self.events)

    def test_wrong_command_path_and_round_refused(self):
        work=self.workspace(2);s=m.Schedule(self.execute,self.root,"unique")
        with self.assertRaises(ValueError):self.call(s,work)
        work=self.workspace(1)
        with self.assertRaises(ValueError):s(["wine","bad"],work,{},work.parent/"cold-build.log")
        self.assertFalse(self.events)

    def test_repeated_round_refused(self):
        work=self.workspace();s=m.Schedule(self.execute,self.root,"unique")
        self.call(s,work);n=len(self.events)
        with self.assertRaises(ValueError):self.call(s,work)
        self.assertEqual(len(self.events),n)

    def test_build_carrier_identity_drift_refused(self):
        work=self.workspace()
        (work/"build.bat").write_bytes(b"drift")
        with self.assertRaisesRegex(ValueError,"^exact original build carrier identity$"):
            self.call(m.Schedule(self.execute,self.root,"unique"),work)
        self.assertFalse(self.events)
        self.build_run.assert_not_called()

    def test_build_tool_and_ini_drift_refused(self):
        for name in ("bin/tup.exe","Tupfile.ini"):
            case=self.root/name.replace("/","_")
            case.mkdir()
            self.output=case/".analysis/th03-main-exact/unique"
            work=self.workspace()
            (work/name).write_bytes(b"drift")
            with self.assertRaisesRegex(ValueError,"pin drift"):
                self.call(m.Schedule(self.execute,case,"unique"),work)
        self.assertFalse(self.events)

    def test_init_failure_never_builds(self):
        work=self.workspace();self.fail="init"
        with self.assertRaisesRegex(ValueError,"mock failure"):
            self.call(m.Schedule(self.execute,self.root,"unique"),work)
        self.assertEqual(len(self.events),1)

    def test_options_failure_never_builds(self):
        work=self.workspace();self.options_text=b"updater.num_jobs = '8' from default values\n"
        with self.assertRaisesRegex(ValueError,"local 1"):
            self.call(m.Schedule(self.execute,self.root,"unique"),work)
        self.assertEqual(len(self.events),2)

    def test_original_build_failure_propagates(self):
        work=self.workspace();self.fail="build.bat"
        with self.assertRaisesRegex(ValueError,"mock failure"):
            self.call(m.Schedule(self.execute,self.root,"unique"),work)
        self.assertEqual(len(self.events),3)

    def test_post_build_options_drift_fails(self):
        work=self.workspace()
        def build(*args,**kwargs):
            result=self.build(*args,**kwargs)
            (work/".tup/options").write_bytes(b"bad")
            return result
        self.build_run.side_effect=build
        with self.assertRaisesRegex(ValueError,"during cold build"):
            self.call(m.Schedule(self.execute,self.root,"unique"),work)

    def test_options_missing_db_and_preexisting_options(self):
        for kind in ("missing-db","existing-options"):
            root=self.root/kind;root.mkdir()
            self.output=root/".analysis/th03-main-exact/unique"
            work=self.workspace()
            def execute(argv,work,env,log):
                result=self.execute(argv,work,env,log)
                if argv[-1]==r"bin\tup init":
                    if kind=="missing-db":(work/".tup/db").unlink()
                    else:(work/".tup/options").write_bytes(b"old")
                return result
            with self.assertRaises(ValueError):
                self.call(m.Schedule(execute,root,"unique"),work)

class OptionParser(unittest.TestCase):
    def test_exact_local_count(self):
        for sep in ("/","\\"):
            m.verify_options(("Parsed option file: .tup"+sep+"options\n"
                              "updater.num_jobs = '1' from .tup"+sep+"options\n").encode())
    def test_wrong_duplicate_or_unproved_origin(self):
        for text in (
            "updater.num_jobs = '2' from .tup/options\n",
            "updater.num_jobs = '1' from default values\n",
            "updater.num_jobs = '1' from .tup/options\n",
            "Parsed option file: .tup/options\nupdater.num_jobs = '1' from .tup/options\nupdater.num_jobs = '1' from .tup/options\n",
        ):
            with self.assertRaises(ValueError):m.verify_options(text.encode())

class CandidatePins(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="th03-candidate-pins-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "control.txt").write_bytes(b"control")
        self.control = {"control.txt": m.sha(b"control")}
        p = patch.object(m, "PINS", self.control)
        p.start(); self.addCleanup(p.stop)

    def test_reviewed_allowlist_is_exact(self):
        self.assertEqual(m.CANDIDATE_PINS, {
            "config/th03_main_yumemi_charge_candidate.toml": "738adfd7eed18609c45eee7a95fa100b9d8659f214875b58305da62bd7bcd4bc",
            "config/th03_main_player_cpu_candidate.toml": "2420db4423b3f7269799ac1631f04cffd2ad322c7f3dda687600de27c22400f5",
            "config/th03_main_player_tail_candidate.toml": "a44ab5667b7f3da1cc4bc26efe7fdc48e60d9bcc40802d6fa13f5c8b33ff8ee3",
            "config/th03_main_yumemi_bomb_candidate.toml": "579736dc74c88de408575e0e94f9141c2ebf498f099e783424de3879cc82cad8",
            "config/th03_main_score_candidate.toml": "81aa3026afb3e15c6bff3d1ee79863ee0f95aa113ccf8856171ea8e695b7a347",
            "config/th03_main_marisa_candidate.toml":
                "fd9722b0f16a8bfe305b7782697b729f2ea1ef3d7b13ea1f83ba21af0eaf908d",
            "config/th03_main_reimu_shared_candidate.toml":
                "8294faefad6ca71e8d9cc684070e043e43a65bbd9b3e856c178b0cdce08752d1",
            "config/th03_main_mima_gameplay_candidate.toml":
                "855730e3d9943ef8afa4117c3b5a4ebe0c22ae12de56049f847e69c6182c270d",
        })

    def test_default_needs_no_candidate_file(self):
        self.assertEqual(m.check_pins(self.root, None), self.control)

    def test_each_candidate_checks_only_selected_manifest(self):
        fixture = {name: m.sha(name.encode()) for name in m.CANDIDATE_PINS}
        with patch.object(m, "CANDIDATE_PINS", fixture):
            for name, expected in fixture.items():
                path = self.root / name
                path.parent.mkdir(exist_ok=True)
                path.write_bytes(name.encode())
                self.assertEqual(m.check_pins(self.root, name),
                                 {**self.control, name: expected})
                path.unlink()

    def test_manifest_drift_fails_closed(self):
        name = next(iter(m.CANDIDATE_PINS))
        path = self.root / name
        path.parent.mkdir(); path.write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "input pin drift"):
            m.check_pins(self.root, name)

    def test_unreviewed_manifest_rejected(self):
        with self.assertRaisesRegex(ValueError, "unreviewed candidate"):
            m.check_pins(self.root, "config/unreviewed_candidate.toml")

    def test_candidate_symlink_rejected(self):
        name = next(iter(m.CANDIDATE_PINS))
        path = self.root / name
        path.parent.mkdir(); path.symlink_to(self.root / "control.txt")
        with self.assertRaisesRegex(ValueError, "symlink"):
            m.check_pins(self.root, name)

if __name__=="__main__":
    unittest.main()
