# TH03 MAIN Bullet: natural large spawn/render loops and fresh negative controls — after719

The live maintained `src/main/bullet/bullet.cpp` is a **complete physical
original TC4 TU** with two CODE segments, a separate original GRCG 386
pellet writer, the large `group_velocity_set()` / `bullets_add()` / 
`bullets_update()` simulations and three-layer `bullets_render()` function.
This pass tested actual current-source object provenance rather than
assuming every historical after607 prose claim describes the current tree.

## Accepted natural source recovery

Six signed local loop-index mutations now use natural prefix C++ `++i`,
`++bullet_i`, `++trail_i` or `++group_i`, including:

- The full bullet reset leaf (all original bullet slots).
- `bullets_add()`'s outer allocation loop, each inserted trail's point
  initialization and bullet-group velocity advancement.
- Both large full-color bullet and delay-cloud render passes in
  `bullets_render()`.

The **pointer increments** in the comma expressions are intentionally still
postfix and the original `bullet_trail_ring_i++` byte mutation remains
unchanged; replacing signed/local register increments does not license
changing byte memory semantics or ordered trail side effects. Original
trail ownership, transfer-pellet bugs and real-mode GRCG register logic
were preserved.

Native proof for the changed entire bullet physical object:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af719d --units bullet
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af719d

Both independently compiled TC4 4.02 objects exactly reproduce **2,685
original CODE bytes (2,602 BULLET_TEXT + 83 PELLET_PUT), 196 literal
ordered OMF fixups, all 20 original PUBLIC offsets**, complete DATA/BSS
segment declarations, full original source-native TLINK MAIN/normalized
MAP, all 124,642 Japanese loaded bytes and 1,553 relocations. Separate
standard MZ serialization reproduces the complete 130,882-byte file.
Only this large Bullet TU was rebuilt; 98 other objects and CRT reused.

Receipt `.analysis/work/exatt-layout-af719d/report.json`, SHA-256
`42ed1de25356adeb286bd441366eaf7f531a52b0e411f1c6d4fd6b73d418a1ef`.

## Native experiments rejected rather than papering over mismatches

- `af719a`: current unmodified baseline confirmed original byte equality.
- `af719b`: `_AX <<= 1` replacing `asm { shl ax, 1 }` in GRCG pixel
  address generation **failed** original bytes. TC4 generated `03 C0`
  (`ADD AX,AX`) where original requires `D1 E0` (`SHL AX,1`): two CODE
  bytes differ despite equivalent arithmetic. The older after607 note
  described a historical form, but the **current source** contains
  explicit SHL and cannot inherit that older source-exactness assertion.
- `af719c`: casting `_AX` to unsigned 16-bit and shifting still produced
  the same two-byte mismatch. Merely changing signedness did not help.
- `af719e`: replacing the manual original `_SI` pellet memory register
  with natural `register unsigned int pellet_source` changed register/stack
  handling and grew the physical CODE from 2,685 to 2,696 bytes.

All negative trials remain preserved in ignored native writer stages;
none are committed as accepted source. No binary patch, spoofed object
or full cold replay was used. The byte-exact necessary hardware/encoding
operations are still explicit; this is **natural source recovery**, not
new canonical Factory packed-unit acceptance or vendor OMF packet identity.
