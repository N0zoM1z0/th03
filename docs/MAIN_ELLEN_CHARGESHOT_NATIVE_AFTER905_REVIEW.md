# TH03 MAIN after905 — complete Ellen Chargeshot/Gauge, six natural loops

The original physical `cs_ellen` Turbo C++ 4.02 object owns the complete
Ellen Chargeshot/Gauge system: 64 × 12-byte reset, 32-slot staggered RNG
creation, Hyper first-free-slot allocation, active scan with `goto active`,
full deceleration-to-homing target tracking, collision, rendering and
mirrored two-phase Gauge attacks. All ten original PUBLICs and the
external 12-byte projectile layout remain intact.

Six principal full-source loops now use ordinary C++ `while`: 64-slot
reset; 32-slot staggered creation; 32-slot first-active scan with its
original `goto active`; the entire 32-slot deceleration/homing/arrival
update with skip/near-pointer mutations; 32-slot collision hit testing;
and 32-slot sprite rendering. The original first-free Hyper allocator
remains `for/continue/return`, as a fresh real compiler trial proved
that changing it to `while` alters native CODE. Its original RNG draws,
target selection, signed/byte length decay, velocity changes and sound
onset are neither reordered nor newly initialized.

Original compiler trial outcomes, each on the entire physical owner:

- `af905a`: 64-slot reset and staggered 32-slot RNG creation as `while`,
  original whole CODE and complete normal MAIN TLINK exact twice.
- `af905b`: 32-slot hit and render loops with explicit skip pointer/index
  updates as `while`, original TC4/TLINK exact twice.
- `af905c`: original active-index `goto active` pre-scan as natural
  `while`, original full-source CODE exact twice.
- `af905d`: substantial update's real active/homing/arrival traversal
  with a `continue` as natural `while`, original whole CODE exact twice.
- `af905e`: Hyper first-free-slot allocator `for`→`while` compiled
  **1,532** CODE bytes vs original **1,530** (first difference CODE
  segment 4 offset 141). Reverted, no simulated opcode padding.
- `af905f`: byte-valued Gauge `%8 ==0` as natural `if(!remainder)`, exact.
- `af905g`: byte Gauge frame postfix→prefix generated **1,544** vs
  **1,530** CODE, first difference segment 4 offset 1083. Reverted.
- `af905h`: natural `hits = hits + ELLEN_CHARGE_HIT_DAMAGE` with a named
  source enum preserved every original instruction, whole unit exact.
- `af905i`: splitting the comparison's byte `--state` into separate
  decrement/if generated **1,531** CODE bytes vs 1,530 (first difference
  segment 4 offset 253). Original predecrement-in-condition retained.
- Final `af905j`: complete current C++ with explanatory original-ABI
  comments passed **two real independent original TC4 4.02/full normal
  MAIN TLINK rounds**, all original scope exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af905j --units cs_ellen
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af905j
```

Both original compiler/linker rounds reproduce **all 1,530 CODE bytes,
169 literal ordered OMF FIXUPP fields and ten PUBLIC offsets**, actual
source/segment/16-bit near/far ABI, complete normal MAIN EXE/MAP,
**124,642 Japanese loaded program bytes and all 1,553 original MZ
relocations**. Independently verified standard DOS MZ serialization
reproduces all **130,882 original Japanese MAIN.EXE bytes**; not proof of
historical vendor MZ header serialization. **98 other original project
objects and CRT reused**, no whole cold replay, patches or fake NOPs.

Current-source-bound native compiler/TLINK receipt:
`.analysis/work/exatt-layout-af905j/report.json` SHA-256
`a066f1f20bcf437cd266a7f9fc1de42d098fbaebbf3ea1d29cffc5a1bccf6dc6`.
Previously source-owned CODE, **not new distinct original CODE, raw
vendor packet identity or canonical Factory packed-game credit**.
