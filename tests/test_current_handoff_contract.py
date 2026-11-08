"""Small docs-only guard against silently reviving stale TH03 handoff claims.

This test never invokes original TC4, the linker, or a cold replay. The
current receipt hash and acceptance still require their separate reviewers.
"""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class CurrentHandoffContract(unittest.TestCase):
    def test_short_active_handoff_and_archived_previous_text(self):
        active = (DOCS / "RE_HANDOFF.md").read_text()
        archive = (DOCS / "RE_HANDOFF_ARCHIVE_AFTER927.md").read_text()
        self.assertIn("active handoff", active.lower())
        self.assertLess(len(active.splitlines()), 240)
        self.assertIn("ARCHIVED", archive[:100])
        self.assertGreater(len(archive.splitlines()), 2700)
        self.assertNotIn("## Latest after871", active)

    def test_readme_workflow_and_handoff_agree_on_current_stage(self):
        active = (DOCS / "RE_HANDOFF.md").read_text()
        readme = (ROOT / "README.md").read_text()
        workflow = (DOCS / "RE_WORKFLOW.md").read_text()
        m = re.search(r"current maintained-source native MAIN proof: `(af\d+[a-z])`", active)
        self.assertIsNotNone(m)
        stage = m.group(1)
        number = re.search(r"af(\d+)[a-z]", stage).group(1)
        self.assertIn(f"--stage {stage}", active)
        self.assertIn(f"latest after{number}", readme)
        self.assertIn(f"[after{number}]", workflow)
        self.assertIn("`af709a` is historical and source-stale", workflow)
        self.assertIn("0/259", active)
        self.assertIn("0/259", readme)

    def test_active_navigation_links_exist(self):
        for relative in ("docs/RE_HANDOFF.md", "docs/RE_WORKFLOW.md", "README.md"):
            path = ROOT / relative
            for url in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                target = url.split("#", 1)[0]
                if not target or target.startswith(("https://", "http://", "mailto:")):
                    continue
                with self.subTest(source=relative, link=target):
                    self.assertTrue((path.parent / target).exists())


if __name__ == "__main__":
    unittest.main()
