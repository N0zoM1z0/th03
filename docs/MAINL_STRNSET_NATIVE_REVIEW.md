# Original DOS strnset: real bounded string fill, source exact

The maintained src/mainl/crt/strnset.cpp reconstructs the original
58-byte Borland DOS large-model far-cdecl counted string-set function.
The actual source uses far strlen to determine the existing string
length,keeps the shorter of that length and the caller's WORD limit,
then calls the genuine far setmem helper and returns the original
far destination. It retains the original length less than n comparison
order,which BCC4.5 turns into the original CMP DX,[BP+12]; JAE.
A reversed but mathematically equivalent comparison changes actual
opcodes and is not the retained source. The original parameter
is an INT WORD,not a character-sized ABI argument.

Two actual BCC4.5 native compilations each reproduce **all58 CODE
bytes** of the original vendor strnset.obj,with the original
far public _strnset,empty DATA/BSS and original DATA-before-BSS
GRPDEF. Both original runtime EXTDEF entries are preserved in their
literal order: _strlen and _setmem. Both **actual OMF FIXUPPs at
CODE offsets41 and12**,their field shapes,targets and writer order
are identical. No byte arrays,original object patches,synthetic
padding or changed unchecked behavior are involved.

The source-only native linker inherits the 15 verified real source
members including the entire 12622-byte xx exception/RTTI TU,
near/far memmove and both integer parsers. It compiles this new
strnset source twice at the original library member index306,
preserves all **877 other original member program records** in the
893-member CRT,and performs two genuine TLIB/TLINK rounds. Both
rounds reproduce the **entire 67,372-byte decoded Japanese MAINL
EXE** and original MAP byte-for-byte,including all677 MZ relocations.
The combined source-built original CODE extent now totals
**14,114 bytes** across16 source members.

This is verified exact source in the isolated working CRT,not
automatic acceptance into the repository's frozen211-owner MAINL
publication or28-provider accepted CRT. Original fixed targets,
source cold outputs and DIET stage remain unchanged.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_strnset_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_strnset_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_strnset_work

The two complete original-native BCC OBJ/LIB/EXE/MAP vectors,
phase logs and bound receipts are retained under
.analysis/work/strnset-* and mainl-strnset-native-{build,review}.json.
