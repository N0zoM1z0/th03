# MAIN input and polar ownership

The maintained sources implement ten functions in two complete TC4J code
contributions. Scope is the pinned Japanese MAIN.EXE. Reuse by packed OP and
MAINL remains a reference hypothesis, so these sources stay under `src/main`.

| Owner | Relative segment:offset | Bytes | Functions | Maintained source |
| --- | --- | ---: | ---: | --- |
| `th03-main-polar` | `0E8F:016D` | 26 | 1 | `src/main/math/polar.cpp` |
| `th03-main-input-modes` | `0E8F:0464` | 367 | 9 | `src/main/hardware/input_modes.cpp` |

## Target review

Independent MZ parsing gives a 6240-byte target header. Payload offsets are
`0xEA5D` and `0xED54`; Ghidra's load base adds `0x10000` to those addresses.
The independently attested headless database reports ten contiguous bodies,
with exact starts, ends and sizes matching an independent 16-bit disassembly.
Every input function ends in a far return, with no shared epilogue outside its
owned span. `input_wait_for_change` owns both loops through `RETF 2`; no padding
or data is assigned to its body. The full input contribution is the contiguous
union of all nine bodies. `polar` has no calls and owns its final `RETF`.

The target `polar` loads signed words from BP+8 and BP+10 into 32-bit registers,
multiplies them, shifts arithmetically by eight, and adds the BP+6 center word.
Its cdecl caller owns six argument bytes. TH04's maintained implementation
confirms the arithmetic hypothesis but uses Pascal; its ABI is not imported.

Input mode calls to the keyboard scanner and frame delay are genuine
far-to-near linker relaxations (`NOP; PUSH CS; CALL near`). Joystick sensing
remains a far master.lib call. DGROUP offsets in MAIN are `0x02CC` for existence,
`0x11B6` for the first joystick word, and `0x1A96/98/9A` for P1/P2/interface
input. All six joystick segment-word relocation sites belong to the input
owner. They are compared at their original values, in order, with duplicates
preserved. No relocation bytes or call operands are masked.

The Ghidra caller query reports 24 direct callers of `polar` and the wait
function calling interface mode. A lack of direct callers for other modes does
not establish dead code; input modes are also selected through function pointers.
Analyzer names and no-argument convention labels do not override the target ABI.

## Source and replay

The two local translation units have local ABI headers and no ReC98 includes.
They were developed from the pinned TH03 reference hypothesis and checked
against TH03 target instructions, compiler objects and linked bytes. TC4J is
invoked with the same large-model, 386, optimization and alignment options as
the TH04 method. Includes use repository-root paths because TC4J resolves nested
wrapper includes differently from modern source-relative compilers.

```sh
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-polar
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-input-modes
python3 scripts/replay_th03_main_exact_units.py --run-id NEW_UNIQUE_ID
```

Each invocation freezes source/configuration/tool/Oracle inputs, materializes
the pinned ReC98 revision twice through `git archive`, overlays local source,
and performs two serial full cold builds. No game objects are copied. ReC98 is
the open link graph's scaffold; only the maintained, reviewed owners receive
exact credit. Link-map contribution starts, lengths, segment, alignment and
all function publics must agree. Both owners and every full function body must
match the original bytes and ordered overlapping MZ relocations.

The declared determinism vector includes the 20 configured game outputs and
350 game objects under `obj/th01` through `obj/th05`. All 416 generated objects,
including non-game objects, are independently validated as OMF. Nine Research
blitting benchmark objects embed `__DATE__/__TIME__` in LEDATA and differ
between rounds; their differences remain diagnostic and are never normalized
away. They are outside every declared game object root and link response.
The older imported all-game calibration hashes remain unchanged and failing;
this separate source replay establishes only the current owned extents.

Each round also links the actual maintained objects to a DOS behavior probe.
Explicit hardware test doubles check joystick/keyboard routing, cancel/OK
normalization, finite release/press waits, 0 and 9999 unlimited waits, negative
wait parameters, negative fixed-point rounding and 16-bit result wraparound.
This is an executable ABI/behavior check, not PC-98 game runtime certification.

Portable Oracle controls reject changed final bytes, changed relocated words,
relocation order/multiplicity changes, split relocation words, invalid MZ
containers and out-of-range extents. Header-size differences are accounted for
through each image's own payload mapping. Outside bytes receive no local credit.

Factory repository-shell execution runs this same checked-in Oracle. Native
TH03 Truth Kernel replay is still unregistered; local exact ledger claims do
not become Factory-accepted receipts through source inspection or shell success.
Whole-game product closure remains open.
