# TH03 — current next-agent handoff (2026-11-07)

**Start here.** This is the active short handoff; detailed per-experiment
history through after709 was moved, unchanged in substance, to
[RE_HANDOFF_ARCHIVE_AFTER709.md](RE_HANDOFF_ARCHIVE_AFTER709.md).
Older roots are [after596](RE_HANDOFF_ARCHIVE_AFTER596.md) and
[after554](RE_HANDOFF_ARCHIVE_AFTER554.md). **Do not treat historical
“latest” paragraphs as current state.** Read [AGENTS.md](../AGENTS.md)
and [the workflow](RE_WORKFLOW.md) before modifying native evidence.

## Current verified checkpoint — what it proves, and what it does not

- **Latest affected source-native proof: `af736a`.** Two independent original
  TC4 4.02 / TLINK rounds compiled **seven complete original physical
  current-source TUs together**: Kotohime/Yumemi **large BOSSes**, the
  large ENEDAT enemy script interpreter `efornb`, and original input
  modes, PI loader, KAJA driver and PC-98 exit owners. All **5,796 original
  CODE bytes, 716 literal ordered OMF FIXUPPs, 37 PUBLICs** and complete
  segment/source dependencies match; the complete normal MAIN/MAP,
  Japanese 124,642-byte loaded program, 1,553 relocations and separately
  serialized 130,882-byte original MAIN.EXE match in both rounds.
  **92 other project objects and CRT reused**, no full cold replay.
- **New original-source routes:** the scoped compiler now directly
  validates `inp_m_w` (nine input/CPU/joystick/wait routines), `pi_load`
  (original PI load/unload), `snd_kaja` (PMD/MIDI interrupt) and `exit`
  (PC-98 display/access page registers) as four distinct original physical
  source TUs. Input release/press polling has natural signed-loop/Boolean
  C++ while preserving the original 9999-frame sentinel. Kotohime/Yumemi
  fixed power-of-two phase masks and the full enemy script VM now have
  fresh current-source native codegen proof. Rejected AL-byte, coordinate
  local, Spawn flag, PI return and input-bit rewrites remain protected
  negative-control evidence, **not accepted source**.
- **Previous affected-scope, current-live-source MAIN proof: `af730a`.** Two
  independent original TC4 4.02/full normal TLINK rounds compiled **six
  complete original physical TUs together**: full player `core` and its
  nested state machine, Rikako/Reimu **major BOSSes**, PMD sound effect
  manager, signed Q8 `polar` math, and original CFG resident loader.
  This covered **7,027 complete original CODE bytes, 769 literal ordered
  OMF FIXUPP fields, 42 PUBLICs**, full original segment/BSS contracts,
  the complete normal MAIN/MAP, Japanese loaded program and all 1,553 MZ
  relocations. Original Japanese 130,882-byte MZ bytes matched after
  independent standard serialization; 93 other original game objects
  and CRT were **reused, not recompiled**. No cold replay.
- **Deeper current source guards:** after725 the `core` original TU now
  force-binds all **ten** maintained direct/nested implementation `.inl`
  bodies (including the large `player_state_update`), not merely Hyper.
  A regression in reading historical source evidence was discovered
  and fixed: prior-to-725 receipts like `af709a` are reviewed against
  their **original hyper-only** compiler input contract; post-725 proofs
  require all ten current source paths and compiler-emitted dependencies.
  Read-only review of old `af709a`, current `af725d` and new `af730a`
  all passes; historical receipts were **not** repinned or mutated.
- **Original additional physical sources now directly proved:** `snd_se`
  (120 original CODE), `polar` (26 CODE), and `cfg_lres` (49 CODE), including
  exact original OMF segment/fixup metadata. Natural C++ changes to the
  BOSS renderer masks, CPU charge/target cadence, sound priority lookups
  and Q8 polar expression were tested in actual native outputs, with
  negative controls retained and source-unequal forms rejected.
- **Prior seven-source affected-scope MAIN proof: `af724a`.** Two
  independent original TC4 4.02 / TLINK rounds **simultaneously rebuilt
  seven complete current original physical TUs**: three large Marisa/Mima/
  Ellen BOSSes, complete `intro` HUD, Bullet engine, newly directly
  source-proved original `initmain` and `hud_stat`. All **9,792 initialized
  CODE bytes, 1,055 ordered native FIXUPPs and 59 PUBLIC offsets**,
  original segment/group ABI and native source dependencies, full normal
  MAIN EXE/MAP, Japanese loaded image and all 1,553 ordered relocations
  matched. 92 other original project objects and CRT were reused. The
  independent standard MZ serializer reproduced the complete original
  130,882-byte Japanese MAIN.EXE. No full cold replay.
- **Earlier `af721a` five-source integration remains separately retained.**
  Two independent original TC4/TLINK rounds rebuilt
  **five genuinely modified complete original physical TUs**: Marisa,
  Mima and Ellen **large BOSSes**, full `intro` HUD particle/animation
  and the complete Bullet/trail engine. All **9,191 CODE bytes, 1,030
  ordered literal native FIXUPPs and 51 PUBLIC offsets**, original
  source and intro `.inl` dependencies, full normal MAIN/MAP, Japanese
  loaded programs and all 1,553 MZ relocations matched. 94 other original
  project objects and original CRT were reused, **not recompiled**.
  Independent standard MZ serialization reproduced the complete original
  130,882-byte Japanese MAIN.EXE.
- **Earlier four-source checkpoint retained separately:** `af715a`
  compiled four complete modified TUs together: Yumemi/Chiyuri **BOSSes**,
  main `entry`/stage/frame scheduler and full CPU movement/dodge logic.
  That retained scope matched 9,139 original CODE bytes, 1,221 ordered
  fixups and 33 PUBLICs. It was not rebuilt again in after721/724/730. This is
  **not** an additional disjoint byte-ownership count.
- **New source-binding routes:** the scoped native compiler now accepts
  both the full `entry` physical TU with its four current included `.inl`
  implementations **and** the full `intro` physical TU with its three
  current HUD particle/renderer `.inl` implementations. Borland OMF
  dependencies are forced and independently reviewed, rather than trusting
  stale historical include copies. Marisa/Mima hardware-masked BOSS
  renderers now naturally allocate the historical SI local; Ellen's
  large radial/three-strip controllers, Bullet loops and HUD particle
  state machine have newly source-verified natural C++ operations. The
  register-specific hardware instructions that could not compile exactly
  from C++ are intentionally retained; see negative stages. The current
  compiler additionally binds original `initmain` and `hud_stat` source
  owners, whose direct original compiler segment/BSS and fixup contracts
  were newly source-verified. `hud_stat` cannot declare an extra C++
  `main_01` group without changing its original OMF relocation frames.
- **Previous after709 proof remains separately retained:** `af709a`
  rebuilt five original Kana/split-shared-BOSS/core/lose TUs (6,622 CODE,
  701 ordered FIXUPPs and 42 PUBLICs) in two rounds, with original MAIN/MAP
  and loaded-image checks. The **historical after709 accumulated union**
  covered **58 original physical source TUs, 66,407 CODE bytes, 7,303
  fixups and 367 PUBLICs**. These are a historical deduplicated union of
  separate native proofs, **not** a simultaneous 58-object compiler run or
  an independently recomputed after730 coverage figure. Entry had already
  been source-proved historically in after594; no duplicate distinct-owner
  count is claimed here.
- **Frozen parent/full MAIN:** ordinary after596 original 99-object source-
  native TLINK is still the unchanged parent. The direct TLINK DOS header
  differs from the original Japanese executable; the separately normalized
  MZ serializer matches the file. Neither step proves historical raw
  vendor OMF record identity, whole-product source ownership or canonical
  packed-file Factory acceptance.
- **MAINL remains distinct:** the historical after587 decoded ending EXE,
  MAP and 677 relocations remain retained, but current source-bound decoded
  publication is **PENDING** after later source changes invalidated an old
  input guard. Do not advertise that historical proof as current
  acceptance. OP/ZUN have their own retained decoded evidence and
  outstanding canonical packed-file/whole-product claims.

Read [the latest after736 seven-source review](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER736_REVIEW.md),
[the earlier after730 six-source review](MAIN_SIX_SOURCE_INTEGRATION_AFTER730_REVIEW.md),
[the earlier after724 seven-source review](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER724_REVIEW.md),
[the earlier after721 five-source review](MAIN_FIVE_SOURCE_INTEGRATION_AFTER721_REVIEW.md),
[the previous after715 four-source review](MAIN_FOUR_SOURCE_INTEGRATION_AFTER715_REVIEW.md)
and [the historical after709 union](MAIN_FIFTYEIGHT_SCOPED_SOURCE_AFTER709_REVIEW.md)
for exact scopes, controls, provenance and replay limitations.

### Fast, non-rebuilding verification

From the repository root (keep the original Japanese pinned targets):

```sh
git status -sb
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af736a
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af730a
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af724a
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af721a
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af715a
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af709a
.venv/bin/python scripts/validate_tracking.py
.venv/bin/python scripts/progress.py --check
git diff --check
```

The latest protected read-only proof root is
`.analysis/work/exatt-layout-af736a/report.json`, containing the seven
new current-source original native object rounds and full TLINK receipts.
The earlier six-TU root is
`.analysis/work/exatt-layout-af730a/report.json`, including all ten nested
`core` source snapshots and both actual six-unit compiler/linker rounds.
The earlier protected seven-TU integration root is
`.analysis/work/exatt-layout-af724a/report.json`, including both actual
rounds, the two newly bound physical owners and all three HUD `.inl`
dependency snapshots. The earlier five-source `af721a` proof is retained.
Earlier protected proof `.analysis/work/exatt-layout-af715a/report.json`
remains source-bound and unchanged.
Evidence roots (ignored but **protected**) also include
`.analysis/work/exatt-layout-af709a/report.json` plus its actual
two-round OBJ, EXE, MAP, writer logs, source/header snapshots and
the `TH03WORK/probe/af709a` compiler worktree. Other relevant
receipts: `af703a` (7 edited TUs), `af693a` (6 edited TUs),
`af686a` (47 selected TUs) and frozen after596 MAIN.
Review the [after736 current seven-source report](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER736_REVIEW.md),
[after730 prior six-source report](MAIN_SIX_SOURCE_INTEGRATION_AFTER730_REVIEW.md),
[after724 seven-source integration](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER724_REVIEW.md),
[after721 prior five-source integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER721_REVIEW.md),
[after715 prior integration](MAIN_FOUR_SOURCE_INTEGRATION_AFTER715_REVIEW.md)
and [after709 cumulative report](MAIN_FIFTYEIGHT_SCOPED_SOURCE_AFTER709_REVIEW.md)
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
