# TH03 handoff

Reconstruction checkpoint: 2026-10-26, after `31fa3bd`. MAINL's complete139-byte
staff hold controller has stateful native loop, fault and conditional-prefix
contracts. Product inputs and prior48 owner observations remain unchanged.
Read `AGENTS.md`, [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md)
and the local [th03-re skill](../.agents/skills/th03-re/SKILL.md) before work.
Detailed findings and witnesses live in source, `config/knowledge.csv`,
`config/evidence.csv` and the current review reports; this is a resume map.

## Verified state

| Product | Accepted source scopes | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 445 functions / 75,317 CODE bytes / 98 extents | Open |
| OP | 31 functions / 3,620 CODE bytes | Open |
| MAINL | 49 extents / 55 procedures / 4,641 CODE bytes | Open |
| ZUN | 77 extents / 89 procedures or entries / 6,179 CODE bytes | Open |

OP includes22 compiler switch/separator bytes with separate proof. ZUN accepts
8,635 CODE+DATA bytes: authored2,179, original ASM1,390, library5,066. No honest
whole-game source/function denominator or completion percentage is known.
Use [generated progress](PROGRESS.md) and the ledgers for current accounting.

OP/MAINL/ZUN current source-only cold pairs repeat every raw output and match
complete decoded **and canonical DIET `-B` stored targets**. This includes
unowned reference/vendor context and does not establish whole-product source
ownership. Publications: `config/{op_work,mainl_work,zun_work}/scoped_acceptance.json`.
MAIN repeats101 raw outputs/99 native objects; its whole file is still unequal.

Last completed reconstruction CI: **2,317 tests, 284 optional archive skips, all
checks passed**;7m07s, about554 MiB peak RSS, no swap. CPU16/nice10 was used.

## Resume

1. Inspect Git, run `.venv/bin/python scripts/preflight.py`, and re-attest the
   selected database before using it: `scripts/ghidra.py th03-mainl check`.
2. Next MAINL units: single229, pair358, verdict389 and roll980, totaling1,956
   CODE bytes. Then remaining cutscene/registration, OP/ZUN ownership and the
   overall four-product source/link graph. Whole-product completion stays open.
3. Preserve complete raw bytes, literal ordered relocations, natural ownership,
   ABI/layout, independent affected-behavior contracts and cold reproducibility.
   End with focused checks, full CI, whitespace checks and an English
   `gpt-6.1-sol: ...` commit; push checkpoints.

Use the [workflow](RE_WORKFLOW.md) for full dependency/rebuild/publication order
and [script index](../scripts/README.md) for entry points. Current full MAINL
chain: `review_th03_mainl_staff_hold_work.py`. `--current-cold` revalidates the
entire existing source/SDK/recipe/output graph and reruns only that stage; it
cannot repair stale prerequisites. After OP/MAINL cold changes, refresh
`review_th03_shared_input_work.py`. Do not rebuild unchanged products gratuitously.

## Current MAINL proofs and hazards

Shared CS/DS: `0C7E/0E3F`; staff CS:`095F`. PiHeader is72 bytes, CDG slot16.
PI buffers/headers: DS:`1F0E/1F26`; CDG slots:`1D0E`.
Each command below is `review_th03_mainl_<suffix>_work.py --current-cold`.

| Scope | CODE bytes | Suffix / essential boundary |
| --- | ---: | --- |
| PI release | 76 | `pi_free`; real HMEM_FREE remains a bounded unowned reply |
| Five PI callers | 555 | `pi`; actual release/memcpy, wrapped row WORD before normalization |
| Five CDG loaders | 593 | `cdg`; unchecked BYTE counts through255, live metadata aliases |
| Three CDG blitters | 493 | `cdg_draw`; actual SMC/color setup, three outer EVEN bytes unowned |
| Ending entry | 280 | `ending`; live resident/script state, returning execl failures |
| Flake/unput | 199 | `staff_draw`; real caller coordinate writes, inherited DF |
| Seven snow procedures | 464 | `snow`; one extent/seven procedures, real RNG/vector/flake |
| Enter/leave/gallery | 446 | `staff_callers`;443 executed bytes plus3 proved unreachable |
| Hold controller | 139 | `staff_hold`; actual two-stage loops and two waiting CFG proofs |

The natural `STAFFP_TEXT` TC4 producer is `src/mainl/staff/data.cpp`, copied
literally to `staffdat.cpp`, GAME3/L:19 procedures/3,695 CODE bytes,224 initialized
DATA, no BSS. Fifteen procedures/1,739 CODE bytes are owned; the other four and
all224 DATA bytes remain unaccepted. Complete current938-output cold pairs bind
nine consumed SDK headers with per-producer fail-closed dependency checks and
normal893-member TLIB order. First-use GAME3/O shared producers remain unchanged.

The listed resource/staff contracts check DWORD/segment state, defined flags/IF/DF,
ordered stores/ports and full flat memory without ignored stack windows. Both native
far return words are checked at callee entry because UC can omit write hooks.
Owned returns are checked before parent restoration can mask ABI corruption.
External data, DOS/library/device replies, assets, planar pixels/latches and
physical IRQ/audio/timing remain explicit unowned boundaries.

- PI interlace heightFFFF has a conditional closed CFG/even-WORD invariant;
  checked prefixes are separate from returning calls. CDG LOOP width0 actually
  executes65,536 iterations; REP0 writes nothing. Native finite recurrences and
  disjoint mapped-memory/stable-SMC assumptions are bound in the verifiers.
- Flake cel is not capped to4; WORD shifts fold it to4,096 source offsets.
  Unput centers signed halves toward zero but clears unsigned width>>4 WORDs
  over three REP rows. DF0 row delta80;DF1 delta80-4*count moduloWORD. A WORD at
  FFFF spans physical bytes. Sprite/table storage receives no ownership credit.
- Snow capacity is an unchecked BYTE through255. Particle80 aliases FRAME27C2,
  PAGE27C4/SLOW27C5 and ADAPT27C6. Preserve live reads across spawn/update/render/
  adaptation. Actual vector DWORD effects and the unsanitized angle WORD's high
  byte are checked; its69 library bytes/tables remain unowned. The immutable-zero
  counter wait at270E has a conditional CMP/JE invariant, never a timeout proof.
- Dissolve masks strength in the real caller WORD. Signed IDIV16 quotient0
  executes65,536 WORD ANDs; unsigned postincrement rows can also reach65,536.
  Both maxima execute separately. The combined2**32 bound is mathematical,
  explicitly not a claimed executed maximal fixture.
- Enter INT0 at2885 retains15 zero-divisor durations(-7..7), or frame8000 and
  eight durations(-15..-8) yielding divisor-1, subject to signed frame<=duration.
  Pre-handler registers/stack/memory and IF/DF pass; no arithmetic-flag/return/
  handler credit follows. A fresh UC clears hidden stopped-exception state,
  retaining exact memory when persistent reentry is requested.
- Leave MOV SI,7 at2925..2928 is proved unreachable under readonly frame and
  disjoint memory: signed frame<160 implies trunc(frame/20)<=7 over all WORDs.
  All three raw bytes still require native equality; execution/control totals
  exclude them. Bytebox is an explicit unowned ABI reply.
- Hold executes normal no-music257+257 iterations,514 ticks and8,224,000 real
  clear WORD callbacks. Counter0 and music-measure-below-request prefixes are
  separate. The latter proof fixes cap0,duration640,speed3,canonical pages,
  centers[180,280],valid immutable slot metadata,returning counter replies and
  PMD0/no DATA writes. Its full frame-WORD domain is safe for IDIV80; gate stays
  false under those assumptions. No guest step is skipped or budget expiry used.
  All139 owner bytes and1,503 context bytes execute;69 vector bytes stay unowned.

## Other open work

- OP's five main/option menu procedures own1,338 CODE bytes including22 inline
  bytes. Entry's14 procedures cover2,831 bytes; root `_main`263, DATA487/BSS6,
  Music Room and resources remain. Preserve ordinary `samecodeseg` far-call
  relaxation; do not restore handwritten call assembly. Eight legacy scope
  observations stay equal to immutable `d118c46`; fresh phase-log hashes need
  not match. `lib/op_nested_context.py` shares actual UC/native/static state.
- MAINL sound mode/PMD/volume/reset still have explicit trailing NOPs. Unpadded
  bodies exist but natural enclosing layout is open. Generated WORD/BYTE
  alignment controls are diagnostics. Five root helpers own150 bytes; three
  adjacent NOPs remain unowned.
- ZUN's five payloads have native producers. ONGCHK owns892 CODE+34 DATA bytes;
  42 BSS bytes are not file-backed. Driver-4's55 procedures/header/tables/natural
  CODE layout pass, but3+9 reserved DATA bytes and vendor/runtime context remain
  open. Do not add an empty segment to force trailing storage. All native loops
  execute; the optimized audit reproduces original complete traces.
- MAIN's124,642-byte image differs only at EC2D and1DB05: target90/candidate00.
  Headers:6,240/7,680 bytes. Of1,553 ordered relocations, first1,072 match and242
  positions differ. Next mismatch: record1072/DC42, state/MAIN_010_TEXT. Shot's
  twelve far calls split7/5 around state records; a combined TU reaches only
  record1073. EC2D follows input_sense RETF before snd_se_reset;1DB05 is DGROUP:
  05A5 between vsync_OldMask and BYTE_MASK. Ordinary TASM/MASM51/QUIRKS emit zero;
  OP's Music Room fix does not explain these bytes. Do not manufacture padding.
- Keep combo P_COMBO_TEXT/MAIN_04 identity, far-Pascal ABI and samecodeseg
  relaxation. Loss renderer near-member ABI and128-byte player layout are
  proved; original class/file organization remains an inference.

## Local state and checks

Retain fixed Japanese private targets/assets (`candidate-local-attested`),
`.analysis/toolchain/wineprefix`, TC4/TASM/JWasm, `.tools/ghidra`, `.tools/jdk`,
`.venv`, `_reference/ReC98` and `ghidra-project/`. Ghidra/JDK attest their entire
installed trees, including documentation/archives; do not trim them.
One working build/product: `drive_c/{TH03WORK,TH03OP,TH03ML,TH03ZUN}`.
Current reports: `.analysis/work/*-build.json` and `main-unit-review.json`.

Required actual source input, despite its old directory name:
`.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar`.
Keep `scripts/lib/zun.py` unchanged: MAIN's promoted serial schedule pins it.
OP's builder is a shared MAINL/ZUN utility; real edits require fresh bound pairs.

```sh
taskset -c 16 nice -n 10 env DISPLAY= WAYLAND_DISPLAY= \
  _JAVA_OPTIONS='-Xmx768m -XX:ActiveProcessorCount=1' \
  .venv/bin/python scripts/ci.py
git diff --check
```

Choose one allowed CPU on another host. Serialize Borland/Wine writers and
preserve the prefix. System Python's Unicorn is unsuitable; use `.venv`.
Old logs/experiments/caches/receipts are disposable; references alone do not
require retention. Preserve actual current inputs/builds/proofs. Cleanup previews
by default; after CI, `clean_generated.py --caches-only --apply` leaves `.analysis`
alone. See the workflow for guarded cleanup and publication commands.
