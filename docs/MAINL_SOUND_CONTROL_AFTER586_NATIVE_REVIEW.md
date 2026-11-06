# MAINL complete sound priority, music dispatch, measure wait and file loader

Four additional natural 16-bit C++ sound producers were compiled under their
actual original first-use GAME=3/BINARY profiles and linked simultaneously
into the existing source-native after585 MAINL image.

| Original module | Maintained natural source | BINARY | CODE | PUBLICs | OMF fixups |
| --- | --- | --- | ---: | ---: | ---: |
| snd_se | mainl/linked_game/sound_se.cpp | M | 120 | 2 | 18 |
| snd_kaja | mainl/linked_game/sound_kaja.cpp | O | 30 | 1 | 2 |
| snd_dlym | mainl/linked_game/sound_measure.cpp | L | 49 | 1 | 3 |
| snd_load | shared/sound/load.cpp | O | 112 | 1 | 8 |
| Total | Four original source bodies | | 311 | 5 | 31 |

The 120-byte effect controller contains both priority arbitration and
per-frame effect state/expiration, not merely leaf helpers. Other routines
dispatch PMD or MMD music commands, wait for actual musical measures with a
frame-delay fallback, and perform the original sound-file loading logic via
DOS interrupts. Importantly, the historical sound loader's lack of DOS
error handling is preserved, not silently rewritten.

Two independent native Turbo C++ 4.02 compilations of each complete source
confirmed that all initialized CODE bytes, all 31 ordered OMF fixup fields,
all PUBLIC offsets and complete segment definitions match the original
objects. These sources contain a conditional codestring directive for
later games, but the actual GAME=3 first-use compiler does not emit such
manual padding in the TH03 producers. This is distinguished from the
previously reconstructed TASM sound routines whose natural EVEN bytes
were separately verified.

Both two-round four-object source groups were simultaneously substituted
into the after585 corrected-CUTSCENE_TEXT MAINL native linker response.
The complete 67,372-byte original Japanese decoded MAINL EXE remains
byte-identical, including all 677 original ordered MZ relocations and
full MAP positions. The only MAP differences are native source diagnostic
module filenames. Original Borland vendor OMF header/COMENT packet identity
is not claimed from linker equivalence.

This affected-only build reused the original C0/CRT, large root/story,
Staff Roll, cutscene, high-score input, source-backed CDG graphics,
input modes, PI raster loops, keyboard and DATA banks. No full cold replay,
vendor binary rewrite, source behavior edit or original acceptance repinning.

Run the read-only review:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_mainl_sound_control_after586_work.py

Builder: scripts/build_th03_mainl_sound_control_after586_work.py
Build: .analysis/work/mainl-sound-control-after586-native-build.json
Review: .analysis/work/mainl-sound-control-after586-native-review.json

All four original first-use sources already existed; these five functions
were historically known. This is improved simultaneous native source-link
evidence, not duplicate function-count or Factory product credit.
