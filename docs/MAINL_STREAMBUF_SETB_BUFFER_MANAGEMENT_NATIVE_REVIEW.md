# Original streambuf::setb buffer management — after442

The original Japanese Borland member stbsetb (CL.LIB index **863**)
is now maintained as native [8086 source](../src/mainl/crt/stbsetb.asm).
The complete 176-byte far member function checks ownership of the
previous buffer, compares the old and incoming far pointers and only
releases a distinct owned buffer via the original far delete-array
function. It writes the new far buffer start and conditionally validated
end pointers, and retains the original null-buffer and ownership flag
decisions. This includes the original quirks in its range comparison;
it is not a defensive rewrite.

All **176 original CODE bytes** agree, with **zero DATA/BSS bytes**
and the exact public/import interface. Its sole OMF FIXUPP is the far
delete-array call at CODE+55; both the complete logical relocation and
its **literal record order** agree with the Japanese original. The
TASM-emitted full OMF module is not raw-record identical and that
stronger claim is not made.

After442 validates the retained 649-source after441 parent and runs
two fresh TASM/TLIB/TLINK rounds with source hashes, full writer logs
and raw OBJ/LIB/EXE/MAP pairs preserved. Both resulting decoded Japanese
MAINL EXE/MAP equal their targets, with all **677 ordered MZ relocations**.
The working CRT contains **650/893** original source-built members
(**175,278 source-built CODE bytes**), with 243 contextual vendor
members unchanged. No full cold replay or Factory acceptance is implied.

Focused checks:
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after442_work.py streambuf-setb-buffer-management
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after442_work -v
