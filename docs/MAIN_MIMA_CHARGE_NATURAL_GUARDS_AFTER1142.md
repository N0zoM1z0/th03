# Mima Chargeshot: active-state guards and complete six-loop native traversal

The original 30-projectile `cs_mima` owner now uses prefix near-pointer
increments in all reset, allocation, movement, collision and rendering loops.
Both complete active-state controllers (update and render) use early-return
guards rather than nesting the full work in conditional blocks. The byte
update frame initializes at first use, as does the render sprite offset.
The release, ring and double-ring Gauge periods use natural byte remainder
truth tests, without replacing their codegen-sensitive division with masks.

Original Turbo C++ 4.02 and normal MAIN TLINK at `af1142d` reproduced all
1,338 CODE bytes, 150 ordered native fields, ten PUBLICs and the complete
Japanese MAIN image plus MZ relocations in both independent rounds.
