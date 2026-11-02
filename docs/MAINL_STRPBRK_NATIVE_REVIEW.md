# Original DOS strpbrk: complete 80-byte far search and 22-source link

The maintained src/mainl/crt/strpbrk.asm is a natural 8086
reconstruction of original large-model far-cdecl CRT member307.
The real function loops over the far input string, resets a
four-byte SS local to the far accept-set pointer for each
character, compares the input byte first with each set byte,
then returns the first matching far input address in DX:AX.
On miss it returns 0000:0000. Both original ES:BX dereference
order and the original checked input/set termination control
flow are preserved without adding modern null/error guards.

The actual TASM5 source reproduces **all80 original CODE
bytes**, the one public _strpbrk at0, no native imports or
FIXUPPs, empty DATA/BSS and the literal original BSS-before-
DATA group 08ff03ff02. The source is not simply a reused
strspn object: it has different branches, pointer return,
local resets and segment-group identity. Real BCC4.5 C++
experiments that appeared semantically equivalent emitted
different code and non-original temporary storage; the final
mnemonic implementation retains the original 8086 behavior
without raw opcode arrays or object edits.

The scoped builder reassembles this source and the already
proved scantol/strspn/strcspn modules, inserts all four
at their real CRT slots alongside 18 preceding complete
source owners (including whole xx and both qsort bosses),
and retains **871 of893 original CRT member program records**
unchanged. Two actual TASM/TLIB/TLINK rounds independently
reproduce the full **67,372-byte Japanese decoded MAINL
EXE** and original MAP bit-for-bit with all **677 original
MZ relocation entries**. **22 simultaneous native source
modules account for 16,486 exact CODE bytes** in the isolated
working library.

The original accepted28-provider CRT and published211-owner
MAINL ledger are unchanged. This is exact source-only
reconstruction evidence, not newly credited formal accepted
bytes. No full cold/DIET replay was performed.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_native_extension_work.py scantol-strspn-strcspn-strpbrk
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_native_extension_work.py scantol-strspn-strcspn-strpbrk
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_native_extension_work

The two complete TASM OBJ/TLIB CRT/EXE/MAP vectors and bound
original source/driver/native command logs remain under
.analysis/work/native-extension-*.
