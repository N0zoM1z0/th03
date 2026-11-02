# Original DOS strstr, full native source and nine-member CRT link

The original Borland large-model strstr is now a maintained 8086 source
translation unit at src/mainl/crt/strstr.asm. It does NOT embed CODE bytes
or patch an object. The implementation preserves both far string scans,
the needle-empty return, the original DS/ES swaps and counted REPNE SCASB
/ REPE CMPSB search. The target deliberately uses BP for a temporary
after saving the caller frame, and it uses particular equivalent XCHG
operand orders. Actual TASM compilation confirmed four XCHG opcode
differences before correcting those operand orders in source.

The recovered function produces **all 108 original CODE bytes**
identically, the same public _strstr, empty DATA/BSS segments, literal
08ff03ff02 BSS/DATA GRPDEF, no imported symbols and zero literal OMF
fixups. Both CODE and source/target segment/public ownership are checked.

The scoped source producer reuses the two previously proven native
objects for all eight existing source members, including the complete
12,622-byte xx exception/RTTI unit, then assembles strstr twice
and reassembles the CRT library at original 893-member order.
The nine source members occupy their genuine old slots, including
strstr at zero-based index 312. The other 884 original member program
records remain untouched. **13,059 original CODE-segment bytes**
come from these nine independently compiled native sources.

Both real TLIB/TLINK rounds produce the full **67,372-byte decoded
Japanese MAINL EXE**, all **677 MZ relocations** and the entire original
MAP byte-for-byte. No full cold replay, DIET repack, patching of target
objects or changes to other game source modules were required.

The accepted28-provider CRT library and formal211-owner MAINL publication
remain separate and unchanged. This is a reproducible source-exact
working library, NOT a claim of published accepted byte credit.

Focused reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_strstr_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_strstr_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_strstr_work

Private build/review receipts, the two complete raw native rounds and
Borland phase logs are retained under .analysis/work/strstr-* and
mainl-strstr-native-{build,review}.json.
