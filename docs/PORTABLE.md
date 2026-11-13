# TH03 semantic and 64-bit port

`port/modern-64` builds native C++17 for Linux/SDL2 and Windows x64/Win32-GDI.
Title, menus, character selection and MAINL stage introduction join through
explicit resident state into the native MAIN battle loop. Enemy scripts, battle
resources/HUD, round-introduction animation, collision primitives, bullets,
explosion chains, fireballs, all nine Charge Shot/Bomb families, Hyper handlers,
shared effects, both background chains, nine Gauge patterns, all nine Extra
Attack families, all nine BOSS families and their shared control, attack warnings,
pause/quit, player/loss state machines and CPU decisions are ported and checked separately.
Battle now runs with enemy/player/CPU movement, shooting, hits, attacks, warnings,
pause/quit, result statistics, playfield transitions and round retries. Matches
commit scores, advance the resident stage and enter MAINL's winner animation.
Ordinary story victories continue through the next introduction into battle;
versus returns to the title. Story losses proceed through score registration and
continue; accepting restarts the stage, while declining or exhausting credits
returns through Game Over. The title's HiScore menu also runs natively.
The late-stage dialogues resume the Chiyuri/Yumemi introductions and battles.
Final victory runs ending dialogue, Staff Roll, the verdict and score registration.
Eligible clears unlock the two final characters and show the optional bonus
dialogue before returning to the title. Music Room now runs its full track list,
comments and polygon animation. Native configuration survives process restarts.
Native PMD music/effects and stereo output are available with `--audio`.
Ordinary campaign play and further naturally reached CPU aliases remain open.

The DOS reconstruction stays on `main`. The live Windows DOSBox session and
`D:\Entertainment\Game\Touhou\th03-reconstruct\play.hdi` are independent.
Do not replace that disk, send input to its window or restart its emulator.
The native program reads external original data and executes no DOS code.
It writes YUME.NEM only to its independent native save directory.

## Windows preview package

The portable branch is `port/modern-64`. From a Windows MinGW-w64 environment
with a 64-bit C++17 compiler, CMake and Ninja on PATH, run
`port64\build-windows.bat`. It builds only the game in
`build\portable-win64\th03-port64.exe` with one compiler process.

For a playable folder, place the executable, `port64/Play.bat` and
`port64/Play-silent.bat` beside your original Japanese game disk named
`th03.hdi` and external `FREECG98.BMP`. Add `ym2608_adpcm_rom.bin` for
`Play.bat` audio. `Play-silent.bat` needs no rhythm ROM. Both launchers use
`save-normal` beside the executable; keep that directory when updating.
The title initially hides its menu until a direction is pressed.

To prepare a data-free ZIP from a clean committed checkout:

```sh
python3 port64/package_release.py --exe build/windows-x64/th03-port64.exe \
  --version preview-1 --output build/th03-preview-1-windows-x64.zip
```

The ZIP contains the executable, launchers, setup instructions, MIT and ymfm
BSD-3-Clause licenses, and SHA-256 checksums. Supply the game disk, font and
rhythm ROM separately. Packaging locally does not publish a GitHub release.

The current local `build/th03-preview-1-windows-x64.zip` was built in Release
from a clean, data-free export of `4ff633ca`. Its executable SHA-256 is
`8c0197bc20c46aab4dfae6694a46343ec875287bc4a6fd63155ff89c0d958ae4`.
The unpacked executable matches the working build's diagnostics and full frame
after 32,000 title/demo refreshes, and passes the private Windows window
create/resize/close/save check. Only Windows system DLLs are imported. ZIP
membership and every included checksum pass. Non-PE input, unsafe version
names, dirty source and an existing output path are rejected.

## Build and inspect

The local port checkout is `.analysis/native/port64/` inside the DOS checkout.
Use one CPU at nice10 for builds. Its ignored `build/` and runtime state remain
separate from DOS/Wine/analyzer state.

```sh
cmake -S port64 -B build/linux-x64 -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake --build build/linux-x64 --parallel 1
ctest --test-dir build/linux-x64 --output-on-failure
build/linux-x64/th03-port64 --hdi /path/to/original/zun.hdi \
  --font-bmp /path/to/FREECG98.BMP --scene menu
```

The font is an external 2048x2048 monochrome Anex86-format PC-98 BMP, also
accepted by DOSBox-X. MAINL introductions, scores and Japanese result labels require it;
menu/selection do not.
Windows cross-build:

```sh
cmake -S port64 -B build/windows-x64 -G Ninja -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_TOOLCHAIN_FILE="$PWD/port64/mingw64-toolchain.cmake"
cmake --build build/windows-x64 --parallel 1
```

MinGW runtime libraries are linked statically. Use `--headless` for native
Windows background checks; it opens no window and takes no keyboard input.
Linux GUI checks use private Xvfb. `port64/check_windows_window.ps1` creates
a separate inactive Windows desktop, checks window creation/resize/close and
configuration persistence, and never switches the user's desktop.

Arrows move through single-player menus; Z/Enter confirms and Escape returns.
The original title initially hides menu labels; a direction reveals them.
Two-player P1 uses T/F/H/B with Z/X; P2 uses keypad movement with Left/Right
for Shot/Bomb. Option changes rank, sound-mode and key-mode state.
Music Room uses Up/Down to select, Z/Enter to request playback and Escape or Quit to return; release held
keys between commands. Playback uses the selected PMD profile when audio is enabled.
Name entry keeps the original alphabet: Z/Enter selects, X erases, and selecting
END or entering eight letters finishes. The following score-table wait requires
release followed by another key press.
Escape fast-forwards dialogue between waits; palette fades keep their original
timing. A blocked page wait requires release followed by a new press.

Scores use `%LOCALAPPDATA%/TH03` on Windows or `$XDG_DATA_HOME/th03`
(default `$HOME/.local/share/th03`) on Linux. `--save-dir DIRECTORY` selects a
different directory. A missing native YUME.NEM starts with the external HDI's
score file; subsequent saves and loads use the native copy. YUME.CFG also uses
this directory, falling back to the HDI on its first run. Configuration saves at
OP handoffs and normal application exit, including closing the native window.
Headless runs use memory only unless an explicit `--save-dir` is supplied.

Useful headless scenes:

```sh
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --headless \
  --scene story-select --screenshot selection.ppm
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --headless \
  --font-bmp /path/to/FREECG98.BMP --scene stage-intro \
  --characters 5,13 --frames 20 --screenshot intro.ppm
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --headless \
  --scene battle-ready --characters 5,13 --screenshot ready.ppm
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --headless \
  --scene battle --characters 5,13 --frames 1200 --screenshot battle.ppm
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --headless \
  --font-bmp /path/to/FREECG98.BMP --scene scores \
  --frames 40 --screenshot scores.ppm
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --headless \
  --font-bmp /path/to/FREECG98.BMP --scene dialogue1 \
  --characters 5,17 --frames 110 --screenshot dialogue.ppm
```

`--characters` supplies two paletted IDs 1..18; `--stage` is zero-based.
`battle-ready` retains the static initialization fixture. `battle` starts story
battle directly; `two-battle` starts two human players with their separate keys.
`--frames` advances idle headless VBlanks or limits a window run. `--inputs`
accepts comma-separated original WORD masks, or tuples `SP:P1:P2`, one per
VBlank. Use release samples between presses. Selection samples every three
VBlanks after its initial 30-frame wait. `--help` lists supported scenes.
`music` opens Music Room directly. `dialogue0` and `dialogue1` inspect the two
late-stage chapters for P1's character;
`ending` includes the original 96-frame black wait before that character's ending
dialogue, followed by Staff Roll and ending registration. `staff` starts the
roll directly; it ignores input until the verdict has waited 257 snow frames.

`--list`, `--extract NAME --output FILE` and `--pi NAME --packed FILE` inspect
OP/MAINL resources. `--main-assets --list` or `--main-assets --extract ...`
selects the second PF for resource inspection. `--archive` accepts an extracted
PF instead of the HDI. Keep output files outside original media and the user's
playable disk.

## Comparisons

The FAT/PF reader, PI decoder, font bitmap reader and master.lib motion adapt
TH04 `port/modern-64` revision `1ba7107` (MIT). TH03 owns its CP932 archive names,
resident/OP flow and graphics/gameplay semantics. The original Japanese targets
pinned in `config/targets.toml` remain the baseline. These native checks do not
add source-exact credit to DOS ledgers.

Run the original-instruction checks with the DOS checkout's Python environment
(Unicorn/Capstone). Set `DOS` to that checkout and `NATIVE` to this branch's
`build/linux-x64` directory. Image comparisons also need ImageMagick `convert`.

| Check | Command arguments after the script | Evidence compared |
|---|---|---|
| `check_title.py` | `--native "$NATIVE/th03-port64" --dos-root "$DOS" --dos-frame "$DOS/.analysis/runtime/candidates/dos-replay-rebuilt/menu.png" --output /new/private/output` | All128,000 decoded PI bytes and the complete DOS menu RGB frame |
| `check_music.py` | Same arguments as `check_round.py`, plus `--output /new/private/output` | Complete OP polygon/RNG/page/input traces, all 19 song requests, full pages after each comment switch, original GRCG polygon rasters and application reentry/exit |
| `check_configuration.py` | Same arguments as `check_round.py` | Original CFG option order and save/exit bytes, native overwrite/reload, invalid native records and Option changes across process restart |
| `check_selection.py` | `--native-checks "$NATIVE/th03-port64-checks" --dos-root "$DOS"` | OP selection/lock/palette state, complete curve rasters and story opponent/seed policy |
| `check_intro.py` | `--native "$NATIVE/th03-port64" --dos-root "$DOS"` | Complete Marisa/Rikako Stage1 DOS frame, minimum wait and fade handoff |
| `check_round.py` | `--native "$NATIVE/th03-port64" --native-checks "$NATIVE/th03-port64-checks" --dos-root "$DOS"` | Six MAIN initializers plus real-resetter SI inheritance, including LCG, backward ring fill, player thresholds and both formation rings |
| `check_enemy.py` | Same arguments as `check_round.py` | Six enemy scripts over 1,237 ticks, including real movement/vector callees |
| `check_battle_graphics.py` | Same arguments as `check_intro.py` | Unchanged DOS borders, P1 gauge/score and TRAM glyph ink |
| `check_player_graphics.py` | Same arguments as `check_round.py` | Original BFNT allocation/conversion, normal-pose atlas preparation and both player draw passes; all three poses/glow images in both palette banks |
| `check_hud_intro.py` | Same arguments as `check_selection.py` | 520 story/versus frames: slide/banner state, all128 particles, seed and ring cursor |
| `check_collision.py` | Same arguments as `check_selection.py` | Six complete 6,624-byte bitmaps, ordinary player hits and wide CPU scans into adjacent DATA owners |
| `check_loop_clock.py` | Same arguments as `check_selection.py` | Original scheduler counters, speed/recovery/CPU gates, WORD wrap and page cadence; native warning/pause suspension and double-refresh presentation |
| `check_combo.py` | Same arguments as `check_selection.py` | Both 80-frame combo lifetimes, expiry/reset and deferred BCD score awards |
| `check_results.py` | Same arguments as `check_selection.py` | Reward accumulation, full BCD scores and TRAM characters/attributes, warning overlap, cover/uncover rasters, result branches, life debit/score commit and application retry/handoff |
| `check_win.py` | Same arguments as `check_round.py` | Winner resource/palette and full message selection, story dispatch including stage9's adjacent byte, every animation refresh with real palette fades under no-BGM timing, and application stage/versus routing |
| `check_scores.py` | Same arguments as `check_round.py` | Complete encrypted sections/files, insertion and name-entry frames, original DOS score RGB frame, continue outcomes, native file reload and application registration/continue/Game Over routes |
| `check_staff.py` | Same arguments as `check_round.py`, plus `--output /new/private/output`; optional `--slow 400 --music` | Complete original snow/RNG/page/tone traces, selected full graphics pages, verdict text calls, initial fade and sound requests; no-BGM and injected measure/slow-refresh profiles |
| `check_cutscene.py` | Same arguments as `check_round.py` | Parameter/carry and complete interpreter refresh state, sound requests, all 28 original scripts through STOP under fast-forward, full masked-picture pixels and the stage 7/8/final dialogue routes |
| `check_bullet.py` | Same arguments as `check_selection.py` | Group vectors, full bullet/trail pools, motion/transfer/cloud/clearing, collision maps and complete pellet rasters |
| `check_combat.py` | Same arguments as `check_selection.py` | Explosion/chain scoring, enemy/fireball hits, derived fireballs, movement/collision, coupled bullet pipelines and known stack aliases |
| `check_charge.py` | Same arguments as `check_selection.py` | All nine Charge Shot lifecycles, full physical pools/history, hit circles and RNG, sound events and four projectile Hyper helpers |
| `check_bomb.py` | Same arguments as `check_selection.py`; add `--caller` for the background/two-Bomb chain | Nine controllers with complete effect pools, palette/foreground state, RNG and sound events; real caller stack bytes through Kotohime's fade |
| `check_cpu.py` | Same arguments as `check_selection.py` | Offensive/defensive CPU, target selection, collision/retry grids, shared velocity/RNG and real Bomb activation |
| `check_boss.py` | Same arguments as `check_selection.py` | Shared launch/reversal/selection/descent/HP/explosion reward and all nine BOSS families coupled to complete bullets, Extra entities, collision, palette/RNG and scores |
| `check_warning.py` | Same arguments as `check_selection.py` | Portrait-to-flash handoff, 27 physical flash tones, red warning/attack activation, complete palettes and text events on every tick; pause/resume/quit outcomes, frozen clocks, sound events and CPU-exit fade |
| `check_extra.py` | Same arguments as `check_selection.py` | All nine Extra lifecycles and special allocators, complete entity/Ellen-history/bullet/effect pools, real shot consumption, collision/RNG and saturated allocation |
| `check_gauge.py` | Same arguments as `check_selection.py` | Nine Gauge patterns and ordinary/special Kotohime Extra, coupled to full bullet/effect/entity pools, shot consumption, palette/RNG and collision maps |
| `check_background.py` | Same arguments as `check_selection.py` | Both particle chains, all80 slots, LCG, acceleration/phase transitions, reset and both indeterminate-byte branches |
| `check_raster.py` | Same arguments as `check_selection.py` | Complete original GRCG circle, clipped DDA line, triangle and trapezoid rasters |
| `check_mrs.py` | Same arguments as `check_round.py` | Original MRS opaque/altered/alpha blits, alignment and horizontal flip in all pixels |

Linux and native Windows x64 state checks pass; menu, selection and isolated
introduction PPMs agree between platforms. Private SDL window checks exercised
menu/Option/selection on Xvfb. Original captures and local evidence live in the
DOS checkout's `.analysis/work/` and `.analysis/runtime/candidates/`.
`th03-port64-checks --hud-picture HDI 100 FILE.ppm` renders an isolated round
introduction without running the surrounding battle loop.

## Audio

Enable music and effects explicitly. PMD86 is the default profile; PMDB2 and
PMD are selected with `--pmd-driver pmdb2` or `--pmd-driver pmd`.
PMD86/PMDB2 require an external 8,192-byte YM2608 rhythm ROM. The local test
copy is `$DOS/.analysis/runtime/audio/ym2608_adpcm_rom.bin`; its SHA-256 is
`53afd0fa9c62eda3e2be939e23f3adf48a2af8ad37bb1640261726c5d5adeba8`.
Keep it outside Git with the original game resources. The three-channel PMD
profile needs no rhythm ROM.

```sh
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi \
  --font-bmp /path/to/FREECG98.BMP --audio --opna-rom /path/to/ym2608_adpcm_rom.bin
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --headless \
  --audio-wav title.wav --opna-rom /path/to/ym2608_adpcm_rom.bin --frames 180
```

`--audio-wav` enables synthesis and streams signed 16-bit stereo at 48 kHz to
WAV. Headless runs open no device. `--mute` suppresses device output while
retaining synthesis and optional capture. Linux uses SDL's queued device;
Windows uses WinMM. BGM Off stops music while preserving FM sound effects.
The original saved sound option 2 still uses FM when no MIDI resident exists.

`sound.cpp` follows TH03's installation, sound priorities, process-local effect
reset and MAIN update order. Title, selection, Music Room, introductions,
battle, winner, dialogue, scores, continue and Staff Roll feed the same owner.
Measure waits read PMD's live counter; score/staff fades wait for its volume
when required. The semantic player, chip renderer and transports derive from
the MIT TH04 port at `1ba7107`; `pmd/vendor/ymfm` retains its BSD-3-Clause
license and upstream revision. Driver COMs are used only by verification.

```sh
"$DOS/.venv/bin/python" port64/check_audio.py \
  --native "$NATIVE/th03-port64" --native-checks "$NATIVE/th03-port64-checks" \
  --dos-root "$DOS" --output build/audio/pmd86 --loops 2
# Use --driver pmd or --driver pmdb2 for the other original residents.
# --song OP.M --all-effects checks every game effect ID with one song.
"$NATIVE/th03-port64-checks" --audio-flow "$DOS/.analysis/runtime/images/zun.hdi" \
  "$DOS/.analysis/runtime/fonts/FREECG98.BMP" \
  "$DOS/.analysis/runtime/audio/ym2608_adpcm_rom.bin" build/audio/flow.wav
```

The checker pins the original HDI and all three TH03 COMs, installs them with
TH03's `/M8 /V0 /E2 /K` flags and compares every ordered FM/SSG/rhythm/timer
register write, measure, fade and loop status. PMD86 covers every song through
two loops or its natural end, followed by effects, mixed IRQs, fade and stop.
The other two profiles cover all songs over 512 IRQs, and all three also pass
the complete 0..21 effect sequence with OP.M. Saved traces agree on Windows.
PCM and fake-device contracts run in CTest. Linux/Windows installation mirrors,
title/flow WAVs and application audio checks agree. A private SDL window with
the dummy backend submitted all 144,000 title/Music Room frames without drops.

The adapter advances one declared 60 Hz refresh at a time; CPU/resource work
does not consume chip time. A complete controlled Reimu campaign with live
PMD86 timing passes on Linux/Windows (see below). Physical listening and Windows
device playback remain open. External MIDI/ADPCM sample memory is not implemented.

## Integration findings and next work

Keep the original draw/call order and explicit integer widths. The current
source preserves these consequential details:

- OP's opponent generator uses a local LCG copy; MAIN seeds anew from the
  resident frame counter. Random-ring fill runs backward and retains its
  cursor. Its WORD getter increments the cursor before loading, so index255
  reads the wrapped cursor as its high byte.
- Stage setup assigns initial versus gauge levels after round preparation,
  replacing the preparation's rank increment. The round counter is DWORD;
  the round/result counter is WORD.
- The formation randomizer's first previous byte inherits the low byte of
  incoming SI through the real Ellen resetter. Initial startup retains the
  attested `0x5e` InitStart context; MAIN holds PLAY_NEXT in SI on retry, giving
  `1`. `check_round.py` executes the real resetters with three SI values and a
  seed whose first candidate is1, verifying the retry's extra rejection/RNG draw.
- TH03's C++ graphics-font renderer uses alternate JIS-row ANK and WORD-truncated
  bold weight. TH04's ASM renderer differs. SPRITE16 uses physical 200-line
  graphics and whole-column clipping; TRAM stays at 400 lines with fixed text
  colors. Graphics score digit5 differs by one dot from `NUM8.BF2`.
- The round-introduction slide destination aliases particle15.x. Collision Y
  reports the scan rectangle's top, not the occupied row; X reports the
  containing eight-tile column. Preserve these coarse values for CPU decisions.

Reimu and the other eight characters' player sprite indices agree with original
BFNT, `SUPER_ENTRY_PAT`, `SUPER_PUT`, atlas preparation and player/overlay calls.
The original normal poses occupy VRAM rows 328/360, relative rows 128/160 in the
SPRITE16 area. Each stored 32x32 pose becomes 32x64 display pixels in 200-line
graphics mode. `check_player_graphics.py` compares all 128,000 visible indices
for every normal/glow image in both palette banks, at the ordinary position
and near the upper edge. It executes the original GRCG masks and models the
resident's vertical clipping at the INT42 device interface.

At player Y=11, the original glow top is `(center.y >> 5) - 8`, or physical
row -3. Dividing the logical top `(11 - 16)` by2 instead truncates toward zero
and produces row -2. The native glow now retains the original arithmetic-shift
rounding, fixing the two-display-pixel offset at the upper edge. Linux and
Windows pass all nine characters' normal/glow pixel comparisons at both heights.

`warning.cpp` separates physical refreshes from simulation ticks. After drawing
the attack portrait, freeze simulation for the 27-refresh white flash, then call
both warning controllers before the background hook. The red warning completes
at flag33 and starts its active Gauge/BOSS pulse in that same call. Persist the
last text attribute, level and label until the original clear; black warning ink
must still cover graphics. Portraits use the original masked MRS blit. Hyper
highlights fill all eight gauge-strip rows, with the original even/odd bar colors.
Pause requires release before accepting commands and release before resuming;
Q takes priority over Cancel. CPU/CPU pause fades through100,94,...,4,0 and quits.
The caller must finish the interrupted loop iteration after pause returns, even
if quit was requested: the original loop tests quit at its next entry.

`check_warning.py` compares nine 180-tick warning traces, including both players
warning simultaneously, with original MAIN instructions. It also checks three
pause/quit outcomes against the original pause and palette-fade owners. Linux
and native Windows x64 agree. `--warning-picture HDI PID KIND STEP HYPER OUT.ppm`
renders the real resources; PID2 means both players, KIND1/3/5 selects the attack,
STEP0 is the portrait,1..27 are white-flash refreshes, and28+ advances the red
controller. Eleven complete pictures agree between platforms and the existing
DOS battle-HUD comparison still passes. `RoundLoop` now calls these controllers.

`round_loop.cpp` follows the original update and draw order. Enemy hits run in
the update; fireball hits run immediately before fireball drawing. Bomb render
changes precede each Bomb draw, BOSS/Extra mutations follow their draw, and
effect quads rotate before drawing. Shot animation and combo expiry advance
only when drawing. Score extends run before warning portraits; combo awards
occur after the score HUD. Two indexed pages preserve background pixels from
skipped draws. Palette writes and page presentation wait for the required
refresh, without repeating simulation or render mutations. Gauge/BOSS level
labels retain their TRAM values until the next white-flash update. Pause and the
27-refresh white flash resume the interrupted iteration exactly once.

The clock probe executes the original loop's control flow while treating its
gameplay/draw calls as foreign services. Native fixtures run the real modules;
this probe covers scheduler cadence rather than a full battle-state comparison.
An idle 1,200-tick battle and held-shot runs through 2,600 input refreshes exercise
the integrated CPU/combat/charge/warning path. Complete pictures and diagnostic
outputs agree between Linux and native Windows at 800, 1,800 and 2,600 input
refreshes. A private Xvfb SDL window accepts movement/shooting, pause and Q,
then returns to the title. Campaign acceptance remains open.

`results.cpp` samples winner statistics on result frame1, divides the reward by
192 with the original 65,535 step cap, then credits the winner on each rendered
result frame. The panel retains the initial total while the remaining balance
decreases. Final-stage lives add their original bonus and disable extends.
Warning/result writers share persistent half-width TRAM cells, preserving odd-X
gaiji halves, attributes, overlap and spaces written by the warning clear.
The checked transition uses the original 5555/AAAA masks and 16-frame halves.
The loop checks its midpoint before the next transition draw, including the
distinct versus, story retry, game-over and match-completion score paths.

Retry increments the round ID and calls `prepare` with the recovered SI byte1.
It retains scores, gauge, wins, combo timers, result balance and background
positions, resets background velocities and Hyper dispatch, restores the palette
and clears TRAM. The uncover callback survives preparation. Hardware access/
display pages reset to0/1 while the page-bookkeeping byte retains its parity.
`--result-picture HDI FONT_BMP PROFILE REFRESHES OUT.ppm` renders controlled
results or retries; profiles0/1 are versus,2/3 story loss with/without lives,
4 story victory and5 final-stage victory. Eight controlled result/retry pictures
agree on Linux and Windows. A natural run of9,000 held-shot refreshes followed
by up to10,000 idle refreshes loses twice, restarts twice, then reaches Game Over
and MAINL with no remaining lives. Both platforms finish with identical state
and complete frames (round2, frame3273, result frame176,10,878 draws).

`win.cpp` keeps the played characters separate from the resident opponent
selected for the next stage. MAINL updates the latter before loading the winner
portrait and message, which still use the played pair. Stages 6 and 7 choose the two
special message blocks when P1 wins. Each block contains three exact 60-byte
CP932 lines. The original dispatch reads the byte after `story_opponents` at
stage 9 before taking the ending branch; `Resident::opponent_tail` retains that
physical alias. The original win loader and dispatcher agree in 25 bounded
cases, covering every winner character/palette and the stage/mode branches.

Winner animation has five logo cels, the white flash, final portrait/logo,
three bold text lines, an unrestricted input wait and a black fade. The clock
check runs the original animation and actual palette fade instructions, replacing
only device output and clock waits. Its entire refresh trace agrees, including
the initial palette synchronization waits. With audio disabled, the native
animation uses the original no-BGM delays of 16, 64 and 4 frames; enabled audio
supplies the live PMD measure. Linux/Windows winner pictures agree. The real
application proceeds from an ordinary win through StageIntro into a fresh MAIN
round with the committed score; versus returns to OP. Story losses enter score
registration, followed by continue or Game Over.
`--win-picture HDI FONT_BMP PROFILE REFRESHES OUT.ppm` inspects the animation:
profiles 0/1 select P1/P2 at stage 1, 4/5 at stage 6 and 6/7 at stage 7.

`score.cpp` retains the four 206-byte YUME.NEM sections, forward decode, backward
encryption, checksum and three LCG draws per save. MAINL recreates all four ranks
when loading corrupt data, including its original all-rank unlock quirk for a
clear without continuing. Equal scores retain insertion order because the sort
ignores the continue digit. Name entry retains release locks, signed WORD repeat
counters, the double-width alphabet commands and all-identical default names.
Its eighth character wraps the backwards cursor to255. The next blank writes14
to a byte in the snow pool, which has no subsequent consumer before exec/exit;
the editor records that location. The associated unput and preview use different
signed/unsigned X shifts, producing the original visible VRAM aliases.

The complete initial score frame matches the retained DOS frame in every RGB
byte. `super_entry_bfnt` replaces the PI palette with the last BFNT's eight-bit
B,R,G palette, rotated to R,G,B; retaining only the PI palette changes the blues.
Page1 retains the initial rows, so name erases restore neighboring overlapping
rows. Linux/Windows editing and continue pictures agree, including the final
underflow preview. The save/registration/continue fixture reloads the native
file and reaches MAIN with the previous stage, two lives, one fewer credit and
a cleared score. Rejecting continue and exhausted credits return through the
original no-BGM Game Over waits. A private SDL window also accepts the score
screen's release/confirm sequence, writes the native copy and returns to title.

Native file writes replace YUME.NEM through a temporary file in the selected
save directory. Short host files are treated as missing before entering the
original recreation path. GCC8 needs its separate `stdc++fs` library; CMake
links it for that compiler, while the Windows GCC13 build uses its ordinary
filesystem support. The original HDI and the user's DOS play disk stay read-only.

`cutscene.cpp` keeps the original two graphics pages, textbox snapshot, quarter
pictures, four EGC masks, viewport shake, font effects and cursor flow. Only the
stop opcode ends a script; NUL is a control byte. Numeric parameters eagerly
read three bytes and rewind the WORD offset. For two digits, DEC preserves the
decimal ADD's carry; three digits retain that carry directly. One digit or a
default obtains carry from the pointer SUB. This matters to GRAPH_GAIJI_PUTC's
ADC: the page1 call passes one less than page0, but two/three-digit parameters
normally cancel that difference with carry. Text speedup increments its cycle
after the blocking glyph delay returns. A cursor-triggered page wait can update
the held input before the glyph delay is selected.

The original interpreter, numeric readers, cursor and palette fades execute in
the comparison, with graphics/storage and physical clock waits treated as foreign
services. Five bounded scripts compare ordinary input, held confirm, fast-forward
and release/press behavior at every refresh. All 18 chapter scripts, nine ending
scripts and the bonus script also match through STOP under fast-forward,
including complete song-load/control/effect requests. A separate original EGC
helper comparison covers every pixel in both pages after each mask and the final
quarter. Linux/Windows intermediate pictures agree. Measure waits use the live
PMD counter when audio is enabled, otherwise the original fallback frames.

The application retains scores and resident RNG seed while dialogue runs, then
launches the actual next introduction/MAIN stage. Stage 7 still shows its winner
animation first; stage 8 goes directly to its dialogue. Final victory retains its
96-frame wait and ending dialogue before starting Staff Roll. A private
SDL window accepts Escape fast-forward and reaches the final battle.

`staff.cpp` preserves the 80-slot snow pool, 15-bit MAINL IRAND, Q4 movement,
rotated blue-plane snow masks and the two independent page centers. Image
motion erases three rows of the E plane; dissolve masks use the absolute screen
row. Paired credits retain the previous image and the separate portrait before
clearing both interiors. A slow refresh during automatic adjustment disables
alpha composition and reduces the active snow slots to 50 after drawing.

The no-BGM gate uses `frame > 256`; a supplied music measure instead needs the
target measure and `frame > 192`. The verdict cannot accept input until its own
257th snow tick, then fades over odd frames. Initial blackout takes 69 refreshes,
followed by one sync refresh. The score's trailing digit is the number of
continues, and the skill's case 3 deliberately falls through case 4 with BYTE
addition before clamping. `check_staff.py` executes these original owners and
compares the whole snow pool, RNG, page, tone and sound-control trace, plus
selected complete two-page rasters. Its font mask comes from the original
verdict's text calls through the previously checked native font renderer.

Ending registration sets stage 99, saves ALL and refreshes character availability.
The bonus requires all three credits and P1's paletted ID below 15. Native ending
flow checks cover a no-continue clear, a continued clear and Chiyuri's clear,
including save reload and return to OP. Enabled audio supplies the music measure
and waits for the initial PMD fade to finish. Linux and Windows agree
in both the no-BGM and injected measure/slow-refresh profiles. A private SDL
window also runs the staff scene.

`music.cpp` adapts TH04's polygon raster while retaining TH03's 19 tracks and
840-byte comment blocks. Original OP instructions verify all sixteen polygon
states and RNG through bounces/resets, input release, the skipped blank list row,
playback order and exit. Comment refreshes restore all four planes in the text
rectangle and recapture the complete B plane. Only B receives polygon fills;
the original GRCG owner renders the poses used in picture comparisons. Both
pages agree after each track's first comment update and at the final observation
in each input profile, using the already checked font renderer as a device.

OP leaves the first animation's accessed page at 0 while its page variable is 1;
keep those distinct. Polygon initialization and the selected playing track
persist across Music Room visits, even though returning to the title restarts
its own song. Selection reseeds OP's shared RNG. Executing a new OP process
resets this state to seed 1 and track 0. The application now retains that process
boundary across selection cancellation, MAIN/MAINL and score viewing.
Linux and Windows state/picture checks agree. A private SDL window accepts
selection/play/exit and returns to the title.

`configuration.cpp` keeps the native YUME.CFG separate from the HDI. Its first
three bytes are BGM mode, key mode and rank; native loading validates the same
typed ranges used by the menu. DOS's ordinary save writes one indeterminate
stack byte after these options. The native file preserves its existing opaque
byte instead; unused and segment/debug metadata never become host pointers.
Exit writes the options followed by five zero bytes, matching original OP.
Both platforms pass original-instruction save comparisons, replacement of an
existing native file, Option changes and reload in a new process. Continue with
the remaining battle caller contexts and campaign acceptance.

`bullet.cpp` retains the 320-slot pool, shared 48-slot trail ring, byte-wrapped
speed tuning and ascending update order. Derived groups can occupy later slots
and update on that same tick. The pellet explosion query is an explicit foreign
service for isolated checks; `Round::update_bullets` now supplies the real
explosion/chain owner. Six full spawn pools, nine update
fixtures, sixteen group vectors and five complete pellet rasters agree with
original MAIN instructions. These include the transfer target's pixel rounding,
independent X/Y trail updates and the narrow pellet-write path. The authored
ReC98 pellet bitmap retains the distinct dots in transfer preshifts6/14.
Native Windows x64 transfer/trail states and collision maps agree with Linux.

`combat.cpp` joins shot, explosion and charge-shot collision in the original
order, including score carry, combo saturation, Boss/Panic state and derived
fireballs. Its Charge Shot callback can now use `ChargeShots::hit`; Extra Attack
callbacks can now bind `ExtraAttacks::add`. Fireball allocation retains a reused
slot's frame; charged red fireballs can read the previous destroyed fireball's generation.
The ordinary fireball-hit stack slot is supplied as `0x0f`. Known out-of-range
slots retain the original cross-player charge, score-digit and extends aliases,
including clearing those bytes when firing an Extra Attack. Unknown aliases
still need their owning state. Enemy speed is shared by both players and only
refreshes when either player spawns a formation, not on every speed increment.

`th03-port64-checks --combat-picture HDI 0 FILE.ppm` renders controlled original
fireball/explosion/circle/bullet states for a visual smoke. It is a graphics
fixture, separate from the game loop.

`player.cpp` now supplies the common movement/charge/fire/hit/knockback
state machine. Hyper, Charge Shot and loss owners are implemented separately;
bind them with Bomb and CPU when joining the game loop. The native player
contracts now use all five actual service implementations.
Native contracts exercise held-charge/release/tap timing, one-halfheart survival,
final defeat, CPU shot cadence and locked-player banking/glow. They pass on
Linux and native Windows x64. The movement velocity is a signed byte shared
across player calls: locked paths can retain the preceding player's velocity
for sprite banking. Audio calls are queued in order for the sound owner.

`charge.cpp` implements all nine characters' add/update/hit paths and projectile
Hyper helpers. Linux and Windows x64 agree with original MAIN instructions on
the full pools and history, collision effects, RNG cursor and queued sound events.
`BattleGraphics` draws each family from its original atlas; all nine fixture
pictures agree between platforms. Kana uses bitplane OR for its trails. Ellen's
normal allocator leaves slot0 inactive and retains old velocity until update.
Round preparation resets only the four charge families called by the original;
in particular it retains Mima's controller bytes and the other families' state.

Hyper dispatch retains its one-frame standby transition and signed-byte speed
adjustments. The common loss owner now runs the 48-frame shake/flash, changes to
the defeat banner and records the winner. Native contracts exercise these paths
through the common player update. Loss particles and winner/loser banners are
also drawn; the round scheduler must use the loss owner's two-VBlank wait.
`--charge-picture HDI CHARACTER TICKS FILE.ppm` and `--loss-picture` on the checks
binary produce isolated rendering fixtures; CHARACTER is zero-based 0..8.

`bomb.cpp` implements stock/Hyper activation, all nine 180-frame Bomb
controllers and the twelve shared circle/quad effects. The controller state,
complete effect pools, palette channels, RNG and sound events agree with original
MAIN on Linux and Windows x64. MRS rendering and the three GRCG primitives also
match original instructions in all pixels. Nine complete Bomb fixture pictures
agree between platforms. `--bomb-picture HDI CHARACTER TICKS FILE.ppm` renders
these isolated effects with both players; it does not advance the battle loop.

Run `Bombs::prepare_render` and `Round::prepare_effects_render` only on scheduled
render frames: they consume RNG, emit effects/sounds, change palette/foreground
state and rotate quads. Keep Marisa's per-player draw position before the next
player overwrites the shared point. Ellen's spawn count, Kotohime's row Y and
Kana's angle are also genuinely shared. Kotohime's final palette phase reads
an uninitialized stack byte at `[BP-2]`, eight bytes below the round loop's SP.
Periodic backgrounds leave their frame local there, so its low byte is the
current result clock. Accelerating backgrounds save MAIN's SI in that slot;
the port retains the existing startup/retry contexts, `0x5e` and `1`.
EGC_ON at load `0704` makes no pushes and leaves the slot intact.

P1 inherits the byte left by P0's Bomb, including each character's distinct
local layout. `Bombs::palette_stack_byte` carries just that observable byte
between the two callbacks. Marisa's initial gray phase shares its trailing
color store with the fade; Chiyuri stops writing her first-phase color at
frame64. Treating either branch as leaving the background byte changed the
original caller trace. Inactive callbacks leave the byte intact.

`check_bomb.py --caller` executes original MAIN's `9858..988D` call sequence,
both real background chains and EGC_ON/OFF, with the real Bomb/effect owners.
It observes the two stack bytes rather than writing them, and compares every
frame's palette, tone and RNG through fade and stop. The production battle
renderer now supplies this context automatically; standalone Bomb fixtures
can still pass an explicit caller byte.
Linux and Windows agree on every checked row and on the complete frame after
600 two-player Bomb inputs. A native debugger confirms both players actually
cast at frames0 and180 and finish all four lifecycles normally.

`cpu.cpp` retains both offensive and defensive strategies, all twelve authored
dodge grids, the three retry sequences, coarse shared collision coordinates and
the real Bomb/Hyper entry. Ordinary in-map fixtures agree with original MAIN on
Linux and Windows x64, including the unused RNG draw during approach, stuck-Bomb
activation and preserving a charged attack by reporting a hit instead.

`background.cpp` supplies both original 48/50-particle chains and the complete
80-slot velocity reset. The second player's character selects the chain. The
initializers consume the LCG directly, so call them after MAIN stage setup,
not during `Round::prepare`. Native states match original instructions and
Linux/Windows fixture pictures agree at acceleration and periodic frames.
`--background-picture HDI CHARACTER TICKS FILE.ppm` renders an isolated chain.

Periodic non-turn paths read an indeterminate `changed` byte in DOS. Either
branch has the same effect in reachable particle states: acceleration records
the final speed, and each actual turn/reset establishes velocity equal to the
polar vector for the current angle/speed. Recomputing that vector without a
turn leaves it unchanged and consumes no RNG. Original comparisons check both
zero and nonzero incoming bytes. The final acceleration call draws with its
original clipping/cels before changing the next callback. Background callbacks
run before the frame-skip branch; a skipped frame can leave background pixels
in the pending back page. Preserve that page when joining the scheduler. Bomb
first-phase fills erase the selected playfield's background as in DOS.

`gauge_attacks.cpp` implements all nine pellet/bullet Gauge patterns. Kotohime's
Gauge uses the same timing bytes as her ordinary Extra Attack; `extra.cpp`
supplies their shared flight, falling charges and delayed bullet rings. The
special allocator uses slot8 or overwrites slot9 when slot8 is occupied, as in
MAIN. Extra hitboxes skip explosions while retaining real charge/shot and
hit-circle effects. Collision dimensions convert pixels to two-pixel tiles.
`--gauge-picture HDI CHARACTER TICKS FILE.ppm` and
`--extra-picture HDI CHARACTER TICKS FILE.ppm` render coupled fixtures. Linux/Windows
state and complete picture comparisons agree.

`ExtraAttacks` now also owns the other eight ordinary attack families and the
Reimu/Marisa/Ellen/Kana/Rikako/Yumemi special allocators used by bosses. The
original-instruction checks include saturated scans and Kotohime's slot9
replacement, all seven Ellen history samples, paired Chiyuri arrival and beam
collision, Mima recoil/bounces, Rikako homing and Yumemi's two collision bars.
Reimu alone advances its Extra animation in the render loop; call
`prepare_render` after drawing, only on rendered frames. Mima uses duration for
its flying animation. Reimu/Mima/Marisa/Ellen appearance sprites use the state
byte rather than the frame byte. Ellen/Kana consume spawn RNG before scanning
occupied slots. Kana's special allocator deliberately retains the existing PID
and Ellen's retains history until the update, as in MAIN.

All families have resource rendering, including Ellen's four visible history
samples, the repeated Marisa beam, Chiyuri trapezoids and Yumemi's outlines and
sprite perimeters. The trapezoid matches original master.lib pixels, including
its clipped-height DDA denominator. Linux/Windows saturated-state snapshots and
18 complete Extra fixture pictures agree. The native round loop now schedules
these owners in their original update/draw positions.

`boss.cpp` supplies all nine templates, attack patterns, collision and shared
launch/reversal, movement, pattern selection, retreat, HP completion and
explosion-ring rewards. Original comparisons include each pattern family,
1,024-frame runs, low-level branches, reversal and HP/ring completion, with real
bullets, all48 trails, Extra allocation/history, effects, palette and RNG.
`check_boss.py --character 0..8` selects a bounded owner; omit it for all nine.
`--boss-picture HDI CHARACTER TICKS FILE.ppm` renders the resource pipeline.
Linux/Windows logical states and complete resource pictures agree.

Seven level-derived parameter bytes are shared at original DATA `1E3F..1E45`.
Each character overwrites only its own parameters. Reimu executes a newly
selected pattern immediately at frame0; the others preserve their distinct
switch/intro timing. Chiyuri uses a 48-frame selection delay and a separate
position/palette cycle. Her interleaved position table is DATA `08D6..08E9`;
Ellen's two nine-entry strip tables are DATA `08B2..08D5`. These are sprite
geometry, with the original distinction between logical pixels and physical
200-line VRAM rows.

Keep draw-dependent state separate from update state. Call
`Bosses::prepare_render` after drawing, only on rendered frames. Mima advances
its particle/carrier frame there, retaining the carrier draw before expansion.
Kotohime and Chiyuri advance intro phase/radius only on visible intro calls.
Explosion-ring completion changes ownership/score after drawing; Chiyuri also
restores her palette. The complementary `AAAA`/`5555` masks remain physical
screen masks. Yumemi's arrival uses OR drawing, and her origin is captured
before a pattern moves the boss. Ordered sound events include `0xff` for the
original `snd_se_reset` service before her intro explosions.

Resolve the remaining caller contexts during campaign testing.
Wide CPU scans near the left edge retain their aliased DGROUP reads.
With an empty bitmap and initialized target DATA,
P0 at (8,336) pixels with a 32-tile scan reads `02D0..02D4` and collides with
`PaletteTone`; at X16 it immediately reads `SinTable8` byte `0380`. P1's
corresponding scans reach CRT C++/signal/string DATA around `0FC0..1128`.
These reads can cause real false collisions. The native owner now supplies the
live tone, original default palette, mathematical sine table, unused CRT
exception workspaces, initial signal data, string settings and range-error
strings. Its compatibility context loads MAIN at segment `1000h`, with a
486-class DOS CPU, DOS5 console handles, CP932 and no SAJ joystick.
The original-instruction edge checks execute the actual C0 startup and CRT
initializers with that profile. Other DATA
reads still report their address and frame until their owner is recovered. The
original ENEDAT does not use its broken loop opcodes; custom loop scripts would
also need the original indeterminate stack context.

The `__environ` far pointer occupies DATA `10CC..10CF`. In this profile C0's
original `SS=263Fh` and 4,096-byte stack place the heap at `3740h`. Stdio first
allocates its 512-byte stdin buffer; the original far allocator then returns
`3761:0004` for the environment list. The port derives that virtual address
from these sizes rather than exposing a host pointer. The environment list is
not replaced during ordinary MAIN gameplay.

A natural Rikako/Chiyuri battle reached this alias during its first retry,
at round frame1036. P1's 80-tile scan at Q4 `(1072,3257)` first reads `10CE`
in its second column. With an empty collision map the allocated pointer still
causes the original false hit. `check_collision.py` compares all four pointer
bytes after executing original C0, stdio, heap and environment initialization,
then checks this actual scan against the original player-hit instructions.
The repaired pairing completes both retries and reaches the winner's required
input wait after 9,385 draws. Linux/Windows diagnostics and complete frames
agree. The neighboring-character battle runs now cover all nine player families
without an unowned-read failure.

The title's first attract battle also reached DATA `10CB`, the final null in
the original `xx.cpp` strings at `10BA..10CB`: the type-name fallback
`<notype>` and handler signature `**BCCxh1`. These immutable strings are now
available to the same alias reader. The startup comparison covers both strings, the allocated environment pointer,
all string options and all three 30-byte range-error messages. The last message
ends at `1136`; the earlier alias reader stopped three bytes too soon.

The same demo also reaches master.lib `file_Handle` at `02B2`. The ENEDAT and
graphics loaders close that API before battle, leaving the original WORD at
`-1`; this closed handle is now retained. Complete startup-byte and collision
comparisons pass on Linux and Windows. Both native executables run 32,000
refreshes from the title without input, reaching the fourth demo pairing with
identical diagnostics.


## Integrated campaign and attract acceptance

`th03-port64-checks --campaign-flow HDI FONT PRIVATE_SAVE_DIRECTORY CHARACTER`
runs the actual application from the first introduction through nine stages,
ending dialogue, Staff Roll, ALL registration, bonus/title return and persisted
character unlock. `CHARACTER` is 0..8; its rank is `CHARACTER % 4`. Each battle
runs 180 ordinary held-shot refreshes, then injects one lethal opponent hit.
The real 48-frame loss animation, results/rewards, score commit, cover and
scene dispatch run normally. These controlled wins check integration; an
ordinary full campaign remains to be played.

All nine characters pass on Linux and Windows, with identical complete stdout
and YUME.NEM/YUME.CFG bytes in separate temporary save directories. Appending
the external rhythm-ROM path enables PMD86 synthesis and real music-measure
waits. Reimu's complete audio campaign also passes on both platforms, with
identical diagnostics/saves and 13,752,000 stereo sample frames. No physical
audio device is opened by this fixture.

`th03-port64-checks --attract-flow HDI FONT` runs each of the four complete
attract battles back to the title, wraps to the first pairing, then exits it
with input. Both platforms agree on every reported duration, round frame and
resident seed. Each timed battle reaches frame 7,017; the input-exit case
returns after two refreshes at round frame 1.

`check_windows_window.ps1 -Game EXE -Disk HDI -Font BMP -Save PRIVATE_DIRECTORY`
created a real Win32 window on its private desktop, resized its client area
from 726x443 to 986x663, closed it normally and verified saved configuration.
It does not exercise physical keyboard input or validate displayed pixels.
