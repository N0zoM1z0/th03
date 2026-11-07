# TH03 MAIN Kana Bomb whole-owner byte-phase recovery (after784)

This pass revises the **whole original physical `b_kana`** source, not just
an isolated helper. The two-stage Kana Bomb controller now names the real
frame boundaries (64/128), distinct center/volley periods (8/4), the
opposite-angle reflection (0x80), and the independently shared circle
center (144,184) and radius 144. In the final palette fade the result is
**assigned back to an 8-bit `frame` before doubling**, preserving the
original byte truncation; do not coalesce this into a 16-bit expression.
The Bomb's one-byte angle storage has an explicit compile-time ABI check.

## C++ alternatives actually falsified by native compiler output

- `af784a`: replace explicit `(_AX = pid_current)` word stack-carrier
  expression at the original MRS call with `static_cast<unsigned int>`.
  The genuine compiler emitted `PUSH word ptr [pid_current]` in place
  of the original `MOV AL,[pid_current]; MOV AH,0; PUSH AX` sequence.
  The code payload differed. `af784b` (cast to byte) and `af784c`
  (`pid_current + 0`) produced the same incompatible lowering; all
  are **rejected**. Preserve the original unmodified hardware/library
  ABI carrier, which is a compiler compatibility idiom, not an invented
  `AX`-parameter calling convention.
- `af784d`: naming the byte-angle increment as an enum `0x10` caused
  TC4 to generate `ADD byte ptr [kana_bomb_angle],10h` rather than the
  original `ADD AL,10h; MOV [kana_bomb_angle],AL` following the previous
  byte-angle subtraction. Semantics agree, native instructions do not.
  The original literal byte increment was restored. The other named
  timeline/geometry and mirror-angle expressions survived native comparison.

## Original native TC4/TLINK acceptance for the affected object

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af784f --units b_kana
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af784f
```

Both independent original compiler and full normal-link rounds match **all
526 CODE bytes, 53 ordered OMF FIXUPP fields and one PUBLIC offset** in
this object. Full Japanese MAIN loaded image and all 1,553 ordered MZ
relocations match; 98 other original project objects and CRT are reused
without cold replay. Independently reviewed current-source evidence is
`.analysis/work/exatt-layout-af784f/report.json`, report SHA-256
`f16b2f1cd5b7828302c962051a592c16d378b91815d4d646b50a37655f72178f`.
This is a revalidated source owner, not new distinct unit coverage or
canonical packed-game Factory acceptance. The discarded variants are
negative codegen controls, not target-equal candidates.
