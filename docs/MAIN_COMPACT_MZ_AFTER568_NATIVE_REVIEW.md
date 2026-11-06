# MAIN original MZ file — source-derived compact DOS container after568

## Why the native link still differed

The after567 link used ten source-native objects together: nine major
BOSS C++ TUs and the natural MAIN input-scan TASM object. Both native
TLINK rounds produce the complete original 124,642-byte Japanese game
load image and the entire original ordered 1,553-entry MZ relocation table.
However, the normal Turbo Link 6.10 MZ output is **132,322 bytes**, while
the pinned Japanese MZ is **130,882 bytes**.

Independent binary-header inspection isolates the remaining difference
strictly to the DOS MZ container layout. Modern TLINK writes its relocation
table at decimal offset 62 (hex 3E) and reserves
480 paragraphs of header. Its relocation data ends at byte 6,274 and is
followed by **1,406 zeros** before the program. The Japanese original uses
the standard 28-byte DOS MZ fixed header (hex 1C) and stores all 1,553
relocations immediately after it:

    28 + 4 * 1553 = 6240 = 390 * 16

This is already paragraph aligned, so no padding is needed. Both
relocation streams are literally equal and their full original order agrees.

## Reconstructing format rather than fixing machine code

The independent pure Python serializer in scripts/lib/main_mz_compact.py
accepts **only the native TLINK file**, never the Japanese target. It
reads all fourteen original native DOS header values and the program
image using the repository's existing MZ parser, then computes the four
format-dependent page count/last-page/header-paragraph/relocation-pointer
fields according to the standard DOS MZ format. It serializes every
original native relocation (offset, segment) in native source order and
appends the unchanged program image.

The two after567 native EXEs were independently reconstructed as compact
MZ files. **Both complete 130,882-byte outputs are byte-for-byte identical
to the pinned Japanese original**, including all header bytes, all
relocations and all machine code. SHA-256 matches exactly, with no target
bytes embedded in the serializer and no file/object overwrite of the
original compiler/linker output.

A strict negative control runs the *same* serializer on the older
source-native MAIN EXE whose input scanner still lacked the EC2D 90h CODE
alignment. Its compact MZ retains that wrong image byte and **does not**
match the original. Thus the format serializer does not mask a code error:
the separate natural TASM source step supplies the true CODE byte, and
the container serializer solely supplies the original DOS file layout.

## Provenance and acceptance limits

This validates **a reproducible, source-derived complete original MZ
file**, not the exact original vendor linker executable, linker flags,
or compiler identity. The direct Turbo Link 6.10 file remains different
and is preserved. The compact program is a *separate, explicit post-link
format stage* and not a target-byte patch, a DIET repack or an additional
source owner. This stage does **not** republish canonical Factory unit
acceptance or assume complete original authored-game source ownership.

Read-only native evidence check:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_main_compact_mz_after568_work.py

Builder: scripts/build_th03_main_compact_mz_after568_work.py
Stage: .analysis/work/main-compact-after568-native-build.json
Review: .analysis/work/main-compact-after568-native-review.json
Both complete alternate MZ files and the original after567 OBJ/EXE/MAP
rounds are retained. No full cold replay, runtime model or original file
byte edits were performed.
