# Script entry points

Run from the repository root with `.venv/bin/python scripts/NAME.py`.
[Workflow](../docs/RE_WORKFLOW.md) gives execution order; [handoff](../docs/RE_HANDOFF.md)
gives current acceptance and open work. Detailed historical witnesses belong in
`config/`, rather than duplicated command descriptions here.

## Environment and checks

| Entry point | Purpose |
| --- | --- |
| `preflight.py` | Check targets, environment and tracking before work. |
| `status.py`, `progress.py --check` | Verify and display current ledger/publication state. `progress.py` regenerates progress documents. |
| `ci.py` | Tests, tracking/progress, target/tool identities and available headless database checks. |
| `verify_targets.py`, `attest_toolchain.py` | Check private target and installed native-tool identities. |
| `attest_analysis_toolchain.py`, `ghidra.py ARTIFACT check` | Check the complete Ghidra/JDK installation and re-attest a database. |
| `bootstrap_jwasm.py --check` | Check the bounded compatible ZUN emitter and pinned source identity. |

## Current cold builds and scope reviews

| Product | Entry point | Purpose |
| --- | --- | --- |
| MAIN | `replay_th03_main_native.py` | Two source cold builds and current native-owner review. |
| MAIN | `build_th03_main_work.py --build --cold --runtime` | One source rebuild and entry/lose contracts. |
| MAIN | `review_th03_main_native_units.py` | Review current native extents, publics/MAP, bytes and ordered relocations. |
| OP | `build_th03_op_work.py` | Rebuild every project object twice, compare complete decoded/stored targets and lifecycle scopes. |
| OP | `review_th03_op_main_menu_work.py` | Full cold/cfg/dispatch/attract/sound/helper/renderer/VS/story/option/main chain; actual owned callee contexts and legacy invariance. |
| OP | `review_th03_op_music_call_work.py` | Native same-CS far-call proof and fresh ordinary-far source control; no Music Room implementation credit. |
| MAINL | `build_th03_mainl_work.py` | Two complete project/CRT builds, normal TLIB membership/order, decoded/stored equality and lifecycle scopes. |
| MAINL | `review_th03_mainl_dissolve_work.py` | Full MAINL cold/sound/root-helper/PI/CDG/ending/staff drawing/snow and dissolve chain. |
| Shared | `review_th03_shared_input_work.py` | Bind both OP/MAINL cold pairs to input policy and MAINL ending-wait contracts. |
| ZUN | `build_th03_zun_work.py` | Native launcher/directory/payload cold pair and complete stored/decoded comparison. |
| ZUN | `review_th03_zun_ongchk_work.py` | Full cold/formatter/graphics/lifecycle/DATA/wrapper/directory/source/ONGCHK chain. |
| ZUN | `build_th03_zun_driver_work.py` | Standalone compatible sprite16 producer and native source controls. |

OP's intermediate `review_th03_op_{cfg,dispatch,attract,sound,helpers,render,vs,story,option}_work.py`
commands remain useful for bounded replays. MAINL sound and ZUN's individual
review stages also remain separate executable entry points. Their `INPUTS`,
`witness()` and `current_scope()` definitions specify exact prerequisites.

Where supported, `--current-cold` revalidates the complete existing
source/SDK/recipe/output pair before replaying that stage. It does not rebuild
stale inputs or automatically refresh every earlier report. Default complete
chains create fresh prerequisites. Use shared-input review after rebuilding
OP/MAINL, then publish.

## Publication

- `publish_th03_op_work_scopes.py`
- `publish_th03_mainl_work_scopes.py`
- `publish_th03_zun_work_scopes.py`

Publishers revalidate live graphs, complete output vectors and scoped witnesses.
They do not grant canonical packed-unit or whole-product source ownership.
Shared verifier changes can invalidate multiple publications; refresh affected
products before regenerating progress.

## Diagnostics and local maintenance

| Entry point | Purpose |
| --- | --- |
| `probe_th03_main_producers.py` | Unresolved state/shot grouping and alignment controls; no new source credit. |
| `probe_th03_sound_nop_layout.py` | OP/MAINL natural trailing-byte investigation; annotated assembly controls are not acceptance. |
| `clean_generated.py` | Preview disposable analysis/cache cleanup; `--apply` deletes and `--keep-analysis PATH` retains an active input; `--caches-only` leaves all `.analysis` state alone. |
| `closeout_cleanup.py` | Receipt-based cleanup planning/application with input/reference drift checks. |
| `import_targets.py`, `bootstrap_toolchain.sh`, `bootstrap_analysis_toolchain.sh` | Initial private input/tool installation. |

Historical replay/probe helpers can refer to deliberately deleted private runs.
They remain provenance/diagnostics, not the current build entry points. Some old
stagers are still called by live builders: names alone are not a deletion test.
Do not move frozen scripts merely to reorganize navigation; current recipes pin
paths and hashes. Product manifests and scoped observations are authoritative.

Keep heavy work headless, on one CPU at nice10, with one Borland/Wine writer.
Preserve the prefix, fixed inputs, installed tool trees and one current build per
product. Source/proof code lives in `scripts/lib/`; behavior tests are in `tests/`.
