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
