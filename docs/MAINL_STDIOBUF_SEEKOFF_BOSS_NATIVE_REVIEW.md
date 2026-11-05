# Complete Borland `stdiobuf::seekoff` C++ boss — after401

The previously contextual original Japanese `CL.LIB` member `sdbskoff`
(index 829) is now maintained as normal 16-bit ASM in
`src/mainl/crt/sdbskoff.asm`. It exports the original Borland large-model
far C++ entry `@stdiobuf@seekoff$ql12ios@seek_diri` in `_TEXTA` (CODE+0).
The **full 291 original CODE bytes** implement 32-bit stream position
arithmetic, conditional flush through the original stream vtable at
+0x24, original direction-to-DOS `SEEK_*` normalization, `_fseek`, buffer
put/get pointer resets (`streambuf::setp`, `streambuf::setg`), and final
`_ftell`. Original unchecked pointer offsets, near/far stack conventions,
and 16-bit cleanup remain intact; there are no executable byte arrays or
patched binary objects.

Original segment layout `_TEXTA`/`_DATA`/`_BSS` = 291/0/0, C++ public
name, four imports and **all four original logical far OMF FIXUPPs** are
reproduced with their sites (155, 212, 246, 279), widths, frames, targets
and addends. Their original Borland *literal FIXUPP record order* is
reverse of native TASM's record order; therefore complete original
Borland member-program serialization is not claimed equal.

The source-bound after401 builder inherits the unchanged 550-member CRT
receipt from after400 (including the full original Japanese link proof).
Two fresh TASM/TLIB/TLINK production rounds rebuild only this added member
and its affected library/link, retaining the entire native OBJ/LIB/EXE/MAP
and phase logs. Both linked original Japanese MAINL EXE/MAP are byte-for-byte
identical (67,372-byte decoded EXE, 677 ordered DOS MZ relocations).
The working CRT is now **551/893 source-built members**, **163,002
original-equal CODE bytes**, and **342 unchanged contextual vendor members**.
No full cold replay, Factory acceptance or packed-file credit was asserted.

Focused checks:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after401_work.py stdiobuf-seekoff-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after401_work -v
```
