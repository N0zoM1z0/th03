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

Every complete CODE comparison differed, and every source experiment was
restored. The earlier signed/unsigned local, register-order and shift trials
remain negative controls; the maintained `_BX` sequence is still the only
source form verified against the full 445-byte owner by the available local
TC4 probe.

A fresh exploratory Ghidra disassembly at `0x1B80B` independently shows the
renderer computing `((age - 1) >> 2) * 6 + 0x1910`; the inlined sequence uses
AX/BX, a word shift, signed `IMUL` by two and two additions. This provider
reported `attestation.status=not-checked` and `exactness_credit=none`, so this
is semantic investigation only, not an accepted Factory Oracle result.
