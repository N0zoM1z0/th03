# Mima Extra Attack: native entity-state rendering and scratch lifetimes

The complete four-function `ex_mima` owner now skips free slots through the
natural `for` continuation in its complete projectile renderer. Its flying
sprite draw returns directly, leaving the other sprite state as the final
path. The 8-bit drawing phase and opponent PID initialize at their first
use, preserving the original near pointers, collision calls and bounce
state. Motion, recoil, and the explicitly unsigned frame-parity remainder
retain their original 16-bit arithmetic and RNG ordering.

Original TC4/TLINK stages `af1306a`, `af1306c`, `af1306d` and final
`af1306e` match the complete 727 CODE bytes, 44 ordered native fields,
four PUBLICs and Japanese MAIN loaded image/ordered relocations in two
independent compiler rounds. An isolated `af1306b` trial narrowed the
complete update loop's signed index; the CODE differed, so that index
keeps its original wider lifetime.
