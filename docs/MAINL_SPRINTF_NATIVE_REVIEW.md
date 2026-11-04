# MAINL original CRT `sprintf` / `vsprintf` source recovery

The original **Japanese** MAINL CRT member `sprintf` at index 287 is a 144-byte
CODE-only unit (three segments: 144 CODE / zero DATA / zero BSS) exporting
`_sprintf` at +69 and `_vsprintf` at +107. Its common nonpublic callback at
+0 copies a counted span using far `_memcpy`, updates the destination cursor,
and writes the trailing NUL. Both public far entry points delegate formatting
to the original near `__VPRINTER`; one supplies the varargs stack cursor and
one supplies the pre-existing `va_list` cursor.

`src/mainl/crt/sprintf.asm` is a complete **instruction-level source**, not
an original-byte initializer, object patch or a copy of the binary. TASM 5.0
`/m /mx /kh32768 /t` independently reassembles all 144 native CODE bytes,
both public positions, both EXTDEFs, all five relocation sites and targets,
and the original `_BSS,_DATA` group membership. The actual original CRT object
and membership are checked, not assumed from the extracted file alone.

The original compiler's FIXUPP record enumerates sites in descending order
`138,120,101,82,25`, whereas TASM emits ascending sites. For both near
`__VPRINTER` calls (+101 and +138), the original uses target frame5 and TASM
uses CODE frame0. Thus **the raw OMF relocation metadata is not byte-identical**;
logical near-call link results are verified independently. Do not promote this
as a literal native-OBJ or published source-ownership acceptance.

For the actual linked product, `build_th03_mainl_after62_work.py sprintf`
reuses the retained 62-source Japanese MAINL native carrier and creates two
independent Borland TASM/TLIB/TLINK OBJ/LIB/EXE/MAP rounds. Both rounds
reproduce the **entire original decoded 67,372-byte MAINL EXE and MAP** with
all 677 MZ relocations; 63 of the 893 library members now come from working
source, the other 830 are untouched. The source CODE total grows from 28,599
to **28,743** original-equal bytes (working source evidence, no added formal
accepted ledger bytes). Verification: `review_th03_mainl_after62_work.py sprintf`
and `tests.test_mainl_after62_work`; source and native phase logs are hash-bound
in the untracked `.analysis/work/mainl-after62-sprintf-*` proof set. No full
cold replay was performed.
