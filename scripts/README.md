# Script entry points

| Task | Command |
| --- | --- |
| Start a session | `python3 scripts/preflight.py` |
| Check game identity | `python3 scripts/verify_targets.py --game th03` |
| Import supplied archive | `python3 scripts/import_targets.py ARCHIVE --include-all-games-smoke --retain-runtime-image` |
| Check compiler/runtime surfaces | `python3 scripts/attest_toolchain.py` |
| Check analyzer installation | `python3 scripts/attest_analysis_toolchain.py` |
| Import/check headless database | `python3 scripts/ghidra.py ARTIFACT import` / `check` |
| Native Factory query wrapper | `python3 scripts/factory_ghidra.py --help` |
| Validate OMF | `python3 scripts/inspect_omf.py OBJECT` |
| Raw artifact comparison | `python3 scripts/compare_artifacts.py --help` |
| Cold reference build | `python3 scripts/build.py --reference --run-id UNIQUE` |
| Inspect open product graph | `python3 scripts/build.py --status` |
| Survey reference output | `python3 scripts/survey_rec98_outputs.py SOURCE --compact` |
| Check ledgers/progress | `python3 scripts/validate_tracking.py` / `scripts/status.py` |
| Regenerate progress | `python3 scripts/progress.py` |
| Available private/public checks | `python3 scripts/ci.py` |

Only one Borland writer may run. All tools are headless. Private artifacts
remain ignored, and diagnostic builds never count as game-source progress.
