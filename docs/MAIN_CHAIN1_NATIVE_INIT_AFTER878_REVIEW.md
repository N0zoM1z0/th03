# TH03 MAIN after878 — complete Chain 1 background owner and particle initialization

The entire original six-function physical `chain1` owner is built here,
including the original near pixel and position helpers, reset, 48-particle
random initializer, two large register-level animation engines and the
shared current `phase.inl`. The original 80 × 16-byte particle pool is
stored externally; the current source does not allocate replacement DATA.

Two genuine natural C++ loop recoveries now replace the 80-slot velocity
reset and the 48-slot randomized sprite initializer: typed `while` loops
preserving exact signed index, near-pointer advances and every RNG/vector2
call. The original X/Y draw ranges now read `TO_SP(640)`/`TO_SP(400)`,
with named 4000-range random auxiliary field, default/alternate sprite
values, and the unchanged conditional additional RNG draw. Chain 1's
32-bit acceleration-to-periodic transition can now use
`round_frame > static_cast<unsigned long>(ACCELERATION_LAST_FRAME)`.
The register-preserving DS:DI/ES hardware loops remain in the original
symbolic register interface; no unsafe generic C++ call convention was
invented for them.

Real original TC4 experiments:
- `af878a`: both typed `for` to `while` changes passed the entire original
  physical unit and normal MAIN linker in both rounds.
- `af878b`: named original subpixel RNG range and auxiliary range; exact.
- `af878c`: attempted to reference a constant in an enum declared *after*
  the reset function. Real Turbo C++ 4.02 **rejected** that C++ source as
  an undefined identifier; the invalid reference was corrected.
- `af878d`: named both true sprite values; complete owner passed twice.
- `af878e`: dropping the explicit `unsigned int` conversion from
  `irand() % 2` **failed** original CODE: candidate 701 vs original 695
  bytes. Original source conversion and RNG behavior retained.
- `af878f`: replacing the 32-bit `round_frame >128UL` with the
  mathematically equal `>=129UL` changed original CODE at offset 411,
  even though initialized length stayed 695. Original comparison restored.
- `af878g/h`: original 128-frame threshold expressed through a named,
  explicitly unsigned-long C++ constant, then current-source explanatory
  comments, twice native exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af878h --units chain1
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af878h
```

Both genuine original TC4 4.02/full normal MAIN TLINK rounds match **695
original CODE bytes, 43 literal ordered native OMF FIXUPP fields, six
PUBLIC offsets**, segment and real OMF compiler-dependency metadata,
complete original normal MAIN EXE/MAP, **124,642 loaded Japanese program
bytes, all 1,553 original MZ relocations** and independent standard MZ
serialization of all **130,882 Japanese MAIN.EXE bytes**. The other **98
original project objects and CRT are reused**, no cold replay or object/
original-target byte patch. Protected source-bound report:
`.analysis/work/exatt-layout-af878h/report.json`, SHA-256
`ba117470eb35b98084ac2ff890098f8b652c180435fd5eebe24554e69773fd08`.
These were historically source-covered original game bytes: new native C++
readability is not new unique CODE or canonical packed Factory acceptance.
