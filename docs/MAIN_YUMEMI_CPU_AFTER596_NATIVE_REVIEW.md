# Original MAIN Yumemi Extra Attack, charged shot and CPU strategy: after596

Three complete, natural 16-bit Turbo C++ source implementations now
compile simultaneously into the original first-use project objects.
These are real nontrivial original algorithms, not symbolic stubs:

| Native producer | Original logic | CODE | PUBLIC entries | Ordered OMF fields |
| --- | --- | ---: | ---: | ---: |
| ex_yume | Yumemi Extra Attack, sprite/projectile patterns | 1,696 | 5 | 87 |
| cs_yume | Yumemi charged-shot acquisition and controls | 1,645 | 10 | 133 |
| p_cpu | CPU player target selection and movement strategies | 1,077 | 4 | 64 |
| Total | Original complete source | 4,418 | 19 | 284 |

The source files src/main/player/exatt_yumemi.cpp,
src/main/player/chargeshot_yumemi.cpp and src/main/player/cpu.cpp
are maintained natural C++ source. Each has a new tiny explicit source
translation-unit wrapper in src/main/player/producers, without copied
instruction bytes or target binary patching. The source retains the
original pointer/packing/segment layout and original uninitialized or
unconsumed state behavior.

Both source-native rounds compile all three original GAME=3/BINARY=M
producer objects with the genuine Turbo C++ 4.02 flags. Each matches the
full original initialized CODE payload (4,418 bytes), all 284 *ordered*
native OMF FIXUPP fields, 19 PUBLIC addresses and exact segment geometry.
The original compiler's warnings about converting int to gba_flag_t and
a variable assigned but never used were retained, not "fixed" by
changing semantics. Raw original vendor object COMENT and source-path
record identity remains distinct from linker-visible proof.

Replacing all three compiled objects at once in the after595 MAIN source
link also includes original game entry/round loop, every character BOSS
callback, nine large BOSS code modules, the bullet and fireball simulation,
collision, CPU interfaces, shooting and HUD. Both complete source-native
TLINK executables match the retained source parent byte-for-byte.
All 124,642 Japanese original loaded program bytes and 1,553 ordered
MZ relocations match. A separate reviewed standard DOS MZ formatting
step recreates the *entire 130,882-byte original Japanese MAIN.EXE*
byte-for-byte in both rounds.

The source-root check is bounded to the three authentic original C++
producers and original linker slot order; no 99-object cold replay was
performed. No new historical authored-function count, canonical Factory
acceptance or original vendor OMF packet/source compiler identity is claimed.

Affected-only review:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_main_yumemi_cpu_after596_work.py

Builder: scripts/build_th03_main_yumemi_cpu_after596_work.py
Native source report: .analysis/work/main-yumemi-cpu-after596-native-build.json
Independent read-only review: .analysis/work/main-yumemi-cpu-after596-native-review.json

Both full native OBJ/EXE/MAP/compact file vectors, exact source wrappers,
link responses and eight writer logs remain retained.
