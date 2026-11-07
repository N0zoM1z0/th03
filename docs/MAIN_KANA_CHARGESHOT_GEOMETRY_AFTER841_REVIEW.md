# TH03 MAIN after841: Kana Chargeshot original four-trail geometry

The original physical `cs_kana` is a **complete nine-function 1,291-CODE-byte
TC4 source**: four independent 13-sample charged trails, creation,
reverse-buffer motion and eight-bit release state, collision test, GRCG
sprite render and the full left-right Gauge sweep. The maintained C++ now
names the four true starting headings in their **reverse pointer write
order**, all four 4-sample history steps `0,4,8,12`, per-sprite 0x500
VRAM cel stride, and the signed 16-bit collision margin. The actual
54-byte record layout and `KANA_CHARGE_SWIRLING`/`RELEASED` state remain
unchanged; no coordinates are reallocated or clamped.

Incremental original native compiler experiments:

- `af841a`: hittest stride uses the same named four-sample step as
  rendering; the whole original physical module matches, two rounds.
- `af841b`: reverse initial heading names and sprite cel increment;
  whole original module remains exact in both rounds.
- `af841c`: challenged the original **unsigned-byte** Gauge `%64` with
  an explicitly widened `unsigned int` `&63`. This is a genuine **failed**
  CODE comparison, **1,288** candidate bytes vs **1,291** original;
  the original byte-sized modulo is retained. Earlier experiments also
  rejected a direct byte `&63` replacement; do not treat the unsigned
  cast as proof of identical compiler lowering.
- `af841d/e`: named exact signed subpixel hit margin and current-source
  explanatory comments; final **`af841e`** genuine original TC4/TLINK
  twice remains exact in the *whole* original physical source.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af841e --units cs_kana
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af841e
```

Both final rounds match **all 1,291 original CODE bytes, 117 literal ordered
native OMF FIXUPP fields, 9 PUBLIC offsets**, the complete native object
segment/ABI and source dependencies, complete normal MAIN EXE/MAP, all
**124,642 Japanese loaded bytes and 1,553 original MZ relocations**.
Independent standard MZ serialization matches all 130,882 original
Japanese MAIN.EXE bytes. The **98 other original project objects and
Borland CRT were reused** without a cold replay, code padding, object
byte patch or target substitution. Protected source-bound report:
`.analysis/work/exatt-layout-af841e/report.json`, SHA-256
`1bd3ddc3689d455debd76c87d38116ce196b8787e9e09668587f9958214cad09`.

This is refined current original C++ for a previously source-owned
physical object, not newly distinct original CODE ownership, raw vendor
OMF packet identity, or canonical packed-file Factory acceptance.
