# Japanese MAINL selected Borland locale-collation pair

Two additional genuine source modules from the original Japanese large-model
CRT, each a complete multi-function source extent:

| Selected member | Original index | Complete CODE | Exports | Fixups |
| --- | ---: | ---: | ---: | ---: |
| `collate` | 207 | **435** | Six public near collation helpers | 0 |
| `_strxfrm` | 192 | **382** | `__strxfrm` at +0 and `_LevelTransform` at +74 | 2 |

`src/mainl/crt/collate.asm` recovers the original key-weight iterator and
substitute/compress/expand/auxiliary-string handlers, including their
flags/stack scratch and far table readers. Its six actual original public
symbols are `_GetNextKeyWeight` at +10, `_GetSubstituteString` at +140,
`_GetCompressLevelWeight` at +228, `_GetExpansionString` at +303,
`_GetNextAuxChar` at +371 and `_GetNextExpansionWeight` at +398.
The original 10-byte stack-frame prelude at CODE+0 is preserved, not
silently attributed to a different function.

`src/mainl/crt/_strxfrm.asm` recovers the two original multilevel collation
transformation routines. Their live interfaces include original far locale
pointer `__pLocale` and six near helper EXTDEFs; output-level handling,
character/key expansion and 16-bit reverse operations are instruction-level
symbolic source rather than native CODE byte arrays. Both members retain
their distinct empty third `COLLATE_TEXT`/`_STRXFRM_TEXT` CODE segments and
original one-member `_DATA` DGROUP (`08ff02`), unlike the standard BSS
layout. This is significant to the real native OMF and linker ownership.

**All original native bytes and ordered relocation fields now agree**:
- 435/435 and 382/382 complete CODE bytes;
- exact zero initialized DATA and zero-byte third CODE segments;
- all eight CODE publics, the exact seven `_strxfrm` imports, group/segment
  layout and 2/2 complete literal ordered fixups, including frames.

An important rejected initial assumption: `lds bx,dword ptr DGROUP:__pLocale`
produced *correct linked bytes* but the wrong OMF frame1 for the original
`_strxfrm` CODE+12 external far pointer. Expressing it naturally as
`lds bx,__pLocale` (the true typed external symbol) causes TASM to emit the
original target frame5, **without patching the object or inserting bytes**.
Register operand order also matters: two `xchg` operations had equivalent
instructions but different ModRM until reconstructed as `xchg al,ah` and
`xchg bl,bh`.

`build_th03_mainl_after73_work.py vprinter-collate-strxfrm` builds both
alongside the recovered `vprinter` boss atop the inherited 73-source
original native carrier. Two independent TASM/TLIB/TLINK rounds reproduce
the entire original Japanese **67,372-byte decoded MAINL EXE** and original
MAP (all **677 MZ relocations**). **76** source-built members reproduce
**32,824 original-equal CODE bytes**, while **817** contextual vendor member
program records stay unchanged. The new scope's **31/31 literal OMF FIXUPPs**
(29 `vprinter` and 2 `_strxfrm`) are original-frame/order identical. The
complete original native program-record serialization beyond these scoped
fields remains a separate claim; no new formal accepted-ledger credit is
claimed.

The source-bound OBJ/LIB/EXE/MAP vectors and writer phase logs are retained
under `.analysis/work/mainl-after73-vprinter-collate-strxfrm-*` and
`.analysis/work/after73-vprinter-collate-strxfrm-*`. Verify with
`review_th03_mainl_after73_work.py vprinter-collate-strxfrm` and
`tests.test_mainl_after73_work`. **No full cold replay** was performed.
