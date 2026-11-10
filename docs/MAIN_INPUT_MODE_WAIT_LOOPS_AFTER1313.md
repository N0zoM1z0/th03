# MAIN input modes: positive joystick branches and exact wait-state loops

The 367-byte physical `inp_m_w` object contains nine far Pascal input
entrypoints, including both joystick-vs-keyboard modes and the two-phase
`input_wait_for_change()` state machine. The maintained implementation in
`src/main/hardware/input_modes.cpp` now expresses joystick availability as
positive `if(js_bexist)` blocks in both VS modes. This is a meaningful C++
control-flow recovery: the driver scan and original two player assignments
execute **only** if the joystick is available, without the former early
returns or misleading assignment indentation. Original TC4 emits the
identical native conditional branch and both original byte stores.

The key-release phase now uses an unbounded `for(;;)` with the original
`input_mode_interface()` scan, `!input_sp` release check and one-frame
`frame_delay(1)`. The second key-press phase uses a signed bounded `for`
header, with explicit `frames_to_wait == 0` mapping to the original 9999-frame
polling sentinel. A negative bound still skips **only** key-press polling;
key-release polling remains unlimited. At the unlimited sentinel, the
counter resets **after** the original scan and frame delay, exactly as in
native code. There are no added input validation or timer guards.

Fresh source-native stages `af1313a` (release-loop structure), `af1313b`
(press-loop structure and zero sentinel), and final `af1313c` (positive
joystick guards) each recompiled the entire 367-byte owner in two original
TC4/TLINK rounds. The final stage matched complete initialized CODE,
ordered OMF fields, PUBLIC offsets and native segment layout, both normal
MAIN links and the original Japanese loaded image and MZ relocations.
The unchanged full-link parent was reused; no all-source cold replay ran.

The direct input scanner `input_s` is a *different* physical owner: its
417-byte function object remains exact, but its frozen parent full-link
has the documented extra trailing NOP. This input-mode proof does not
resolve or hide that separate historical link gap.

Review the preserved source-bound evidence with:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1313c
```
