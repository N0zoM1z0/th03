# Ellen full bomb controller: restore original CODE-vs-BSS ownership and native C++ (after653)

The original `b_ellen` physical TU contributes three complete functions:
bomb particle update (280 CODE bytes), particle renderer (163 bytes),
and the long palette/screen/particle effect (580 bytes). This is
**1,023 original CODE bytes** linked from `MAIN_05_TEXT`.

The live maintained `bomb_ellen.cpp` has a conditional original
physical storage view. The first v2 forced-current-source compile
`af653a` **did not reproduce the original object**, despite
both versions having 1,023 CODE bytes, 116 fixups and identical PUBLIC
offsets. The new native object incorrectly had **132 bytes of BSS**
because its private globals were allocated a second time. The
original physically linked `b_ellen` CODE producer has **zero private
BSS**. Its 18 different 16-bit addresses/addends originate in that
duplicated private storage, not changed gameplay logic.

The correctly sourced original compiler wrapper now specifies
`TH03_BOMB_EXTERNAL_STORAGE`, making the 132 historical
bytes a separately owned frozen external carrier. With that
original ABI, the fresh `af653b` control produces **exact original
CODE, fixups, PUBLIC offsets, segments, full MAIN executable and MAP**.
The v2 wrapper verifies the actual native OMF COMENT source path.
This corrects a tangible false ownership hypothesis rather than
repinning old receipts or copying original objects.

Maintained natural C++ recovery after correcting the ABI:

- The long three-stage `ellen_bomb` palette/shake routine's
  first/second-frame sound pulse is expressed as
  `(static_cast<unsigned int>(frame) % 2) != 0`, with original
  native codegen (`af653c`).
- Eight 8-byte particles per player use a checked **128-byte
  physical two-player array**, +04 velocity word-pair offset,
  and an original 132-byte external carrier (array + 2-byte count
  + 2-byte pointer).
- Physical sentinels 19999 (unspawned) and 9999 (respawn requested),
  first 64-frame palette stage, next 64-frame shake/particle stage
  and every-four-frame explosion cadence have distinct compiler-time
  meanings without extra runtime data.
- The original `goto respawn` must remain. A structured
  fallthrough candidate (`af653e`) changed actual 16-bit branch
  bytes. A natural `frame % 4 < 2` shake replacement
  (`af653d`) likewise differed, so the original `frame & 3`
  comparison remains. These original-unequal negative controls
  were *not* accepted as success.

Final original compiler plus linker verification:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af653g --units b_ellen
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af653g

Both independent original Turbo C++ 4.02 compiler/TLINK rounds
reproduce **all 1,023 original CODE bytes, 116 literal ordered
FIXUPP fields, three PUBLIC offsets and original BSS=0 segment
definitions**, the complete normal MAIN executable and
path-normalized MAP. Both original Japanese program images,
1,553 ordered MZ relocations and separately serialized
130,882-byte original Japanese MAIN.EXE match.

Retained native evidence:
`.analysis/work/exatt-layout-af653g/report.json`,
SHA-256 `427ea575785cf475fbee6e1294262f5c33d150e08c6b07bd115f856d88f0eee9`.
Two full compiler/linker rounds, staged consumed source,
original and candidate objects, response files, EXEs/MAPs,
and all writer logs are retained. Other 98 original project
objects and CRT libraries were not recompiled. This was
**not** a cold replay of the whole game.

These were already source-owned original target CODE bytes.
No new canonical packed-game Factory credit, raw historical
vendor OMF packet identity or physical PC-98 runtime
behavior is claimed.
