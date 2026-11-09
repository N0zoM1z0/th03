# TH03 MAIN HitCircle cel calculation: register-allocation experiments

The original inline `HitCircle::cel()` sequence is intentionally kept in the
`_BX` compiler-register form. The renderer's target uses SI for the record
cursor, DI for the twelve-enemy loop index, and BX for the intermediate cel
calculation. The cel expression zero-extends the byte age, decrements AX,
shifts the unsigned word by two, multiplies by two, adds the result twice, and
adds the sprite base.

Several natural-local rewrites were compiled against the complete `hitcirc`
owner and rejected:

| Stage | Source form | CODE bytes | Differing bytes |
| --- | --- | ---: | ---: |
| `af1029a` | signed `int cel` local | 461 | 162 |
| `af1029b` | `register int cel` local | 453 | 194 |
| `af1029c` | `register unsigned int cel` local | 447 | 186 |
| `af1029d` | ordinary `unsigned int cel` local | 455 | 153 |
| `af1029e` | register local moved into renderer | 445 | 156 |
| `af1029f` | same local, declaration order reversed | 445 | 156 |
| `af1029h` | `_BX >>= 2` instead of unsigned `/ 4` | 437 | 145 |

The signed local selects `IDIV`; unsigned locals select `SHR` but take DI or a
stack slot, displacing the target's DI loop index or changing the target's BX
traffic. Moving the local to the renderer and reversing declaration order
still leaves the loop counter on the stack and the cel temporary in DI. The
shift form changes both code size and instruction selection. All experiments
were reverted; the maintained `_BX` division form remains the only tested
source form that reproduces the target's complete code.


## Independent current-source re-tests (af1068b/c/f/i/j)

The maintained `_BX` expression was re-tested against the current complete
`hitcirc` owner. Four distinct natural C++ rewrites were compiled and rejected:

- `af1068b`: `register unsigned int frame = age; --frame; frame /= 4;
  frame *= 2; return base + frame + frame + frame;`
- `af1068c`: a register word initialized from `age - 1`, divided by four,
  then multiplied by the complete six-column VRAM width.
- `af1068f`: the same division/multiplication as one direct return expression,
  without a local register variable.
- `af1068i/j`: a register `cel` local with either three explicit stride terms
  or the original staged divide/multiply/three-add expression.
- `af1068l`: a register monochrome-color local replacing the explicit DX
  setup and word-sized AND; the complete CODE comparison differed.
- `af1068u`: pass `p->cel()` directly as the final `sprite16_put()` argument
  in both enemy and player paths, removing the shared sprite-offset local;
  complete CODE differed.
- `af1068v`: use a `register int cel` local with the staged age decrement,
  divide, multiply-by-two and three-add return; complete CODE differed.

Every complete CODE comparison in the listed local-variable, shift,
scaled-accumulation and direct-return trials differed, and those experiments
were restored. The earlier signed/unsigned local, register-order and shift
trials remain negative controls. The accepted register-bound alternatives are
the original `_BX = (_BX / HITCIRCLE_FRAMES_PER_CEL)` self-assignment and the
later natural `_BX /= HITCIRCLE_FRAMES_PER_CEL` compound form.

## Current natural compound self-division (af1084n)

The current source replaces the redundant self-assignment with the more
natural compound operation:

```cpp
_BX = (age - 1);
_BX /= HITCIRCLE_FRAMES_PER_CEL;
_BX *= HITCIRCLE_VRAM_W_PER_CEL_TERM;
return (SO_HITCIRCLE + _BX + _BX + _BX);
```

This is not a C local-variable rewrite: the intermediate remains bound to BX,
so the original compiler register allocation and the renderer's SI/DI
lifetimes are preserved. Stage `af1084n` rebuilt the complete 445-byte
`hitcirc` owner in two original TC4 rounds: all 445 CODE bytes, 30 ordered
native fields and four PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered relocations, and the current
source overlay checked the live `hitcircle.cpp` producer.

Report: `.analysis/work/exatt-layout-af1084n/report.json`

SHA-256: `7a7f948b1849023be10bb5c20e483c6d64f40d16eb13e0a8236de5af8bf79250`

Current `hitcirc` source SHA-256:
`ad008ef753ebf1ae30b52e90730ce25757c0057a810dd9192fa9c503563ac503`

A fresh exploratory Ghidra disassembly at `0x1B80B` independently shows the
renderer computing `((age - 1) >> 2) * 6 + 0x1910`; the inlined sequence uses
AX/BX, a word shift, signed `IMUL` by two and two additions. This provider
reported `attestation.status=not-checked` and `exactness_credit=none`, so this
is semantic investigation only, not an accepted Factory Oracle result.
