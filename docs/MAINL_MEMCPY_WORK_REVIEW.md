# MAINL original DOS memcpy source and native carrier

The maintained `src/mainl/crt/memcpy.asm` reconstructs the **36-byte** DOS
large-model `_memcpy` from the pinned Japanese MAINL library member. It is a
real, independent 8086 TASM translation unit, not a copied byte array or an
object-file patch. The function uses a far cdecl frame: two far pointers and
one WORD count, forward CLD / REP MOVSW, one conditional trailing MOVSB,
DS restoration and the original far DX:AX destination return. The original
unchecked behavior is preserved. DATA and BSS are genuine empty segments.

Native `TASM32 /m /mx /kh32768 /t` produces the complete **same 36 CODE
bytes** and zero relocation fields. Both OMF objects have the same three
segment extents and one public `_memcpy`, with no external imports. The
object wrappers and assembler metadata differ, so the proof compares the
complete native semantic extents and actual relocation vectors, not raw OBJ
file identity.

`build_th03_mainl_memcpy_work.py` validates and reuses the unchanged current
MAINL cold pair and accepted library. It extracts all **893 original library
members**, verifies their preserved program records and replaces only the
`memcpy` member at index261 (zero-based). The other 892 remain byte-record
identical. TLIB/TLINK preserve the native member order and all36 existing
project objects and pinned startup/runtime inputs. Two serialized native
TASM/TLIB/TLINK rounds reproduce complete raw OBJ/LIB/EXE/MAP vectors. Both
rounds link an EXE **byte-identical to the 67,372-byte decoded Japanese target**
and a **byte-identical original MAP**, without refreshing the accepted cold
pair or running an ancestor runtime chain. The independent retained-pair
reviewer rechecks all outputs, actual phase logs, source hashes, original
member contents and library membership.

This is a **source-present, scoped native-exact vendor replacement**. It is
not automatically an additional accepted authored unit: the maintained
211-owner MAINL publication, 28-provider accepted source library, and
whole-game source-ownership claims remain unchanged. The pinned target has
`candidate-local-attested` provenance. The diagnostic build uses a private
alternate library; it never overwrites the accepted working library.

Focused replay:

```sh
PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_memcpy_work.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_memcpy_work.py
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_memcpy_work
```

Retain `.analysis/work/mainl-memcpy-{build,review}.json`, the two complete
`memcpy-roundN-*` raw vectors, native phase logs, and the actual emitted source
and response files. Do not repeat an unchanged native pair just to validate
a downstream document change.
