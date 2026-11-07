# Original MAIN results, shots and HUD animation: combined native C++ link

Three distinct complete natural 16-bit C++ source producers were tested
together rather than checking only small leaf functions:

| Original source module | Real implemented behavior | Original CODE | PUBLICs | Ordered fixups |
| --- | --- | ---: | ---: | ---: |
| results.cpp | Round reset, result scoreboard and numeric rendering | 1,060 | 3 | 89 |
| shots.cpp | Player shot creation, per-frame update and render | 449 | 3 | 17 |
| intro.cpp | HUD start animation, particles, sprites and stage intro | 1,478 | 4 | 145 |
| Total | Three complete first-use C++ producers | 2,987 | 10 | 251 |

New small source-first-use wrappers under src/main/round/producers,
src/main/player/producers and src/main/hud/producers include the original
unchanged natural C++ code, including its original local Borland
segment/packing/optimization directives. There are no opcode-byte arrays,
manual linker byte edits or novel error-handling changes.

In the first real native trial, three genuine Turbo C++ 4.02
GAME=3/BINARY='M' objects matched the original entire initialized CODE,
all original ordered OMF literal fixups and original PUBLIC/segment
definitions. Replacing all three objects simultaneously into the native
after594 MAIN link produced the identical full EXE and original MAP
geometry. Two independent source-native compilation and normal link
rounds then repeated that result from fresh source staging.

The resulting 132,322-byte direct TLINK file remains equal to the
previous source-native complete MAIN. Its 124,642-byte loaded original
Japanese program and all 1,553 original ordered MZ relocations agree.
A separate, previously reviewed standard DOS MZ container serializer
reconstructs the **entire original 130,882-byte Japanese MAIN.EXE**
byte-for-byte in both independently compiled rounds. The separate file
format step is not claimed to be the original historical TLINK output.

This source-backed chain also contains nine major BOSSes, the full
bullet/fireball/collision sources, character resources and callbacks,
player core movement/hits, top-level round/stage scheduling, natural
keyboard and retained C0/CRT. All three modules here were historical
existing authored function owners, not new Factory units or a newly
established vendor raw OMF packet identity.

Read-only affected verification:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_main_round_hud_after595_work.py

Producer: scripts/build_th03_main_round_hud_after595_work.py
Build: .analysis/work/main-round-hud-after595-native-build.json
Review: .analysis/work/main-round-hud-after595-native-review.json

Both rounds of complete OBJ, direct EXE/MAP, original full Japanese
compact MZ results, native source inputs and eight writer logs remain
retained. No full cold replay or historic acceptance repinning occurred.
