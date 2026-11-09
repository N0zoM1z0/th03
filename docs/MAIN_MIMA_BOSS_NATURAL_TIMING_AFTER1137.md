# Mima BOSS: native intro exit and attack cadence

The complete Mima BOSS physical owner now handles the unfinished intro
through a natural early-return guard. Its spread, random-bomb and orbital
attacks use natural zero-remainder checks for the original 16-bit even,
four-frame and six-frame clocks. All RNG draws, projectile groups, sounds,
visual state transitions and full collision/render procedures retain their
original order; byte-local timing and the register-sensitive mode-5 renderer
entry remain unchanged.

Fresh source-linked original TC4/TLINK `af1137b` reproduces all 1,922 CODE
bytes, 277 ordered native fields, nine PUBLICs and complete Japanese MAIN
image/relocations in both independent rounds. A separate `af1137c` trial
flattened the random-bomb warning branch into two successive `if` guards;
although equivalent for frame values, it changed target CODE. That variant
was restored, retaining the earlier branching.
