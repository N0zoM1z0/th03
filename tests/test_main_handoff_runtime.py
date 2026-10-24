"""Independent service/state contracts cover the complete native handoff span."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.pc98 import parse_mz
from lib.main_handoff_runtime import Machine, compare, negative_controls, state, PATTERNS


@unittest.skipUnless((ROOT / ".analysis/targets/th03/main.exe").is_file(), "private target absent")
class HandoffRuntime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image = parse_mz((ROOT / ".analysis/targets/th03/main.exe").read_bytes())

    def test_all_instruction_bytes_and_counter_values_are_executed(self):
        result = compare(self.image, self.image)
        self.assertEqual(result["cases"], 1110)
        self.assertEqual(result["bytes_by_entry"], {"exec": 79, "none": 5, "cover": 354, "uncover": 304})

    def test_actual_guest_mutations_fail_independent_contracts(self):
        result = negative_controls(self.image)
        self.assertEqual(result["count"], 10)

    def test_counter_wrap_does_not_signal_midpoint_or_replace_callback(self):
        result, _ = Machine(self.image, 0x3000).run("cover", state(255, PATTERNS[1]))
        self.assertEqual((result["state"]["frame"], result["state"]["midpoint"], result["state"]["callback"]),
                         (0, 0x79, 0x4567))
        self.assertFalse(any(event[0] == "bomb" for event in result["events"]))

    def test_near_callback_switches_and_pattern_register_are_observed(self):
        result, _ = Machine(self.image, 0x2000).run("cover", state(15))
        self.assertEqual((result["state"]["frame"], result["state"]["midpoint"], result["state"]["callback"]),
                         (0, 1, 0x1F2A))
        self.assertEqual([event for event in result["events"] if event[0] == "bomb"],
                         [("bomb", (0x3932,)), ("bomb", (0x395A,))])

    def test_successful_exec_has_no_return_path(self):
        result, _ = Machine(self.image, 0x2000).run("exec", state(success=True))
        self.assertTrue(result["replaced"])
        self.assertIsNone(result["ax"])

    def test_failure_preserves_signed_ax_result(self):
        result, _ = Machine(self.image, 0x3000).run("exec", state(status=0x8001))
        self.assertEqual(result["ax"], -32767)
        self.assertFalse(result["replaced"])
