# TH03 MAIN after851: exact original 16-bit Gauge saturation leaf

This verifies the **complete original 55-byte** physical `p_gauge`
Turbo C++ translation unit, not a fabricated per-function substitute.
The C++ source's actual `gauge_avail_add(pid, uint8_t charge)` now
naturally **combines the original Hyper-active and already-full-gauge
guards with a short-circuit `||`**, preserving their shared original
return address and unchanged 16-bit memory semantics. The original
source updates `p.gauge_avail` with a **compound memory `+= charge`**,
then independently saturates at the physical `GAUGE_MAX=0xFF0`. That
post-add clipping is not equivalent in codegen to merging operations.
The maintained source also asserts its original 16-bit Gauge value,
8-bit charge and saturation value at compile time with file-scope
`typedef char[...]` constraints supported by the historical compiler.

Actual original native experiments:

- `af851a`: merged early-return conditions via natural C++ `||`;
  two genuine original TC4/complete normal MAIN TLINK rounds exact.
- `af851b`: replacing the original `p.gauge_avail += charge` with an
  explicit `p.gauge_avail = p.gauge_avail + charge` failed the real
  original CODE comparator (**58** candidate vs **55** original bytes).
  It was reverted without byte patches.
- `af851c`: replacing post-add `> GAUGE_MAX` with mathematically
  equivalent `>= GAUGE_MAX + 1` also failed original CODE comparison
  (the initialized size remained 55), so the original strict `>` stays.
- `af851d`: a trial file-scope C++ `static_assert` declaration was
  rejected by the actual TC4 parser. The final file-scope `typedef char`
  compile-time ABI constraints use the authentic legacy grammar instead.
- Final `af851e`: the entire maintained current source recompiles
  twice with genuine original TC4/TLINK, each round byte-exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af851e --units p_gauge
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af851e
```

Both original compiler/linker rounds reproduce **55 CODE bytes,
one literal ordered native OMF FIXUPP field and one PUBLIC offset**,
original source/segment ABI, full original normal MAIN EXE/MAP, all
**124,642 Japanese loaded program bytes and 1,553 original MZ
relocations**. Independently checked standard DOS MZ serialization
matches all 130,882 original Japanese MAIN.EXE bytes. The other
**98 unchanged original game objects and Borland CRT** were reused;
no full-project cold replay, object patch, padding or source bypass.

Protected original-source-bound report:
`.analysis/work/exatt-layout-af851e/report.json`, SHA-256
`4302ddae67fe8110212a8e43c234aeebff6c0753bc53b3448499c7ffb6f5eebd`.
This is native C++ recovery/ABI verification for a **previously
source-owned original leaf**, not additional unique CODE ownership,
raw historical vendor OMF identity or canonical packed-file Factory
acceptance.
