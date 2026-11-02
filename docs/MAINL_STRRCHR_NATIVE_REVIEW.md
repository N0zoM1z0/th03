# Original DOS strrchr: complete far reverse search and 24-source MAINL

The new maintained original-8086 source
src/mainl/crt/strrchr.asm reconstructs all **77 bytes** of
Borland DOS large-model far-cdecl _strrchr at original
CRT library index308. It preserves the far _strlen call,
counts the string terminator as a searchable character,
then scans the far string backward with a four-byte stack
cursor, returning the last matching ES:BX address in DX:AX
or 0000:0000 if absent. The full original BP frame, return
convention and original unchecked pointer-offset arithmetic
are retained; no modern defensive null handling is added.

Native TASM5 generates all original **77 CODE bytes** and the
sole literal OMF relocation at site15: a 4-byte far target
with original **TARGET frame-method5**, external _strlen
index1 and zero addend. It also retains the one public
_strrchr at offset0, zero DATA/BSS and the exact original
BSS-before-DATA GRPDEF 08ff03ff02. The first experimental
assembly already matched CODE and the relocation, but produced
the opposite empty-segment group order. The maintained source
corrects that group order directly, without rewriting OMF.
These are actual mnemonic and symbolic source statements,
not embedded object bytes or an output binary patch.

The independent scoped source-only builder reuses the proven
23-member exact CRT carrier with the 1,282-byte scanner and its
128-byte initialized ASCII classification table, complete
exception/RTTI xx and two qsort bosses. Only this new member
is assembled and inserted in the original 893-member CRT;
the other **869 original native member program records remain
unchanged**. Two complete real TASM/TLIB/TLINK rounds reproduce
the **entire 67,372-byte Japanese decoded MAINL EXE**, the
complete original MAP and all **677 ordered MZ relocations**
bit-for-bit. The **24 exact source CRT modules** together
generate **17,845 original CODE bytes**.

The retained original accepted28-provider library, frozen
211-owner MAINL accepted ledger, fixed candidate-local-attested
Japanese target and original cold artifacts have not changed.
Source-only native exactness does not automatically publish
new formal accepted bytes. No full cold/DIET replay was run.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_postscanner_work.py strrchr
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_postscanner_work.py strrchr
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_postscanner_work

Retained private raw OBJ/LIB/EXE/MAP vectors and phase logs:
.analysis/work/mainl-postscanner-strrchr-{build,review}.json
and .analysis/work/postscanner-strrchr-*.
