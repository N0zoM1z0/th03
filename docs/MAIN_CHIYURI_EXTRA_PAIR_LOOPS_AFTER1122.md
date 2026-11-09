# Chiyuri Extra Attack: native pair-wise control in natural C++

The full four-function `ex_chyu` owner now expresses its two-entity allocation,
beam/flight update, and render traversals with natural `for` loops. The update
is the important recovery: its empty/active `continue` and two-entity flight
paths share the original post-iteration signed index and global entity-pointer
advance. The separate first-pointer advance at `chiyuri_first_done` is
retained; no beam drawing, RNG order or state transition was removed.

Current original Turbo C++ 4.02/TLINK evidence is `af1122c`, matching all 978
CODE bytes, 55 ordered native fields, four PUBLICs and the complete Japanese
MAIN image/relocations in two independent rounds. The accepted `for`-scoped
index was verified after recovering the substantial update control flow.

A further `af1122d` experiment moved `first_arrived` into its conditional
flight path. That changed native CODE and was restored. The register-bound
beam renderer still uses its proven explicit AX/DI machine contract.
