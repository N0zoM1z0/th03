# Original DOS setargv startup boss: entire PSP/DBCS parser and sparse INIT

The original Japanese Borland CL.LIB member **362** (`setargv`) is now
reconstructed in `src/mainl/crt/setargv.asm` as natural 8086 code,
not a wrapper or target-byte executable array. Its complete **343-byte
CODE** program parses the original DOS PSP command tail, manages quoted
and unquoted arguments, handles PC-98/DBCS lead-byte and backslash escape
logic, allocates the argument pointer array on the stack, restores the
original startup registers and transfers control back to the CRT. It calls
the real original `___path_isdbcsleadbyte` and `__abort` far routines,
not sanitized replacements.

This member preserves unusually important sparse initialization:
- `_TEXT` is **343 bytes**, of which offsets 0 and 1 are *truly
  uninitialized* startup saved-DS space; only 341 bytes appear in LEDATA.
- `_DATA` is **16 bytes**, with six initialized bytes for exported
  `__argc` and far `__argv` and ten genuinely uninitialized bytes of
  argument/stack-register state at offsets 6..15.
- `_INIT_` is **6 bytes**, with original priority `1000h`, a near CODE
  offset reference to entry CODE+2 and two unwritten trailing bytes.

The original Borland object also exports an **absolute** public symbol
`__setargv__` at 0, in addition to DATA `__argc` at 0 and `__argv` at 2.
The source reproduces that original ABS PUBDEF with a real `EQU`/`PUBLIC`
declaration, not a fictitious near code entry. It also correctly distinguishes
the far `__C0argv` offset (external addend 0) from its segment word
(external addend +2), which was identified by direct original OMF evidence.

The source's **all 341 materialized CODE bytes, six initialized DATA bytes,
four actual INIT bytes**, all actual sparse/uninitialized sites, original
segments/public/import/group ABI and all **30 logical OMF relocation fields**
match the pinned original Japanese CL.LIB member, including frame, target,
width and addend. **Limitation:** the original Borland ordered FIXUPP record
sequence differs from TASM's emission order and full Borland OBJ program
serialization differs too. This is retained as
`literal_OMF_FIXUPP_equal = false`, rather than normalized away.

`scripts/build_th03_mainl_after363_work.py startup-dos-argv-boss` takes
the verified **427-source** parent and compiles this one changed original
member, reassembling the original 893-slot library with native TASM/TLIB/
TLINK in **two independent rounds**. Despite the different OMF record
ordering, both rounds reproduce the original **67,372-byte Japanese decoded
MAINL EXE and complete MAP byte-for-byte**, including all **677 ordered DOS
MZ relocations**. The source-backed CRT now reaches **428 members**,
**465 unchanged contextual original members**, and **136,524 original-equal
logical CODE bytes**, an increase of 343. Raw OBJ/LIB/EXE/MAP rounds, logs,
SHA receipts and the full independent OMF/MZ checks are retained under
`.analysis/work/after363-*`, `scripts/review_th03_mainl_after363_work.py`
and `tests/test_mainl_after363_work.py`.

No full cold replay, formal Factory-accepted extent, packed-unit credit or
whole-game source exactness is asserted.
