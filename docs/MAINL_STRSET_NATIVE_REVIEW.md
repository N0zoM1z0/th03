# Original DOS strset: natural BCC4.5 source and 27-source MAINL

The maintained natural C++ translation unit
src/mainl/crt/strset.cpp reconstructs the complete original
46-byte large-model far-cdecl _strset in CRT member310. It
uses the original nested call of the real _setmem helper with
the length returned by far _strlen. Crucially the original
Borland expression evaluates arguments right-to-left: the
WORD character argument is already on the stack before the
far strlen call, then the result length and original far
destination are pushed for setmem. It returns the same
destination as a far DX:AX pointer.

Borland C++ 4.5 compiles this source to **all 46 original
CODE bytes**, the same one far public, original ordered
_ strlen and _setmem library imports (written _strlen
without whitespace in the actual object), empty DATA/BSS,
and original group 08ff02ff03. Both genuine four-byte
far CALL FIXUPPs agree literally in descending source order:
site29 external _setmem first, site15 external _strlen
second, using original TARGET-frame method5. This is
original high-level source semantics, not inline opcode
byte arrays or a modified binary.

This source is built and linked twice in the real original
893-member library along with the previous 26 exact source
units: full xx, the two large sorting functions, the
1282-byte scanner, source-built path searching srchstr,
strrev and the other CRT providers. All **866 other member
program records** remain original. The complete **67,372
byte Japanese decoded MAINL EXE and entire MAP** are
identical in both native BCC/TLIB/TLINK rounds; all
**677 MZ relocations** agree. **27 source units supply
18,265 exact original CODE bytes** simultaneously.

The accepted28-provider CRT and frozen211-owner MAINL
publication remain untouched. Source-exact working evidence
is not automatically accepted byte credit; the original
target is still candidate-local-attested. No full cold
or DIET replay was executed.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_strset_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_strset_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_strset_work

The original target, two full native OBJ/LIB/EXE/MAP raw
vectors, phase logs and bound source/build receipts are
retained under .analysis/work/strset-* and
mainl-strset-native-{build,review}.json.
