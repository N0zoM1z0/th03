# TH03 reconstruction progress

| Artifact | Target bytes | Source-present units | Ledger exact units | Exact functions | Ledger exact owned bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| th03-op | 36041 | 61 | 0 | 0 | 0 |
| th03-main | 130882 | 106 | 106 | 459 | 78737 |
| th03-mainl | 37975 | 256 | 0 | 0 | 0 |
| th03-zun | 16242 | 77 | 0 | 0 | 0 |

**Reading this table:** Target bytes are the pinned original packed-file sizes, not decoded native EXE sizes. Source-present units count existing source paths; ledger exact units/owned bytes count only the canonical packed-file unit ledger. An exact-function count is a separately reviewed function scope, not a whole-executable percentage.

**Decoded source acceptance is separate from this packed-unit ledger.** For example, decoded MAINL accepted ownership below can be nonzero even when its canonical packed-file unit exact column above remains zero. A separately verified source-only CRT normal link may reproduce the complete original decoded EXE and MAP while still being **unaccepted working evidence**, not extra accepted ledger credit. The source-module count and byte scope are in the [current agent handoff](RE_HANDOFF.md).

Validate the affected native scope; reuse an unchanged cold pair when its inputs still match.
See [current work](RE_HANDOFF.md) and [workflow](RE_WORKFLOW.md).

OP decoded publication: installed.

OP current decoded source acceptance: 60 extents / 92 procedures / 14,985 bytes (13,221 CODE + 1,764 initialized DATA). Validated source-only cold pair and complete native ownership/ABI pass; older runtime observations remain historical support. Canonical packed-file unit credit and whole-product source exactness remain unchanged; whole-game percentage is unknown.

MAINL current decoded source acceptance: 217 extents / 290 procedures / 37,287 bytes (34,431 CODE + 2,850 initialized DATA + 6 uninitialized file DATA). Accepted source comprises 17,036 authored and 20,251 library bytes. Complete native ownership/ABI and the retained source-only cold pair are validated. Earlier runtime observations remain supporting history, not a per-unit test requirement. Unowned context, physical devices and whole-product source ownership remain open; canonical packed-file unit credit is unchanged.

ZUN current decoded source acceptance: 77 extents / 89 procedures or entries / 6,179 CODE + 2,456 DATA bytes. Accepted bytes comprise 2,179 authored, 1,390 original ASM and 5,066 library bytes. Complete native ownership/layout, ordered relocations and the retained source-only cold pair are validated. Earlier runtime observations remain supporting history. Twelve reserved DATA bytes and physical devices remain open. Original source/assembler identity, canonical packed-file unit credit and whole-product source ownership remain unchanged.
