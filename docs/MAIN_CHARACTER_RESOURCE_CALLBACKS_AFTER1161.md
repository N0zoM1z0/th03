# Character setup: nine exact callback selectors and resource filename bytes

The complete `ch_setup` owner binds nine characters' far-Pascal Extra Attack,
Chargeshot, Gauge, Bomb and BOSS callbacks and installs the matching
background render/reset hooks. Its 12-byte resource filename initialization
now uses a natural `for` loop, while decimal digit updates use C++ compound
`+=` and `%=` operations and an equivalent constant-first radix guard.
The generated nine callback selectors use natural byte `!pid` to choose
player one. No DATA allocation, far pointer width or resource-load order
has changed.

Original TC4/TLINK `af1161f` matches the full 3,888 CODE bytes, all 1,135
ordered native fields, twelve PUBLICs and the Japanese MAIN image plus
ordered MZ relocations in two independent compiler rounds. The successful
sequence `af1161a`–`af1161f` checks each natural rewrite cumulatively.
The two-stage 16-bit division and remainder still occur before the filename
byte stores, so this source spelling does not silently change filenames.
