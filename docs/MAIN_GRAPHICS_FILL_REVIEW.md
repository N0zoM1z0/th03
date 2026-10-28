# MAIN register-only graphics helpers

The initial source/ABI recovery added no ownership. The narrower current review
below selects four existing complete entries; it does not claim a new implementation.

The pinned Japanese MAIN SHA-256 is
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`.
Raw disassembly establishes load[B37C,B454),216 bytes,zero MZ relocations:
B37C near,B398 near,B39E far,B3A2 near,B3F6 near. The preceding complete
character setup ends at B37C; GameExecl begins at B454. B398 shares B37F;
B39E only calls the near entry and returns far. No stack arguments.

B3DD/B427 execute. B397/B39D/B3F5/B453 follow returns/unconditional jumps
and are even-alignment candidates, not proved original alignment directives.
All six NOPs remain unchanged. Keeping ASM does not prove original ASM origin.

## Caller-backed ABI

All entries require DF=0. Callers own GRCG mode/color and EGC enable/disable.
Source comments record preserved/clobbered registers and physical VRAM geometry.

* Raw09A49/09A5A pass BX=3932h/395Ah after GRCG RMW setup:288 pixels,
  184 physical rows8..191,x16/x336. Logical playfield height is368 because
  display Y is doubled. The highlight entry instead receives232h/25Ah,
  drawing physical rows192..199 at the same X positions.
* C839 calls B3A2 between EGC-on/off. The source strip is physical
  (320,392)..(607,399), duplicated into both highlight strips. MOVSW loads
  the EGC latch, not AX; the following AX store uses that hardware latch.
* C91E passes DX=charged+32,BX=available; other gauge calls use x352 or the
  corresponding charged offset. B3F6 draws physical rows194..197. It rounds
  X down to16 pixels and adds X modulo16 to width, deliberately without a
  left-edge mask, clipping or a zero-width guard. WORD wrapping and signed
  DI termination remain intact, not sanitized for invalid inputs.

## DATA and origin

The only DATA read is the16-WORD table at DS:064C/load1DBAC..1DBCC.
`_hud_gauge_left_masks` stays in the same root-derived DATA contribution.
Its bounded include constructs width-based leftmost masks, swaps pixel-order
bytes for little-endian WORD VRAM writes, and preserves index0=FFFFh.
The filename and three preceding zero bytes are untouched. Staging uniquely
anchors and hashes the old source declarations; no target bytes generate source.

Unused fp_1FBC0/byte_1FBC2/byte_1FBC3/word_1FBC4..1FBD2 externs describe
transition state, not these helpers. Removing their declarations changes no
storage. Unused PI/exit/triangle externs were removed as well.

ReC98 blame traces the body to d569ad64f2f798c50de52b01513973d52ad44d0e,
`th03/main: Initial state`(2014): disassembly, not surviving original source.
The original masters.lib SHA-256
`6be41dbcfcf4504977165ccc44443525a29a01f85a1580e6ad0c620bf802faf6` has640
validated OMF modules. No LEDATA contains the complete B37C/B3A2/B3F6 body,
the mask table, or the checked fill/copy loop fragments. WORDMASK.ASM has
only8 DATA bytes(BYTE_MASK); GC_FILL.ASM has102 CODE bytes with clip-state
externs; EGC.ASM has96 CODE bytes supplying enable/disable APIs. This excludes
literal unchanged vendor identity, not all derivations or proof of authorship.

Existing native/cold checks verify bytes/layout. The only added static check
binds the exact new DATA public/address and semantic mask values. No new
runtime harness, ownership count or whole-game percentage is introduced.

## Source checkpoint verification (2026-10-26)

The focused existing `build_th03_main_work.py --build --rebuild-context`
completed99 native phases. Full124642-byte load and entire executable repeat
the preceding build, including all1553 literal ordered relocations. Existing
98 owned extents/75317 bytes remain unchanged. The target difference is still
EC2D plus the pre-existing MZ header difference; this edit closes neither.

MAP adds only `_hud_gauge_left_masks` at1D56:064C (1359 to1360 public names).
All old names/addresses stay fixed. Removing dead EXTRNs changes exactly these
11 existing public idle flags from false to true:fp_1FBC0,byte_1FBC2,
byte_1FBC3,word_1FBC4,word_1FBC6,word_1FBC8,word_1FBCA,word_1FBCC,
word_1FBCE,word_1FBD0,word_1FBD2. No generic MAP relaxation was added.
Independent read-only source/raw-target review found no blocker. Temporary
artifacts from this intermediate checkpoint were removed during handoff cleanup.
Current acceptance and retained native reports establish the verification status;
this historical source note adds no new acceptance or pending CI requirement.


## Narrow complete-entry ownership review (2026-10-26)

The scope is **207 instruction bytes /96 instructions /four complete entries**,
not the216-byte provider and not all212 instructions in it. Three owners retain
unchanged generic RET/RETF boundary checks:

| Load span | CODE offset (096E) | Object offset | Target file offset | Bytes | Entry |
| --- | --- | --- | --- | --- | --- |
| B37C..B397 | 1C9C | 00 | CBDC | 27 | near playfield clear |
| B39E..B3A2 | 1CBE | 22 | CBFE | 4 | far bomb adapter |
| B3A2..B3F5 | 1CC2 | 26 | CC02 | 83 | near dual-strip restore |
| B3F6..B453 | 1D16 | 7A | CC56 | 93 | near gauge bar fill |

The adjacent adapter/restore entries form one87-byte owner. The full physical
partition is owned27/context7/owned87/context1/owned93/context1. Context7 is
B397..B39E, including B398's five-byte prefix. B3F5 and B453 remain context too.
These **nine bytes are unowned context**, not established padding, unreachable
storage or extra credit. B3DD/B427 remain executed code instructions.

The unowned B398 entry loads its own segment and branches at B39B to B37F,
inside the owned first body. That dependency is explicitly checked in both
images; the shared implementation is counted once. B398 receives no standalone
function or five-byte ownership claim. No claim excludes all indirect entries
into retained context. The adapter's B39E near CALL reaches B37C and returns far.

Actual target/candidate incoming transfers are checked at9A49/9A5A toB37C,
C87A/C8BA toB398,C839 toB3A2,C91E/C953/C9A3/C9F3 toB3F6, and
1840A/187AF/18C04/18E11/148FF/1522B/17202/B5D3/B5DB toB39E.
These are known real caller edges, not a fabricated exhaustive call graph.
The caller-backed register conditions and physical geometry above still apply.

### Native and origin boundaries

The actual maintained ASM is staged as `th03/gf_ctx.asm`. Native TASM5 produces
one216-byte LEDATA in HITCIRC_TEXT (OMF segment6), ten complete publics and no
private DATA/BSS. TLINK places it at096E:1C9C, size00D8, MAIN_01, ACBP48.
The only native FIXUPP is literal `c4cc5601`: OFFSET16 at objectCC references
the sole external `_hud_gauge_left_masks`, resolving its zero addend to064C.
The linked load operand isB448, target fileCCA8
(`0xB448 + 0x1860 = 0xCCA8`), distinct from load/object coordinates.
All other object CODE bytes map directly; complete216 linked bytes equal target.
There are zero MZ relocations in the whole provider. Both public MAP tables,
full OMF checksums/records and full-source cold graph remain bound.

The positive game-code evidence is the fixed288-pixel playfield/HUD geometry,
dual-player highlight-strip duplication, game-facing near/far adapter, and
four-row gauge-only operation with actual caller register arguments. The
negative vendor search supports this classification but is not its sole basis.
Neither standard mask values nor absence of a literal vendor match establishes
historical authorship. Original filename, language and historical derivation
remain unknown. The mask table, callbacks, external storage and unowned context
receive no ownership credit.

The graphics-specific fixed partition adapter lives in the existing context
helper. Player partition policy, generic accounting and return rules are
unchanged. No source bytes, runtime harness or new tests were added. Existing
focused tests and fresh two-cold/native review are used; the final receipt and
CI result are reported separately, not inferred from the proposed counters.


### Current native verification

Two independent source-cold builds repeat100 outputs/98 objects. Existing native
review passes all11 required gates for the three new owners; complete replay
covers106 extents/78,737 bytes and all1553 literal MZ relocations. The full
executable repeats the previous candidate, not the still-different target header
andEC2D byte. Existing focused42 tests pass. The bounded snapshot is
`config/main_work/graphics_fill_acceptance.json`; final full CI is pending at
writing and its result is reported separately. No whole-product exactness claim.
