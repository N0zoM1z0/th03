# Original native strnset and sixteen simultaneous MAINL source members

The original large-model DOS strnset is now maintained as natural
Borland C++ 4.5 source in src/mainl/crt/strnset.cpp. Its bounded fill
first calls the actual far strlen provider, clamps the requested
character count to the observed length, then calls the real _setmem
far CRT helper and returns its unchanged destination far pointer.
The original character argument is a WORD int;changing it to an
8-bit formal changes the compiler output.

The source reproduces all **58 original CODE bytes**, the original
one public _strnset, zero DATA/BSS, DATA-before-BSS GRPDEF and all
**two literal ordered OMF far-call fields**, to _strlen and _setmem.
Alternative syntax and parameter types were actually compiled:
several superficially equivalent ternaries and reversed comparisons
changed the object. The selected natural C++ therefore follows
original code generation without byte tables or binary modifications.

The scoped native producer inherits fifteen exact source CRT objects
including complete xx, natural signed/unsigned parsers, tokenizer,
overlap-safe movmem and bounded strncat;then compiles strnset using
real BCC4.5 and replaces precisely original library slot306 in the
893-member MAINL CRT. **All 877 other original member program
records remain byte-identical**. Two independent native BCC/TLIB/TLINK
rounds generate the complete **67,372-byte Japanese decoded MAINL EXE**
and its original MAP raw-equal, including **677 original MZ relocations**.
The simultaneous source-built CODE total is now **14,114 bytes**.

No full cold or DIET replay was performed. The accepted 28-provider CRT
library and published 211-owner MAINL ledger remain frozen: this is
true source-only reconstruction evidence, *not newly credited accepted
bytes*. The target still has candidate-local-attested provenance.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_strnset_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_strnset_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_strnset_work

The private .analysis/work/strnset-roundN-* native raw vectors, phase
logs and source-bound receipts are retained for independent review.
