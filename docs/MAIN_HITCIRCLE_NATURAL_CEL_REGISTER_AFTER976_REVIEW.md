# TH03 MAIN HitCircle: TC4 register allocation blocks natural cel arithmetic

The four-frame HitCircle sprite-cel calculation still needs the original
explicit BX register sequence. The maintained source computes
(age - 1) / 4, scales the cel by six VRAM bytes, and returns the sprite bank
offset. The original 445-byte hitcirc object uses BX for the intermediate
word while keeping the HitCircle record pointer in SI and the loop index
in DI.

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

The direct formula is cleaner algebraically but does not reproduce the
original target's intentionally unoptimized multiply/add sequence. The
register-local variants also change SI/DI lifetime and stack layout. Keep
the explicit BX sequence until a natural expression is found that preserves
both the intermediate code and the surrounding record-pointer allocation.

The explicit BX cel calculation remains unchanged in the current
complete hitcirc source. The latest full-owner proof is af985b: two
original TC4 rounds reproduce all **445 CODE bytes, 30 literal ordered
OMF FIXUPP fields and four PUBLIC offsets**, with complete normal MAIN
image and all 1,553 ordered relocations exact. The other 98 original game
objects and Borland CRT were reused. The af931b receipt is historical after
the later HitCircle loop recovery; the cel arithmetic itself was retained.

Protected current-source report:
.analysis/work/exatt-layout-af985b/report.json, SHA-256
000fc1edb8af9c71f4daa3c91f14a9c64825f8fb4b06e89c1b25853d804641a1.
