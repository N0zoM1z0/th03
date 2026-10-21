"""Pending maintained registration does not earn source/exact acceptance."""
import importlib.util
from pathlib import Path
from unittest.mock import patch
import unittest
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("regist_progress", ROOT / "scripts/progress.py")
progress = importlib.util.module_from_spec(spec); spec.loader.exec_module(progress)
def units():
    return [{"id": "th03-mainl-decoded-" + name, "artifact": "th03-mainl", "segment": "decoded:095F",
             "offset": offset, "size": size, "boundary_state": "reviewed", "state": "boundary-reviewed", "source": ""}
            for name, offset, size in (("regist", "0x189e", "2720"), ("scoredat", "0x17b9", "229"))]
class PendingTests(unittest.TestCase):
    def test_pending_caption_without_credit(self):
        rows = units()
        self.assertTrue(progress.mainl_regist_source_pending(rows))
        svg = progress.render_svg(rows, [])
        self.assertIn("17 bodies / 2,949 B owned", svg)
        self.assertIn("native proof pending", svg)
        self.assertIn("Source 0/2", svg)
        self.assertIn("exact 0/2", svg)
    def test_mutated_or_incomplete_scopes_rejected(self):
        for key, value in {"state": "source-present", "size": "2721", "source": "src/mainl/regist.cpp"}.items():
            rows = units(); rows[0][key] = value
            self.assertFalse(progress.mainl_regist_source_pending(rows))
        self.assertFalse(progress.mainl_regist_source_pending(units()[:1]))
        self.assertFalse(progress.mainl_regist_source_pending(units() + units()))
    def test_absent_owner_hides_caption(self):
        with patch.object(Path, "is_file", return_value=False):
            self.assertFalse(progress.mainl_regist_source_pending(units()))


def accepted_units():
    rows = units()
    for row, name in zip(rows, ("regist", "scoredat")):
        row.update(state="source-present", source="src/mainl/" + name + ".cpp",
                   evidence_ids=";".join(progress.MAINL_REGIST_SOURCE_EVIDENCE[name]))
    return rows

def accepted_evidence():
    evidence=[]
    for row, unit in zip(accepted_units(), ("regist", "scoredat")):
        for name, kind in progress.MAINL_REGIST_SOURCE_EVIDENCE[unit].items():
            evidence.append({"id":name,"artifact":"th03-mainl","unit_id":row["id"],
                "oracle":"analysis-bundle","extent_start":row["offset"],"extent_size":row["size"],
                "evidence_class":kind,"result":"pass","output_sha256":progress.MAINL_REGIST_SOURCE_RECEIPT})
    return evidence

class SourceCaptionTests(unittest.TestCase):
    def test_both_owned_scopes_count_without_exact(self):
        rows=accepted_units(); evidence=accepted_evidence()
        self.assertTrue(progress.mainl_regist_hybrid_source(rows,evidence))
        svg=progress.render_svg(rows,[],evidence)
        self.assertIn("6 PI bytes still differ",svg)
        self.assertIn("Source 2/2",svg)
        self.assertIn("exact 0/2",svg)
        self.assertEqual(progress.mainl_unit_progress(rows)["source_bytes"],2949)
    def test_missing_or_mutated_proof_hides_caption(self):
        for changes in ({"result":"fail"},{"output_sha256":"0"*64},{"evidence_class":"binary"}):
            evidence=accepted_evidence();evidence[0].update(changes)
            self.assertFalse(progress.mainl_regist_hybrid_source(accepted_units(),evidence))
        self.assertFalse(progress.mainl_regist_hybrid_source(accepted_units(),accepted_evidence()[:-1]))
        self.assertFalse(progress.mainl_regist_hybrid_source(units(),accepted_evidence()))
