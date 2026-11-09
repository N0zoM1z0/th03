# TH03 MAIN — Explosion collision leaf: iterator and charge semantics (af1120c)

The original `e_expl` physical Turbo C++ 4.02 translation unit owns the full
`explosions_hittest` collision and chain-reward helper. Its Enemy/Fireball
explosion traversal now uses natural prefix progression for the signed record
index and near pointer, still after every `continue` and matching collision.
A semantic compile-time charge multiplier replaces the three separate
non-pellet matchup constants and the live source multiplier, without changing
original signed integer promotion, score/reward thresholds, or RNG behavior.
This improves the complete routine rather than inserting a byte patch.

Fresh native `af1120a` (iterator) and final `af1120c` (charge semantics)
each passed two independent original TC4/normal MAIN TLINK rounds, matching
all 630 original initialized CODE bytes, 49 ordered native fields, the original
PUBLIC, the full Japanese MAIN loaded image and all 1,553 MZ relocations.
Source-bound final report: `.analysis/work/exatt-layout-af1120c/report.json`.

Two natural alternatives were rejected by direct native compiler evidence:
`af1120b` collapsed the initial enemy/pellet selector into a ternary local
initializer, and `af1120d` narrowed the mutable hit-count byte to its
collision branch. Both changed original CODE. The original byte-frame hit
filter remains an explicit mask, not an unverified byte modulo rewrite.
This native proof is separate from canonical Factory packed-game acceptance.
