# Ellen major BOSS: intro exit and attack-phase guards

The complete original `ba_ellen` owner now uses a natural early-return
guard for unfinished intro frames. Both unsigned-word two-frame spread
gates use truthy remainder tests while retaining the original
`fire_single`/`done` branch labels and eight-shot volley call sequence.
The template's player-side test uses natural truthiness; the pellet-pattern
termination is expressed by a constant-first frame comparison. Ring bursts,
random-angle order and the three render-strip lookup sequences are unchanged.

The final source-bound Turbo C++/TLINK stage `af1145c` reproduces all
1,675 original CODE bytes, 213 ordered native fields, nine PUBLICs, the full
Japanese MAIN loaded image and every ordered MZ relocation in two separate
native compiler rounds.
