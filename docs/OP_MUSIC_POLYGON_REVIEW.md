# OP Music Room polygon native findings

The maintained `animation_and_menu.inl` contains these complete procedures:

| Procedure | Decoded address | CODE | ABI |
| --- | --- | --- | --- |
| `polygon_build` | `0990:0D14` | 143 | Near Pascal, 12 argument bytes |
| `polygons_update_and_render` | `0990:0DA3` | 502 | Near C, no arguments |

All645 raw bytes,219 instructions,54 OMF fields and14 literal ordered MZ
relocations match the natural producer and fixed Japanese target. Native
records, segment/public ownership and containing MAP geometry remain checked.
Use `scripts/review_th03_op_music_menu_work.py` for the complete carrier check.

Preserve these source details:

- Y is shifted arithmetically; angle uses its low BYTE. `(i << 8)` wraps as a
  WORD before signed division. The closing point duplicates the first point.
- All16 polygons are built at old positions before movement. Signed X reflects
  at `<=0` or `>=639`; updated Y resets at `>=8000`. WORD/BYTE overflow remains.
- Initialization and reset consume different random sequences. Zero horizontal
  velocity becomes1 and zero angle speed becomes4. Reset Y is-1600 subpixels;
  radii are64/80/96/112. Initialization state persists.
- The authorized TH04 source uses the same geometry but its radius96 comment
  conflicts with its expression, which also yields112. Do not copy its helper
  wrapper in place of TH03's original macro/random-call order.

The earlier 2026-10-28 diagnostic completed2,284 executions and46 mutation
controls. Its original receipt at `config/op_music_polygon_work/observation.json`
is historical: the large emulator model and seven CI tests were removed when
the user requested exact-first verification. That receipt no longer binds the
current simplified checker and is not a new acceptance prerequisite.
Complete CODE ownership is now accepted in the current OP publication.
The separate native storage review now accepts DATA1008 and reviews BSS1060
layout without file-backed BSS credit. Physical rendering remains separate.
