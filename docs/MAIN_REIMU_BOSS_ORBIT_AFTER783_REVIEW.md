# TH03 MAIN Reimu BOSS signed orbit-angle recovery (after783)

`ba_reimu` is the **entire original physical major-BOSS source owner**, not
an isolated leaf or simulated function. Three orbit phases use the same
signed integer quotient `(i * 256) / reimu_orbit_count`, with an unsigned-byte
angle offset applied **after** division. Two phases rotate the starting angle
by eight byte-angle units per frame. The maintained C++ now gives both
invariants explicit compiler-time semantic names while retaining the exact
original expression order and byte-width result. This avoids inadvertently
replacing signed integer division with a byte-arithmetic approximation.

The separate natural-C++ experiment `af783a` also tried replacing
`angle = (0 - angle)` with `angle = -angle` in the cloud pattern.
The genuine original compiler's whole CODE payload comparison **failed**.
The unary-minus simplification was rejected and removed; the original
parenthesized subtraction remains in the maintained source. This failed
experiment does **not** establish target equality or source acceptance.

## Two-round current-source native verification

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af783b --units ba_reimu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af783b
```

Both original TC4 4.02 and complete normal MAIN TLINK rounds, using the
maintained source and original one-object slot, reproduced all **2,020 CODE
bytes**, **270 literal ordered OMF FIXUPP fields**, **9 PUBLIC offsets**, the
complete original loaded Japanese MAIN game image and **1,553 literal ordered
MZ relocations**. The complete game link reuses the 98 other unchanged
project objects and original CRT; no full cold replay was performed.
The independent review returns `full_Japanese_MAIN_equal: true`, report
`SHA-256 b83743c981e06874fedf68c26a979e0f51fa18a79d5b0802a50dd9fc3595ee5f`,
under protected local evidence
`.analysis/work/exatt-layout-af783b/report.json`. Native original OMF
packet-identity and canonical packed-game acceptance are **not** claimed.
This is a reverified existing full BOSS owner, **not** newly counted
byte coverage in addition to the previous union.
