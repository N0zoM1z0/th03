# Reimu major BOSS: cloud, mirror and intro render controls

The complete original `ba_reimu` BOSS owner now uses natural remainder
truth tests for the variable cloud volley interval, two-frame cloud
acceleration and sixteen-frame mirrored volley skip. Direction/skip and
rendering opponent predicates use byte-state truthiness, while the
intro's eight-sprite loop advances its signed index with prefix increment.
The three full orbit-burst C++ loops, signed angle division, and the exact
render-mode and hit-test state machine remain in place.

Original TC4/TLINK `af1139c` matched 2,020 CODE bytes, 270 ordered native
fields, nine PUBLICs and the complete Japanese MAIN image/relocations in
both rounds. Two independent negative trials were also completed:
`af1139b` moved the intro sprite index into its for header, and `af1139d`
reordered mirrored-spread termination into an early-return-first path.
Both changed original CODE and were discarded. Neither the floating
render-frame byte mask nor the original mirror branch order was changed.
