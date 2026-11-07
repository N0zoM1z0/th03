# TH03 MAIN input modes and PI resource load: original native source proof (after734)

Two previously unverified complete physical original Turbo C++ producers were
added to the *current source-bound scoped compiler* rather than trusting
old compiler/assembler object inventory descriptions:

- `inp_m_w` — `src/main/hardware/input_modes.cpp`, complete 367-byte
  original `SHARED` CODE. It owns **nine original PUBLIC functions**:
  interface/key/joystick/CPU/attract input modes and the nontrivial
  `input_wait_for_change()` release/press state machine (58 ordered original
  native FIXUPPs).
- `pi_load` — `src/main/formats/pi_load.cpp`, 70-byte original `SHARED`
  CODE with the single original far-Pascal PI graphics unload/reload
  routine (six native FIXUPPs). It preserves its local `ret` temporary and
  original graphics-descriptor ownership.

The scoped compiler also now maps original `snd_kaja` (30 CODE, 2 fixups,
one PUBLIC) and `exit` (67 CODE, 8 fixups, one PUBLIC) from maintained
source, with all four original linker slots and original three-segment
CODE/DATA/BSS map rows checked. The **unchanged** first-use `af734a` trial
compiled all four current producers twice, matching 534 bytes, 74 ordered
fixups, 12 PUBLICs and complete normal MAIN/MAP. Later `af734c` is the
current-source modified checkpoint for input and PI. The `snd_kaja` and
`exit` original source still belongs to the historical first-use trial
until separately modified/current-source re-reviewed.

The real release/press input state machine now naturally uses `for(;;)` for
its intentionally *unbounded* key-release polling. Its 8-bit `input_sp`
condition is expressed as native-exact `if(!input_sp)` (release) and
`if(input_sp)` (press), with distinct semantics from the control bit tests.
The signed waited-frame counter uses `++frames_waited` and the exact
`9999` infinite-press sentinel is a named compile-time constant. The
original counter reset at the sentinel, negative-frame skip, frontloaded
key-release phase and intervening one-frame delays remain intact.

Two important **negative** TC4 trials constrain further refactoring:

- `af734b` changed `pi_load` to directly `return graph_pi_load_pack(...)`
  instead of storing the result in the original `int ret` stack/local.
  Native CODE changed. The original local was restored.
- `af734d` combined two separately short-circuit tested OK/CANCEL bits
  into one `input_sp & (INPUT_CANCEL | INPUT_OK)` mask. Original CODE
  changed despite similar flags for conventional inputs. The original two
  conditions were restored. Both negative original writer trees remain.

The accepted **modified** input/unchanged PI source pair was independently
compiled and full-linked twice with real Turbo C++ 4.02 at `af734c`:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af734c --units inp_m_w,pi_load
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af734c

Both rounds reproduce **437 original initialized CODE bytes, 64 ordered
native OMF FIXUPP fields, 10 original PUBLIC offsets**, original segment
metadata and real per-source COMENT dependencies, full normal MAIN
EXE/normalized MAP, Japanese 124,642-byte loaded game and all 1,553 MZ
relocations. The separately reviewed standard DOS MZ serializer matches
all 130,882 bytes of the original Japanese MAIN.EXE. 97 other project
objects and original CRT were **reused** rather than cold-rebuilt.

Source proof: `.analysis/work/exatt-layout-af734c/report.json` SHA-256
`9e766527960ca133ae38a6a14ab6498ad536a259077bc52b104f3e449cb91675`.
All native compiler/linker outputs and negative controls are retained.
These are newly directly source-verified physical objects in the current
scoped workflow, **not** additional Factory canonical packed-file accepted
bytes, historical raw vendor OMF packet identity or whole-product source
acceptance. Historical source-proof owner counts are not double-counted.
