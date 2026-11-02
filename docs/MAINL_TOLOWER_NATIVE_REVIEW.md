# Full original DOS tolower: 48-byte source and 62-source Japanese MAINL

The original Borland DOS large-model far-cdecl tolower at CRT member131
is now maintained as real 8086 source in src/mainl/crt/tolower.asm.
It preserves the original signed EOF (-1) case, obtains the input
byte from DX:AL, uses the actual native __ctype character-class table
to test the uppercase flag, and adds 0x20 only for qualifying bytes.
It retains the original 16-bit register/stack convention and far AX
return, without substituting host C locale handling or modern guards.

Actual TASM5 source emits **all 48 original CODE bytes**, the
original far _tolower PUBLIC at0, the real native __ctype EXTDEF,
and its single exact original **GROUP-frame** byte-table FIXUPP
at CODE+26 with +1 addend. The original empty DATA/BSS and literal
DATA-before-BSS group 08ff02ff03 are preserved. No embedded
original opcode bytes, object rewriters, synthetic NOPs or
register-encoding approximations are used.

The scoped source-only builder replaces the real original
member131 alongside 61 preceding original CRT source modules,
including the large tzset/ISDST native four-segment runtime,
lsearch/lfind, getenv and original far access C wrapper.
**831 of893 original member program records remain untouched**.
Both genuine TASM/BCC/TLIB/TLINK rounds reproduce the entire
**67,372-byte original decoded Japanese MAINL EXE and complete
MAP bit-for-bit** with all **677 original DOS MZ relocations**.
The simultaneous working library now contains **62 true source
CRT modules generating 28,599 original CODE bytes**.

Earlier raw OMF differences in the separate fopen, fclose,
timecvt, strftime and tempnam modules remain explicitly
OPEN. This tolower object itself is byte exact in complete
CODE, symbolic imports, public, OMF field and segment group.
The fixed Japanese target, accepted28-provider CRT, formally
published211-owner MAINL ledger and retained cold pair are
unchanged. No newly credited accepted bytes, full cold replay
or DIET repacking.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_posttzset_work.py lsearch-getenv-access-tolower
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_posttzset_work.py lsearch-getenv-access-tolower
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_posttzset_work

Complete two-round native original OBJ/LIB/EXE/MAP vectors and
real Borland writer phase logs are retained under
.analysis/work/posttzset-lsearch-getenv-access-tolower-*.
