# MAINL CRT reconstruction candidates

These six providers are readable semantic reconstruction candidates, not accepted source
coverage, exact acceptance, or a copied compiler-library implementation. The source ledger
remains unchanged until actual linked/runtime/repeat proof is accepted.

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
FIXUPP indices/order differ, and actual linking must resolve them. Both earlier C336 and
ASM351 attempts remain retained. No composed link, runtime matrix or independent repeat
has yet established the new source.
These probes are diagnostic results, not exact/source-ledger acceptance.

Source-only tests validate named DATA, absence of encoded instructions/padding, public
aliases, explicit calling conventions, and the actual external-segment regression. They do
not execute the produced implementation and do not replace the existing7858-scenario CRT
CPU model, full-image comparison, relocation checks or independent native repetition.

Provenance and current limitations are recorded in provenance.json. No original library
objects, opcode blobs, guessed fill bytes or OMF postprocessing are implementation inputs.
