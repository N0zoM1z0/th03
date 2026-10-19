# MAIN combined cold proof — 2026-10-19

At source checkpoint `61aed81a2b7299efb73f3fad96fa2f0167135f62`, fresh default
and cumulative Marisa/Reimu/Mima replays each passed two independent cold
rounds. The installed strict four-output preservation verifier also passed.
This is bounded repository proof, **not Factory acceptance, ledger exact
promotion, whole-game completion or a whole-game percentage**.

## Scope and result

- Default: 74 declared extents, 334 functions, 53,122 owned bytes.
- Combined: 78 extents, 371 functions, 59,624 owned bytes: 58,701 function bytes
  plus 923 pre-existing producer bytes. The authored candidate delta is 6,502
  bytes / 37 functions (Marisa 1958/10, Reimu/shared 2373/14, Mima 2171/13).
- Both rounds pass the original raw-byte, MAP, literal relocation, behavior,
  completeness and configured determinism gates. Game objects and products
  agree between rounds. **All-object equality is false**: the same nine
  non-game `obj/Research/{086,286,386}/{if_shift,wide,xfade}.obj` metadata drifts
  remain disclosed; no new all-object equality claim is made.
- Across all four outputs, the entire load payload outside combined intervals
  `[142D0,158F5)` and `[17043,17384)` and its literal relocation subsequence
  match the fresh default baseline. The verifier checks DATA/BSS metadata and
  file-backed contents, including 241 allocation rows; uninitialized BSS has
  no file bytes. Source/tool/control inputs are bound and unchanged.
- The retained HITBOX tail `[158F5,159FF)` additionally matches target bytes
  and literal relocations in every output. It remains reference-owned, with
  **zero additional authored-byte credit**. No other excluded/remainder range
  is promoted by baseline preservation.
- Both supervisors exited zero, retained no claim and reported no cleanup
  uncertainty. The round-initializer candidate remains outside this proof.

## Pinned results

Paths below are relative to the repository and retained intact.

| Artifact | Path | SHA-256 |
|---|---|---|
| Default receipt | `.analysis/th03-main-exact/gpt-dots-mima-default-cold-v02/receipt.json` | `a615005f2b98ebc09762e2ae4a0bfd1bea2381ef8ebf82209324f63c523c7e1d` |
| Combined receipt | `.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/receipt.json` | `49131a744e05826ffb5fc14316932f46e9e3fa8b9c138e329952cd5cea6d7981` |
| Default completion | `.analysis/th03-main-serial/runs/gpt-dots-mima-default-cold-v02/completion-evidence.json` | `6eb796b6280a772e9f9b0dec5d0e0c48a3cf6cdd92d2f478dabf6aa2bb8e0433` |
| Combined completion | `.analysis/th03-main-serial/runs/gpt-dots-mima-combined-cold-v02/completion-evidence.json` | `0a26b9516ed46a83e9de5080c18a9a2c29a7640ba3edb79b4c07900156bd9136` |
| Strict preservation | `.analysis/gpt-dots-mima-gameplay-source-v01/cold-plan-v02/four-output-preservation.json` | `e9d4547276cc9f85eb88966356f70864857a7462e33bd3caa15d116af41b9359` |
| Frozen launch plan | `.analysis/gpt-dots-mima-gameplay-source-v01/cold-plan-v02/fresh-four-output-plan-v02.json` | `3d27e8db71642e916476f94c6b4a5235d31084b8cceaeb24b0780296fc6c5e9b` |

Original target remains
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`, with
candidate-local-attested provenance. Reference revision remains
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47` (archive
`9f7a4eb17f24ae2d99adaba4320f6c46f4fc8d659f9b784f6d8e5f3af99bf705`).
The frozen plan pins source inventories, candidate manifest, complete tool
surface, supervisor, scheduler, original Oracle, layout helper and verifier.
The small `MAIN_COMBINED_COLD_EVIDENCE.json` records the relevant control hashes
and evidence append baseline; the large certificates are retained, not copied.

## Executed commands and reproduction

The completed foreground invocations used the repository Python dependencies:

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/.venv/lib/python3.12/site-packages" python3 scripts/replay_th03_main_serial.py --foreground --run-id gpt-dots-mima-default-cold-v02
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/.venv/lib/python3.12/site-packages" python3 scripts/replay_th03_main_serial.py --foreground --run-id gpt-dots-mima-combined-cold-v02 --candidate-manifest config/th03_main_mima_gameplay_candidate.toml

Default completed at 08:29:16 UTC, combined at 08:36:00 UTC; strict verification
completed at 08:36:20 UTC. The strict command over these retained outputs is:

    python3 scripts/verify_th03_main_combined_preservation.py --default-receipt .analysis/th03-main-exact/gpt-dots-mima-default-cold-v02/receipt.json --candidate-receipt .analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/receipt.json --default-completion .analysis/th03-main-serial/runs/gpt-dots-mima-default-cold-v02/completion-evidence.json --candidate-completion .analysis/th03-main-serial/runs/gpt-dots-mima-combined-cold-v02/completion-evidence.json --launch-plan .analysis/gpt-dots-mima-gameplay-source-v01/cold-plan-v02/fresh-four-output-plan-v02.json --launch-plan-sha256 3d27e8db71642e916476f94c6b4a5235d31084b8cceaeb24b0780296fc6c5e9b --not-before 2026-10-19T08:20:57.623124+00:00 --report .analysis/gpt-dots-mima-gameplay-source-v01/cold-plan-v02/four-output-preservation.json

These exact IDs/report already exist and must not be reused or overwritten.
For another fresh experiment, review and freeze a new plan with unique IDs,
current source/control pins and a new UTC cutoff, then substitute those IDs
and plan/hash/cutoff consistently. For a read-only recheck of these outputs,
use a new report filename; source/control pin drift must fail closed.

## Historical failures remain evidence

The earlier retained-Reimu strict outside-order failure is unchanged history,
not erased by this combined result. Its carrier Mima ordering and startup
binding change were separate observations. See the retained failure narrative
in [Reimu/shared review](MAIN_REIMU_SHARED_GAMEPLAY_REVIEW.md).

The v01 four-output verifier failed with `independent pinned MAP mismatch` for
`ENEMY_2_TEXT` in `MAIN_04`, module `th03/e_enemy.cpp`. Its report remains
`.analysis/gpt-dots-mima-gameplay-source-v01/cold-plan-v01/four-output-preservation.json`,
SHA-256 `5eb120e7f2385ca70b51c3b82f27684a797175b3e74ce0dbcfc34d707a70868b`.
The reviewed MAP checker correction and new v02 plan were followed by entirely
fresh default and combined runs; v01 outputs did not replace new outputs.

Remaining: formal ownership/acceptance review, whole-product coverage, original
provenance and other artifacts. Existing source-present unit states remain
unchanged; this proof adds observations, not exact-state promotion.
