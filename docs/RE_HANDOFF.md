# TH03 — current next-agent handoff (2026-11-07)

**Start here.** This is the active short handoff; detailed per-experiment
history through after709 was moved, unchanged in substance, to
[RE_HANDOFF_ARCHIVE_AFTER709.md](RE_HANDOFF_ARCHIVE_AFTER709.md).
Older roots are [after596](RE_HANDOFF_ARCHIVE_AFTER596.md) and
[after554](RE_HANDOFF_ARCHIVE_AFTER554.md). **Do not treat historical
“latest” paragraphs as current state.** Read [AGENTS.md](../AGENTS.md)
and [the workflow](RE_WORKFLOW.md) before modifying native evidence.

## Current verified checkpoint — what it proves, and what it does not

- **MAIN original source-native local evidence:** `af709a` actually rebuilt
  **five complete original physical TUs** from the maintained Kana BOSS,
  split shared BOSS, player `core`/Hyper and `lose`/defeat sources.
  Both independent original Turbo C++ 4.02/TLINK rounds matched
  **6,622 CODE bytes, 701 literal ordered FIXUPPs, 42 PUBLICs**,
  the entire normal original-source-native MAIN executable/MAP,
  Japanese loaded image and 1,553 ordered MZ relocations.
  Independent standard MZ serialization matches the full
  **130,882-byte Japanese MAIN.EXE**. The other **94** game project
  objects and CRT were reused, **not recompiled**.
- **Accumulated MAIN source coverage:** the retained independent receipts
  now cover the **union of 58 distinct physical source TUs**,
  **66,407 previously source-owned CODE bytes**, **7,303 literal
  ordered fixups** and **367 PUBLICs**. **This is not a fresh
  58-TU compiler run.** The prior after703 union had 56 TUs;
  `core` and `lose` were added in after706–709.
- **Frozen full MAIN parent:** original 99-object normal link after596
  remains the baseline. The ordinary new TLINK output header is
  **not historically byte-identical** to the Japanese file; the
  independently normalized/serialized MZ is. Never confuse
  loaded-code equality with original compiler/vendor raw OBJ packet
  identity, whole-product source ownership or canonical packed-file
  Factory acceptance.
- **Canonical acceptance:** these later C++ refactors and extra
  native source scopes contributed **no new accepted canonical packed
  game bytes**. See the authoritative generated [progress ledger](PROGRESS.md),
  not the “proof owner” count, for actual acceptance.
- **MAINL:** the historical after587 native decoded link and all
  677 relocations remain retained evidence, **but current source-bound
  decoded publication is PENDING** after subsequent source changes
  invalidated its preserved-source guard. Do not advertise historical
  extent/byte totals as present acceptance. Use the current
  [progress ledger](PROGRESS.md) and independent reviewer before
  resolving this gate. OP/ZUN have separately retained decoded
  evidence; their canonical packed-file/whole-product ownership
  claims remain distinct.

### Fast, non-rebuilding verification

From the repository root (keep the original Japanese pinned targets):

```sh
git status -sb
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af709a
.venv/bin/python scripts/validate_tracking.py
.venv/bin/python scripts/progress.py --check
git diff --check
```

Evidence roots (ignored but **protected**) include
`.analysis/work/exatt-layout-af709a/report.json` plus its actual
two-round OBJ, EXE, MAP, writer logs, source/header snapshots and
the `TH03WORK/probe/af709a` compiler worktree. Other relevant
receipts: `af703a` (7 edited TUs), `af693a` (6 edited TUs),
`af686a` (47 selected TUs) and frozen after596 MAIN.
Review the particular [after709 native report](MAIN_FIFTYEIGHT_SCOPED_SOURCE_AFTER709_REVIEW.md)
for numbers, limits and exact commands. A new rebuild needs a **fresh
DOS-safe stage ID**; do not overwrite prior receipts.

## Do the next actual reconstruction work

1. Prioritize **unproved physical owner/ABI scopes and substantial
   BOSS/player functions**, with the small leaves that feed them;
   don't spend a turn re-counting already source-owned CODE.
   The 58-TU native proof union is **not** all 99 project TUs.
2. Challenge old source comments and v1 results. Original-byte
   exactness requires current maintained compiler-consumed source
   (emitted Borland OMF COMENT dependency), complete CODE and
   initialized DATA, literal ordered FIXUPPs, PUBLICs,
   segment/BSS ownership, real TLINK response and full MAIN/MAP.
   Equivalent math may produce different TC4 bytes; preserve
   signedness, operation order, 16-bit widths, register and
   near/far/Pascal ABI, RNG consumption and original bugs.
3. Use `scripts/probe_th03_main_exatt_layout.py --stage NEW --units a,b`
   to rebuild **only affected original TUs**, and
   `scripts/review_th03_main_source_overlay.py --stage NEW`
   for independent review. Reuse unchanged source-native
   objects and libraries in the original 99-object TLINK.
   Do not run another whole cold replay for routine source edits.
4. Consider the **MAINL current publication gate** separately:
   the after587 source/native evidence is historical, not a
   current signed-off decoded acceptance. Diagnose its exact source
   guard and re-review only affected dependency inputs rather than
   repinning original receipt hashes.
5. Commit each substantive verified improvement `gpt-web: xxx`,
   preserve rejected experiments and both original compiler rounds.
   Don't push without a request.

### Known physical-source traps

- `core` uses original link slot `probe/af593p/rN/core.obj`;
  `ch_setup` uses `probe/af592p/rN/ch_setup.obj`.
  `chain1/chain2` originals are in `obj/`, **not**
  `obj/th03/`. Yumemi Bomb's compiler shortname is
  `bomb~cxk` despite its original linker slot's long filename.
- `combo.cpp` physically emits two original TUs:
  `p_combo` (score/HUD) and `p_cmbhl` (fireball/BOSS/
  panic helpers). The original BOSS `shared.cpp` also emits
  two TUs (`ba_sring`/`ba_srest`). Compiler flags and
  original MAP module row counts are not interchangeable.
- Certain character Bomb `CODE` producers have **zero private BSS**:
  storage is owned by external frozen carriers. Recompiling with
  duplicate BSS changes relocation fields even when CODE sizes match.
- The active scoped compiler binds current `hyper.inl` and
  all four loss/defeat `.inl` bodies with explicit source
  snapshots and OMF dependency checks. It does **not**
  claim every other nested `.inl` in the core is newly
  modified or independently source-bound.
- Do not simplify an original `& 3` to `% 4`,
  prefix/postfix byte mutation or an original
  AL/AX/BX intermediate **without a full native comparison**.
  Multiple exact negative controls are documented.

## Storage and handoff discipline

The ignored `.analysis` contains the source-native receipt DAG,
both round outputs, original private toolchains and Japanese
targets. Do **not** delete by age or run
`clean_generated.py --prune-unreferenced-receipts`.
The current restricted policy and measured audits are in
[STORAGE_HANDOFF_CURRENT.md](STORAGE_HANDOFF_CURRENT.md).
Only verified disposable stage outputs and regenerable caches
may be removed; preserve an audit manifest with hashes before
deleting any bounded failed scratch stage.

For historical details and **negative codegen experiments**, use
[the archived chronology](RE_HANDOFF_ARCHIVE_AFTER709.md)
and the relevant `docs/MAIN_*_AFTER*_REVIEW.md`.
Avoid re-expanding this live handoff into a one-section-per-commit log.
