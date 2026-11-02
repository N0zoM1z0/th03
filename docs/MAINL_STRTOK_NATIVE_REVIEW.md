# Recovering the original DOS stateful strtok with native Borland C++ codegen

The new maintained src/mainl/crt/strtok.cpp is a natural Borland C++4.5
source implementation of the original DOS large-model tokenizer.
It contains two real delimiter loops and a persistent four-byte far
cursor in uninitialized BSS. It returns null at the end,otherwise
retains the original token start and sets the terminating delimiter
byte to zero. It does not introduce reentrant data structures,
null-pointer guards not in the target,or function-byte arrays.

Original static ownership is _TEXT203, _DATA0 and _BSS4, with one
far public _strtok and the literal DATA-before-BSS GRPDEF 08ff02ff03.
The original native OMF has **twelve ordered word relocation fields**
against that BSS cursor;these are NOT sorted or normalized in validation.

An initial direct TASM source matched all 203 bytes but emitted the
twelve relocations in ascending order and the group in the opposite
order,so it was NOT accepted. An ordinary Borland C++ for-loop produced
216 bytes and 13 fields;refactoring to the original structured
delimiter scanning loops reduced it to 207 bytes. The remaining
four-byte LES reload occurred when writing *next_token after a
comparison that had already loaded its far address into ES:BX.
Using the typed Borland MK_FP(_ES,_BX) pseudo-register pointer for
that write preserves the source's real far pointer semantics and
emits the original single MOV byte ptr ES:[BX],0. This restores
**all 203 original CODE bytes and all twelve native OMF fields**
with the original group and BSS,not by any binary patch.

The separate scoped build uses the original BCC4.5 native object
recipe,then combines this new original source object with the nine
already reviewed real source CRT members (the entire xx exception/
RTTI bank, seven memory/string helpers,and strstr). Both complete
TASM/BCC/TLIB/TLINK rounds reproduce the full **67,372-byte decoded
Japanese MAINL** and the entire MAP byte-for-byte,including 677
original MZ relocations. All ten original source member positions
are retained;the other **883 of893 real native member program records**
remain unchanged. The simultaneous source CODE scope is **13,262 bytes**.
The retained fixed targets, cold pair, accepted28-provider normal
CRT and211-owner publication are not overwritten.

This is bounded source-exact working evidence, not new published
accepted credit: both receipts report source_acceptance=false and
added_accepted_bytes=0. No full cold,DIET or ancestor replay ran.

Focused reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_strtok_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_strtok_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_strtok_work

Private actual original/compiled OBJ pairs, BCC/TLIB/TLINK phase logs,
response files and complete retained source-linked raw results live
under .analysis/work/strtok-* and mainl-strtok-native-{build,review}.json.
