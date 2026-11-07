# TH03 — current next-agent handoff (2026-11-07)

**Start here.** This is the active short handoff; detailed per-experiment
history through after709 was moved, unchanged in substance, to
[RE_HANDOFF_ARCHIVE_AFTER709.md](RE_HANDOFF_ARCHIVE_AFTER709.md).
Older roots are [after596](RE_HANDOFF_ARCHIVE_AFTER596.md) and
[after554](RE_HANDOFF_ARCHIVE_AFTER554.md). **Do not treat historical
“latest” paragraphs as current state.** Read [AGENTS.md](../AGENTS.md)
and [the workflow](RE_WORKFLOW.md) before modifying native evidence.

## Current verified checkpoint — what it proves, and what it does not

- **Latest current-source original TC4/TLINK integration: `af758a`.** Two
  independent original TC4 4.02 and complete normal MAIN TLINK rounds
  simultaneously rebuilt **12 complete original physical TUs**, covering
  Chiyuri/Marisa/Mima **large BOSSes**, full Fireball/Explosion engines,
  Ellen/Kotohime Extra Attacks, both Combo scoring/BOSS-panic partitions,
  complete Ellen Chargeshot and the two Extra Attack/Gauge leaf owners.
  All **12,979 initialized original CODE bytes, 1,429 literal ordered OMF
  FIXUPPs, 71 PUBLICs**, complete segment/current-source dependency
  metadata, full normal MAIN/MAP, Japanese 124,642-byte loaded game and
  **all 1,553 original MZ relocations** match. Independent standard MZ
  serialization reproduces the **130,882-byte original Japanese MAIN.EXE**.
  **87 other project objects and CRT reused**, no full cold replay.
- **New original-native C++ register recovery:** Ellen's 10-function
  Chargeshot module `cs_ellen` now uses **normal typed C++ `register`
  SI/DI sprite-coordinate locals** in place of manual `_SI`/`_DI`/`_AX`
  writes. Actual TC4 emits original code with the restored declaration
  order; reversing the locals failed native codegen. Its full deceleration,
  tracking, collision and Gauge emitters are compiled as one object.
  Kotohime's complete eight-function Extra Attack, both Combo source
  partitions and both leaf objects also have actual codegen-verified
  natural C++ recovery and retained negative-control trials.
- **Keyboard `input_s` remains blocked** (not part of `af758a`): its
  current C++ matches the true original 417-byte physical OBJ, but the
  frozen after596 parent linker used an extra trailing 0x90 NOP in a
  418-byte experimental OBJ, so full MAIN link exactness fails by one
  byte. Never count this as accepted original full-link reconstruction.
- **Previous ten-source checkpoint: `af753a`.** Two real
  independent original Turbo C++ 4.02/full TLINK rounds simultaneously
  rebuilt **ten complete modified original physical TUs**: Chiyuri,
  Marisa and Mima **major BOSSes**, Fireball, Ellen/Kotohime Extra
  Attacks, explosion-chain collision, **both** separately linked Combo
  scoring/BOSS panic source partitions, and full Ellen charged-shot
  targeting/Hyper/Gauge. All **12,883 CODE bytes, 1,426 literal
  ordered original OMF FIXUPP fields and 69 PUBLICs**, real native
  source dependencies, segment and DATA/BSS ABI, complete normal
  MAIN EXE/MAP, Japanese 124,642-byte loaded program and all 1,553
  ordered relocations match. Independently serialized original Japanese
  **130,882-byte MAIN.EXE** also matches both rounds. **89 other
  original project objects and CRT reused**, no full cold replay.
- **Additional dirty C++ source fully recovered:** complete Ellen charged-
  shot's 10-function original `cs_ellen` owner now uses natural register
  SI/DI allocation in its sprite leaf, along with native-exact 32-slot
  scan/update/hit/render C++ loops. Its final `af752e` codegen proof
  matches **1,530 original CODE bytes, 169 fixups and 10 PUBLICs**;
  reversing the register declaration order failed native CODE, so the
  original ordering is preserved. This owner joins all preceding nine
  changed source objects in the current ten-source `af753a` proof.
- **Previous nine-modified-TU current-source checkpoint: `af752a`.** Two
  genuinely independent original Turbo C++ 4.02/full TLINK rounds
  **compiled nine complete original physical TUs simultaneously**:
  Chiyuri/Marisa/Mima **major BOSSes**, full Fireball, Ellen/Kotohime
  Extra Attacks, large explosion collision and the two **distinct**
  physical Combo score/HUD and BOSS/panic producers from one current
  `combo.cpp`. All **11,353 original initialized CODE bytes, 1,257
  literal ordered OMF FIXUPP fields and 59 PUBLICs**, original
  DATA/BSS/segment/source dependencies, complete normal MAIN/MAP,
  Japanese 124,642-byte loaded program and all 1,553 relocations
  matched. Independent standard MZ serialization matches the original
  **130,882-byte Japanese MAIN.EXE** in both rounds. **90 other project
  objects and original CRT reused**, no cold replay or byte patch.
- **No dirty changed owners abandoned:** Mima's whole BOSS `af749d`,
  Kotohime's eight-function Extra Attack `af750d`, and **both original
  Combo physical partitions together** `af751d` were resumed, byte-
  checked and saved separately as `gpt-web:` commits, then **all three
  added to the joint after752 proof**. The older after748 five-TU
  receipt remains protected and still live-source reviewable.
- **Previous original-source affected-scope checkpoint: `af751a`.** Two
  independent real original Turbo C++ 4.02/full TLINK rounds rebuilt
  **seven complete modified physical original TUs together**: Chiyuri,
  Marisa and Mima **major BOSSes**, complete Fireball, Ellen and Kotohime
  Extra Attack controllers and the large explosion/chain collision
  function. All **10,375 original CODE bytes, 1,200 ordered OMF FIXUPP
  fields and 54 PUBLICs**, original DATA/BSS/segment contracts and actual
  compiler source dependencies, full normal MAIN EXE/normalized MAP,
  Japanese 124,642-byte loaded program and all 1,553 MZ relocations
  matched both rounds. Independent normal MZ serialization matched the
  complete **130,882-byte original Japanese MAIN.EXE**. **92 other project
  objects and original CRT were reused**, with no cold replay.
- **Dirty worktree owner recovery included:** Mima's full BOSS natural
  attack-phase/renderer edits were preserved and independently source-
  verified (`af749d`; 1,922 CODE / 277 fixups / 9 PUBLICs). The modified
  Kotohime Extra Attack 8-function state/volley owner was likewise
  continued and independently verified (`af750d`; 1,054 CODE / 100
  fixups / 8 PUBLICs). Rejected Mima opponent-ID register reuse and
  Kotohime byte `%4` mask / event-byte prefix remain native negative
  controls, **not** accepted source. Both are included in `af751a`.
- **Previous affected current-source original MAIN proof: `af748a`.** Two
  independent genuine Turbo C++ 4.02/full TLINK rounds **simultaneously
  rebuilt five complete changed original physical TUs**: full Chiyuri
  and Marisa major BOSSes, complete Fireball engine (including its one
  initialized DATA byte), six-function Ellen Extra Attack with original
  seven-point trail, and the large explosion collision/chain controller.
  All **7,399 original CODE bytes, 823 ordered OMF FIXUPP fields, 37
  PUBLICs**, segments/source dependencies, normal full MAIN EXE/MAP,
  Japanese 124,642-byte loaded image and all 1,553 MZ relocations matched.
  Independent standard MZ serialization matched all **130,882 original
  Japanese MAIN.EXE bytes**. **94 other project objects and original CRT
  reused**, no complete cold replay or object patching.
- **New exact-object but blocked-full-link native keyboard finding:**
  `input_s` now naturally expresses its two-pass BIOS/port-delay polling
  in current `src/main/hardware/input_sense.cpp`. Real TC4 compiles match
  the original **417 CODE bytes, 42 ordered original FIXUPPs and one
  PUBLIC**, but the frozen parent MAIN link used an older **418-byte**
  object with an additional trailing **0x90 NOP** (at CODE offset 417).
  Switching to the true 417-byte object changes **only raw EXE file byte
  68,141 from 90 to 00**, so **full MAIN exactness fails** for that unit.
  No padding/byte patch was added. Read
  [the explicit blocked-input proof](MAIN_INPUT_S_LINK_GAP_AFTER744_REVIEW.md)
  and the read-only `scripts/review_th03_input_s_link_gap_after744.py`
  diagnostic; it deliberately returns `normal_MAIN_exact=false`.
- **Current source-drift audit:** the read-only current reviewer passes
  `af748a`, unaffected `af741b` and unaffected `af730a`. It **rejects**
  older `af724a`, `af721a`, `af715a` current-input hashes after this
  turn's Marisa/Chiyuri changes; these remain intact historical native
  source/OBJ/linker snapshots, not live-current-source passes. The
  previously source-drifted `af736a` and `af709a` also remain historical.
- **Previous affected current-source proof: `af741b`.** Two original
  TC4 4.02/TLINK rounds **simultaneously rebuilt eight complete
  original physical TUs**: large Kana BOSS, large Yumemi Extra Attack,
  all four physical `enemy.cpp` formation/script/hittest/update objects,
  and original `frmdely1` VSYNC delay and MAIN `execl` handoff.
  All **6,995 original CODE bytes, 596 literal ordered OMF FIXUPPs,
  35 PUBLICs**, segments and compiler-consumed source dependencies
  match. The entire normal MAIN/MAP, Japanese 124,642-byte loaded
  program, all 1,553 relocations and separately serialized original
  130,882-byte Japanese MAIN.EXE match both rounds. **91 other original
  objects and CRT reused**, no full cold replay or object byte patch.
- **Newly current-source-bound owners:** the original `frmdely1` shared
  object lives at `obj/th02/frmdely1.obj` and occupies 21 CODE bytes in
  TH03; the original TH03 `execl` occupies 79 CODE bytes, including the
  genuine 16-bit far/near vararg handoff. Both now have actual current
  C++ source dependencies, whole-object native OMF fields and complete
  linked MAIN acceptance in this scoped proof. The source-native
  `enemy.cpp` also now passes **all four current compiled partitions**
  after the changed enemy hit/chain controller, not only `eupdb`.
- **Source-codegen negative controls:** direct Kana signed-AL expression,
  simplified Yumemi clip-side selection, enemy parity-expression
  negation, and modern far/near `execl` pointer casts failed actual
  compiler/code comparisons and were **restored**, not credited.
- **Previous affected source-native proof: `af736a`.** Two independent original
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
  The original after730 review of `af709a`, `af725d` and `af730a`
  passed with those appropriate contracts. After new Kana/enemy source
  changes, the **current-live-source reviewer correctly rejects** older
  `af709a` / `af736a` receipts due to changed source hashes. This does
  not invalidate their immutable original snapshot proofs; they are
  **historical**, not current checkout validation, and are not repinned.
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
  fixups and 33 PUBLICs. It was not rebuilt again in after721/724/730/748. This is
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

Read [the current after758 twelve-source integration](MAIN_TWELVE_SOURCE_INTEGRATION_AFTER758_REVIEW.md),
[the preceding after753 ten-source integration](MAIN_TEN_SOURCE_INTEGRATION_AFTER753_REVIEW.md),
[the previous after752 nine-source integration](MAIN_NINE_SOURCE_INTEGRATION_AFTER752_REVIEW.md),
[the prior after751 seven-source integration](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER751_REVIEW.md),
[the previous after748 five-source integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER748_REVIEW.md),
[the previous after741 eight-source review](MAIN_EIGHT_SOURCE_INTEGRATION_AFTER741_REVIEW.md),
[the prior after736 seven-source review](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER736_REVIEW.md),
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
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af758a
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af753a
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af752a
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af751a
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af748a
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af741b
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af730a
# Diagnostic success means the input_s full-link failure was detected:
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_input_s_link_gap_after744.py
.venv/bin/python scripts/validate_tracking.py
.venv/bin/python scripts/progress.py --check
git diff --check
```

This list contains **current-source checks that actually pass on this
checkout**. Do not run `af736a`, `af724a`, `af721a`, `af715a` or
`af709a` as current-input validation: their source input hashes intentionally differ from later
maintained files. They remain immutable historical native evidence.

The latest protected read-only proof root is
`.analysis/work/exatt-layout-af758a/report.json`, with twelve current
complete source-native original objects, both genuine full compiler and
TLINK rounds. The previous ten-source root is
`.analysis/work/exatt-layout-af753a/report.json`, with all ten
modified original physical sources, both Combo partitions, Ellen
charged-shot and both independent real compiler/full linker rounds.
The previous after752 proof is
`.analysis/work/exatt-layout-af752a/report.json`, with all nine
current original physical source owners, both Combo partitions and full
independent TC4/TLINK writer evidence. The previous after751 root is
`.analysis/work/exatt-layout-af751a/report.json`, with all seven
modified original physical source owners and both real TC4/TLINK rounds.
The earlier after748 proof `.analysis/work/exatt-layout-af748a/report.json`
retains two actual native
compiler/TLINK rounds for five current modified physical originals. The
previous after741 root is `.analysis/work/exatt-layout-af741b/report.json`,
which still reviews successfully with its eight unaffected sources.
The **historical** after736 root is
`.analysis/work/exatt-layout-af736a/report.json`, preserving its seven
source-snapshot original native object rounds and full TLINK receipts.
Its live-source hash check now **correctly fails** after `enemy.cpp`
changes. Historical `af709a` (Kana), `af715a` (Chiyuri), and `af724a` /
`af721a` (Marisa) must likewise **not** be advertised as current-source
passes. Retain their original snapshots and never weaken the source-bound
reviewer to conceal input drift.
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
Review the [current after758 twelve-source report](MAIN_TWELVE_SOURCE_INTEGRATION_AFTER758_REVIEW.md),
[after753 previous ten-source report](MAIN_TEN_SOURCE_INTEGRATION_AFTER753_REVIEW.md),
[after752 preceding nine-source report](MAIN_NINE_SOURCE_INTEGRATION_AFTER752_REVIEW.md),
[after751 preceding seven-source report](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER751_REVIEW.md),
[after748 prior five-source report](MAIN_FIVE_SOURCE_INTEGRATION_AFTER748_REVIEW.md),
[after741 preceding eight-source report](MAIN_EIGHT_SOURCE_INTEGRATION_AFTER741_REVIEW.md),
[after736 previous seven-source report](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER736_REVIEW.md),
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
