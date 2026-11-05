# Complete original istream::ipfx(int) state/tie/skip Boss — after436

The original Japanese Borland `CL.LIB` member `istdipfx` (index 756) is
now reconstructed in readable natural 8086 at `src/mainl/crt/istdipfx.asm`.
Its actual far C++ `@istream@ipfx$qi` code clears the original input gcount,
checks `ios` error flags, and on failure invokes the real far
`@ios@setstate$qi`. For a healthy stream it checks the tied `ostream`,
computes buffered `egptr-gptr` availability through the original far object
layout, conditionally calls `@ostream@flush$qv`, and follows the original
`skipws` flag into `@istream@eatwhite$qv`. Final return-status logic
preserves the original error/EOF branch and far ABI.

All **262 original CODE bytes** are source-assembled, including the 8-byte
stack scratch area, near and far pointer traversal, authentic short/near
jump widths and all error paths. The original `_TEXTA`/`_DATA`/`_BSS`
segments, C++ public name at CODE+0, three ordered external imports and
all **four original logical OMF FIXUPP fields** are reproduced without
site/frame/target/width/addend normalization. Their literal record order
differs between Borland and TASM; full raw original OMF member-record
equality is not claimed. No copied executable original bytes or patches.

The after436 builder reuses the unchanged source-bound after435 native
receipt and performs two fresh native TASM/TLIB/TLINK producer rounds,
retaining full OBJ/LIB/EXE/MAP outputs and logs. Both full Japanese decoded
MAINL EXE/MAP are byte-for-byte original-equal (67,372-byte EXE, 677
ordered DOS relocations). The working CRT becomes **644/893** source-built
members, **173,948 original-equal CODE bytes** and **249** contextual vendor
programs. This is not Factory accepted-source credit or full cold replay.

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after436_work.py istream-prefix-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after436_work -v
```
