# TH03 MAIN after715: four changed physical sources integrated together

This review is a **concurrent changed-source native proof**, not four isolated
past success claims and not a full cold rebuild. The maintained game source
from the preceding four commits was compiled together into four original
complete TC4 physical translation units in each of **two independent**
original Turbo C++ 4.02/TLINK rounds. Remaining original game project objects
and the Borland CRT remained the unchanged source-native parent.

| Changed original TU | Actual recovered behavior | CODE | Ordered OMF FIXUPPs | PUBLICs |
| --- | --- | ---: | ---: | ---: |
| `ba_yumem` | Full Yumemi BOSS pattern timing, 12-bullet rain loop and render dispatch | 2,358 | 343 | 10 |
| `ba_chiyu` | Full Chiyuri BOSS update/attack phases, natural boolean/palette renderer gates | 2,654 | 381 | 11 |
| `entry` | Whole MAIN entry + frame/round scheduler, stage reset, outcome/score paths | 3,050 | 433 | 8 |
| `p_cpu` | CPU collision grid leaf, target direction, pursuit and long dodge/retry controller | 1,077 | 64 | 4 |
| **Four rebuilt original units** | | **9,139** | **1,221** | **33** |

Current product source files included by the four producers:

- `src/main/boss/yumemi.cpp` and `src/main/boss/chiyuri.cpp`
- `src/main/player/cpu.cpp`
- `src/main/core/entry.cpp`, `src/main/core/entry.inl`,
  `src/main/round/round_loop.inl`, plus the unchanged but newly bound
  `src/main/round/stage_round.inl` and `src/main/core/roundfin.inl`

The real `entry` original physical source is newly supported in the scoped
source overlay driver. All four original ENTRY `.inl` files are explicitly
copied from current source and required in the original TC4 OMF source
COMENT records; the compiler cannot fall back to an old WORK copy of the
changed round scheduler or game main.

Reproduce this **affected-scope** (four objects only) native compiler check:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af715a --units ba_yumem,ba_chiyu,entry,p_cpu
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af715a

Both independent rounds exactly reproduced complete CODE and initialized
segment definitions, literal ordered OMF fixups, PUBLIC offsets, complete
normal TLINK MAIN.EXE and path-normalized MAP against retained original
source-native parent. They reproduced the entire **124,642-byte Japanese
loaded game image** and **all 1,553 ordered MZ relocation words**. Separately
reviewed standard MZ serialization matched every byte of the original
**130,882-byte Japanese MAIN.EXE**. No fabricated object bytes, patched
linker outputs, changed reference targets or cold toolchain replay were used.

Primary read-only receipt:
`.analysis/work/exatt-layout-af715a/report.json`, SHA-256
`1f6e2ece5f4df0e75ace579cf1c615f03b9ed69567e22484dc0a126c50a895d8`.
Both native compiler rounds' OBJ, EXE/MAP, source/headers, linked response
inputs, output file images and writer logs are retained in ignored evidence.

Negative/incomplete trials are not counted: `af711a` was unchanged-source
control after an edit script assertion; `af713b` was a failing TC4 compile
from a temporary enum-name collision. The final changed-source successes
were `af711b`, `af712a`, `af713c`, `af714a` and this concurrent `af715a`.

These are **already existing original owned bytes**. New natural expressions,
new current-source/OMF provenance and another full-link proof do **not**
create new canonical Factory packed-file acceptance, prove vendor OMF raw
record identity or establish whole-game source ownership. The historic
58-distinct-owner union in after709 was not recomputed; `entry` was already
original-source covered by the historical after594 chain.
