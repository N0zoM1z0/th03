"""Mock-only foreground runner and completion capture tests."""
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("scheduled_runner",HERE.parent/"scripts/replay_th03_main_serial.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

ORIGINAL_SUPERVISE = m.supervise

class UnpatchedLayout(unittest.TestCase):
    def test_runner_and_adapter_share_repository_and_runtime_paths(self):
        root = HERE.parent.resolve()
        adapter_path = root / "scripts/lib/th03_serial_schedule.py"
        spec = importlib.util.spec_from_file_location("serial_layout_adapter", adapter_path)
        adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(adapter)
        self.assertEqual(m.ROOT, root)
        self.assertEqual(adapter.ROOT, root)
        self.assertEqual(m.STATE_ROOT, root / ".analysis/th03-main-serial")
        self.assertEqual(adapter.STATE_ROOT, m.STATE_ROOT)
        self.assertEqual(m.CLAIM, m.STATE_ROOT / "active.claim")
        self.assertEqual(m.SCHEDULE, adapter_path)
        self.assertEqual(adapter.REPLAY, root / m.REPLAY)
        self.assertEqual(m.digest(adapter_path), m.SCHEDULE_SHA)
        self.assertEqual(m.STATE_ROOT.relative_to(root).parts[0], ".analysis")

class Foreground(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="th03-foreground-mock-")
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve()
        self.here=self.root/"stage";self.here.mkdir()
        for name,value in (("ROOT",self.root),("STATE_ROOT",self.here),("CLAIM",self.here/"active.claim")):
            p=patch.object(m,name,value);p.start();self.addCleanup(p.stop)
        p=patch.object(m,"pins",return_value={"f":"hash"});p.start();self.addCleanup(p.stop)
        def digest(path):
            return m.SCHEDULE_SHA if path==m.SCHEDULE else m.ORIGINAL_REPLAY_SHA
        p=patch.object(m,"digest",side_effect=digest);p.start();self.addCleanup(p.stop)
        p=patch.object(m,"process_identity",return_value=(12,12,"123","python","S"))
        p.start();self.addCleanup(p.stop)
        p=patch.object(m.subprocess,"Popen",side_effect=AssertionError("native forbidden"))
        self.popen=p.start();self.addCleanup(p.stop)
        p=patch.object(m,"supervise");self.supervise=p.start();self.addCleanup(p.stop)
        p=patch("sys.stdout",new_callable=io.StringIO);self.stdout=p.start();self.addCleanup(p.stop)
    def test_foreground_no_outer_spawn_and_explicit_binding(self):
        result=m.launch("fresh")
        self.popen.assert_not_called()
        self.supervise.assert_called_once_with(self.here/"runs/fresh")
        state=json.loads((self.here/"runs/fresh/status.json").read_text())
        self.assertEqual(state["schedule_adapter_sha256"],m.SCHEDULE_SHA)
        self.assertEqual(state["original_replay_sha256"],m.ORIGINAL_REPLAY_SHA)
        self.assertIn(str(m.SCHEDULE),state["argv"])
        self.assertIn("--supervisor-state",state["argv"])
        self.assertEqual(result["mode"],"foreground")
        self.assertEqual(len(self.stdout.getvalue().splitlines()),1)
    def test_launch_creates_initially_absent_state_root(self):
        self.here.rmdir()
        self.assertFalse(m.STATE_ROOT.exists())
        result = m.launch("fresh")
        self.assertTrue(m.STATE_ROOT.is_dir())
        self.assertTrue(m.CLAIM.is_dir())
        self.assertTrue((m.STATE_ROOT / "runs/fresh/status.json").is_file())
        self.assertEqual(Path(result["status_path"]), m.STATE_ROOT / "runs/fresh/status.json")
        self.supervise.assert_called_once_with(m.STATE_ROOT / "runs/fresh")
        self.popen.assert_not_called()

    def test_claim_refuses_second_entry(self):
        m.launch("fresh")
        with self.assertRaises(FileExistsError):m.launch("other")
        self.assertEqual(self.supervise.call_count,1)
    def test_pin_failure_does_not_supervise(self):
        with patch.object(m,"pins",side_effect=ValueError("pins failed")):
            with self.assertRaises(ValueError):m.launch("fresh")
        self.supervise.assert_not_called()
        state=json.loads((self.here/"runs/fresh/status.json").read_text())
        self.assertEqual(state["state"],"launch_error")
        self.assertFalse(state["launch_ambiguous"])
    def test_error_after_entry_preserves_supervisor_status(self):
        def fail(run):
            m.atomic(run/"status.json",{"state":"running"})
            raise RuntimeError("supervisor failure")
        self.supervise.side_effect=fail
        with self.assertRaises(RuntimeError):m.launch("fresh")
        self.assertEqual(json.loads((self.here/"runs/fresh/status.json").read_text())["state"],"running")
        self.assertTrue((m.CLAIM/"launch-error.json").exists())
    def test_adapter_pin_drift_blocks_before_claim(self):
        with patch.object(m,"digest",return_value="wrong"):
            with self.assertRaises(ValueError):m.launch("fresh")
        self.assertFalse(m.CLAIM.exists())

    def test_completion_failure_retains_claim_and_terminal_error(self):
        m.launch("fresh")
        run=self.here/"runs/fresh"
        with patch.object(m,"limits"), \
             patch.object(m.subprocess,"Popen",return_value=SimpleNamespace(pid=12)), \
             patch.object(m,"finish",return_value={"replay_exit_code":0,"cleanup_uncertain":False}), \
             patch.object(m,"capture_completion",side_effect=ValueError("attestation mismatch")):
            ORIGINAL_SUPERVISE(run)
        state=json.loads((run/"status.json").read_text())
        self.assertEqual(state["state"],"supervisor_error")
        self.assertTrue(state["claim_retained"])
        self.assertTrue(m.CLAIM.exists())
        self.assertIn("attestation mismatch",state["error"])

    def test_main_failure_returns_nonzero(self):
        m.launch("fresh")
        status=self.here/"runs/fresh/status.json"
        m.atomic(status,{"state":"finished","replay_exit_code":1,"source_inputs_unchanged":True})
        with patch.object(m,"launch",return_value={"status_path":str(status)}), \
             patch.object(sys,"argv",["runner_schedule.py","--foreground","--run-id","fresh"]):
            self.assertEqual(m.main(),1)

    def test_main_success_requires_unchanged_sources(self):
        m.launch("fresh")
        status=self.here/"runs/fresh/status.json"
        for unchanged,expected in ((False,1),(True,0)):
            m.atomic(status,{"state":"finished","replay_exit_code":0,"source_inputs_unchanged":unchanged})
            with patch.object(m,"launch",return_value={"status_path":str(status)}), \
                 patch.object(sys,"argv",["runner_schedule.py","--foreground","--run-id","fresh"]):
                self.assertEqual(m.main(),expected)

class Completion(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="th03-completion-mock-")
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve()
        self.run=self.root/"run";self.run.mkdir()
        self.output=self.root/".analysis/th03-main-exact/fresh"
        self.output.mkdir(parents=True)
        (self.root/"scripts").mkdir()
        (self.root/m.REPLAY).write_bytes(b"replay")
        self.att=self.root/".analysis/toolchain/attestation.json"
        self.att.parent.mkdir();self.att.write_bytes(b'{"checks":[]}\n')
        self.receipt={"run_id":"fresh","pass":True,"rounds":[{"round":1},{"round":2}],
                      "toolchain_receipt_sha256":m.digest(self.att)}
        (self.output/"receipt.json").write_text(json.dumps(self.receipt))
        for n in (1,2):
            d=self.output/("round"+str(n))
            (d/"source/obj/th03").mkdir(parents=True)
            (d/"source/obj/th03/main.map").write_bytes(b"main map")
            (d/"source/obj/th03/extra.MAP").write_bytes(b"extra map")
            (d/"scheduling.json").write_text("{}")
        p=patch.object(m,"ROOT",self.root);p.start();self.addCleanup(p.stop)
        self.state={"run_id":"fresh","replay_exit_code":0}
    def test_attestation_and_all_maps_frozen(self):
        r=m.capture_completion(self.run,self.state)
        self.assertEqual(len(r["maps"]),4)
        self.assertEqual((self.run/"tool-attestation.json").read_bytes(),self.att.read_bytes())
        self.assertEqual(r["tool_attestation"]["sha256"],self.receipt["toolchain_receipt_sha256"])
        self.assertTrue((self.run/"completion-evidence.json").exists())
    def test_changed_attestation_fails_before_copy(self):
        self.att.write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError,"differs"):m.capture_completion(self.run,self.state)
        self.assertFalse((self.run/"tool-attestation.json").exists())
    def test_missing_main_map_fails(self):
        (self.output/"round2/source/obj/th03/main.map").unlink()
        with self.assertRaisesRegex(ValueError,"MAP missing"):m.capture_completion(self.run,self.state)
    def test_missing_scheduling_sidecar_fails(self):
        (self.output/"round2/scheduling.json").unlink()
        with self.assertRaises(FileNotFoundError):
            m.capture_completion(self.run,self.state)
        self.assertFalse((self.run/"completion-evidence.json").exists())

    def test_map_symlink_fails(self):
        p=self.output/"round1/source/obj/th03/main.map";p.unlink();p.symlink_to(self.att)
        with self.assertRaisesRegex(ValueError,"MAP path"):m.capture_completion(self.run,self.state)
    def test_missing_success_receipt_fails(self):
        (self.output/"receipt.json").unlink()
        with self.assertRaisesRegex(ValueError,"no original receipt"):m.capture_completion(self.run,self.state)
    def test_failed_missing_receipt_recorded_without_acceptance(self):
        (self.output/"receipt.json").unlink();self.state["replay_exit_code"]=1
        r=m.capture_completion(self.run,self.state)
        self.assertFalse(r["receipt_present"]);self.assertFalse(r["exact_acceptance"])

class OwnedProcess(unittest.TestCase):
    def setUp(self):
        self.events = []
        self.states = {41: (41,41,"100","python","Z")}
        self.proc = SimpleNamespace(pid=41, returncode=None)
        def wait(timeout):
            self.events.append("reap"); self.proc.returncode=0; return 0
        self.proc.wait=wait
        patches = [
            patch.object(m,"process_identity",side_effect=lambda pid:self.states[pid]),
            patch.object(m,"process_ids",side_effect=lambda:list(self.states)),
            patch.object(m.os,"waitid",return_value=object()),
            patch.object(m.os,"pidfd_open",side_effect=lambda pid,flags:pid+1000),
            patch.object(m.os,"close"),
            patch.object(m.signal,"pidfd_send_signal",side_effect=self.send),
            patch.object(m.time,"sleep"),
        ]
        for p in patches: p.start(); self.addCleanup(p.stop)
        self.stop=SimpleNamespace(exists=lambda:False)
    def send(self,fd,sig,info,flags):
        self.assertNotIn("reap",self.events)
        pid=fd-1000; self.events.append(("signal",pid))
        self.states[pid]=self.states[pid][:4]+("Z",)
    def test_exit_reaps_last(self):
        self.assertEqual(m.finish(self.proc,self.stop)["replay_exit_code"],0)
        self.assertEqual(self.events,["reap"])
    def test_stop_cleans_only_owned_members(self):
        self.states[41]=(41,41,"100","python","R")
        self.states[42]=(42,41,"101","wineserver","S")
        self.states[43]=(43,999,"102","unrelated","R")
        with patch.object(m.os,"waitid",return_value=None):
            result=m.finish(self.proc,SimpleNamespace(exists=lambda:True))
        self.assertEqual(result["reason"],"stop_requested")
        self.assertEqual(self.events,[("signal",41),"reap"])
    def test_wall_timeout(self):
        self.states[41]=(41,41,"100","python","R")
        with patch.object(m.os,"waitid",return_value=None), patch.object(m.time,"monotonic",side_effect=[0,901]):
            result=m.finish(self.proc,self.stop)
        self.assertEqual(result["reason"],"wall_timeout")
    def test_drift_never_signals(self):
        owner=m.OwnedGroup(self.proc)
        self.states[41]=(41,41,"CHANGED","python","Z")
        with self.assertRaises(RuntimeError): owner.cleanup()
        m.signal.pidfd_send_signal.assert_not_called()
    def test_reaped_never_signals(self):
        owner=m.OwnedGroup(self.proc); owner.reaped=True
        with self.assertRaises(RuntimeError): owner.cleanup()
        m.signal.pidfd_send_signal.assert_not_called()

if __name__=="__main__":
    unittest.main()
