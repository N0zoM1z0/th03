# Japanese MAINL original `vprinter`: recovered 1,243-byte formatting boss

The selected original Borland large-model CRT `vprinter` is member **150**
of 893, exporting the near Pascal formatting engine `__VPRINTER` at original
CODE+24. It is the format-output core used by the recently recovered
`sprintf`/`vsprintf` wrappers. We rechecked the selected member's native
record identity, not merely a separate vendor object or old assumption.

The new working `src/mainl/crt/vprinter.asm` reconstructs the **entire 1,243
CODE / 103 initialized DATA / zero BSS** source. It comprises a small hexadecimal
emitter, the near formatting engine with its 80-byte stack output buffer,
a flush-to-callback path, width/precision parsing, signed/unsigned, string,
character, pointer and floating-format branches, and the real near conversion
helpers `__LONGTOA` and `__REALCVT`. The final 24-entry CODE switch table
contains actual symbolic `dw` label references, not original code bytes.
The initialized DATA holds the literal `(null)` string and a 96-byte
format-specifier classification lookup. Those are genuine named DATA values,
not machine-code arrays or an object patch.

During source recovery the original compiler's alternate encodings of
`xchg ah,al`, `xchg cx,di`, and `xchg cx,dx` were identified. Swapping
syntactically equivalent register operand orders reproduces the **exact
original instruction bytes**. Six prefixed `lods byte ptr es:[si]` instructions
are also restored with the correct explicit source segment rather than a
semantically different implicit DS access. Complete original control-flow
branch targets and the 24 switch destinations were checked, rather than
emitting an opaque executable byte array.

Native TASM 5.0 `/m /mx /kh32768 /t` emits:

- **1,243/1,243 whole CODE bytes** and **103/103 DATA bytes** identical to the
  selected original native CRT member;
- the original `_DATA,_BSS` group, `_TEXT/_DATA/_BSS` sizes, original
  CODE+24 public and ordered imports;
- **all 29/29 OMF FIXUPP fields in the original literal record order**, with
  identical locations, location types, targets, addends **and frame methods**.
  This includes 24 symbolic CODE jump-table fields, the classification table
  and null-string DATA references, and both external near converter calls.

`build_th03_mainl_after73_work.py vprinter` starts from the retained original
Japanese 73-source CRT and builds this one new member in two independent
native TASM/TLIB/TLINK rounds. The 893-member library preserves all **819
untouched vendor member program records**; the **full 67,372-byte decoded
Japanese MAINL EXE and original MAP match byte-for-byte**, including **677
original MZ relocations**. The working source CRT now has **74 members** and
**32,007 original-equal CODE bytes**. This *does not* claim full literal OMF
program-record identity, whole-source ownership, or new accepted-ledger credit.

Original and new raw OBJ/LIB/EXE/MAP rounds, writer logs and source-hash-bound
receipts are retained under `.analysis/work/mainl-after73-vprinter-*` and
`.analysis/work/after73-vprinter-*`. Verify via
`review_th03_mainl_after73_work.py vprinter` and
`tests.test_mainl_after73_work`. The unchanged original cold build was reused;
**no full cold replay** was performed.
