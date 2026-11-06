# MAIN original PC-98 keyboard scan and real CODE alignment — after565

This stage finally closes the previously unresolved **EC2D** byte in the
original Japanese MAIN load image. It does so using an independently compiled
natural assembler directive, **not** a handwritten NOP, object patch or
target-image byte array.

## Source and boundary recovered

The maintained C++ source in src/main/hardware/input_sense.cpp already
represents the full original two-pass held-key scanner, 115 real instructions
and 417 native bytes. Its cold TC4J object has those exact 417 bytes and
42 complete literal native fixups but no final initialized alignment byte.
Ordinary TLINK previously inserted 00h between this WORD-aligned CODE
allocation and the next sound module, creating the only difference in the
entire 124,642-byte MAIN program image.

The new maintained **linear, source-order 8086 assembly TU**
src/main/hardware/input_scan.asm reconstructs those same 115 instructions
with genuine labels and ordinary named input state variables, then uses
native TASM 5.0 EVEN at odd CODE offset 417. TASM emits the original 90h NOP
at that offset as a CODE alignment result, not as an instruction invented
for the scanner. The original held-key scanner still ends at RETF offset416.

The native object has **418 CODE bytes: 417 instruction bytes + one assembler
alignment byte**; all 42 literal native reference sites, the far public
entrypoint and all external symbol declarations match the original cold
object. The new source is sequential (no discontiguous ORG blocks), so
TASM's raw OMF FIXUPP packet/order is *not asserted identical* to the old
Turbo C++ emission. Both the set of literal sites and the final **ordered
1553 MZ relocations** are checked separately and agree.

## True complete native link

Two original TASM/TLINK rounds were run with only the input scanner
object replaced in the 99-object MAIN link. The compiler library, other 98
game objects, C0, link order, Japanese target and every other project
contribution remained unchanged. In both rounds:

- The complete 124,642-byte decoded program image matches the original
  Japanese MAIN byte for byte, including EC2D.
- Every one of the 1,553 literal ordered MZ relocation entries agrees.
- The original 417-byte source object contribution grows to 418 naturally.
  The only MAP difference beyond its source-module diagnostic name is
  this one correctly owned CODE byte. Later addresses do not move.
- Both complete native OBJ/EXE/MAP vectors reproduce exactly, with
  compiler/linker logs, responses and staged source inputs preserved.

The source did not receive a target-byte code string. Inline source-level
EVEN was also tested in TC4J, but the compiler did not accept it; an
independent TASM source producer was required. A second alternative TASM
source laid out with discontiguous ORG directives achieved the original OMF
field order as well, but the maintained version prefers natural sequential
instructions because the final executable field order remains exact.
All experimental drafts and negative writer logs are retained privately.

## Still unaccepted: the complete original EXE file header

The original Japanese file is 130,882 bytes, while the ordinary Borland
TLINK output is 132,322 bytes. Both now load the *same* 124,642-byte program.
The original header has 390 paragraphs (6,240 bytes) and relocation-table
offset 28; the normal native TLINK header has 480 paragraphs (7,680 bytes)
and relocation-table offset 62. Thus no original full-file raw equality,
canonical packed-unit or whole-product source acceptance is claimed.

Current native build record:
.analysis/work/main-input-after565-native-build.json
Read-only verifier:
scripts/review_th03_main_input_after565_work.py

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_main_input_after565_work.py

No full-game cold replay was executed to obtain this bounded source-native
progress. All active raw parent receipts and stage writer logs remain retained.
