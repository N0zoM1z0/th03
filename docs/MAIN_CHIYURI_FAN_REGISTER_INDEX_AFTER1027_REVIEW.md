# TH03 MAIN Chiyuri fan generator: explicit SI loop index

`chiyuri_pattern_fans()` now declares its common loop index as a register
local:

```cpp
pid_t pid_other = (1 - pid_current);
register int i;
```

The original function is 528 bytes. Its four fan passes all initialize and
increment the same signed word index. The original machine code uses `SI`
(`XOR SI,SI`, `MOV AX,SI`, `INC SI`, and `CMP AX,SI`) for these loops, while
the PID scratch value is kept separately in the one-byte BP local. The
explicit register declaration records that recovered allocation without
changing any of the four pass bodies or their order.

Stage `af1027a` rebuilt the complete `ba_chiyu` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,654 CODE bytes, 381 ordered
native fields and eleven PUBLIC offsets match. Both normal MAIN links
reproduce the original Japanese loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1027a/report.json`

SHA-256: `4831911bcd1daf29ea9c74da9f72cd1ebb5c9e9b344bad02495ff6710ea9e03e`

## Rejected horizontal two-pass factoring

Stage `af1027b` tested replacing the two horizontal ascending/descending
passes with one outer `speed_pass` loop and a conditional speed update inside
its inner loop. The complete `ba_chiyu` CODE payload differed, so the factoring
was reverted. This confirms that preserving the same projectile order and
speed sequence is not enough to preserve this TC4 code shape. The two explicit
passes remain until a different disassembly-led natural form is found.
