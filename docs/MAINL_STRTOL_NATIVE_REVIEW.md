# Recover the original 290-byte DOS signed long parser

The new maintained src/mainl/crt/strtol.cpp reconstructs the original
Borland C++ 4.5 large-model native strtol,not a retrofitted modern
implementation. It has **290 CODE bytes**,two private near input/unget
callbacks at0/41 and a far public _strtol at offset56. It imports
_errno, __ctype and __scantol in their genuine original order;all
**seven original literal OMF fields** agree as an ordered list,not
just equal counts. The source has original empty DATA/BSS extents
and unchanged segment group ownership.

Beyond whitespace scanning and the scanner callback ABI, the signed
parser implements actual leading minus detection, status/errno
handling, 32-bit signed overflow checks and the original INT32
minimum/maximum clamp. It preserves the near-stack far pointer
parameters consumed by __scantol. This is a substantial control-flow
reconstruction rather than a small wrapper.

Actual compiler investigations found that a direct char read after
the whitespace loop was optimized into a cached BP[-12] local,
making a12-byte frame instead of the original10-byte frame.
Using a volatile signed-char far read restored the10-byte frame,
but BCC reloaded the far ES segment,leaving one wrong opcode:
LES BX versus the original MOV BX. A typed address expression
using MK_FP(_ES,FP_OFF(text)) forces the correct original segment
reuse, without a hardcoded address or object-byte patch. In the
final maintained C++ source BCC4.5 generates all290 original CODE
bytes and seven OMF fields,including the original sign test and
signed-clamp branches. The earlier 290-byte almost-match is
retained only as a private diagnostic.

The scoped normal-link producer inherits the previously proved
eleven-source native working library (complete xx,seven DOS
memory/string CRTs,strstr,strtok,strtoul),then compiles strtol twice
and links all **12** source objects at their original native library
positions. The remaining **881 of893 original member program records**
stay unmodified. Two full real BCC/TLIB/TLINK rounds independently
reproduce the **complete 67,372-byte Japanese decoded MAINL EXE**
and MAP byte-for-byte,with all **677 original MZ relocations**.
This demonstrates **13,783 cumulative native source CODE bytes**
in one exact source-only library,not an invented credit count.

The original accepted28-provider CRT library,211-owner publication,
pinned Japanese target and complete retained cold pair are unchanged.
No cold/DIET or ancestor runtime chain was rerun. These are genuine
natural-source reconstruction artifacts,not yet formally promoted
accepted ledger units;the explicit reports still say
source_acceptance=false and added_accepted_bytes=0.

Affected-only commands:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_strtol_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_strtol_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_strtol_work

The complete two BCC OBJ/TLIB/TLINK output pairs,phase logs and
source-bound build/review receipts remain under
.analysis/work/strtol-* and mainl-strtol-native-{build,review}.json.
