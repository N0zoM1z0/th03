# TH03 MAIN Marisa Chargeshot/Gauge: native 12-sample GRCG and dual volleys after769

The original `cs_mari` physical Turbo C++ translation unit owns **nine
functions** and 1,509 original CODE bytes: Marisa shot/hyper activation,
12-position trailing-beam update, hit testing, the substantial three-band
GRCG renderer and the two 24-frame Gauge attack implementations. This
pass reconstructed natural source in the **whole physical original
module**, not merely individual small calls.

## Accepted source changes

The original 12-sample beam history initialization and signed reverse
update loops, all three GRCG color-band render loops and both five-shot
Gauge projectile-volley loops now use natural local signed `++i` or
`--i`, while retaining all original 16-bit signed array indexing and
GRCG video register/port state. The middle and final rendering bands
start from named original 6/3 sample boundaries. The original
`previous_x != x` gap test, coordinates and color-band tile calls remain
ordered exactly, including the EGC off/on and GRCG setup/cleanup.

The two original Gauge side volleys' vertically accumulated signed
subpixel steps, originally `total_frames * 16`, now use the natural
`total_frames << 4` expression. All other byte mutation, RNG state and
left/right shot angles remain identical. The repeating **24-frame**
Gauge cadence is non-power-of-two and remains `% MARISA_GAUGE_PERIOD`,
not an invalid modulo-to-mask substitution. The two Gauge effect helpers
also now naturally test an active flag with `if(gba_flag_active[...])`.

## Real original TC4 codegen experiments

- `af769a`: first whole-object test with natural signed beam/renderer
  loop increments and Gauge activation checks, all original bytes,
  OMF FIXUPPs and whole normal MAIN image matched twice.
- `af769b`: added both natural subpixel `<<4` Gauge y steps and again
  matched all original code and full link results in both rounds.
- `af769c`: tested changing the mutable **8-bit memory**
  `marisa_chargeshot_p->frame++` into prefix `++...`. Actual original
  native CODE changed. This is a **rejected** experiment; the original
  byte-memory postfix is retained and the failed compiler output kept.
- `af769d`: final maintained source with named GRCG sample boundaries,
  explanatory codegen comment and the accepted natural loops/shift
  was independently compiled again with original TC4 4.02 and full
  normal TLINK twice. Both rounds were original-byte exact.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af769d --units cs_mari
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af769d

Both rounds reproduce **all 1,509 original CODE bytes, all 152 literal
ordered OMF FIXUPP fields, 9 PUBLIC offsets**, original segment/ABI
records, source COMENT dependencies, full normal 99-project-object
MAIN EXE/normalized MAP, 124,642-byte original Japanese loaded game
and all 1,553 original MZ relocation words. The separately validated
standard MZ serialization reproduces the entire 130,882-byte original
Japanese MAIN.EXE; 98 other project objects and CRT were reused, not
cold-rebuilt. No target/code patch or synthetic NOP was added.

Live source receipt `.analysis/work/exatt-layout-af769d/report.json`
SHA-256 `afa1898f29f310f3001c4e03d5710b1961f076d19096328781eef87bc45155b0`.
This represents original-codegen natural C++ recovery of already owned
physical bytes; not new canonical Factory packed-game accepted credit,
vendor raw OMF packet identity or whole-game source ownership.
