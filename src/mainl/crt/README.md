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
- fbrk.c: near heap-break functions, huge pointers,16-bit PSP rounding and cached granules.

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
No composed link, runtime matrix or independent repeat has yet established the new source.
These probes are diagnostic results, not exact/source-ledger acceptance.

Source-only tests validate named DATA, absence of encoded instructions/padding, public
aliases, explicit calling conventions, and the actual external-segment regression. They do
not execute the produced implementation and do not replace the existing7858-scenario CRT
CPU model, full-image comparison, relocation checks or independent native repetition.

Provenance and current limitations are recorded in provenance.json. No original library
objects, opcode blobs, guessed fill bytes or OMF postprocessing are implementation inputs.
