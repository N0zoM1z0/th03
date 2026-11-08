# TH03 MAIN HitCircle: TC4 register allocation blocks natural cel arithmetic

The four-frame HitCircle sprite-cel calculation now uses a natural
self-assignment for division while preserving the original BX register
sequence. The maintained source computes (age - 1) / 4, scales the cel by
six VRAM bytes, and returns the sprite bank offset. The original 445-byte
hitcirc object uses BX for the intermediate word while keeping the
HitCircle record pointer in SI and the loop index in DI.

Several fresh attempts tried to express that work as ordinary C++:

- af976b moved the calculation into a register unsigned-int local inside
  HitCircle::cel(). TC4 assigned that local to SI, moved the record pointer
  to DI, changed the loop index from DI to a stack local, and expanded the
  complete CODE from 445 to 447 bytes.
- af976c hoisted the register local into hitcircles_render(); it still
  displaced the record pointer and changed the complete object.
- af976d placed the register local after the loop index; the complete
  physical object still differed.
- af976e replaced the original BX sequence with the direct formula
  ((age - 1) / 4) * 6. TC4 optimized it into SHR AX,2 followed by the
  three-operand IMUL AX,AX,6, reducing CODE from 445 to 413 bytes.
- af976f explicitly declared the record pointer, loop index and cel value
  as ordered register locals. The complete object still differed.

- af987a used an ordinary unsigned local with sequential divide and
  multiply assignments. TC4 placed the intermediate in DI, moved the
  renderer index from DI to a stack slot, and expanded the object to
  **447 CODE bytes**.
- af989a repeated the experiment with explicit register declarations for
  the record pointer, loop index and cel local. The compiler still chose
  DI for the cel, moved the index to the stack, and emitted a four-byte
  ENTER frame; the complete object remained **447 bytes**.
- af989b expressed the scale as three natural cel-times-two terms. The
  object returned to **445 bytes**, but TC4 spilled cel to [bp-4] and
  generated repeated DX loads/additions instead of the original BX
  multiply/add sequence. Equal size did not mean equal CODE.
- af993e used a register unsigned local with an explicit right shift
  before scaling. TC4 assigned the record pointer to DI, the cel to SI and
  the loop index to a stack slot; it also emitted a four-byte ENTER frame
  and reduced the complete object to **443 CODE bytes**. The explicit BX
  sequence remains necessary for the original SI/DI lifetime and code.
- af999a replaced the division assignment with _BX >>= 2. TC4 shifted
  BX directly, whereas the original sequence copies BX to AX, shifts AX,
  then copies the result back to BX. The complete object changed.
- af999b combined (age - 1) / 4 into the initial BX assignment. TC4
  removed the original BX-to-AX round trip before SHR, changing CODE.
- af999c expressed the division as _BX = (_BX / HITCIRCLE_FRAMES_PER_CEL).
  This ordinary self-assignment preserves the original BX/AX round trip
  and reproduces the complete 445-byte object in two original compiler
  rounds.
- af999d changed the following multiply to _BX = (_BX * 2); this altered
  the original IMUL/register sequence. Keep _BX *= 2.
- af999e tried _BX * 3 in the return expression, af999f tried
  _BX + (_BX << 1), and af1000a tried 2 * _BX for the scale step.
  All three changed complete CODE; retain the three original BX additions
  and the compound multiply.
- af1000c replaced the literal multiply-by-two with
  _BX *= (HITCIRCLE_VRAM_W / 3). The compiler constant-folded the
  semantic stride and preserved all original instructions.
- af1000d named that compile-time term as
  HITCIRCLE_VRAM_W_PER_CEL_TERM = (HITCIRCLE_VRAM_W / 3) and used
  _BX *= HITCIRCLE_VRAM_W_PER_CEL_TERM. The complete physical object
  still matched, so the cel calculation now derives its stride from the
  actual six-byte VRAM width instead of a standalone magic 2.

The direct formula is cleaner algebraically but does not reproduce the
original target's intentionally unoptimized multiply/add sequence. The
register-local variants also change SI/DI lifetime and stack layout. The
self-division assignment is the useful exception: it is natural C++ and
keeps the original intermediate BX/AX code without changing the surrounding
record-pointer allocation. The multiply and return expression remain in
their original forms.

The current self-division and named VRAM-term assignments are source-bound
to af1000d: two original TC4 rounds reproduce all **445 CODE bytes, 30 literal ordered
OMF FIXUPP fields and four PUBLIC offsets**, with complete normal MAIN
image and all 1,553 ordered relocations exact. The other 98 original game
objects and Borland CRT were reused. The earlier af985b and af999c proofs are historical after this source
improvement.

Protected current-source report:
.analysis/work/exatt-layout-af999c/report.json, SHA-256
fce7038dc10ab00c9b42e0a8d62c912b929e2fb93653b95518d6d51bddf5ad88.
