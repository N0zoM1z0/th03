# Mima full BOSS pattern controller: native C++ source after630

The real original Mima BOSS translation unit includes nine complete
functions, not only a leaf function: four attack routines, the large
`gba_boss_update_mima` scheduler, intro/split renderers and template
setup. The previous ring-direction initialization branched solely to
write AL with +7 or -7. Genuine Turbo C++ 4.02 emits identical original
bytes from the readable expression:

    _AL = (randring_far_next16_and(1) ? 7 : -7);
    mima_orbit_delta = _AL;

This preserves the original RNG draw, signed eight-bit step and
register ABI, with no embedded assembly bytes or object patches.
The independent v2 source-rooted control `af630b` proved the complete
original object unchanged.

The long `gba_boss_update_mima` switch now names the original 18 attack
modes as Mima-specific spread, random, trail and orbit cases. The shared
scheduler still assigns the same values 2..17; no additional DATA or
change in selection probabilities is introduced. The orbit routine's
direction-initialization and exit frames are named compile-time values,
with the original even-tick test and angle wrap preserved.

The final current-source and OMF dependency-attested native test is:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af630c --units ba_mima
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af630c

Both independently compiled source objects and original TLINK rounds
reproduce **all 1,922 CODE bytes**, **277 ordered native FIXUPP fields**,
**nine PUBLIC offsets** and the original segment definitions. Both full
MAIN ordinary EXEs and normalized complete MAPs match the unchanged
after596 source-native ancestor. The loaded Japanese program, all
1,553 literal ordered relocations, and separately serialized original
130,882-byte Japanese MAIN.EXE agree.

Receipt:
`.analysis/work/exatt-layout-af630c/report.json`,
SHA-256 `286ce126894d568f7669287728cc27a8c0ea7de36303cc16994958fbfb3efd1b`.
The earlier `af630a` attempt to invert Ellen's spread branch changed
the native CODE and was rejected. All evidence lives in scoped ignored
work, with real compiler input paths verified from OMF COMENT records.

This is maintainable source recovery for an existing original owner,
not newly accepted canonical Factory bytes, original historical vendor
OMF packet identity or physical gameplay test coverage.
