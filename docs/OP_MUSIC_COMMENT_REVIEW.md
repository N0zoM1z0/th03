# OP Music Room comment, copy and flip native findings

| Procedure | Decoded address | CODE | Callee cleanup |
| --- | --- | --- | --- |
| `nopoly_B_put` | `0990:0CF6` | 30 | 0 |
| `music_update_render_and_flip` | `0990:0F99` | 54 | 0 |
| `cmt_bg_snap` | `0990:0FCF` | 315 | 0 |
| `cmt_load` | `0990:110A` | 73 | 2 |
| `cmt_bg_free` | `0990:1153` | 41 | 0 |
| `cmt_unput` | `0990:117C` | 285 | 0 |
| `cmt_load_unput_and_put` | `0990:1299` | 109 | 2 |

All907 CODE bytes,315 instructions,63 OMF fields and14 literal ordered
relocations match the natural producer and pinned target. Complete records,
publics, MAP allocations, include chain and consumed SDK dependencies remain
checked. Use `scripts/review_th03_op_music_menu_work.py` for the complete native
carrier; no emulator matrix or new cold build is needed for unchanged inputs.

Preserve the original implementation:

- B restore uses16,000 REP MOVSW iterations with incoming DF. Background capture
  uses four12,800-byte buffers and a continuous3,200-DWORD cursor per plane.
  Pointer arithmetic, reloads and unchecked allocator results stay unchanged.
- Track*840 truncates to a WORD then sign-extends for seek: track40 yields-31936.
  The20 comment records have stride42; byte40 is cleared, byte41 is preserved.
- TH03 draws all20 lines, including semicolon-prefixed lines, and recaptures
  8,000 DWORDs afterward. Free reloads each segment and does not clear pointers.
- Flip restores B, updates polygons, switches display/access pages and calls
  the owned unsigned frame delay. The page remains an unchecked BYTE.
- TH04's `_MUSIC.TXT`, rectangle background and fade path differ from TH03's
  `MUSIC.TXT`, four planar buffers and per-page recapture. It is reference only.

The earlier 2026-10-28 diagnostic completed1,684 executions and65 mutation
controls. `config/op_music_comment_work/observation.json` preserves that original
historical receipt. Its large model, allocation/null/aliasing matrices and eight
CI tests were removed at the user's direction. The old receipt is not a current
implementation binding or prerequisite for native source ownership review.
These complete CODE extents are now accepted by the native Music Room ownership
review. The separate storage review accepts DATA1008 and verifies BSS1060
layout with zero file-backed credit. Canonical packed-unit credit stays separate.
