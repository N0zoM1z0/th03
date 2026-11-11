# Frame delay: native volatile VSYNC wait

The original `frmdely1` physical owner can express its interrupt-driven wait
as an explicit counter reset followed by a natural `while` loop. The counter
remains volatile and unsigned 16-bit; the signed 16-bit duration parameter
and original comparison order are preserved. No sleep, timeout, input poll,
or second counter reset was added.

Original TC4/TLINK stage `af1179a` matches all 21 CODE bytes, two ordered
native fields, the PUBLIC and complete Japanese MAIN image/relocations in
two independent rounds. Previous operand-reversal and forced-signed counter
variants do not preserve this original instruction stream.

## Current-source native refresh (2026-11-11)

The maintained TH02 `frmdely1` C++ consumed by TH03 now again writes the
volatile counter exactly once before entering a natural `while` loop.
The comparison reads the interrupt-updated unsigned 16-bit counter each
iteration, with the original signed frame parameter and no software tick.
This is source- and compiler-equivalent to the earlier accepted natural
form, not a new physical owner.

Fresh independent `af1352i` compiles the whole leaf in two native TC4
rounds, matching all **21 CODE bytes, two ordered native fields, one
PUBLIC** and both normal MAIN links. Joint `af1352g` independently
verifies the leaf with the complete current Reimu BOSS, without a cold
rebuild. Proof: `.analysis/work/exatt-layout-af1352i/report.json`,
SHA-256 `5534f836ea28c64df331a96341fc047bebe29b55b0ea6cc710ec0c4e5689dc44`.
