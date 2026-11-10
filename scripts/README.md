# Script entry points

Run from the repository root with `.venv/bin/python scripts/NAME.py`.
[Workflow](../docs/RE_WORKFLOW.md) gives execution order; [handoff](../docs/RE_HANDOFF.md)
gives current acceptance and open work. Detailed historical witnesses belong in
`config/`, rather than duplicated command descriptions here.

## Environment and checks

| Entry point | Purpose |
| --- | --- |
| `preflight.py` | Check targets, environment and tracking before work. |
| `status.py`, `status.py --json` | Display active inventory, canonical ledger, decoded publication and independent current source-native reviews. Pending publications include the failing input and native audit reason. |
| `progress.py`, `progress.py --check` | Generate or check the Markdown/SVG from the same verified statuses. All bars count tracked extents; MAIN's function ledger is separate. Private evidence is required to reproduce verified native rows. |
| `ci.py` | Default lightweight check: syntax of changed machine inputs and Git whitespace. It does not run tests, native tools or publication audits. |
| `ci.py --full` | Explicit broad unittest suite, tracking/progress, target/tool identities and available headless database checks. Historical private tests can require their original source checkout; see the limits below. |
| `verify_targets.py`, `attest_toolchain.py` | Check private target and installed native-tool identities. |
| `attest_analysis_toolchain.py`, `ghidra.py ARTIFACT check` | Check the complete Ghidra/JDK installation and re-attest a database. |
| `bootstrap_jwasm.py --check` | Check the bounded compatible ZUN emitter and pinned source identity. |

## Current cold builds and scope reviews

| Product | Entry point | Purpose |
| --- | --- | --- |
| MAIN selected current-source | `probe_th03_main_exatt_layout.py --stage NEW --units unitA,unitB`, `review_th03_main_source_overlay.py --stage NEW` | Preferred bounded original TC4/TLINK two-round source/OMF/MAP check for changed physical TUs. Reuse the other original objects; do not cold replay. |
| MAIN | `replay_th03_main_native.py` | Two source cold builds and current native-owner review. |
| MAIN | `build_th03_main_work.py --build --cold --runtime` | One source rebuild and entry/lose contracts. |
| MAIN | `review_th03_main_native_units.py` | Review current native extents, publics/MAP, bytes and ordered relocations. |
| OP | `build_th03_op_work.py` | Rebuild every project object twice, compare complete decoded/stored targets and lifecycle scopes. |
| OP | `review_th03_op_music_menu_work.py` | Complete Music Room native CODE and ordered relocations using the unchanged cold pair. |
| OP | `PYTHONPATH=scripts .venv/bin/python -m lib.op_select_native` | Complete two-TU character selection/score-loader CODE, source slices, native fields and ordered relocations. Run from the repository root. |
| OP | `review_th03_op_entry_data_work.py` | Full cold/cfg/menu/startup/DATA chain; actual nested execution, semantic initialized storage and prior-observation invariance. |
| OP | `review_th03_op_music_call_work.py` | Native same-CS far-call proof and fresh ordinary-far source control; no Music Room implementation credit. |
| MAINL | `review_th03_mainl_text_banks_work.py` | **Historical after554 dependency review**, retained for its root/picture/text bank native evidence; not the present source-publication gate. |
| MAINL | `review_th03_mainl_score_input_pi_after587_work.py` | Read-only historical after587 source-native full MAINL link and 677-relocation proof; current decoded publication now uses the separate `af1055m` refresh. |
| MAINL current Staff Roll | `review_th03_mainl_staff_native_probe.py --stage af942s --check` | Read-only complete current 19-procedure owner, two original compiler rounds and complete normal links. For new source changes, use its stage-specific builder with a fresh `afNNNs` stage. |
| MAINL current root controller | `review_th03_mainl_root_native_probe.py --stage af944r --check` | Read-only complete current 11-function owner, two original compiler rounds and complete normal links. Use its builder with a fresh `afNNNr` stage for source changes. |
| MAINL current Staff/root | `build_th03_mainl_current.py --stage NEW --build`, or omit `--build` for a read-only review | Two complete affected physical owners and full normal links in two original TC4 rounds. Current publication selects `af1055m`. |
| MAINL cold ancestor | `build_th03_mainl_work.py` | Retained full project/CRT recipe. Its current source composer now transports maintained C++; use the incremental entry point above to preserve the protected cold worktree. |
| MAINL | `build_th03_mainl_exception_work.py` | Scoped historical new/xalloc/xmsg producer; composes the reviewed 28-provider CRT baseline with retained project inputs, not a current Factory acceptance declaration. |
| MAINL | `build_th03_mainl_xx_work.py`, `review_th03_mainl_xx_work.py` | Native full-xx object,normal893-member library and actual product candidate;raw-different and unaccepted. Reuse unchanged cold inputs. |
| MAINL | `review_th03_mainl_staff_roll_work.py` | Full MAINL cold/resource/ending/staff/DATA/roll chain, including actual owned nested calls, input waits, fade and cleanup. |
| Shared | `review_th03_shared_input_work.py` | Bind both OP/MAINL cold pairs to input policy and MAINL ending-wait contracts. |
| ZUN | `build_th03_zun_work.py` | Native launcher/directory/payload cold pair and complete stored/decoded comparison. |
| ZUN | `review_th03_zun_ongchk_work.py` | Full cold/formatter/graphics/lifecycle/DATA/wrapper/directory/source/ONGCHK chain. |
| ZUN | `build_th03_zun_driver_work.py` | Standalone compatible sprite16 producer and native source controls. |

OP's intermediate `review_th03_op_{cfg,dispatch,attract,sound,helpers,render,vs,story,option,main_menu,startup}_work.py`
commands remain useful for bounded replays. MAINL sound and ZUN's individual
review stages also remain separate executable entry points. Their `INPUTS`,
`witness()` and `current_scope()` definitions specify exact prerequisites.

Where supported, `--current-cold` revalidates the complete existing
source/SDK/recipe/output pair before replaying that stage. It does not rebuild
stale inputs or automatically refresh every earlier report. Default complete
chains create fresh prerequisites. Run them when changed native inputs require
that chain. After rebuilding OP/MAINL, revalidate affected shared inputs before
publishing; unchanged ancestor runtime observations need no routine replay.

## Publication

- `publish_th03_op_work_scopes.py`
- `publish_th03_mainl_work_scopes.py`
- `publish_th03_zun_work_scopes.py`

Publishers revalidate live graphs, complete output vectors and scoped witnesses.
They do not grant canonical packed-unit or whole-product source ownership.
MAINL's current decoded publication is restored through the `af1055m` Staff/root
refresh and unchanged retained ancestry. Use `publish_th03_mainl_work_scopes.py
--stage NEW` after a new verified Staff/root build. See the
[focused review](../docs/MAINL_CURRENT_SOURCE_REFRESH_AFTER1055_REVIEW.md). Missing current publication never falls back to
the old 145-owner mixed-product proposal. OP and ZUN have current decoded
publications; presentation code is not a MAINL/ZUN verifier input.
Changing an actual verifier requires revalidating the affected graph before a
new publication; do not edit historical evidence hashes.

## Audit and historical limits

The 2026-11-09 script audit parsed all 1,358 Python scripts and found no syntax
errors or missing literal `scripts/*.py` dependencies. Current reporting, CI
dispatch, cleanup guards and affected publication checks have focused tests.
Passing current checks are retained in
`.analysis/work/script-audit-affected-tests.log` and
`.analysis/work/script-audit-final-preflight.log`.
The broad unittest investigation is retained at
`.analysis/work/script-audit-baseline.log.gz` (losslessly archived; read with
`gzip -cd`). It is not a passing current-source
acceptance receipt: 574 errors stopped at the same historical Staff backend pin,
and older storage tests expect cleanup commands that now correctly refuse this
checkout. Some early private native runs are also absent. These historical
chains require their recorded source snapshots. The later `af1055m` refresh
repairs the current build/publication route; it does not reclassify the old
all-tests run as passing. Do not bypass source pins or rerun the
entire ancestry to update a progress chart.

## Diagnostics and local maintenance

| Entry point | Purpose |
| --- | --- |
| `probe_th03_main_producers.py` | Unresolved state/shot grouping and alignment controls; no new source credit. |
| `probe_th03_sound_nop_layout.py` | OP/MAINL natural trailing-byte investigation; annotated assembly controls are not acceptance. |
| `build_th03_mainl_after520_work.py`, `review_th03_mainl_after520_work.py` | **Historical after520 source stage**, retained as a native dependency, not a current entrypoint. The historical after554 selected source link and later after587 full-MAINL link are distinct evidence; current publication additionally requires its selected native refresh. |
| `cleanup_mainl_after520_handoff.py` | **Historical applied deletion audit:** protects its258-stage/5,760-file prefix; now rejects after521+ source. The old zero-candidate preview does not authorize cleanup here. |
| `cleanup_mainl_after439_handoff.py`, `cleanup_mainl_after388_handoff.py` | **Historical frozen cleanup guards**, not current deletion commands; deliberately reject this checkout. |
| `clean_generated.py` | Analysis preview only. `--apply` requires `--caches-only`; generic receipt pruning is rejected. Cache-only apply leaves `.analysis` untouched. |
| `cleanup_after710_disposable_native_stages.py --verify` | Read-only verification of the one-time after710 retired six unreferenced native tool-config failures and preserved audit SHA manifest. **Not** a general stage-pruning tool. |
| `closeout_cleanup.py` | Historical generic planner, now preview-only. `--apply` and `--retire-proof` are rejected; native evidence deletion requires a separate audited allowlist. |
| `import_targets.py`, `bootstrap_toolchain.sh`, `bootstrap_analysis_toolchain.sh` | Initial private input/tool installation. |

Historical replay/probe helpers can refer to deliberately deleted private runs.
They remain provenance/diagnostics, not the current build entry points. Some old
stagers are still called by live builders: names alone are not a deletion test.
Do not move frozen scripts merely to reorganize navigation; current recipes pin
paths and hashes. Product manifests and scoped observations are authoritative.

Keep heavy work headless, on one CPU at nice10, with one Borland/Wine writer.
Preserve the prefix, fixed inputs, installed tool trees and the entire active
source-bound receipt DAG, including both complete raw rounds and writer logs
at every retained stage. Source/proof code lives in `scripts/lib/`; behavior tests are in `tests/`.
