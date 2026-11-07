# Kotohime full BOSS attacks: native angle updates and mode recovery (after637)

The original Kotohime BOSS translation unit contains eleven functions
and four substantial attack patterns: expanding random ring, aimed
double ring, periodic pellet arc and radial nested burst. This native
source refinement keeps the original RNG/distance/division order and
retains the 16-bit sprite renderer's signed AX shift contract.

Three real natural C++ changes compile to original machine code:

- The aimed ring's 8-bit angle update and the radial burst's follow-up
  decrement now both use `boss_move_phase -= 2` instead of staging
  the original 0xFE adjustment via AL. Independent source-rooted
  compiler tests `af637b` and `af637c` verified each rewrite.
- The ring renderer's original 4-frame flicker mask
  `((boss_frame & 3) < 2)` now uses
  `((boss_frame % 4) < 2)`. Turbo C++ lowers this modulo to
  the same native 16-bit mask/test instructions (`af637a`).

The original `_AL += 2` in the random ring and
`_AL += (unsigned char)0xFC` at radial start are *not* replaced
by direct C++ additions/subtractions: controls `af637e` and
`af637d` changed CODE byte content. These failed variants were
rejected, not padded or patched.

The 18 original scheduler byte modes now have Kotohime-specific
names and map to random ring (2..6), aimed ring (7..9),
pellet arc (12..14) and radial burst (10/11/15..17).
The common ring expansion threshold 0x400, first frame 1 and
release after 0x40 are named; pellet arc release/finish timings
are likewise compiler-time constants. No source-level
runtime table or DATA/BSS ownership change was introduced.

The final two original Turbo C++ 4.02 compiler/TLINK rounds
used forced, OMF-COMENT-attested source paths:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af637f --units ba_koto
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af637f

All **1,840 original CODE bytes, 262 literal ordered FIXUPP fields,
11 PUBLIC offsets**, complete original segment metadata, both full
normal MAIN EXEs and normalized MAPs match. Both Japanese program
images and all **1,553 ordered MZ relocations** match, and the
separate standard MZ serialization reproduces the complete original
130,882-byte Japanese MAIN.EXE.

Retained two-round evidence:
`.analysis/work/exatt-layout-af637f/report.json`,
SHA-256 `727c24abadf5b0ad2799b195375cf5c62154975c5cdec0c38380a3a22f9b4a9e`.
Other 98 project objects and startup libraries were reused
unchanged, no full cold replay was run.

This is better natural source over previously owned game CODE, not
new Factory packed-byte credit, historical vendor raw OMF packet
identity or real-hardware runtime proof.
