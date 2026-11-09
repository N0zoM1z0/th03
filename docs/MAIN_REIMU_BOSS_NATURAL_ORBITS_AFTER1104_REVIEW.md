# TH03 MAIN — Reimu BOSS radial traversal and clocks (af1104e)

The full physical `ba_reimu` original Turbo C++ 4.02 owner was rebuilt, not
just a leaf or replacement object. Its three attack-state orbit traversals now
use natural signed-index `for` loops; every byte angle initializes at first use
from the original signed quotient, followed by its ordered polar writes or
Extra Attack creation. Both orbit-cloud angle temporaries also initialize
at first use. The unsigned 16-bit BOSS frame uses prefix increment, and the
cloud acceleration and mirrored-volley clocks use natural `%2` and `%16`.
The hit-render sprite offset is named without changing its placement.

The changes were verified cumulatively at `af1104a` (loops), `af1104b`
(radial angle lifetimes), `af1104c` (cloud angle lifetimes), `af1104d`
(frame increment), and final `af1104e` (clocks/renderer). Each passed two
original TC4/full normal MAIN TLINK rounds with the complete 2,020-byte CODE
owner, all 270 ordered native fields, nine PUBLICs, the original loaded MAIN
image and all 1,553 ordered MZ relocations. The exact current source is bound
to `.analysis/work/exatt-layout-af1104e/report.json`; the original frame
mutation, RNG emissions and original 16-bit division remain in place.
This is local native source improvement, not new canonical Factory credit.
