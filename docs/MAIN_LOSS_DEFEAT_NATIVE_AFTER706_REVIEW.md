# TH03 original loss update, particle ring and winner banner: source-native after706

The full original `lose` physical Turbo C++ 4.02 project object
owns four complete original functions, **664 CODE bytes**, 61 literal
ordered native FIXUPP fields and four PUBLIC offsets. Its large
`player_lose_anim_update` handles the loss-to-round-complete
transition, palette/frame shakes, score and winner accounting;
the companion near player renderer draws three 16-particle rings
and the defeat-banner leaf renders the frame-dependent winner bounce.

The genuine full source TU is `src/main/player/lose.cpp` and
contains its function bodies in maintained `lose_update.inl`,
`lose_particle.inl`, `losedraw.inl` and `defeat.inl`.
The original TLINK MAP module really is
`src/main/player/lose.cpp`, not an invented `th03/lose.cpp`.

The scoped original-source driver and independent reviewer now force
the *current maintained .inl file bytes* into their actual original
Turbo C++ source graph and verify every path from the emitted OMF
COMENT dependencies. Compiling unchanged sources first (`af705e`,
`af706a`, `af706c`) reproduced the original physical object,
full normal MAIN/MAP and Japanese relocations before source edits.
The driver separately supports the 3,135-CODE-byte core player owner
at the actual `probe/af593p` original TLINK source slot;
its `hyper.inl` source was likewise explicitly bound and checked.

Real maintainable C++ changes now proven with full original compiler
output:
- The defeat banner uses a natural unsigned
  `round_or_result_frame % 32` for its 16+16-frame vertical
  bounce instead of an authored `&31` (`af706b`).
- The original loss timer updater's alternating 30-level palette
  uses an unsigned `round_or_result_frame % 2` rather than
  a frame bitmask (`af706d`).
- The completion/round-win transition checks the original
  countdown using ordinary `if(!player->lose_anim_time)`,
  preserving the frame where the winner is actually credited
  (`af706f`).
- Three separate 16-iteration loss particle rings now use
  `++_DI` while retaining the original DI register-bound
  loop and polar angle advancement (`af706g`).

Negative control: Replacing the 8-bit
`(player->lose_anim_time & 3) < 2` shake gate with explicitly
unsigned modulo four changed native TC4 CODE (`af706e`);
the original mask remains. No defensive initialization or
alternate winner transition was introduced.

Final actual-source/OMF-COMENT-attested two-round original
TC4/TLINK native proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af706h --units lose
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af706h

Both rounds reproduce **all 664 original CODE bytes, 61 ordered
literal native fixups, four PUBLIC offsets**, complete OMF
segments/ABI, the original normal MAIN EXE and normalized whole MAP,
the original 124,642-byte Japanese loaded program, 1,553 ordered MZ
relocations and independently serialized exact original 130,882-byte
Japanese MAIN.EXE. The other 98 original project objects and
startup/CRT libraries were reused.

Retained real compiler and source evidence:
`.analysis/work/exatt-layout-af706h/report.json`,
SHA-256 `794ce3eceafd37dc44a0875d39cf142d160a907d10e17a03ba81f5934b7f605b`.
No whole cold replay, object patch or new canonical Factory
packed-game acceptance is claimed.
