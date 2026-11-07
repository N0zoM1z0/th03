# TH03 MAIN full CPU collision/target/retry source: original-native after714

The complete four-function `p_cpu` original physical source was improved,
not merely its small direction-choice leaf. The 3x3 collision direction
selector now gives named **subpixel-space** field boundaries (left/right,
low playfield, floor and vertical collision bands). The pursuit and long
careful-mode movement paths use consistent horizontal and vertical target
margins and explicit second-chance retry-region boundaries. Cautious movement
retains its original 8-direction plus neutral movement lattice and signed
`int8_t` collision probe/retry counter.

Named conditions express the two **different** bomb charge thresholds
(0x500 after a direct target hit versus 0x400 after exhausted dodge
retries), the 3-region **unused but still actually executed RNG division**,
the random-bomb period 4, the first/retry collision radii, and the two
alternate dodge strategies. Replacing the original discarded RNG division
with no operation, swapping the search order or changing bounded retry
writes would have changed semantics. We kept them. The old tested
signed-byte probe-loop bound and original postincrement sequence are
untouched because prior native negative controls rejected cosmetic changes.

Natural zero-truth checks `if(player->cpu_dodge_strategy)` and
`if(!attempt)` replace verbose zero comparisons without altering the
whole original codegen. Nothing was rewritten into an approximate
high-level navigation algorithm.

Current physical source provenance and two independent original Borland
TC4 4.02 compiles and full normal MAIN link were verified solely for the
changed `p_cpu` object (other original 98 project objects/CRT reused):

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af714a --units p_cpu
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af714a

Both compiler rounds match all **1,077 CODE bytes**, **64 literal ordered
OMF FIXUPPs**, **4 original PUBLIC offsets**, entire segment definitions,
normal linker EXE/MAP, original Japanese loaded game image and all **1,553
ordered relocations**. Independently serialized original 130,882-byte
Japanese MAIN.EXE file equality also passes.

Evidence: `.analysis/work/exatt-layout-af714a/report.json` SHA-256
`6c5918f5474f30b754026e2d3d1ddd0fde56ca3629931ffc5092057316a1d3e2`.
The actual native writer outputs, logs and source-dependent OBJ are retained.
This is a more natural source representation, not additional canonical
packed-game Factory acceptance or proof of full-source completion.
