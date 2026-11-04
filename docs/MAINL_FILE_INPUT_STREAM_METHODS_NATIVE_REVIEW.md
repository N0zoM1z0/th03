# Original Japanese C++ `filebuf`, `stdiobuf`, `istream`: eight complete algorithms

Eight distinct **selected original CRT members** have full authored symbolic
8086 implementations, covering complete buffer pointer arithmetic, file
seek/write/read synchronization and virtual stream input methods:

| Original slot | Module | CODE | Method |
| ---: | --- | ---: | --- |
| 715 | `fsbskoff` | 434 | `filebuf::seekoff` |
| 717 | `fsbuflow` | 440 | `filebuf::underflow` |
| 716 | `fsbsync` | 415 | `filebuf::sync` |
| 831 | `sdbuflow` | 416 | `stdiobuf::underflow` |
| 774 | `istgbuf` | 369 | `istream::get(streambuf&, char)` |
| 760 | `istebuf` | 361 | `istream::operator>>(streambuf&)` |
| 761 | `istechp` | 355 | `istream::operator>>(char&)` |
| 830 | `sdbsync` | 286 | `stdiobuf::sync` |

All **3,076 original CODE bytes** are real 16-bit assembly instructions,
not original machine byte array initializers or equivalent reimplementations
with different calling conventions. All eight use the correct large-model
Borland C++ `far` public ABI, exact `_TEXTA` segment and empty `_DATA/_BSS`,
and original DGROUP `08ff02ff03`. Original `filebuf` routines perform
actual DOS `_read`, `_write` and `_lseek` plus `streambuf` buffer management;
`stdiobuf` uses the real C `FILE` `_fgetc`, `_ungetc`, `_fseek` interfaces;
`istream` methods preserve the original sentry, character classification,
error states, far streambuf pointers and explicit buffer calls.

The original selected CRT reveals **10 real virtual far indirect calls**
in this family (e.g. `filebuf::underflow` CODE+114 `FF 5F 24`, `stdiobuf::
underflow` +126 `FF 5F 18`, and `istream::get` +69/+178/+259). Untyped
`call [bx+...]` would silently emit the wrong near `FF /2`; all original far
virtual calls are expressed as real `call dword ptr [...]` instructions,
with original `FF /3` opcode and buffer register ownership. The `__ctype`
reference in `istechp` uses original DGROUP frame and original `+1` offset.

TASM 5.0 `/m /mx /kh32768 /t` independently reproduces **all eight complete
original CODE segments and original public offsets**, ordered imports,
segment names/classes, and **all 32 native OMF relocations at the exact
original site, kind, target, addend, width and frame method**. The BCC/TASM
literal FIXUPP record sequence is generally different; whole original OBJ
serialization is not claimed where false. No byte or OBJ patches used.

`build_th03_mainl_after177_work.py file-stream-methods` inherits the full
source-bound **177-source Japanese MAINL CRT**, replacing eight genuine
selected member slots in two independent normal TASM/TLIB/TLINK rounds.
Both rebuild the **entire original 67,372-byte decoded Japanese MAINL EXE and
MAP byte-for-byte**, preserving all **677 ordered MZ relocations**, with
**708 unchanged original contextual vendor CRT program records**. Working
source reaches **185 members / 82,159 original-equal CODE bytes**. This is
working-source reconstruction, not formal accepted-ledger promotion;
no full cold replay was performed.

Proof: `review_th03_mainl_after177_work.py file-stream-methods`,
`tests.test_mainl_after177_work`, two actual raw OBJ/LIB/EXE/MAP vectors,
source-bound receipts and native writer logs under `.analysis/work/after177-*`
and `.analysis/work/mainl-after177-*`.
