# MAINL far vector computation: two complete native functions (after557)

The old ownership-gap audit counted the 160-byte `obj/th03/vector_far.obj`
contribution as **outside published decoded CODE ownership**, although the
maintained natural source `src/shared/math/vector_far.asm` already existed.
This review now compiles and re-links that **actual current source**, not a
historical hypothesis, independently against the current after556 MAINL
source-backed native parent. Neither the old ownership publication nor any
canonical acceptance claim is changed.

The contribution contains **two real FAR Pascal vector operations**:
`VECTOR2` (69 CODE bytes, SHARED+0) and `VECTOR2_BETWEEN_PLUS` (90 CODE
bytes, SHARED+70). Both multiply 16-bit polar lengths by signed, Q8.8
sin/cos-table values using 386 32-bit intermediate registers and arithmetic
right shift. The second function derives its heading with a genuine FAR
`IATAN2` call before applying the additional angle. Real near/far pointer
arguments, return stack adjustments and x86 segment state remain visible in
the symbolic source. All complete bodies disassemble to instruction boundaries
ending at FAR RET.

The **one byte between functions at SHARED+69 is 90h** emitted by TASM's
natural `EVEN` directive in a CODE segment, not a hand-inserted hex byte,
a third function or a credited instruction. The original object's two PUBLIC
positions are 0 and 70. All **160 original contributor initializer bytes**,
**five ordered native OMF FIXUPP fields**, both PUBLIC definitions/positions
and all non-variable other OMF metadata matched in the native recompilation.
Native TASM's existing alignment warning is recorded in retained native logs,
not hidden or treated as a failed byte comparison.

For **two independent rounds**, the driver compiled the real maintained
source (explicit LF-to-DOS-CRLF transport) and linked the new vector object in
place of only the old contribution. It reused the after556 DATA/root/text and
the earlier first-use C0 and CRT library, without recompiling unrelated
objects. Both full **67,372-byte decoded MAINL EXE** outputs matched exactly,
including all **677 MZ relocations**. The complete MAP contribution sizes,
addresses and order matched, accounting only for the new assembler wrapper
filename. The entire raw OBJ/EXE/MAP vector repeated in both rounds.

Run the retained, read-only affected review:

```sh
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
  .venv/bin/python scripts/review_th03_mainl_vector_work.py
```

Driver: `scripts/build_th03_mainl_vector_work.py`. Retained native report:
`.analysis/work/vector-after557-native-build.json`; artifacts include both
compile logs, TLINK logs, two complete output vectors and staged input bytes.
This is new scoped CODE **source-binding evidence**, not a complete cold
rebuild, proof of the original vendor OMF packet ordering, Factory accepted
receipt, or project-wide function ownership publication. In particular, the
unresolved 418-byte input scan CODE boundary was not changed or disguised.
