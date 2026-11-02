# Original DOS getenv: 112-byte far environment scan and 60-source MAINL

The original Borland DOS getenv CRT member240 now has real maintained
8086 source in src/mainl/crt/getenv.asm. It examines the caller's
far string pointer, computes its length using actual REPNE SCASB,
walks the far pointer vector at the native __environ symbol,
checks the original NAME=VALUE separator and uses REP(E) CMPSB
with saved/restored DS to return the original far value pointer
in DX:AX. No host-language environment substitute, added guards,
changed DOS codepage or synthetic binary patches are present.

The real TASM 5.0 output reproduces **all 112 original CODE bytes**,
the one far _getenv public at offset0, the single native
__environ TARGET-framed OMF fixup at CODE+35, original EXTDEF
order and zero DATA/BSS group 08ff03ff02. Both original
source register encodings and the entire far traversal loop match.

An important assembler syntax trap was resolved by native trials.
TASM initially rejected the original PUSH DS / POP DS operands
under the active ASSUME DS:DGROUP (reporting "Illegal indexing
mode" at both instructions). A scoped, **zero-byte**
ASSUME DS:NOTHING around the actual save/restore pair allows
the original instructions without emitting any helper bytes.
The assembler also chose the other equally valid XCHG encoding;
writing XCHG CX,BX in source restores the exact original
XCHG opcode/modrm bytes instead of just equivalent semantics.
No raw machine-code DB directives are used.

The scoped native library now contains **60 authentic source CRT
members**, including this getenv at its original slot240,
the 202-byte lsearch/lfind module, the four-segment tzset/ISDST
boss, both qsort algorithms, full xx and DOS streams/formatting
modules. **833 other original vendor member program records**
remain unchanged. Two actual TASM/TLIB/TLINK rounds reproduce
the complete **67,372-byte Japanese decoded MAINL EXE and
entire native MAP bit-for-bit**, preserving all **677 original
MZ relocation entries**. The simultaneous exact source-built
working CODE extent reaches **28,525 bytes**.

Older original OMF metadata differences in fopen/fclose,
_timecvt/strftime/tempnam stay explicitly OPEN in their
separate members. The formally accepted28-provider CRT,
211-owner MAINL ledger, original candidate-local-attested
Japanese target and retained cold pair are unchanged. No
formal accepted byte promotion, full cold replay or DIET
repacking is claimed.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_posttzset_work.py lsearch-getenv
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_posttzset_work.py lsearch-getenv
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_posttzset_work

Two entire native source OBJ/LIB/EXE/MAP vectors and actual
tool command logs are under .analysis/work/posttzset-lsearch-getenv-*.
