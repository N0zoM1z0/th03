# Correcting a real source hypothesis: the MAINL continue menu CODE segment

The existing maintained src/mainl/root/continue.cpp compiled all 417 original
machine-code bytes and all 35 literal original ordered OMF FIXUPP fields for
mainl_continue_menu, but its Borland source declared the segment
CONTINUE_TEXT. Independent native object analysis proved the *actual*
original contmenu.obj segment is CUTSCENE_TEXT. Earlier source notes had
treated the old maintained file as complete; this was a falsified source
assumption, not merely a diagnostic name difference.

An actual negative experiment compiled the historical source unchanged,
with its wrong CONTINUE_TEXT segment. Every original function instruction
and OMF reference matched, but normal TLINK then emitted an incorrect
MAINL EXE with **696 MZ relocations**, versus the Japanese original's
**677**. It differed across the linked program and relocation table.

The new maintained natural C++ source
src/mainl/root/continue_cutscene_text.cpp differs from that historical
source in **exactly one Borland pragma**: the proper segment declaration
CUTSCENE_TEXT. It does not alter the function's logic, stack handling,
input behavior, code bytes, or unchecked failure semantics. The historical
original source stays unchanged so old published source/receipt hashes
remain valid. A new, small first-use wrapper
src/mainl/root/continue_producer.cpp makes the corrected TU explicit.

The same genuine original GAME=3/BINARY='L' Turbo C++ profile produces
the entire original 417-byte CODE body, ordered 35 OMF references, near
PUBLIC entry and correct segment. The exact original CODE, PUBLIC and FIXUPP
identities were separately established for both the wrong and right
segment experiments. Their different results confirm the critical role
of section grouping in real-mode executable layout.

**Two fresh independent compiler/linker rounds** now replace this one
corrected contmenu.obj in the after583 source-native MAINL link. Both
complete **67,372-byte Japanese decoded EXEs** and all **677 ordered MZ
relocations** match the Japanese original byte-for-byte, with original
MAP segment names and contribution coordinates. The other 35 project
objects and C0/CRT library remain unchanged.

Preserved diagnostic negative control:
TH03ML/probe/af584cont-try/old and /fixed; both native compiler objects,
normal link responses, EXEs and writer logs remain untouched.

Read-only review:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_mainl_continue_after584_work.py

Driver: scripts/build_th03_mainl_continue_after584_work.py
Build receipt: .analysis/work/mainl-continue-after584-native-build.json
Review: .analysis/work/mainl-continue-after584-native-review.json

This source correction is substantial *layout fidelity*, not a new function
entry or canonical Factory source credit. Complete vendor OMF packet identity,
packed-file acceptance and whole-project source ownership are still separate.
