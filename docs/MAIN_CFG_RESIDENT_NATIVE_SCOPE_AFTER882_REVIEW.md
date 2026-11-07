# TH03 MAIN after882 — original resident CFG leaf and external filename ABI

The real original physical `cfg_lres` Turbo C++ 4.02 translation unit
owns one 49-CODE-byte `resident_t __seg* near cfg_load_resident_ptr()`
entrypoint. It allocates the original local `cfg_t` scratch record and
returns the real `cfg_load_and_set_resident(cfg, CFG_FN)` result. The
filename symbol is an original **external constant**, not newly
allocated program DATA.

The maintained source now naturally declares `extern const char
CFG_FN[]` at **file scope**, immediately following the necessary
`#undef CFG_FN` from the historical header. This emits exactly the
same original native linker symbol and full original CODE as the
function-local extern spelling, without changing segmented resident
pointer ABI or introducing an extra call. The cfg scratch is
intentionally **not zero initialized**: this source is measured against
the original compiler, not automatically cleaned up.

Genuine original compiler trials:

- `af882a`: moved the filename symbol to natural file scope; both
  original TC4/full normal MAIN TLINK rounds match original CODE.
- `af882b`: declared an extra local return pointer with explicit
  `near` after the segment-pointer modifier; the actual historical
  TC4 4.02 parser rejected that local declaration as conflicting type
  modifiers. The invalid C++ candidate was not accepted.
- `af882c`: used a valid, default-near segment-pointer local result,
  then returned it. Real TC4 generated **53 original CODE bytes**
  versus original **49**, altering stack/register codegen; reverted.
- `af882d`: initialized the real local scratch as `cfg_t cfg = {0}`.
  Actual TC4 generated **74** initialized CODE bytes versus original
  **49**, with original CODE offset 5 changed. The original uninitialized
  scratch variable was restored; no speculative initialization.
- Final `af882e`: direct return, true original scratch lifetime and
  natural file-scope external symbol declaration. Both independent
  original compiler/normal full MAIN linker rounds exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af882e --units cfg_lres
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af882e
```

Both rounds reproduce **all 49 original CODE bytes, six literal
ordered native OMF FIXUPP fields and one PUBLIC offset**, physical
source/segment/ABI, complete original normal MAIN EXE and normalized
MAP, **124,642 Japanese loaded program bytes and all 1,553 original
ordered MZ relocations**. Independently verified standard DOS MZ
serialization reproduces all **130,882 bytes** of the original
Japanese MAIN.EXE; it is not historical vendor header serialization.
The **98 other unchanged original game project objects and Borland CRT
were reused**, no full cold replay, patched source/target buffers or
extra data owner.

Protected genuine two-round original compiler/TLINK/source report:
`.analysis/work/exatt-layout-af882e/report.json`, SHA-256
`8e4809810468206f04facf9ff1df145f6f21f3d04582ef33ef40c423ea72155a`.
This original leaf was already source-covered; it does not add distinct
original CODE bytes or canonical Factory packed-file accepted credit.
