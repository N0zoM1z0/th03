# Complete original filebuf::open: 321-source native MAINL carrier

The source `src/mainl/crt/fsbopen.asm` recovers the full 346-byte original
Japanese Borland `filebuf::open(const char far *, int, int)` member. This is
not a shortened wrapper: the native control flow checks the opened state,
translates input/output/append/truncation/binary/inheritance mode flags,
invokes `_open`, records descriptor and mode, calls `_lseek`, returns failure
when the seek position is `-1`, computes buffered/unbuffered pointer bounds,
and invokes both far `streambuf::setp` and `streambuf::setg`.

Original CRT member **713** (`.analysis/work/mainl/vendor/fsbopen.obj`)
contains 346 CODE bytes, zero DATA and BSS, one member public, four far
imports (`_lseek`, `_open`, `setp`, `setg`), and four relocation fields. The
source and ABI are bound to this original member rather than an inferred
C++ library version or another game's CRT.

`scripts/build_th03_mainl_after320_work.py filebuf-open` reuses the full
319 → 320 verified source-bound parent receipt chain, checks original member
program, compiles with native TASM, rebuilds the 893-member CRT library and
links the Japanese target **twice** with TLIB/TLINK. Both rounds have matching
complete CODE and zero DATA, every public/import and relocation site/target,
**321** source members, **572** unchanged original contextual members, and
raw-equal decoded Japanese EXE and MAP (67,372-byte MZ image, 677 ordered
relocations). All source-input hashes, native raw OBJ/LIB/EXE/MAP and writer
logs are retained in `.analysis/work/after320-*` and reviewed by
`scripts/review_th03_mainl_after320_work.py filebuf-open` and
`tests/test_mainl_after320_work.py` without a new cold replay.

**Known serialization difference:** the original BCC FIXUPP order is
`327,293,176,122`, whereas TASM emits `122,176,293,327`. Each field's
site, target, frame and addend match. The original *ordered* OMF record
program does **not** match. Native link equality does not establish complete
BCC OBJ serialization identity or formally accepted source ownership;
Factory ledger acceptance and whole-game exactness remain open.
