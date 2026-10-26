# MAIN register-only graphics helpers

Source/ABI recovery only: no new accepted ownership or authored counts.

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
Focused artifacts are `.analysis/work/main-graphics-source-20261026/`.
Independent read-only source/raw-target review found no blocker. The existing
two-cold replay and full CI are pending at this source checkpoint; their final
reports, not this pending note, establish subsequent verification status.
