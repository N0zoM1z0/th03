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
| Check frozen ReC98 TH03 intake queue | `python3 scripts/inventory_rec98_th03.py --check` |
| Replay all maintained MAIN exact owners | `python3 scripts/replay_th03_main_exact_units.py --run-id UNIQUE` |
| Review raw enemy boundaries and dispatch table | `python3 scripts/review_th03_main_enemy.py --output .analysis/REVIEW/raw-review.json` |
| Review complete MAIN character charge/gauge boundaries | `python3 scripts/review_th03_main_charge_gauge.py --output .analysis/REVIEW/charge-gauge.json` |
| Review complete MAIN boss-attack boundaries and TC4 switch tables | `python3 scripts/review_th03_main_boss.py --output .analysis/REVIEW/boss.json` |
| Probe Chiyuri charge/gauge TC4 object shape | `python3 scripts/probe_th03_main_chargeshot_chiyuri_cpp.py --run-id UNIQUE` |
| Probe Ellen charge/gauge TC4 object shape | `python3 scripts/probe_th03_main_chargeshot_ellen_cpp.py --run-id UNIQUE` |
| Probe Kana charge/gauge TC4 object shape | `python3 scripts/probe_th03_main_chargeshot_kana_cpp.py --run-id UNIQUE` |
| Probe Kotohime charge/gauge TC4 object shape | `python3 scripts/probe_th03_main_chargeshot_kotohime_cpp.py --run-id UNIQUE` |
| Probe Rikako charge/gauge TC4 object shape | `python3 scripts/probe_th03_main_chargeshot_rikako_cpp.py --run-id UNIQUE` |
| Export complete raw MAIN owner observations | `python3 scripts/review_th03_main_code.py --owner OWNER_ID --output .analysis/REVIEW/raw-review.json` |
| Inspect open product graph | `python3 scripts/build.py --status` |
| Survey reference output | `python3 scripts/survey_rec98_outputs.py SOURCE --compact` |
| Check ledgers/progress | `python3 scripts/validate_tracking.py` / `scripts/status.py` |
| Preview disposable outputs | `python3 scripts/clean_generated.py` |
| Audited cleanup with documented-path protection | `python3 scripts/closeout_cleanup.py --output .analysis/closeout/UNIQUE/receipt.json --apply` |
| Replay latest shared input/timing carrier proof | `python3 scripts/replay_th03_shared_input.py --run-id UNIQUE` |
| Check MAINL candidate index policy | `python3 scripts/review_rec98_th03_mainl_intake.py --check` |
| Regenerate progress Markdown/SVG | `python3 scripts/progress.py` |
| Available private/public checks | `python3 scripts/ci.py` |

Only one Borland writer may run. All tools are headless. Private artifacts
remain ignored, and diagnostic builds never count as game-source progress.

Reconstruction resumed on 2026-10-07. The current handoff records active state;
the closeout record is the historical 2026-10-06 snapshot.

`closeout_cleanup.py` defaults to an audited dry run. It preserves the existing
cleanup policy plus literal tracked private references, freezes references and
candidates before deletion, and records retained input states. Optional
`--retire-proof PATH` selects one superseded top-level unaccepted diagnostic;
any live ledger/document/JSON dependency rejects retirement. Historical corpus
fingerprints remain records of past existence. Use a fresh receipt path and
finish all builds/replays before cleanup. Never delete evidence by age alone.
