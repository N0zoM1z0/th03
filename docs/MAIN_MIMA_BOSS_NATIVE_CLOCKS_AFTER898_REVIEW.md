# TH03 MAIN after898 — complete Mima major BOSS native attack and render controls

The entire original **nine-function `ba_mima`** Turbo C++ 4.02 physical
BOSS is compiled together here: BOSS template, four full bullet/aimed/
trail/orbit controllers, mode/collision scheduler, masked sprite renderer,
polar-split 2-half sprite and render dispatch. Its externally allocated
shared-BOSS and private DGROUP state remain untouched.

The two distinct *unsigned 16-bit* random-bomb and six-frame supporting
pellet clocks now use natural C++ `if(!(boss_frame % PERIOD))`, with
original bullet/audio ordering preserved. The original **56×56 collision
tile**, signed 32-pixel hit radius, 144×112 full sprite, 64×80 damaged
sprite and true signed (72,40)-pixel placement margins have named
compile-time C++ geometry. The original `goto render_mode_2` and
separate modes 2/5 remain: collapsing them was codegen-unequal in an
earlier original-native experiment. All three real GRCG mask planes
(0xAAAA, 0x5555, 0xFFFF) and far-pascal ABI stay unchanged.

## Fresh real original TC4 compiler experiments

- `af898a`: both unsigned boss modulo zero tests became natural C++
  `if(!remainder)`, and the whole original BOSS and normal MAIN were
  exact in *both independent genuine TC4/TLINK rounds*.
- `af898b`: replacing the compound signed byte-orbit rotation
  `mima_orbit_angle += mima_orbit_delta` with explicit assignment
  `angle = angle + signed_delta` emitted **1,924** initialized CODE
  bytes vs original **1,922**, first discrepancy segment 4 offset 788.
  Original compound byte mutation restored.
- `af898c`: named the actual 56×56 collision geometry, 32-pixel hit
  margin and normal/hit sprite dimensions/placement. Both complete
  original compiler/linker rounds remained exact.
- `af898d`: replacing two live **byte interval `/2`** calculations
  with `>>1` generated **1,908** CODE bytes vs original **1,922**,
  discrepancy segment 4 offset 589. Original promoted division retained.
- `af898e`: changing the mutable byte `boss_render_frame++` to prefix
  generated **1,926** CODE vs original **1,922**, first difference
  segment 4 offset 1392. Original postincrement restored.
- Final `af898f`: current complete maintained C++ and compiler-specific
  source comments recompiled through real original TC4 4.02 and full
  normal MAIN TLINK **twice**, original-exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af898f --units ba_mima
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af898f
```

Both original native compiler and normal full linker rounds match
**all 1,922 CODE bytes, 277 literal ordered native OMF FIXUPP fields,
9 PUBLIC offsets**, original source/segment/DGROUP/16-bit ABI, complete
original normal MAIN EXE and normalized MAP, **all 124,642 Japanese
loaded program bytes and 1,553 ordered MZ relocations**. Independent
verified standard DOS MZ serialization recreates all **130,882 bytes
of the pinned Japanese MAIN.EXE**. **98 other original project objects
and CRT reused unchanged**, no full cold replay, target/OBJ patches,
NOP padding, byte-array-code substitution or weakened source guards.

Protected authentic source-bound two-round original compiler/TLINK proof:
`.analysis/work/exatt-layout-af898f/report.json`, SHA-256
`aac7736945aa4e54ade94c39489ad3970545474e7420c9c445042f9c23724641`.
Already source-owned game CODE; native C++ improvements are **not
new distinct original bytes, vendor raw OMF identity or canonical
Factory packed-game acceptance**.
