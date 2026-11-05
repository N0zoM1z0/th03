# Large original `string::insert` with complete C++ exception machinery

The original Japanese Borland CRT member **407**, `insert1`, is recovered in
`src/mainl/crt/insert1.asm`. This is a complete **960-byte CODE** member,
not just the exported insertion function. The original OMF separates the
365-byte `_TEXT` cleanup/catch machinery, the 595-byte `_TEXTC` insert
implementation and typed RTTI into two CODE segments, together with the
original **30 bytes initialized DATA** containing the diagnostic message.
The untouched empty `_BSS` segment and the nondefault DGROUP ordering
remain part of the native object.

The natural source includes original far copy/destructor thunks, typed
`xmsg`/`string`/`length_error`/`xalloc`/`out_of_range` exception descriptors,
C++ exception block bookkeeping, native bounds and shared-reference logic,
copy-on-write clone, and `TStringRef::splice`. The source retains all
12 imported far functions and the original exported
`@string@insert$quimx6string` member ABI. The entire original 43-field
fixup inventory is checked with segment, width, *frame*, target and addend.

`scripts/build_th03_mainl_after323_work.py string-insert-boss` reuses the
source-bound 323-member parent. Two serialized native TASM/TLIB/TLINK
rounds independently match both executable segments, all initialized
DATA, the exact Japanese MAINL EXE/MAP and its 677 ordered MZ relocations.
The CL.LIB carrier now contains **324 source-producer members** and **569
contextual original members**, with **107,665 source-compiled CRT CODE
bytes**. The `.analysis/work/after323-*` full raw OBJ/LIB/EXE/MAP and
writer logs remain retained; run
`scripts/review_th03_mainl_after323_work.py string-insert-boss` and
`tests/test_mainl_after323_work.py` for source-bound verification.

The **original ordered OMF FIXUPP record sequence is not identical** to
the TASM program (and its full library member record program is not the
original BCC serialization). This does *not* reduce the complete CODE,
DATA and logical relocation/linked EXE/MAP equality, but it prevents a
literal original OBJ serialization claim. No packed-file or Factory
accepted ownership credit is inferred from the local native checks.
