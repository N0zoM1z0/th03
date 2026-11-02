# Original DOS unsigned long scanner: natural BCC4.5 strtoul source

The new maintained C++ source at src/mainl/crt/strtoul.cpp reconstructs the
complete **231-byte** original Borland DOS large-model native strtoul
translation unit. This is not a one-function leaf:the object has two
private near input/unget callbacks (offsets0/41),a far public _strtoul
entry at offset56 and a complex parser adapter that delegates to the
original __scantol library provider. The original import order
_errno, __ctype, __scantol and all **six literal OMF fields** are
retained exactly. All 231 CODE bytes,empty DATA/BSS and actual GRPDEF
match the fixed Japanese vendor object without any binary patching.

Recovery required checking the real original machine code,not trusting
an assumed C library implementation. The callbacks use a far cursor
pointer with near function entries;unreadChar has a leading unused
character argument,which shifts its cursor argument to BP+6.
The native scanner passes far pointers to two near-stack output locals,
preserving both PUSH SS operands and the full 20-byte cdecl argument
area. Whitespace lookup uses the original signed-char index into
__ctype, then errno, the callback pair,radix and overflow status
follow original control flow. Changing the import declaration order
restores the original EXTDEF numbering.

A nearly exact variant differed at one instruction (OR DX,DX instead
of OR AX,AX). BCC's register int variable plus the _AX pseudo-register
condition preserves the actual 16-bit return register while allowing
the value to stay live in DX for the second return arm. This generates
the complete original prologue,conditional return,near callback and
subsequent public function at its true offset. No fake alignment bytes,
original object bytes embedded in source or rewritten OMF fixups.

The scoped producer adds only this new native BCC source object to the
ten already independently verified source CRT units (complete xx,
seven memory/string helpers,strstr and stateful strtok). It retains
original index315 for strtoul and preserves the other **882 of893
library program records** unchanged. Two actual isolated BCC/TLIB/TLINK
rounds reproduce the entire **67,372-byte decoded Japanese MAINL EXE**
and complete original MAP byte-for-byte,including all677 MZ relocations.
The simultaneous source-built native CODE scope totals **13,493 bytes**.

This is a proven working original-source replacement,not an automatic
promotion of the accepted211-owner MAINL ledger. The original
28-provider CRT library,all prior cold outputs and the pinned Japanese
target remain untouched. No full cold replay,DIET stage or ancestor
runtime pipeline was rerun.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_strtoul_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_strtoul_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_strtoul_work

Actual unchanged compiler input hashes,all native writer logs,two
complete raw OBJ/LIB/EXE/MAP vectors and independent review are
retained under .analysis/work/strtoul-* and
mainl-strtoul-native-{build,review}.json.
