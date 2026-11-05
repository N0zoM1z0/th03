# Complete original C++ ostream insertion of streambuf — after406

Previously contextual Japanese Borland `CL.LIB` member **ostibuf** (index
812) is now reconstructed as natural 8086 ASM at `src/mainl/crt/ostibuf.asm`.
Its whole **290 original CODE bytes** implement far C++
`ostream::operator<<(streambuf*)`, exported as
`@ostream@$blsh$qn9streambuf` in original `_TEXTA` at CODE+0. It calls
`ostream::do_opfx` when enabled, obtains characters from the source
streambuf's actual virtual underflow slot, writes to the destination
streambuf's put area, uses the virtual overflow slot when full, sets the
original ios error-state bit on write failure, conditionally calls
`ostream::do_osfx`, and returns the original far ostream pointer. The
source retains the exact 16-bit object layout, near/far pointer operations,
vtable offsets and stack conventions. Its control flow even preserves the
original no-op short branch following the osfx callback; this is a real
compiler-emitted jump to the adjacent epilogue, not byte padding.

The entire original CODE, `_TEXTA`/`_DATA`/`_BSS` 290/0/0 layout,
public/mangled name, three ordered far imports and **three logical OMF
FIXUPPs** (CODE+28, +173, +270) match their original sites, widths,
frames, targets and addends. Borland's literal FIXUPP record chronology is
opposite TASM's chronological emission; literal ordered FIXUPP equality
and original member-program serialization are explicitly *not* claimed.
No target CODE arrays, synthetic relocation records or patched objects
were used to obtain the matching native output.

The after406 builder validates the unchanged 563-member after405 receipt,
then runs two actual fresh TASM/TLIB/TLINK native rounds, retaining complete
source/driver/parent-bound OBJ/LIB/EXE/MAP and writer logs. Both full decoded
Japanese original MAINL EXE and MAP are byte-for-byte equal (67,372-byte
EXE, 677 ordered DOS MZ relocations). The working CRT now has **564/893**
source-linked original members, **164,492 original-equal CODE bytes** and
**329** unchanged contextual vendor programs. This is not Factory accepted
source or a new complete cold replay.

Focused reproduction:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after406_work.py ostream-streambuf-insertion-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after406_work -v
```
