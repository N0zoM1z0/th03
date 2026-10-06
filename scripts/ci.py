#!/usr/bin/env python3
"""Run portable TH03 checks and available private headless identity gates."""

from pathlib import Path
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def run(*arguments: str) -> None:
    subprocess.run([sys.executable, *arguments], cwd=ROOT, check=True)


def main() -> int:
    try:
        run("-m", "unittest", "discover", "-s", "tests", "-q")
        run("-m", "compileall", "-q", "scripts", "tests")
        run("scripts/validate_tracking.py")
        run("scripts/progress.py", "--check")
        run("scripts/review_rec98_th03_mainl_intake.py", "--check")
        if (ROOT / "_reference/ReC98/.git").exists():
            run("scripts/inventory_rec98_th03.py", "--check")
        targets = tomllib.loads((ROOT / "config/targets.toml").read_text())["artifacts"]
        if all((ROOT / a["private_path"]).is_file() for a in targets if a["required"]):
            run("scripts/verify_targets.py", "--game", "th03")
        if all((ROOT / a["private_path"]).is_file() for a in targets):
            run("scripts/smoke_oracles.py")
        if (ROOT / ".analysis/toolchain/wineprefix/drive_c/TC4/BIN/TCC.EXE").is_file():
            run("scripts/attest_toolchain.py")
        if (ROOT / ".tools/ghidra/support/analyzeHeadless").is_file():
            run("scripts/attest_analysis_toolchain.py")
            for artifact in (a for a in targets if a["required"]):
                if (ROOT / f"ghidra-project/TH03-{artifact['id']}.gpr").is_file():
                    run("scripts/ghidra.py", artifact["id"], "check")
                    run("scripts/smoke_ghidra_oracle.py", artifact["id"])
        subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
        print("CI: PASS")
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"CI: FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
