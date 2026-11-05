# MAINL CRT `_locking` — original DOS file locking boss (after389)

Source: `src/mainl/crt/locking.asm`. The original Japanese large-model
`CL.LIB` member **locking** (index 246) contains **310 CODE bytes**, an
unexported 96-byte near wait/time-rollover helper, and the public far `_locking`
entry at CODE+96. The exported method implements the original five-mode
lock/retry/unlock dispatch, including DOS file seeking, one-second waits and
the ten-attempt failure path. Its five-entry CODE-resident dispatch table at
CODE+300 is authored as `dw offset` labels, not binary payload.

The maintained assembler source exactly reproduces **all 310 original CODE
bytes**, original segment sizes (`_TEXT`/`_DATA`/`_BSS` = 310/0/0), the
public and five ordered imports (`__dos_lock`, `__dos_seek`, `__dos_unlock`,
`__dos_gettime`, `_errno`), and **all 16 logical OMF fixups** including their
actual frame methods, targets and addends. `_errno` accesses use genuine
DGROUP-relative fixups; the dispatch table has five relocatable code offsets
(249, 153, 220, 153, 220). No original bytes are inserted to force equality.

`PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_after389_work.py dos-file-locking-boss`
links **512/893** source-built CRT members with unchanged original context.
The source/driver/parent-bound receipt is
`.analysis/work/mainl-after389-dos-file-locking-boss-build.json`; the strict
reviewer is `scripts/review_th03_mainl_after389_work.py`. Both actual fresh
TASM/TLIB/TLINK rounds retained their full native OBJ/LIB/EXE/MAP and logs.
The decoded original Japanese **EXE (67,372 bytes, 677 MZ relocations) and
MAP both match byte-for-byte in each round** without a full cold replay.

**Exactness boundary:** The original Borland member's 16 FIXUPP records occur
in a different literal record order from TASM's output, although the complete
set including frame methods is identical. Consequently raw original OMF
member-program serialization is **not** claimed equal. The remaining vendor
members number 381, while the full game, original packed-member ownership and
Factory acceptance remain open. The increased working-source CRT count is not
an accepted-source or packed-file unit ledger increment.

Focused reproduction:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after389_work.py dos-file-locking-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after389_work -v
```
