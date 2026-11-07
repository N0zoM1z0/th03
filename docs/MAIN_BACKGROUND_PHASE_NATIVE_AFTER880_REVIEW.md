# TH03 MAIN after880 — one real shared periodic phase, two original background owners

The live `src/main/background/phase.inl` is included **inside both**
substantial original Chain 1 and Chain 2 periodic particle renderers.
Every actual compiler trial here simultaneously rebuilt **both full
physical original objects** (`chain1` and `chain2`), not merely a
standalone state-machine fragment. Both already maintained complete
native code for the CPU/PC-98 ES:DI graphics interfaces; no unsafe
register-to-ordinary-argument conversion was invented.

The current natural C++ phase is now expressed as:

- `frame = round_or_result_frame % BG_PHASE_FULL_PERIOD`, where the
  global is **already unsigned 16-bit** and the result is assigned to a
  signed 16-bit local frame; no redundant extra cast is required.
- All **eleven original six-phase/tick boundary values** (4096, 1024,
  1280, 2048, 2304, 3072, 4064, 8, 4, 127, 64) are named as local
  compile-time C++ enum constants, without creating additional DATA.
- The 8- and 4-frame rotation ticks now use natural
  `if(!(static_cast<unsigned int>(frame) % PERIOD))` truth predicates.
- The original **signed-local** `frame & 127` then `<64` direction-wave
  check and both `goto` destinations remain intact. The real original
  `changed` byte remains **intentionally uninitialized on 416 phase
  paths**: this is target/compiler behavior, not portable defined C++
  and not a license to initialize, merge or eliminate its read.

## Real original compiler trials on both complete objects

- `af880a`: omitted redundant explicit unsigned cast on the **already
  unsigned global** before `%4096`; both original physical owners and
  complete normal MAIN link matched in both genuine TC4 rounds.
- `af880b`: omitted the unsigned cast on the **signed local** before `%8`.
  Original Chain 1 generated **702** CODE bytes versus its true **695**
  (first mismatch CODE segment 4 offset 459). Rejected; explicit unsigned
  cast stays. This is not equivalent to the global-clock case.
- `af880c/d`: changed the 8-frame and then 4-frame zero remainder
  checks to natural `if(!remainder)` with explicit unsigned cast.
  Both full original objects remain byte-exact in both native rounds.
- `af880e`: changed the signed-local 128-frame direction wave to an
  explicitly unsigned `%128` and `<64` test; **Chain 1 CODE changed at
  offset 520** (although 695 initialized bytes still existed). Rejected.
- `af880f`: introduced all eleven typed original phase/period/angle
  constants, preserving original register/branch paths. Both source
  owners and full MAIN remained exact in both original compiler rounds.
- `af880g`: replaced original `(frame & 127)<64` with an apparently
  equivalent `!(frame & 64)`. TC4 generated **690** Chain 1 CODE bytes
  instead of **695**. The original mask and comparison were restored.
- Final `af880h`: corrected comments, precise original signed/unsigned
  semantics and authentic current shared include, two independent
  real original compiler/full normal MAIN TLINK rounds exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af880h --units chain1,chain2
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af880h
```

| Full original physical TU | CODE | Literal ordered native FIXUPPs | PUBLICs |
| --- | ---: | ---: | ---: |
| `chain1`, six functions | 695 | 43 | 6 |
| `chain2`, three functions | 550 | 43 | 3 |
| **Together, in each real TC4/TLINK round** | **1,245** | **86** | **9** |

Both actual rounds reproduce these original full physical object CODE,
fixups, PUBLICs, OMF dependency provenance for **both current
background files and current `phase.inl`**, entire original normal MAIN
EXE/MAP, **124,642 Japanese loaded program bytes** and all **1,553
ordered MZ relocations**. Independent standard MZ serialization also
recreates the **130,882-byte original Japanese MAIN.EXE**, not
historical vendor direct header-byte identity. **97 other original game
objects and Borland CRT reused**, no all-project cold replay, object
patches, code padding, target buffer substitution or weakened source
binding. Protected native source/OBJ/EXE/MAP/TLINK report:
`.analysis/work/exatt-layout-af880h/report.json`, SHA-256
`85003c4708f0d0a1d249fc3f88ec4be6ab27e974d681ebb22e0947b767a74805`.

These original CODE bytes were already historically source covered.
This is live-source and codegen fidelity improvement, **not additional
unique original CODE ownership, raw historical vendor OMF packet
identity or canonical Factory packed-unit acceptance**.
