# Original Japanese MAINL CRT `strerror` / `__strerror`

This is Borland's **selected** CRT library member index 297, not an alternate
standalone object. `src/mainl/crt/strerror.asm` recovers a complete near
error-formatting helper plus two public far wrappers, **176 native CODE bytes
/ 26 initialized DATA bytes / 161 BSS bytes**. Publics are `__strerror` at
CODE+135 and `_strerror` at CODE+157. The source uses the real far error
message table `__sys_errlist`, signed error bounds `__sys_nerr`, current
`_errno`, and far `_sprintf`. It preserves the original error-text fallback,
prefix/empty-prefix handling, newline formats, and static result buffer.

The original DATA is reconstructed symbolically as `Unknown error`, `%s: %s\n`
and `%s\n`; the BSS is an uninitialized 161-byte message buffer. The source
is a real 8086 assembler implementation, **not** a baked CODE/DATA byte array
or object patch. Its initial standalone TASM comparison recovers the complete
CODE and initialized DATA bytes, original public/extern interfaces, segment
layout and **all 12 OMF relocation locations/targets**.

The original object's twelve fields are emitted in *descending* CODE-site
order by the original compiler; TASM emits the corresponding fields in
*ascending* order. **Frame metadata matches for all twelve** when paired by
site, but literal original FIXUPP record order does not. Source-built OBJ
identity is therefore not claimed, and there is no accepted-ledger promotion.

`scripts/build_th03_mainl_after66_work.py strerror` uses the retained,
source-bound original 66-source carrier; two independent normal TASM/TLIB/TLINK
rounds replace this member at original position 297, preserve the other
original vendor program records, and produce the complete **67,372-byte
Japanese decoded MAINL EXE and MAP exactly**, including all 677 ordered MZ
relocations. Working source CRT reaches **67 modules / 30,391 original-equal
CODE bytes**; **826** contextual member programs are unchanged. Evidence
is retained under `.analysis/work/mainl-after66-strerror-*` and
`.analysis/work/after66-strerror-*`, checked by
`scripts/review_th03_mainl_after66_work.py strerror` and
`tests.test_mainl_after66_work`. No full cold replay was run.
