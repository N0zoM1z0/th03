# Original MAINL stdiobuf overflow: source-bound native check

`src/mainl/crt/sdboflow.asm` implements the **entire** original Japanese
Borland C++ far `stdiobuf::overflow(int)` member, not a synthetic byte blob.
It retains the existing file-error test, iterates the pending put area,
forwards each character through the original FILE buffer or `__fputc`,
handles the EOF/character branch, restores get/put bounds through the
far `streambuf::setp` and `streambuf::setg` calls, and checks the FILE error
flag on exit. These control-flow paths and their stack layouts should be
cross-checked against the pinned original member rather than inferred from
another game's CRT.

Native input: `.analysis/work/mainl/vendor/sdboflow.obj`, original CRT
member **827**. The complete original member has **342 CODE bytes**, no
initialized DATA or BSS, one far public, three imported far functions, and
four CODE relocation fields. The source-bound builder
`scripts/build_th03_mainl_after319_work.py stdiobuf-overflow` and reviewer
`scripts/review_th03_mainl_after319_work.py stdiobuf-overflow` reuse the
validated 319-member parent without running a cold replay. Two independent
TASM/TLIB/TLINK rounds are preserved with source hashes, full raw
OBJ/LIB/EXE/MAP and logs under `.analysis/work/after319-*`.

Both rounds match the **complete** original materialized CODE bytes, public
and import interface, segment boundaries, all four relocation sites and
targets, all 893 CRT library slots (320 replaced by source, 573 carried as
original contextual vendor members), and the complete Japanese decoded
**67,372-byte EXE / MAP**, including the 677 ordered DOS relocations.

**OMF limitation:** Original Borland FIXUPP order is `307, 273, 214, 142`;
TASM writes `142, 214, 273, 307`. The site, target, addend and frame
metadata of all four fields agree. This is **not** a literal ordered OMF
record match, nor proof of full BCC OBJ serialization identity. It is a
complete CODE and native-link reconstruction of one working-source member.
No Factory acceptance or additional accepted decoded/packed-file extent is
claimed. See `tests/test_mainl_after319_work.py` for direct original-OBJ
checks; the reviewer checks the full inherited receipt DAG and both native
rounds without repeating the cold build.
