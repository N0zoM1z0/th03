# Original filebuf::attach descriptor, buffer and get/put setup — after443

The original Borland filebuf member fsbattch (Japanese CL.LIB index
**706**) is now maintained as natural [8086 source](../src/mainl/crt/fsbattch.asm).
This 238-byte far C++ member rejects a second attach, records the
provided DOS descriptor, conditionally allocates a 0x204-byte far work
buffer, registers ownership through streambuf::setb, then calculates
the native get/put window offsets and calls streambuf::setp and setg.
It preserves the exact original optional-allocation and zero-buffer
paths, parameter widths, 28-byte final stack cleanup, and far result
pointer. The branch through the original signed size comparison is not
normalized into a safer alternative.

The entire **238 CODE bytes** match the original; there are no
initialized DATA or BSS bytes. All four OMF relocation fields match
with the original symbolic calls (CODE+71: new array, +110: setb,
+185: setp, +219: setg), as do the exact segment/GROUP definitions,
imports and FAR public ABI. The literal FIXUPP chronology and full
program record serialization differ from the original Borland member,
which is explicitly **not** claimed to match in that stronger sense.
There are no target byte arrays or post-assembly binary patches.

The after443 producer verifies the complete inherited after442
650-source carrier and performs two independent native
TASM/TLIB/TLINK rounds, preserving all raw OBJ/LIB/EXE/MAP pairs,
writer logs and source hashes. Both complete 67,372-byte decoded
Japanese MAINL EXE and MAP are byte-for-byte original-equal, with
all 677 original ordered DOS MZ relocations. The working CRT advances
to **651/893** source-linked members and **175,516 CODE bytes**, leaving
**242 contextual vendor members**. No full cold replay or new formal
Factory accepted-source credit is implied.

Focused review:
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after443_work.py filebuf-attach-descriptor-boss
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after443_work -v
