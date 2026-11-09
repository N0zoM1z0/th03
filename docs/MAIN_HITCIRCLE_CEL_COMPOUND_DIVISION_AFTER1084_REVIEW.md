# TH03 MAIN HitCircle cel: natural compound self-division (af1084p)

The 445-byte `hitcirc` owner contains four functions and the inline
`HitCircle::cel()` member used by the renderer. This pass replaces the
redundant explicit self-assignment with the natural compound assignment:

```cpp
_BX = (age - 1);
_BX /= HITCIRCLE_FRAMES_PER_CEL;
_BX *= HITCIRCLE_VRAM_W_PER_CEL_TERM;
return (SO_HITCIRCLE + _BX + _BX + _BX);
```

The expression is intentionally still written through `_BX`. The complete
cel calculation uses the original BX/AX round-trip for unsigned division,
then the named VRAM stride term and three BX additions. It preserves the
renderer allocation in which SI is the near-record pointer and DI is the
signed enemy loop index. Replacing the sequence with an ordinary local,
a direct scaled expression, a shift, or a single multiply-by-six has already
been tested and changes code generation or register allocation.

## Isolated original-toolchain result

Stage `af1084n` rebuilt the complete `hitcirc` physical owner in two
independent original Turbo C++ 4.02 rounds. All 445 CODE bytes, 30 ordered
native fields and four PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations. The source
overlay independently checked the maintained `hitcircle.cpp` producer.

Report: `.analysis/work/exatt-layout-af1084n/report.json`

SHA-256: `7a7f948b1849023be10bb5c20e483c6d64f40d16eb13e0a8236de5af8bf79250`

Current `hitcircle.cpp` SHA-256:
`ad008ef753ebf1ae30b52e90730ce25757c0057a810dd9192fa9c503563ac503`

## Seven-owner integration

Stage `af1084p` rebuilt the current `hitcirc` source alongside
`ba_koto`, `ba_reimu`, `ba_yumem`, `ba_chiyu`, `ex_rfly` and `ex_reup` in two
independent original TC4 rounds: 10,473 CODE bytes, 1,359 ordered native
fields and 55 PUBLIC offsets match. Both normal Japanese MAIN links reproduce
the original loaded image and ordered MZ relocations. All seven source hashes
are recorded in the protected report.

Report: `.analysis/work/exatt-layout-af1084p/report.json`

SHA-256: `92ce981cad470a6faeccddc87742e915c2483e567034f145eb148a38c495bcef`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.
