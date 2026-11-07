# TH03 MAIN after856: entire Yumemi Chargeshot, targeting and ring renderer

The original physical `cs_yume` contains **ten functions in 1,645 CODE
bytes**, including the shared `ellen_target_set` 40-enemy formation/BOSS
target selection, Yumemi Chargeshot's two-state lifetime, direct/blooming
collision, sixteen-sprite ring renderer, eight-phase ring effect and the
full two-triangle Gauge volley switch. This is a complete original
compiler-unit test, not a rendered-animation leaf in isolation.

## Real natural C++ source recovery

The ring's coupled `i`/byte-angle traversal now uses ordinary **typed
`while(i < YUME_RING_SPRITES_PER_WAVE)`** with original **ordered `++i;
angle += 16;` mutations**. Genuine original TC4 4.02 emits exactly the
original 16-call loop CODE for that natural form. The original angle is
initialized from the byte frame and **retains its byte truncation**.
Meaningful physical constants now state target fallback coordinates
(144,300 pixels in original subpixel units), formation-target signed
X/Y bias, Chargeshot flight speed and narrow 8-pixel vs blooming
56-pixel hitboxes, origin offsets, and sixteen-sprite ring placement.
The `yumemi_chargeshots_reset()` functions now use the real named
inactive byte state. The Gauge's **byte-valued `% 8`** period is named;
its natural `if(!(byte_frame % period))` truth check is native exact.
All original segmented far/near calls and actual gauge switch jump-table
values remain compiler generated and unpatched.

## Independent original compiler trials and essential negative controls

- `af856a`: whole 16-sprite ring traversal converted to `while`;
  two complete original compiler/full normal MAIN TLINK rounds exact.
- `af856b`: replacing the live byte's literal `angle += 16` with a
  named enum **failed** the original CODE comparison (same 1,645-byte
  length but first difference at CODE segment 4, offset 615). The
  literal original update remains, unlike safely named loop bounds.
- `af856c`: restoring byte angle update while naming the ring count and
  eight-frame Gauge period passes both real native rounds.
- `af856d`: replacing the renderer's **byte `frame & 1`** with `%2`
  **failed** (candidate **1,651** initialized CODE bytes vs original
  **1,645**). Retain the byte mask: the different Gauge byte modulo
  was already original native.
- `af856e`: named the two physical collision margins, flight speed,
  and ring center/screen offsets; complete original module still exact.
- `af856f`: ordinary C++ `if(!(gauge_byte_frame % 8))` compiled all
  original bytes exactly, with the original eight-case jump table.
- `af856g`: named signed 16-bit fallback/target geometry and explicit
  inactive states, both original-native rounds exact.
- Final `af856h`: recompiled the **entire final current maintained C++
  source**, including exact byte/overflow constraints and original
  source ABI, in two independent actual TC4/full normal MAIN TLINK rounds.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af856h --units cs_yume
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af856h
```

Both genuine original compiler/normal linker rounds matched **all
1,645 original initialized CODE bytes, 133 literal ordered native OMF
FIXUPP fields, ten PUBLIC offsets**, source/segment ABI, complete
normal MAIN EXE and path-normalized MAP, **124,642 loaded Japanese
program bytes** and **all 1,553 literal ordered original MZ relocations**.
Independent reviewed standard DOS MZ serialization reconstructs all
130,882 original Japanese MAIN.EXE bytes. The **98 other unchanged
original game project objects and Borland CRT** were reused; no
whole-project cold replay, object/target patching, fake padding or raw
original code buffer.

Protected source-bound genuine native report and both complete writer
rounds: `.analysis/work/exatt-layout-af856h/report.json`, SHA-256
`4ec4655300eae6d47379affe29b9fcdea7257fe1675e4cdf9f9aca87c35763cd`.
The historical real physical owner was already native source-backed.
These CODE bytes are **not newly distinct original target ownership**,
raw vendor OMF packet identity, original historical source spelling
or canonical packed-game Factory acceptance.
