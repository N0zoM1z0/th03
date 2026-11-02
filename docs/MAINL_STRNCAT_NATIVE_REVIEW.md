# Original DOS strncat: two strlen calls and a real far movmem

The maintained src/mainl/crt/strncat.cpp is natural Borland C++ 4.5
large-model source for the complete original **105-byte** CRT object.
It contains two genuine far strlen calls,clamps copy length to count,
calls the original far movmem with a source and destination pointer
plus WORD count,writes the terminating NUL and returns the destination.
The original import order _strlen, _movmem, and the **three literal
ordered OMF far fixups** match at CODE sites71/31/15. No target
machine-code array,caller model,padding or patched object was used.

The first C++ version produced108 instead of105 bytes: BCC reloaded
the saved second strlen result from BP[-2] before comparing it to the
length limit,adding an extra MOV AX,[BP-2]. Declaring the actual locals
in the original order and assigning strlen(source) inside the
comparison preserves the return value in AX and original stack slots,
restoring all105 CODE bytes and all3 native OMF fields.

The scoped builder reuses the exact fourteen-source CRT library (the
complete xx,seven original memory/string CRTs,strstr,strtok,strtoul,
strtol,strncpy and overlap-safe movmem). Only strncat is compiled.
Two actual BCC/TLIB/TLINK rounds place **15 genuine original source
members** in their old positions among893,keeping the other **878
native member programs** unchanged. Both produce the complete
**67,372-byte original Japanese decoded MAINL EXE** and MAP
byte-for-byte,including all677 MZ relocations. Total exact
native source CODE scope is **14,056 bytes**.

The previous accepted28-source CRT,211-owner MAINL publication,pinned
Japanese targets and cold pipeline remain unchanged. This is exact
native working source evidence,not new formally accepted credit.
No full cold or DIET recompression was performed.

Focused reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_strncat_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_strncat_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_strncat_work

All native source,OBJ/LIB/EXE/MAP raw pairs,logs and reviews are
retained under .analysis/work/strncat-*.
