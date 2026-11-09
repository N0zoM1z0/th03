# TH03 — active handoff (2026-11-09)

Follow [AGENTS.md](../AGENTS.md). This page records current work and evidence;
[generated progress](PROGRESS.md) provides the ledger/publication counters.
The complete pre-consolidation text is preserved in the
[after1096 archive](RE_HANDOFF_ARCHIVE_AFTER1096.md); older chronology remains
in the [after1053](RE_HANDOFF_ARCHIVE_AFTER1053.md) and
[after927](RE_HANDOFF_ARCHIVE_AFTER927.md) archives.

## Current status

The latest preflight passes target identity, tracking and current decoded
publications. OP, MAINL and ZUN retain their accepted decoded scopes; MAIN's
ledger and separate function inventory remain unchanged. Recent work improves
natural C++ while preserving original native output, so ledger totals need
not increase. The whole-game completion percentage remains unknown.

`status.py` and generated progress select the sixty-five current disjoint MAIN
source reports below. The old `af1053k` and `af1092k` composites and shared
BOSS `af1056c` are historical after source changes, not current all-owner proofs.

## Current MAIN native evidence

These sixty-five disjoint stage reports have passed read-only source/native review.
Each retains two original TC4 compiler rounds, complete physical CODE/DATA,
literal ordered native fields, PUBLICs and segment geometry, plus normal MAIN
links matching the Japanese loaded image and all ordered MZ relocations.

| Stage | Current physical owners |
| --- | --- |
| `af1172f` | Shared BOSS providers `ba_sring`, `ba_srest` |
| `af1173c` | PI image loader `pi_load` |
| `af1181b` | DOS executable handoff `execl` |
| `af1182a` | Resident CFG loader `cfg_lres` |
| `af1184d` | PC-98 exit/shutdown `exit` |
| `af1174e` | Input modes and key-wait `inp_m_w` |
| `af1176e` | PMD/MIDI and SE services `snd_kaja`, `snd_se` |
| `af1178a` | Polar Q8 geometry `polar` |
| `af1179a` | VSYNC frame delay `frmdely1` |
| `af1180b` | DOS MAIN initializer `initmain` |
| `af1129e` | Ellen Extra Attack `ex_ellen` |
| `af1127g` | Yumemi Extra Attack `ex_yume` |
| `af1128c` | Mima Extra Attack `ex_mima` |
| `af1112h` | Reimu Extra Attack flight/prefix and update `ex_rfly`, `ex_reup` |
| `af1113c` | Marisa Extra Attack `ex_maris` |
| `af1121d` | Kotohime Extra Attack `ex_koto` |
| `af1122c` | Chiyuri Extra Attack `ex_chyu` |
| `af1124d` | Rikako Extra Attack `ex_rika` |
| `af1125e` | Kana Extra Attack `ex_kana` |
| `af1188c` | Rikako BOSS `ba_rikak` |
| `af1189d` | Kana BOSS `ba_kana` |
| `af1190d` | Chiyuri BOSS `ba_chiyu` |
| `af1158e` | Kotohime BOSS `ba_koto` |
| `af1175f` | Reimu BOSS `ba_reimu` |
| `af1168b` | Mima BOSS `ba_mima` |
| `af1183f` | Marisa BOSS `ba_maris` |
| `af1187e` | Ellen BOSS `ba_ellen` |
| `af1185e` | Yumemi BOSS `ba_yumem` |
| `af1107c` | Bullet engine `bullet` |
| `af1177g` | Fireball engine `e_fireb` |
| `af1192d` | Enemy formation/VM/update engine `eforna`, `efornb`, `eupda`, `eupdb` |
| `af1120c` | Explosion collision `e_expl` |
| `af1194c` | Hitbox `hitbox` and HitCircle `hitcirc` |
| `af1115b` | Both background chain controllers `chain1`, `chain2` |
| `af1171d` | Large MAIN entry/round controller `entry` |
| `af1164e` | Round result/reset `results` |
| `af1166i` | Round intro HUD `intro` |
| `af1165h` | Static HUD `hud_stat` |
| `af1191e` | Complete player core `core` |
| `af1163i` | Player loss/defeat `lose` |
| `af1169a` | Gauge and shared Extra Attack `p_gauge`, `p_exatt` |
| `af1134f` | Marisa Chargeshot/Gauge `cs_mari` |
| `af1135h` | Chiyuri Chargeshot/Gauge `cs_chiyu` |
| `af1136f` | Reimu Chargeshot/Gauge `cs_reimu` |
| `af1138f` | Ellen Chargeshot/Gauge `cs_ellen` |
| `af1140e` | Rikako Chargeshot/Gauge `cs_rika` |
| `af1141f` | Kana Chargeshot/Gauge `cs_kana` |
| `af1142d` | Mima Chargeshot/Gauge `cs_mima` |
| `af1143h` | Yumemi Chargeshot/Gauge `cs_yume` |
| `af1146d` | Kotohime Chargeshot/Gauge `cs_koto` |
| `af1147c` | Ellen Bomb `b_ellen` |
| `af1148f` | Rikako Bomb `b_rika` |
| `af1149e` | Mima Bomb `bm_mima` |
| `af1152f` | Yumemi Bomb `bomb~cxk` |
| `af1153d` | Reimu Bomb and shared lifecycle `bm_reish` |
| `af1154d` | Kotohime Bomb `b_koto` |
| `af1155b` | Kana Bomb `b_kana` |
| `af1156b` | Chiyuri Bomb `b_chiyu` |
| `af1159d` | Marisa Bomb `bm_mari` |
| `af1131a` | Combo HUD and chain `p_combo`, `p_cmbhl` |
| `af1132b` | Shotpair creation/update/render `shots` |
| `af1133a` | Player effects `effects` |
| `af1160e` | Warning/Gauge HUD `warning` |
| `af1161f` | Nine-character callback/resource setup `ch_setup` |
| `af1170d` | Four-function CPU controller `p_cpu` |

Reports live at `.analysis/work/exatt-layout-STAGE/report.json`. These are
separate scoped links, not a new combined build of all listed owners.
The older `af1092k` retains historical native evidence, but its full
live-source binding is stale after newer BOSS, engine, collision and Extra
Attack changes. Its formerly selected owners now have disjoint current native
proofs above. These are still separate scoped links, not a new combined
source-native replay. Do not overwrite the old report or invent one.
Local native proof is separate from Factory acceptance.

## Latest natural-source recovery

- **Rikako/Kana/Chiyuri BOSS:** exact new full-owner stages `af1188c`,
  `af1189d` and `af1190d` retain original RNG and signed projectile cadence
  after restoring natural attack terminal and release-frame exits.
- **Player and Enemy state:** `af1191e` rechecks the complete player-core
  movement retry/glow conditions; `af1192d` rechecks four Enemy owners with
  natural explosion and per-frame update continues. `af1194c` covers Hitbox
  guards and HitCircle update/render live-slot skips.
- **Input scan remains excluded:** the fresh current-source `af1193a` TC4
  overlay reproduced the original 417-byte object and literal fixups, but
  its normal MAIN link differed at exactly file offset 68141 (`90` vs `00`).
  File-scope `asm { even }` failed actual TC4 compilation at `af1193b`.
  The working source was restored; no trailing filler was introduced.

- **Three complete BOSS controllers:** Marisa `af1183f` has exact terminal
  returns for ring, wide and narrow columns; Yumemi `af1185e` recovers five
  attack families; Ellen `af1187e` covers spread, radial Extra and pellets.
  The entire original CODE and linked image match in each scoped round.
- **DOS and PC-98 services:** `execl` (`af1181b`) retains the far-null
  argument and exact archive cleanup, `cfg_lres` (`af1182a`) keeps its real
  uninitialized CFG scratch, and `exit` (`af1184d`) now uses native Borland
  `outportb()` for every original port write, including the repeated one.
- **Remaining excluded original owner:** BIOS input scan `input_s` retains
  exact 417-byte original OBJ evidence, but the normal-link parent expects an
  extra one-byte post-RET alignment slot. Do not treat it as current full-link
  source proof; see `MAIN_INPUT_S_LINK_GAP_AFTER744_REVIEW.md`.

- **Reimu BOSS and Fireballs:** native receipts `af1175f` and `af1177g`
  cover the complete 2,020-byte BOSS and 1,555-byte engine. Both spread
  stages and the orbit renderer have natural early exits; the Fireball
  explosion keyframes and two complete 24-slot walks have native-exact
  first-use index lifetimes. Its original uninitialized chain slot remains.
- **Main services and bootstrap:** native stages `af1174e` (input modes),
  `af1176e` (audio), `af1178a` (signed Q8 polar), `af1179a` (VSYNC delay)
  and `af1180b` (DOS init) verify previously unselected original owners.
  Exact ABI/control effects, including register interrupts and the original
  allocation error exit, are retained.

- **Shared BOSS and PI loader:** `af1172f` verifies the two shared BOSS
  owners after naturalizing launch and RNG-wait early returns; `af1173c`
  adds the previously unselected far-Pascal PI loader. A direct return from
  `graph_pi_load_pack` changed native CODE, so the named result remains.

- **Enemy and Mima BOSS:** the four-owner Enemy clip/speed recovery is
  source-bound at `af1167c`; Mima's two full attack state machines now use
  native-exact early returns (`af1168b`).
- **Round/HUD and player control:** current original-compiler receipts
  `af1171d` (stage/round initialization), `af1170d` (CPU dodge),
  `af1163i` (loss/defeat), `af1164e` (results/reset), `af1165h` (static HUD),
  `af1166i` (intro), and `af1169a` (Gauge/shared Extra Attack) now replace
  their superseded proofs or document their previously unselected owners.

- **Rikako/Kotohime BOSS:** current full-owner stages `af1157c` and
  `af1158e` validate natural spin guards, intro/attack termination and the
  radial-burst early return. The original signed angular loops remain intact.
- **Bomb and HUD:** Kana, Chiyuri and Marisa Bomb owners now use current
  source proofs `af1155b`, `af1156b` and `af1159d`. The complete Warning/Gauge
  controller `af1160e` restores natural pause polls and flash cadence.
- **All-character setup:** `af1161f` reproduces the full 3,888-byte callback
  owner, including the nine character bindings and natural filename/digit
  creation. No callback ABI, order or external storage was changed.

- **Bomb particle controllers:** `af1148f` (Rikako), `af1149e` (Mima),
  `af1152f` (Yumemi), `af1153d` (Reimu/shared), and `af1154d`
  (Kotohime) prove their current source against original TC4/TLINK.
  Rikako and Kotohime use natural explosion-row loops; Reimu restores
  two full 32-slot pointer traversals; Yumemi names the two triangle
  geometries. The historically unused Kotohime row index is retained.
- **Large BOSS states:** Kana `af1150c` now uses a natural nested warning
  renderer and introductory exit, while Chiyuri `af1151d` uses inactive
  early returns in its four-direction volley and 32-ring attack. All
  three intro outcomes stay source-visible without changing native CODE.

- **Current source refinements:** Kana, Mima, Yumemi and Kotohime Chargeshot
  owners are reverified at `af1141f`, `af1142d`, `af1143h`, `af1146d`.
  Mima's complete update/render now use early guards; Kotohime's BX-based
  hit-test retains native register semantics under a natural early return.
  The complete Ellen Bomb particle respawn/render controller uses natural
  shared for-header advancement at `af1147c`. Marisa and Ellen BOSS full
  owners have current attack/intro proofs `af1144c` and `af1145c`.

- **Chargeshot/Gauge control:** the five complete physical owners `cs_mari`
  (`af1134f`), `cs_chiyu` (`af1135h`), `cs_reimu` (`af1136f`), `cs_ellen`
  (`af1138f`) and `cs_rika` (`af1140e`) have new original two-round
  TC4/TLINK evidence. Their history shifts, full deceleration/homing state,
  five-way collision skips, monochrome beam renders and Gauge volleys now
  have native-exact natural C++ loops. Chiyuri reset still deliberately
  clears the first slot repeatedly, and compiler-sensitive loop locals stay
  in their proven scopes.
- **Reimu/Mima BOSS:** latest full-owner proofs `af1139c` and `af1137b`
  naturalize original word-sized attack clocks, intro and opponent-state
  predicates. Compiler-negative alternate branch structures were restored.

- **Yumemi BOSS and Extra Attack:** `af1130c` refines the full attack-phase
  and render guards in the BOSS owner, and `af1127g` rechecks the entire
  16-entity Extra Attack update and its four beam sprite perimeters.
- **Mima and Ellen Extra Attacks:** `af1128c` and `af1129e` naturalize the
  six-slot Mima and twelve-slot Ellen pointer/allocator progressions. The
  original wider update scratch lifetimes remain after negative TC4 tests.
- **Combo, shotpairs and effects:** `af1131a`, `af1132b`, `af1133a` verify
  full physical owners with natural index/pointer progressions, including
  Combo's early-continue path, shotpair allocation/render and effect expiry.

- **Kotohime, Chiyuri, Rikako and Kana Extra Attacks:** real first-free
  allocation, full physical entity update and rendering passes now use natural
  `for` headers. Native receipts `af1121d`, `af1122c`, `af1124d`, `af1125e`
  each passed two original TC4/full MAIN links. Chiyuri's paired-beam path
  and Kotohime's 10-slot event state are preserved, including their original
  separate pointer hops and byte state mutations.
- **Kotohime BOSS and MAIN scheduler:** `af1123e` independently reverified
  the complete BOSS after naturalizing intro/renderer controls, and `af1126c`
  verified the complete MAIN entry/round scheduler with natural unsigned-word
  cadence and VSync predicates. The byte masks and special register/I/O
  contracts remain unchanged.

- **Background chains:** full Chain 1 / Chain 2 reset and particle
  initializers use natural `for` loops, preserving all RNG and drawing
  order. `af1115b` is the current dual-owner source proof (1,245 CODE bytes);
  the low-level DS:DI renderer and uninitialized phase byte remain unchanged.
- **Player core:** the complete 3,135-byte `core` physical owner at `af1116g`
  contains natural `while(1)` human movement retry, CPU shot remainder and
  named charge/Hyper thresholds. The narrowed `first_attempt` Boolean is
  native-exact, but narrowing `movement` is not.
- **Kana, Rikako and Chiyuri BOSS:** current full-owner proofs are `af1117f`
  (1,874 bytes, natural staged/rotating branches), `af1118e` (1,677 bytes,
  three signed-spin clock tests and separate emission indices) and `af1119b`
  (2,654 bytes, trail/render word clocks and normal/mono dispatch).
  Their original byte-angle and register-sensitive branches were tested
  independently and retained where natural alternatives changed CODE.
- **Explosion collision:** original `e_expl` is source-bound at `af1120c`
  (630 CODE bytes). Its near-pointer collision scan uses natural prefix
  progression, and the non-pellet charge multiplier is now named. A ternary
  selector and narrower collision hit-count local both changed TC4 CODE.

- **Marisa and Ellen BOSS:** full attack/update/render owners were refined
  with original word-frame modulo and natural early-return column/Extra Attack
  phase dispatch. The current original TC4 matches are `af1110d` (Marisa,
  1,431 CODE bytes) and `af1111e` (Ellen, 1,675 CODE bytes). Attempts to
  change Marisa's compound sprite steps and Ellen's byte render-frame compound
  update were rejected by direct compiler comparisons.
- **Reimu and Marisa Extra Attack:** Reimu's two physical owners share the
  current `af1112h` source proof (1,156 CODE bytes). Creation loops, collision
  stripes and renderer-local values are naturalized while the original flight
  transition label stays. Marisa's `af1113c` (676 CODE bytes) proves all four
  fourteen-slot entity traversals using for-header advancement, including
  three substantial update `continue` paths. Both retain exact native links.
- **Complete Enemy engine:** all four physical producers are bound together
  at `af1114e` (3,325 CODE bytes). Enemy update/render, reverse hit-testing,
  formation parsing, emission and RNG walks use natural for-loops. The native
  ENEDAT VM pointer lifetime and original uninitialized RNG history stay
  unchanged after a real-compiler negative test.

- **Shared BOSS:** the ring's primary/secondary sprite loops use natural
  prefix index and compound angle progression; active RNG and angle scratch
  initialize at first use. Two physical owners are source-bound together at
  `af1109c` (949 CODE bytes). Register-based template copying is preserved.
- **Bullet and Fireball engines:** full Bullet (`af1107c`, 2,685 CODE bytes)
  and Fireball (`af1108e`, 1,555 CODE bytes) original objects have naturalized
  traversal progression, flag reset and explosion coordinates. Fireball also
  names the unchanged chain/transfer thresholds. The low-level pellet
  `do/while` and the original uninitialized Fireball chain slot remain.
- **Reimu, Mima and Yumemi BOSS:** Reimu's three orbit phase traversals and
  byte-angle lifetimes (`af1104e`, 2,020 CODE bytes), Mima's typed template,
  early render guard and word frame (`af1105d`, 1,922 CODE bytes), and Yumemi's
  active render guard, shot period and size-derived RNG group indexing
  (`af1106d`, 2,358 CODE bytes) are independently source-native verified.
  Focused native reviews document positive and rejected real-compiler variants.

- **CPU:** the complete four-function dodge/aim/retry controller uses a
  bounded `for` over its original signed-byte collision radii, retaining
  the early-break behavior. Target steering's byte flag initializes at
  first use after `ellen_target_set`. Final `af1103d` matches all 1,077
  CPU CODE bytes, 64 original ordered native fields and full Japanese
  MAIN in two rounds. A structured if/else retry-column rewrite
  (`af1103a`), a ternary bottom-escape rewrite (`af1103b`) and a narrower
  unused-but-observable RNG remainder local (`af1103e`) changed CODE;
  those variants were not kept.

- **MAIN entry/round reset:** eight fixed-length digit, player, callback,
  EFE, Extra Attack, shotpair and random charge-threshold traversals now
  use natural `for` loops. The original 3,050-byte physical controller
  (`main`, frame scheduler, stage setup and round reset) is verified by
  independent full MAIN link rounds at `af1102a` and final `af1102b`;
  all 433 ordered native fields and Japanese MZ relocations match. Source
  keeps every original `IRand()` draw and duplicated hit-flag store.

- **Collision:** `hitbox_hittest` now expresses both shot-pair half-extents
  explicitly, with a natural negative-Y guard and two-frame bomb remainder.
  HitCircle producers use native C++ array indexing for their ring slots.
  Fresh `af1101g` verifies both physical owners together (711 original CODE
  bytes, 63 ordered native fields, full MAIN image and relocations) twice.
  Moving the hitbox center temporaries inside the scan (`af1101e`) changed
  original CODE; their original stack-local lifetimes remain.
- **Chiyuri:** four horizontal/vertical fan passes now use natural
  `for` headers, with the original bullet speed update preceding the signed
  index advance. Fresh `af1101a` independently compiled the complete 11-function
  BOSS owner twice and matched all 2,654 CODE bytes, 381 ordered native fields,
  complete Japanese MAIN image and ordered relocations.

- **Kotohime:** the angle in the projectile-ring emitter and renderer
  initializes at first use, and sprite hit-offset/half-width are named.
  Fresh `af1101d` compiled the entire eleven-function BOSS twice and matched
  all 1,840 CODE bytes, 262 ordered native fields and complete normal MAIN.
  A trial that also moved the projectile x/y declarations (`af1101b`)
  changed CODE; those lifetimes were restored.
- **Rikako:** all five BOSS attack/render iteration sites use natural `for`
  loops; the update PID and renderer angles initialize at first use. Preserve
  the shared entity index, signed/unsigned arithmetic and RNG/emission order.
  Narrower coordinate and sprite-offset lifetimes that changed CODE remain
  rejected. See the [complete Rikako review](MAIN_RIKAKO_BOSS_NATURAL_FOR_AND_LIFETIMES_AFTER1095_REVIEW.md).
- **Kana:** the sixteen-sprite intro uses a natural `for` with its original
  shared register index. Radius, angle and X scratch initialize at first use;
  the update PID follows the inactive-player return. The zero-minus angle
  expression, wider Y/sprite-offset lifetimes and draw order remain necessary.
  See the [complete Kana review](MAIN_KANA_BOSS_NATURAL_FOR_AND_LIFETIMES_AFTER1096_REVIEW.md).
- **Ellen Extra Attack:** its separate six-function owner has natural loops
  for history shifting, initialization and spiral/render iteration, with
  first-use PID and branch/loop-local scratch. See the
  [Ellen Extra Attack review](MAIN_ELLEN_EXATT_NATIVE_HISTORY_AFTER873_REVIEW.md).
- Earlier Bullet/Fireball, Reimu, Mima/Marisa, Ellen and Yumemi natural-source
  changes remain documented in the focused historical reviews. Do not treat
  superseded composite source hashes as current native proof.

## MAINL build and publication

The `af1055m` Staff/root refresh restores the current decoded publication.
Both complete decoded EXE/MAP rounds and ordered relocations match their
reference targets; the unchanged cold pair and selected providers are retained.
See the [current MAINL build review](MAINL_CURRENT_SOURCE_REFRESH_AFTER1055_REVIEW.md).

For a later Staff/root change, choose an unused `afNNNm` stage:

    .venv/bin/python scripts/build_th03_mainl_current.py --stage afNNNm --build
    .venv/bin/python scripts/publish_th03_mainl_work_scopes.py --stage afNNNm
    .venv/bin/python scripts/progress.py

Omit `--build` for read-only review. Other dependency changes require their
actual affected scope. Do not run the original cold builder in place over the
protected ancestor.

## Next useful work and open limits

1. Continue unselected original gameplay engine/character owners, and
   challenge BOSS and round-controller state machines with new original
   compiler hypotheses. The background chains and explosion collision now
   have updated current local native evidence.
   Inspect current source and focused evidence before choosing a function;
   recently naturalized leaves are not an unowned work queue.
2. Select genuinely unowned regions from `config/units.csv`,
   `config/evidence.csv` and focused reviews when expanding ownership.
   MAINL, OP and ZUN still have open scopes; source presence alone is not
   accepted ownership. Original ASM and library contributions remain separate
   from authored-source credit.
3. The standalone MAIN BIOS `input_s` source has a historical one-byte
   trailing-NOP link gap despite its exact 417-byte CODE owner. Preserve that
   finding; do not manufacture a NOP or call it full-link acceptance.
4. Whole-product ownership, canonical packed-unit acceptance and historical
   vendor OBJ/header-writer identity remain separate open questions.

Factory's read-only registry lists `th03`, but the accepted snapshot still
contains no OracleResults for imported claims. The earlier replay-worker
registration rejection is recorded in the archive; worker readiness was not
retested by submitting a replay here. Continue local native reconstruction and
keep Factory receipt acceptance separate.

## Minimal checks and retention

    git status -sb
    .venv/bin/python scripts/preflight.py
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1172f af1173c af1181b af1182a af1184d af1174e af1176e af1178a af1179a af1180b af1129e af1127g af1128c af1112h af1113c af1121d af1122c af1124d af1125e af1188c af1189d af1190d af1158e af1175f af1168b af1183f af1187e af1185e af1107c af1177g af1192d af1120c af1194c af1115b af1171d af1164e af1166i af1165h af1191e af1163i af1169a af1134f af1135h af1136f af1138f af1140e af1141f af1142d af1143h af1146d af1147c af1148f af1149e af1152f af1153d af1154d af1155b af1156b af1159d af1131a af1132b af1133a af1160e af1161f af1170d

For source changes use a fresh DOS-safe stage, compile only the affected
original physical TUs with `probe_th03_main_exatt_layout.py`, compare both
complete native rounds and normal links, then retain useful findings and
commit as `gpt-web: xxx`. No full cold replay is needed for ordinary scoped
changes. See [workflow](RE_WORKFLOW.md) and [script entry points](../scripts/README.md).

Preserve dirty/untracked work, targets, the game-specific Wine/analyzer state
and the entire active source-bound receipt DAG, including both raw rounds and
writer logs. The [current storage policy](STORAGE_HANDOFF_CURRENT.md) and
[after1024 audit](STORAGE_HANDOFF_AFTER1024.md) remain authoritative. Generic
receipt pruning and analysis deletion remain retired; cache-only cleanup is
the routine route. Finish affected checks and `git diff --check`.
