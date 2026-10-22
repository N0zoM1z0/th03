# OP PFOPEN maintained source

This checkpoint owns only the complete game-modified PFOPEN routine, 281 decoded
bytes at `0000:2EF2..300B`. The following STR_IEQ and every other root routine,
table and alignment byte remain context. The physical producer is unchanged:
`th03_op.asm` assembles as `obj/th03/op.obj`; PFOPEN is not a fabricated standalone
object or a payload emitted with byte directives.

`src/shared/formats/pfopen.asm` retains the exact original instructions and adds
ASCII semantic comments. The 12 isolated files under `compat/op_pfopen/` preserve
the genuine macro/header closure, including the large-model FAR ABI and original
structure definitions. Exact-path Git attributes retain their original bytes and
line endings. No CP932 conversion or broader encoding exemption is introduced.

The source-only stager validates the full 142-file original physical source context
before applying this single routine overlay. The dated native observation uses the
original TASM32 command and original link response, rebuilds only the mixed root
object, and retains 27 other objects from the actual 28-object graph. The source
scope does not expand to the remainder of that root object.

The offline replay binds the actual two native phases and their immutable receipts,
source and toolchain provenance, and the separately corrected selection-link
prerequisite. It checks all 44 preceding scopes (12,940 bytes), PFOPEN's 281 bytes,
whole-context equality and literal relocation order. Historical registry transitions
are evidence, not a requirement that today's mutable registry or repository HEAD
still equal the native observation. Replaying does not run a compiler or emulator.

The verified mixed output remains unequal to the complete historical target.
DD95 vendor alignment, unresolved global relocation ordering, IRAND ownership,
runtime/packing reconstruction and exact whole-product acceptance are unchanged.
The sparse source ledger has 45 maintained units among 46 decoded units; the
separate fixed 33-unit acceptance cohort is not expanded or published here.
