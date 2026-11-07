# TH03 MAIN after877 — five modified original physical owners compiled together

The `af877a` experiment **genuinely compiles all five original physical
sources changed in after872–876 simultaneously**, in two independent
original Turbo C++ 4.02 + complete normal MAIN TLINK rounds. This is not a
synthetic sum of separate per-owner proofs, and it does not cold-compile
unaffected objects.

| Physical owner | Entire current source | CODE bytes | Ordered native OMF FIXUPPs | PUBLICs |
| --- | --- | ---: | ---: | ---: |
| `ba_chiyu` | Full eleven-function **Chiyuri major BOSS**: four signed fan loops, 16-sprite orbit renderer and entire attack/lifecycle controller | 2,654 | 381 | 11 |
| `ex_ellen` | Complete Ellen Extra Attack, 12-slot initializer/render dispatcher, four-sprite tail, seven-sample history shift and fill | 1,129 | 79 | 6 |
| `ex_rika` | Full Rikako Extra Attack including 14-slot homing, collision, allocation and rendering, with two early-`continue` paths | 702 | 46 | 5 |
| `cs_chiyu` | Full Chiyuri Chargeshot/Gauge, five signed-index loops, five collision `continue` paths and original reset quirk | 1,011 | 96 | 9 |
| `exit` | Actual PC-98 far-`__cdecl` shutdown, four hardware OUT instructions and byte/word page-port ABI | 67 | 8 | 1 |
| **Five original physical objects recompiled together** | | **5,563** | **610** | **32** |

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af877a --units ba_chiyu,ex_ellen,ex_rika,cs_chiyu,exit
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af877a
```

Both real original compiler rounds reproduce **all 5,563 original CODE
bytes**, **610 literal ordered native OMF FIXUPP fields** and all **32
PUBLIC offsets**, original physical segment/ABI/data owner and compiler
source/header dependencies. Both normal original MAIN TLINK rounds match
the entire original normal MAIN EXE and normalized MAP, **all 124,642
Japanese loaded program bytes** and **1,553 ordered MZ relocations**.
Independently checked standard DOS MZ serialization reproduces the
complete **130,882-byte original Japanese MAIN.EXE**; it does not prove
historical vendor MZ-header serializer identity.

**94 other original game objects and original Borland CRT reused**, not
cold-rebuilt. No source binding guard was weakened, no old receipt was
replaced, and neither original source/target objects, CODE arrays nor
EXE bytes were patched or padded. Protected genuine original compiler,
normal linker, source-ABI and independent MZ evidence:
`.analysis/work/exatt-layout-af877a/report.json`, SHA-256
`34ce6e5c501bcd3cf2b555e4c8ebe371fed1421a625b6b5339e4fa70dce114f3`.

The previous independent `af871a`, `af865a`, `af859a`, `af853a`, `af847a`,
`af842a`, `af835a` are separate real native experiments for different
previously modified physical owners; they must **not** be represented as
a fictitious combined all-owner build. Older receipts covering today's
five changed sources still establish their historical input snapshots,
but not current-source hash matching. The five subjects already had
historical source-CODE coverage. This is improved exact maintained C++
provenance, **not new unique original CODE bytes, historical raw vendor
OMF packet identity, or canonical Factory packed-file unit acceptance**.
The BIOS `input_s` historical one-NOP parent link gap and complete
historical source ownership remain unresolved.
