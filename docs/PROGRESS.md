# TH03 reconstruction progress

| Artifact | Target bytes | Source-present units | Ledger exact units | Exact functions | Ledger exact owned bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| th03-op | 36041 | 58 | 0 | 0 | 0 |
| th03-main | 130882 | 106 | 106 | 459 | 78737 |
| th03-mainl | 37975 | 193 | 0 | 0 | 0 |
| th03-zun | 16242 | 77 | 0 | 0 | 0 |

These are recorded ledger scopes, not a whole-game completion percentage.
Historical private verification outputs were removed at the owner's request.
Validate the affected native scope; reuse an unchanged cold pair when its inputs still match.
See [current work](RE_HANDOFF.md) and [workflow](RE_WORKFLOW.md).

OP decoded publication: installed.

OP current decoded source acceptance: 40 extents / 65 procedures / 10,635 bytes (9,140 CODE + 1,495 initialized DATA). Validated source-only cold pair and complete native ownership/ABI pass; older runtime observations remain historical support. Canonical packed-file unit credit and whole-product source exactness remain unchanged; whole-game percentage is unknown.

MAINL current decoded source acceptance: 97 extents / 102 procedures / 16,362 bytes (16,138 CODE + 224 initialized DATA). Complete native ownership/ABI and the retained source-only cold pair are validated. Earlier runtime observations remain supporting history, not a per-unit test requirement. Unowned context, physical devices and whole-product source ownership remain open; canonical packed-file unit credit is unchanged.

ZUN current decoded source acceptance: 77 extents / 89 procedures or entries / 6,179 CODE + 2,456 DATA bytes. Accepted bytes comprise 2,179 authored, 1,390 original ASM and 5,066 library bytes. Complete native ownership/layout, ordered relocations and the retained source-only cold pair are validated. Earlier runtime observations remain supporting history. Twelve reserved DATA bytes and physical devices remain open. Original source/assembler identity, canonical packed-file unit credit and whole-product source ownership remain unchanged.
