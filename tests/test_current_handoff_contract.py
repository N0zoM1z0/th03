"""Check that current navigation links resolve; prose is reviewed through Git."""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class CurrentHandoffContract(unittest.TestCase):


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
