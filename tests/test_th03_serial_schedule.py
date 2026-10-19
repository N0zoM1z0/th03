"""Mock-only scheduling tests; no subprocess, Wine or compiler is started."""
import importlib.util
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
        self.assertFalse((work/".tup").exists())

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

    def test_build_tool_and_ini_drift_refused(self):
        for name in ("build.bat","bin/tup.exe","Tupfile.ini"):
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
        def execute(argv,*rest):
            result=self.execute(argv,*rest)
            if argv==m.BUILD_ARGV:(work/".tup/options").write_bytes(b"bad")
            return result
        with self.assertRaisesRegex(ValueError,"during cold build"):
            self.call(m.Schedule(execute,self.root,"unique"),work)

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

if __name__=="__main__":
    unittest.main()
