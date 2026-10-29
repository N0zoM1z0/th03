# MAINL semantic CRT reconstruction

Current decoded ownership is documented in
[the six-provider review](../../../docs/MAINL_CRT_NATIVE_REVIEW.md) and
[the complete far-heap review](../../../docs/MAINL_FARHEAP_NATIVE_REVIEW.md).
`farheap.asm` adds the paragraph allocation/free/reallocation bank, with1,103
CODE and12 file-backed CS state bytes. A selected normal-library replacement
rebuilds this seventh provider twice while preserving the unchanged full cold
pair. [The overlay execution review](../../../docs/MAINL_EXEC_NATIVE_REVIEW.md)
adds `exec.asm` and demonstrates all eight source providers in one normal
library, reusing the unchanged farheap object.
[The program loader review](../../../docs/MAINL_LOADPROG_NATIVE_REVIEW.md) adds
`loadprog.asm`, whose selected library composes all nine source providers.
The historical observations below
describe earlier checkpoints and do
not define current source acceptance or its remaining whole-product limits.

These six semantic ASM providers have actual source-consumption, native repetition, linked
image and CPU-model evidence. They are not copied library implementations. Source coverage
is distinct from formal exact or canonical packed acceptance; neither is claimed here.

- h_llsh.asm: DX:AX left shift, including near/far return bridge and CPU count masking.
- h_padd.asm: signed huge-pointer addition/subtraction, paired cross-branches and bridges.
- n_pcmp.asm: huge-pointer comparison returning CPU ordering flags.
- ioerror.asm: signed DOS/System-V error translation and original-code return, with named
  errno mapping constants in the actual DATA table.
- setblock.asm: far cdecl DOS memory resize and failure maximum-size return.
- fbrk.c: retained high-level C candidate, including its336-byte native result.
- fbrk.asm: semantic assembly provider with explicit near/far ABI and16-bit PSP invariants.
  Use one FBRK provider, never link both implementations together.

IOERROR/DOSERROR are near callee-pop; setblock is far caller-pop. The private C growth helper
is near Pascal, and brk/sbrk are near cdecl. Pointer arithmetic intentionally clobbers ES.
Important quirks remain intentional: signed INT_MIN errno negation, BX=FFFF DOS failure
colliding with the resize success sentinel, failure writes to heap top, unsigned16 wrapping
before PSP rounding, signed-long upper limit without a lower limit, and the -1MiB alias.

Actual TASM probes now naturally reproduce raw CODE/public contracts for all five ASM
providers (276 bytes), including IOERROR's82 CODE and91 DATA bytes. The first IOERROR
attempt was84 bytes because CODE-scoped external errno declarations caused two incorrect
CS overrides; the retained successor places them in _DATA. Corrected IOERROR has the same
five symbolic fixups, with two entries reordered relative to the historical member.

The initial C probe rejected unsupported -0 before compilation. The fresh successful TC4
probe used -c -ms -3- -2- -1- -O, following the compiler's documented switch-disable syntax.
It naturally emitted the intended near helper externs and far setblock call, plus matching
DATA2, but FBRK CODE is336 rather than352 bytes. Public offsets are __brk126/__sbrk189,
versus historical142/209. Register allocation, prologues and epilogue arrangement differ.
The first semantic FBRK ASM probe emitted351 bytes because CODE-scoping the far external
let TASM shorten the call prematurely. Declaring that imported far code outside all segments
produces the genuine five-byte far call. The corrected native ASM result is352 CODE bytes,
DATA2 and public offsets142/209, all raw-equal to the historical member. All six ASM
providers therefore match628 raw CODE bytes and93 owned DATA bytes in isolated objects.
FIXUPP indices/order differ; actual TLINK resolves them naturally, including its far-call
relaxation. Both earlier C336 and ASM351 attempts remain retained.

Normal TLIB extraction/rebuild preserves all893 original A3 member positions, retaining887
contextual payloads and substituting only the six freshly assembled providers. A second
actual assembly of all six produces identical raw objects; the second private library, EXE
and MAP also match exactly. The full EXE matches the prior cold aggregate carrier. Two fresh
actual-image CPU runs, decoded target and final repeat, each pass7858 scenarios across13
partitions and cover277 instruction positions. Complete CPU observations match except the
pre-existing before/after whole-memory hash fields. Raw EXE equality bridges the first link
to the tested repeat without a redundant third CPU run.

Replay: scripts/replay_th03_mainl_crt_link.py, recipe config/th03_mainl_crt_link.json.
The fast replay checks retained evidence; it does not rerun native tools or CPU matrices.
Known whole-image differences remain: DATA linear60473 is target90h/candidate00h, and461
relocation ordering positions differ although all677 relocation members match. Formal exact
acceptance remains zero and canonical packed acceptance is still separate.

Source-only tests validate named DATA, absence of encoded instructions/padding, public
aliases, explicit calling conventions, and the actual external-segment regression. They do
not execute the produced implementation and do not replace the existing7858-scenario CRT
CPU model, full-image comparison, relocation checks or independent native repetition.

Provenance and current limitations are recorded in provenance.json. No original library
objects, opcode blobs, guessed fill bytes or OMF postprocessing are implementation inputs.
