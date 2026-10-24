# TH03 reconstruction progress

| Artifact | Target bytes | Source-present units | Ledger exact units | Exact functions | Ledger exact owned bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| th03-op | 36041 | 45 | 0 | 0 | 0 |
| th03-main | 130882 | 98 | 98 | 445 | 75317 |
| th03-mainl | 37975 | 145 | 0 | 0 | 0 |
| th03-zun | 16242 | 15 | 0 | 0 | 0 |

These are recorded ledger scopes, not a whole-game completion percentage.
Historical private verification outputs were removed at the owner's request.
Regenerate source builds and verification before any new exact acceptance.
See [current work](RE_HANDOFF.md) and [workflow](RE_WORKFLOW.md).

OP decoded publication: installed.

OP current decoded source acceptance: 3 functions / 133 bytes. Fresh source-only cold pair, native ownership/ABI and bounded instruction models pass. Canonical packed-file unit credit and whole-product source exactness remain unchanged; whole-game percentage is unknown.

MAINL current decoded source acceptance: 4 functions / 210 bytes. Current native ownership/ABI, two source-only cold builds and 4,800 guest cases per image pass. Canonical packed-file unit credit and whole-product source ownership remain unchanged.

ZUN current -3 decoded source acceptance: 10 functions / 1,299 bytes. Native -a2 word alignment replaces the padding variable. Two current source builds, complete CODE/DATA/BSS ownership and 5,111 guest cases per image pass, with eighteen mutations rejected. Canonical packed-file unit credit and whole-product source ownership remain unchanged.
