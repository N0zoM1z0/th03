# MAIN foundation exact ownership

The maintained sources implement nineteen exact functions in nine reviewed
authored extents totaling 1273 owned bytes: 1272 function-body bytes plus one
explicit assembler alignment byte. Scope is the pinned Japanese MAIN.EXE.
The accepted frontier now covers vector/polar math, frame timing, keyboard/input
mode sensing, the complete sound-effect play/update and KAJA interrupt
contributions, main initialization, and PI slot loading. Reuse by packed OP and MAINL remains a reference
hypothesis, so these sources stay under `src/main`.

| Owner | Relative segment:offset | Bytes | Functions | Maintained source |
| --- | --- | ---: | ---: | --- |
| `th03-main-vector-far` | `0E8F:008A` | 160 | 2 | `src/main/math/vector_far.asm` |
| `th03-main-polar` | `0E8F:016D` | 26 | 1 | `src/main/math/polar.cpp` |
| `th03-main-frame-delay` | `0E8F:0187` | 21 | 1 | `src/main/hardware/frame_delay.cpp` |
| `th03-main-input-sense` | `0E8F:019C` | 417 | 1 | `src/main/hardware/input_sense.cpp` |
| `th03-main-snd-se` | `0E8F:034A` | 120 | 2 | `src/main/sound/se.cpp` |
| `th03-main-snd-kaja` | `0E8F:03C2` | 30 | 1 | `src/main/sound/kaja.cpp` |
| `th03-main-initmain` | `0E8F:03E0` | 62 | 1 | `src/main/core/initmain.cpp` |
| `th03-main-pi-load` | `0E8F:041E` | 70 | 1 | `src/main/formats/pi_load.cpp` |
| `th03-main-input-modes` | `0E8F:0464` | 367 | 9 | `src/main/hardware/input_modes.cpp` |

## Target review

Independent MZ parsing gives a 6240-byte target header. The nine accepted
payload starts are `0xE97A`, `0xEA5D`, `0xEA77`, `0xEA8C`, `0xEC3A`,
`0xECB2`, `0xECD0`, `0xED0E`, and `0xED54`; Ghidra's load base
adds `0x10000` to those addresses. The independently attested headless
database reports nineteen complete bodies inside the accepted owners, with exact
ends and sizes checked against independent 16-bit decoding.
Every accepted function ends in a far return, with no shared epilogue outside
its owned span.

`vector2` is the complete 69-byte far Pascal body at `SHARED:008A`; it is
followed by one assembler alignment `NOP` at `SHARED:00CF`, outside either
function body but inside the reviewed 160-byte owner. `vector2_between_plus`
then occupies the complete 90-byte body at `SHARED:00D0..0129`. TH03 target
instructions confirm the signed 16-bit length, byte angle, far output references,
32-bit `MOVSX`/`IMUL`/`SAR` fixed-point arithmetic, and `RETF 0x0C` / `RETF 0x14`. The between-plus form computes
`IATAN2(y2-y1, x2-x1) + plus_angle`; it has the owner's only MZ relocation,
the segment word of that far call at owner-relative site 94 (function-relative
site 24). Ghidra reports 15 direct callers / no callees for `vector2`, and
four direct callers / one `IATAN2` callee for `vector2_between_plus`.
The maintained source expresses these operations as symbolic TASM instructions
and `EVEN`; it contains neither the historical raw opcode byte array nor a
C++ `codestring` used to manufacture the alignment byte.

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

`snd_kaja_interrupt` is the complete 30-byte `th03/snd_kaja.cpp` contribution at
`SHARED:03C2`. TH03 itself shows an early return while `snd_active` is zero, then
loads the signed word argument from `BP+6` into AX and dispatches `INT 60h` or
`INT 61h` according to `snd_midi_active`, before `RETF 2`. The owner has no MZ
relocation sites and Ghidra reports two direct callers. TH04 supplied the source
hypothesis, but these details and the exact boundary were re-checked on TH03.

`game_init_main` is a complete 62-byte non-leaf far Pascal body at
`SHARED:03E0` with one direct caller and seven callees. Its 4-byte far-pointer
argument is consumed by `RETF 4`. Target control flow first calls
`MEM_ASSIGN_DOS(0x4650)` and returns 1 on failure; on success it calls
`vram_planes_set`, `VSYNC_START`, `EGC_START`, `GRAPH_400LINE`,
`JS_START`, and `PFSTART` before returning 0. Six ordered MZ segment-word
relocations occur at owner-relative sites 9, 30, 35, 40, 45, and 54. The
`vram_planes_set` call is linker-relaxed to `NOP; PUSH CS; CALL near` and therefore
has no segment relocation.

`pi_load` is a complete 70-byte far Pascal body at `SHARED:041E`. The target
loads the slot word from `BP+A`, scales it by `0x48` to address `PiHeader`, and
indexes the parallel far-pointer buffer array with `slot*4`. It first calls
`GRAPH_PI_FREE(&pi_headers[slot], pi_buffers[slot])`, then calls
`GRAPH_PI_LOAD_PACK(fn, &pi_headers[slot], &pi_buffers[slot])`, stores the
returned word in its local, and returns it through `RETF 6`. The filename is a
far pointer at `BP+6`. The two far-call segment words are the only owner MZ
relocations, at relative sites 31 and 60. Ghidra reports two direct callees and
no direct callers; the latter is recorded only as an analyzer observation, not
as proof that the routine is unreachable.

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

The nine maintained translation units use local ABI headers and no ReC98
includes. They were developed from the pinned TH03 reference as hypotheses and
then checked independently against TH03 target instructions, compiler/assembler
objects, link-map placement, relocations, and final linked bytes. The vector
owner deliberately uses a symbolic TASM translation unit because TC4J's inline
assembler cannot express the target's 32-bit register forms without raw opcode
bytes. The replay replaces only MAIN's `th03/vector.cpp` build-list entry
with `th03/vectorfar.asm`; the historical C++ object remains built where
MAINL/TH04/TH05 still require it. `input_sense.cpp` uses
Borland symbolic register/inline-assembly syntax for the zero-distance control
edge and the PC-98 delay-port `OUT`/`LOOP`; it contains no copied opcode array or
target-derived trailing padding byte. TC4J is invoked with the same large-model,
386, optimization and alignment options as the TH04 method. Includes use
repository-root paths because TC4J resolves nested wrapper includes differently
from modern source-relative compilers.

```sh
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-vector-far
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-polar
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-frame-delay
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-input-sense
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-snd-se
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-snd-kaja
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-initmain
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-pi-load
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
351 game objects under `obj/th01` through `obj/th05`. All 417 generated objects,
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
rounding, and 16-bit result wraparound. `frame_delay`, `input_sense`, `snd_se`, `initmain`, and
`pi_load`, `snd_kaja_interrupt`, `vector2`, and `vector2_between_plus` are not
claimed as directly exercised by that probe;
their acceptance here is based on complete target-boundary review plus exact
compiler/link/MAP/relocation/raw-byte replay. This is not PC-98 game runtime
certification.

Portable Oracle controls reject changed final bytes, changed relocated words,
relocation order/multiplicity changes, split relocation words, invalid MZ
containers and out-of-range extents. Header-size differences are accounted for
through each image's own payload mapping. Outside bytes receive no local credit.

Development replay `gpt-web-pi-load-probe1-0948` expanded the checked set to
16 functions / 1083 bytes. Post-promotion repository-shell run
`gpt-web-main-seven-owner-final-20261005-a` then began with all seven owners
already accepted and passed the full two-round aggregate. The subsequent KAJA
development replay `gpt-web-snd-kaja-probe1-1005` expanded the checked set to
17 functions / 1113 bytes. Post-promotion run
`gpt-web-main-eight-owner-final-20261005-a` began with all eight owners accepted
and again matched every function/owner byte, MAP contribution and ordered
relocation vector while the 20-product and 350-game-object vectors stayed
deterministic.
Vector development replay `gpt-web-vector-far-probe1-20261005-1828`
expanded the aggregate to 19 functions / 1272 function-body bytes and 1273
owned bytes including the single declared alignment NOP. Both cold rounds
matched the full 160-byte owner, both function bodies, MAP placement, and the
owner relocation vector. The all-game deterministic object vector is now 351
game objects / 417 generated OMF objects because MAIN adds `vectorfar.obj`
while other products still build the historical `th03/vector.obj`.
Post-promotion aggregate `gpt-web-main-nine-owner-final-20261005-a`
then began with all nine owners already accepted and independently passed the
same two-round 20-product / 351-game-object vector, all 417 OMF validations,
all 19 function bodies / 1272 function bytes, the declared alignment byte,
full 1273-byte owner aggregate, MAP placement, and ordered relocations.
Factory repository-shell execution runs this same checked-in Oracle. Native TH03
Truth Kernel replay is still unregistered; local exact ledger claims do not
become Factory-accepted receipts through source inspection or shell success.
Whole-game product closure remains open.
