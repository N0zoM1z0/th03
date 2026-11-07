# TH03 MAIN Kotohime: full BOSS intro/ring flicker and attack state native C++ (after731)

The complete original `ba_koto` physical translation unit contains **eleven
BOSS functions**, including the full boss update/collision dispatcher,
random/aimed ring emitters, five-arc pellet attacks, nested radial-burst
projectiles and both main/entrance ring renderers. These are not independent
leaf-only compiler outputs. The original 1,840-byte MAIN_03_TEXT CODE,
262 ordered native FIXUPP fields and 11 PUBLICs are compared as a whole.

## Newly recovered C++ controls

- The original 16-bit boss frame intro transition (`0x64`) and arrival
  blink ending (`0x40`) are now named, while `round_frame_mod2` uses its
  original direct unsigned-byte truth test.
- The ring renderer's unsigned **four-frame, first-two-frame** flicker now
  uses natural mask arithmetic instead of `%4`, with separate phase/period
  constants. Its `boss_render_mode == 2` and sprite offset effects remain
  in the original order.
- The five-arc attack's four-pellet ring count and eight-sprite entrance
  renderer count are named compile-time values, and entrance/explosion
  branches use the actual original Kotohime mode enum.

## Actual compiler experiments and constraints

Two alternative *deeper* C++ refactors were separately tested and rejected:

- `af731a`: replaced both ring attacks' byte `_AL` load/add/store with a
  local `unsigned char next_phase` and ordinary `+= 2`. This lengthened
  native CODE by eight bytes, so the explicitly modeled original AL
  lifetime/assignment remains necessary.
- `af731b`: wrote each ring pellet's returned polar coordinate directly
  into `bullet_template.center` instead of preserving `int x, y` locals.
  The original codegen changed, demonstrating that apparently redundant
  two-register intermediate values cannot be removed blindly.

These failed experiments remain in their original compiler writer stages;
no target/object patch was attempted. `af731c` restored these original
register/lifetime patterns while applying the phase, mask and mode C++
changes above. Both genuine original **Turbo C++ 4.02** compiler/full
normal MAIN TLINK rounds pass:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af731c --units ba_koto
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af731c

All **1,840 original CODE bytes, 262 literal ordered OMF FIXUPP fields,
11 PUBLICs and complete segment definitions** match. The complete
source-native normal MAIN EXE and path-normalized MAP match; the original
124,642-byte Japanese loaded program and all 1,553 ordered relocations
match in both rounds. Independent standard MZ serialization reproduces
all 130,882 bytes of original Japanese MAIN.EXE, without asserting that
the original historical TLINK emitted the same header. The other 98
original project objects and CRT are reused; no cold replay.

Current-source two-round receipt:
`.analysis/work/exatt-layout-af731c/report.json` SHA-256
`9c6d581d021029a18a450b56f6820271f915f4b21585a991b780f95da7fa2850`.

This is stronger natural C++/fresh source-bound proof for an already
owned large BOSS object; no canonical packed-file Factory credit, vendor
raw OMF packet equality or entire-game completion claim is added.
