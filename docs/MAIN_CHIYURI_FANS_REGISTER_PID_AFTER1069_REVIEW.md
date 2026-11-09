# TH03 MAIN Chiyuri fan producer: register-qualified PID lifetime (af1069b)

The 528-byte `chiyuri_pattern_fans()` producer now declares its opposite-player
PID as a register local:

```cpp
register pid_t pid_other = (1 - pid_current);
register int i;
```

The four horizontal/vertical fan passes, their two warning-bomb pairs,
per-iteration byte-speed assignment, postfix index progression, signed
multiply/divide-before-`TO_SP` coordinate scaling, mirrored horizontal angle,
and final vertical SELECT transition are unchanged. This is a local lifetime /
register-allocation recovery inside the complete large fan producer, not a
new projectile algorithm or a change to emission order.

## Original-compiler verification

Stage `af1069b` rebuilt the complete `ba_chiyu` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,654 CODE bytes, 381 ordered
native fields and eleven PUBLIC offsets match. Both normal Japanese MAIN
links reproduce the original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1069b/report.json`

SHA-256: `fb64d17e3ad3bc36e02c49e956f0343ccd3174cc1d45946b0920930f4390953f`

Source SHA-256: `2bce7be8094c79b220fb184b843686a18fb3feac2d56ddbd40ad32a49fed04b3`

## Negative controls re-tested against the complete owner

- Initializing the shared `register int i` at its declaration rather than
  leaving initialization to each `for` header changed complete CODE
  (`af1069k`).
- Declaring the same `register int i` in each of the four `for` initializers
  failed under TC4 with duplicate declarations in this function (`af1069d`).
- Giving each loop a distinct register index name compiled but changed the
  complete CODE payload (`af1069e`). The shared signed `i` and the original
  four iteration expressions remain.

The TC4 failures and complete-owner byte comparisons are distinct evidence;
none of the rejected forms is retained in maintained source.


## Superseding current-source fan-loop recovery

The register-qualified `pid_other` remains in the current source. The four
fan passes were subsequently rewritten as natural `while` loops with explicit
speed mutation followed by prefix index increment; see
[the current four-while review](MAIN_CHIYURI_FANS_NATURAL_WHILE_AFTER1069_REVIEW.md).
The latest source binding is `af1069u`, which rebuilds the complete owner in
two original TC4 rounds.
