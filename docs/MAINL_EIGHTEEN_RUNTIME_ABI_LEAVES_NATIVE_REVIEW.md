# MAINL original 18-member CRT ABI leaf recovery (after391)

This source-bound step replaces **18 previously contextual members** of the
original Japanese Borland `CL.LIB` with maintained human-readable 16-bit
assembler in `src/mainl/crt/`: `stkavail`, `newarray`, `newfarry`, `vnewn`,
`vnewvn`, `vdeln`, `vdelxn`, `gfreemem`, `ggetmem`, `gexit`, `del`,
`delarray`, `ffmalloc`, `coreleft`, `scantod`, `realcvt`, `stxalc`, and `ctor7`.
Their original source membership was verified against the live inherited
after390 library rather than inferred from a missing `.asm` filename.

Every complete original CODE segment was reproduced byte-for-byte: **268 CODE
bytes in total**. The original per-member segment layout, exported/imported
symbol ABI and every logical OMF relocation (site, width, frame, target and
addend) were compared with the actual pinned original CL.LIB programs. This
includes the special two-segment `_stackavail` layout, the grouped
`_SCNSEG`/`_CVTSEG` scan and conversion vector jumps, the BSS-first group of
`_coreleft`, the alternate `_TEXTA` of `ios::xalloc` and the empty `_TEXTC`
segment and retained import of `ctor7`. None is an original machine-code byte
array or a patched OBJ.

**17 of 18** members also reproduce the original *literal ordered FIXUPP
sequence*. `stxalc` has the same two original `@ios@usercount` relocations,
with original sites in order 7,4 versus native TASM's 4,7: this is a **record
chronology gap**, not a field/frame/target mismatch. Original Borland full
member-program OMF serialization is not claimed equal for any of the 18.

The affected-only native build and reviewer are:

```
PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_after391_work.py eighteen-runtime-abi-leaves
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after391_work.py eighteen-runtime-abi-leaves
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after391_work -v
```

Both original TASM/TLIB/TLINK producer rounds retained complete raw
OBJ/LIB/EXE/MAP and logs. **531/893** original CRT members now link from
source; 362 original vendor members are unchanged contextual programs. Native
source CODE totals **159,989 original-equal bytes**. The two complete decoded
Japanese MAINL EXE/MAP rounds still equal their originals byte-for-byte
(67,372-byte EXE, 677 ordered DOS MZ relocations). No full cold replay was
performed. This does *not* establish packed-file ledger source ownership or
Factory acceptance for the whole MAINL product.
