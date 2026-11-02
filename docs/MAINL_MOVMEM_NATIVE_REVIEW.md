# Native original DOS movmem / memmove overlapping-copy member

The maintained 8086 TASM source src/mainl/crt/movmem.asm reconstructs
the original **119-byte DOS large-model CRT object** at member index266.
It includes two real far public entries: _movmem at offset0 and
_memmove at offset82. The original near arithmetic helper import
N_PCMP@ and its **one literal OMF relocation** match in the complete
native object,including the original CODE/DATA/BSS ownership and
BSS-before-DATA group record.

The helper compares original far pointers,selects direction with CLD
or STD,correctly handles overlapping source/destination and odd
addresses with MOVSB/MOVSW,and always clears DF before returning.
The _memmove wrapper passes its five near-stack WORD parameters via
PUSH CS / a genuine near CALL and returns the original destination
in DX:AX. This retains the full original 16-bit near/far calling
conventions and unchecked behavior. No original target-byte table,
object patch or synthetic padding is present.

The native expansion builder independently compiled strncpy49 and
movmem119 as ordinary TASM translation units and linked them with
the previously verified full xx and ten other DOS CRT source objects,
preserving **879 other original library programs of893**. Two
TASM/TLIB/TLINK rounds reproduce the entire original **67,372-byte
Japanese decoded MAINL EXE** and full original MAP byte-for-byte,
including all **677 MZ relocation entries**. The combined native
source CODE segment coverage is **13,951 bytes**.

Original accepted28-provider CRT library,formal211-owner publication,
cold artifacts and Japanese targets are unchanged;this is verified
source-only native reconstruction,not new accepted-ledger credit.
No full cold/DIET or ancestor runtime replay was performed.

Focused reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_crt_expand_work.py strncpy-movmem
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_crt_expand_work.py strncpy-movmem
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_crt_expand_work

Retained original/source native OBJ/LIB/EXE/MAP pairs,phase logs and
source-bound build/review receipts are under
.analysis/work/crt-next-strncpy-movmem-* and
mainl-crt-expand-strncpy-movmem-{build,review}.json.
