# MAIN foundation exact ownership

The maintained sources implement fourteen exact functions in five reviewed
authored extents totaling 951 bytes. Scope is the pinned Japanese MAIN.EXE.
The accepted frontier now covers polar math, frame timing, keyboard/input mode
sensing, and the complete sound-effect play/update translation-unit
contribution. Reuse by packed OP and MAINL remains a reference hypothesis, so
these sources stay under `src/main`.

| Owner | Relative segment:offset | Bytes | Functions | Maintained source |
| --- | --- | ---: | ---: | --- |
| `th03-main-polar` | `0E8F:016D` | 26 | 1 | `src/main/math/polar.cpp` |
| `th03-main-frame-delay` | `0E8F:0187` | 21 | 1 | `src/main/hardware/frame_delay.cpp` |
| `th03-main-input-sense` | `0E8F:019C` | 417 | 1 | `src/main/hardware/input_sense.cpp` |
| `th03-main-snd-se` | `0E8F:034A` | 120 | 2 | `src/main/sound/se.cpp` |
| `th03-main-input-modes` | `0E8F:0464` | 367 | 9 | `src/main/hardware/input_modes.cpp` |

## Target review

Independent MZ parsing gives a 6240-byte target header. The five accepted
payload starts are `0xEA5D`, `0xEA77`, `0xEA8C`, `0xEC3A`, and `0xED54`;
Ghidra's load base adds `0x10000` to those addresses. The independently
attested headless database reports fourteen complete bodies at the reviewed
starts, with exact ends and sizes checked against independent 16-bit decoding.
Every accepted function ends in a far return, with no shared epilogue outside
its owned span.

`frame_delay` is a complete 21-byte far Pascal function through `RETF 2`.
`input_reset_sense_key_held` is one large 417-byte far cdecl body with no
callees and ten direct callers in the target database. The target byte
immediately after its `RETF`, at `SHARED:033D`, is a standalone `NOP`: it is
outside the reviewed function body. The maintained translation unit therefore
owns 417 bytes rather than the historical 418-byte object contribution. It does
not add a `codestring` merely to claim that padding byte. The linker still
places the following object at `SHARED:033E`, so excluding the NOP does not move
any later accepted owner.

`snd_se_play` and `snd_se_update` are adjacent 60-byte bodies at
`SHARED:034A` and `SHARED:0386`. Together they exactly cover the 120-byte
`th03/snd_se.cpp` MAP contribution through `SHARED:03C1`; the next owner starts
at `03C2`. The play entry is far Pascal and returns with `RETF 2`; the update
entry is far cdecl. Target disassembly confirms the PMD `INT 60h` path, the
`0xFF` no-effect sentinel, and byte tables/state at the observed DGROUP offsets.
The owner has no MZ relocation sites. Ghidra reports 55 direct callers of play
and three of update, so this is not a leaf-only expansion.

`input_wait_for_change` owns both loops through `RETF 2`; no padding or data is
assigned to its body. The full input-mode contribution is the contiguous union
of all nine bodies. `polar` has no calls and owns its final `RETF`.

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

The Ghidra caller query reports 24 direct callers of `polar`, three direct
callers of `frame_delay`, and ten direct callers of
`input_reset_sense_key_held`; the wait function calls interface mode. A lack of
direct callers for other modes does not establish dead code because input modes
are also selected through function pointers. Analyzer-generated convention
labels do not override the target ABI.

## Source and replay

The five maintained translation units use local ABI headers and no ReC98
includes. They were developed from the pinned TH03 reference as hypotheses and
then checked independently against TH03 target instructions, compiler objects,
link-map placement, relocations, and final linked bytes. `input_sense.cpp` uses
Borland symbolic register/inline-assembly syntax for the zero-distance control
edge and the PC-98 delay-port `OUT`/`LOOP`; it contains no copied opcode array or
target-derived trailing padding byte. TC4J is invoked with the same large-model,
386, optimization and alignment options as the TH04 method. Includes use
repository-root paths because TC4J resolves nested wrapper includes differently
from modern source-relative compilers.

```sh
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-polar
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-frame-delay
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-input-sense
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-snd-se
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-input-modes
python3 scripts/replay_th03_main_exact_units.py --run-id NEW_UNIQUE_ID
```

Each invocation freezes source/configuration/tool/Oracle inputs, materializes
the pinned ReC98 revision twice through `git archive`, overlays local source,
and performs two serial full cold builds. No game objects are copied. ReC98 is
the open link graph's scaffold; only the maintained, reviewed owners receive
exact credit. Link-map contribution starts, lengths, segment, alignment and
all function publics must agree. Every accepted owner and every full function
body must match the original bytes and ordered overlapping MZ relocations. The
unowned `input_sense` tail NOP is intentionally outside exact authored-byte
credit.

The declared determinism vector includes the 20 configured game outputs and
350 game objects under `obj/th01` through `obj/th05`. All 416 generated objects,
including non-game objects, are independently validated as OMF. Nine Research
blitting benchmark objects embed `__DATE__/__TIME__` in LEDATA and differ
between rounds; their differences remain diagnostic and are never normalized
away. They are outside every declared game object root and link response.
The older imported all-game calibration hashes remain unchanged and failing;
this separate source replay establishes only the current owned extents.

Each round also keeps the existing DOS behavior probe passing. Its explicit
hardware test doubles exercise the accepted input-mode and polar behavior:
joystick/keyboard routing, cancel/OK normalization, finite release/press waits,
0 and 9999 unlimited waits, negative wait parameters, negative fixed-point
rounding, and 16-bit result wraparound. `frame_delay`, `input_sense`, and
`snd_se` are not claimed as directly exercised by that probe; their acceptance
here is based on complete target-boundary review plus exact
compiler/link/MAP/relocation/raw-byte replay. This is not PC-98 game runtime
certification.

Portable Oracle controls reject changed final bytes, changed relocated words,
relocation order/multiplicity changes, split relocation words, invalid MZ
containers and out-of-range extents. Header-size differences are accounted for
through each image's own payload mapping. Outside bytes receive no local credit.

Post-promotion repository-shell run `gpt-web-main-five-owner-final-20261005-a`
began with all five current owners already accepted and passed the full two-round
aggregate again. Factory repository-shell execution runs this same checked-in
Oracle. Native TH03 Truth Kernel replay is still unregistered; local exact ledger
claims do
not become Factory-accepted receipts through source inspection or shell success.
Whole-game product closure remains open.
