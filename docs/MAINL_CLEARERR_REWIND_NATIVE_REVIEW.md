# Original DOS clearerr and rewind: complete 42-source native link

The Borland DOS CRT source modules clearerr (member10) and rewind
(member279) are now maintained as real 8086 mnemonics at
src/mainl/crt/clearerr.asm and src/mainl/crt/rewind.asm.

The 17-byte far clearerr code clears the two original FILE error/EOF
flags using the original far stream pointer and never introduces new
FILE side effects. The 40-byte far rewind calls the genuine far
_fseek(stream,0L,SEEK_SET), then clears the original EOF flag only
after successful seeking. No generic libc emulation, extra guards,
NOP filler or binary patches are used.

Native TASM matches all **17+40 original CODE bytes** and the original
public symbol offsets, empty DATA/BSS, each original distinct GRPDEF,
real _fseek EXTDEF and its sole literal TARGET-framed OMF FIXUPP at
rewind CODE+17. clearerr has no native relocations. Both are original
source-code-reproduced objects, not length-only matches.

The scoped builder inherits the previously attested 40-source
original Japanese MAINL carrier with full xx, both qsort bosses,
scanner, stat, open, fread/fwrite and other native source CRT units.
It assembles the two new modules at their original positions inside
the original 893-member CRT library. The other **851 native CRT member
program records** remain unchanged. Both independent real
TASM/TLIB/TLINK rounds produce the entire original **67,372-byte
Japanese decoded MAINL EXE** and complete original MAP bit-for-bit,
including all **677 original MZ relocations**. Exact source-built CODE
in the working library totals **22,227 bytes from 42 source modules**.

The inherited fopen raw FIXUPP order and fclose near frame discrepancies
remain open in the working carrier. No formal accepted ledger promotion
is claimed for these working sources: the accepted28-provider CRT,
published211-owner MAINL ledger and original candidate-local-attested
targets remain unchanged. No full cold/DIET replay was run.

Affected-only validation:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_postopen_work.py clearerr-rewind
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_postopen_work.py clearerr-rewind
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_postopen_work
