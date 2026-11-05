# NEC PC-98 text-color and attribute Boss — after397

The original Japanese Borland `CL.LIB` member **cneccolr** (index 537) is
reconstructed in human-readable 8086 source at `src/mainl/crt/cneccolr.asm`.
It has six original complete far APIs: `___nec_textcolor` at CODE+0,
`___nec_textbackground` at +52, `___nec_textattr` at +90,
`___nec_highvideo` at +175, `___nec_lowvideo` at +193 and
`___nec_normvideo` at +211. These preserve the actual NEC display-mode
branching, `__video` attribute-bit arithmetic and the original 16-bit ABI.

The full **222 original CODE bytes** and **128 initialized DATA bytes** are
source-reconstructed, including four explicit sixteen-word color/attribute
lookup tables at DATA+0/32/64/96. This is real authored DATA, not disguised
machine-code byte stuffing. All 21 original OMF logical relocation fields
(site, width, frame, target, addend), all six public offsets, the lone
`__video` import, and the original `_TEXT`/`_DATA`/`_BSS` layout 222/128/0
match. The final TASM group record is the original DATA-first
`08ff02ff03` rather than a superficially reasonable but wrong group order.
The original Borland FIXUPP *record chronology* differs from TASM's emitted
order, so **literal ordered FIXUPP equality and original member-record
serialization are not claimed**. The complete logical fields are equal.

The source-bound `scripts/build_th03_mainl_after397_work.py` uses only the
unchanged parent after396 native evidence and builds two fresh actual
TASM/TLIB/TLINK rounds retaining raw OBJ/LIB/EXE/MAP and writer logs. The
complete Japanese decoded MAINL EXE/MAP match the originals byte-for-byte
in both rounds; EXE is 67,372 bytes with 677 ordered DOS MZ relocations.
This produces **538/893** working-source CRT members and **162,077 original-
equal source CODE bytes**, leaving 355 unchanged original contextual vendor
members. No full cold replay was run; packed-file canonical source acceptance
and Factory validation of ownership remain open.

Focused native verification:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after397_work.py pc98-text-color-attribute-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after397_work -v
```
