# Marisa BOSS: intro return, ring cadence and column phases

The complete `ba_maris` physical owner now expresses the 0x64-frame intro
as an unfinished-state early return, preserving the subsequent selector,
attack dispatch, collision and renderer. The 32-frame orbit ring uses
natural unsigned-word zero remainder. Both wide and narrow column controllers
retain the four distinct paired-Extra-Attack call sites, with native-exact
constant-first terminal frame guards; the template's player-side condition
uses byte truthiness.

Original TC4/TLINK `af1144c` reproduces the entire 1,431-byte CODE owner,
199 ordered native fields, nine PUBLICs and the Japanese MAIN loaded image
and relocations in two rounds. A separate experiment `af1144d` made the
spread attack's finish path an early return; that visibly changed TC4 CODE
and was reverted. The original packet and caller effects remain untouched.
