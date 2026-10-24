# TH03 reconstruction progress

| Artifact | Target bytes | Source-present units | Ledger exact units | Exact functions | Ledger exact owned bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| th03-op | 36041 | 45 | 0 | 0 | 0 |
| th03-main | 130882 | 98 | 98 | 445 | 75317 |
| th03-mainl | 37975 | 145 | 0 | 0 | 0 |
| th03-zun | 16242 | 32 | 0 | 0 | 0 |

These are recorded ledger scopes, not a whole-game completion percentage.
Historical private verification outputs were removed at the owner's request.
Regenerate source builds and verification before any new exact acceptance.
See [current work](RE_HANDOFF.md) and [workflow](RE_WORKFLOW.md).

OP decoded publication: installed.

OP current decoded source acceptance: 3 functions / 133 bytes. Fresh source-only cold pair, native ownership/ABI and bounded instruction models pass. Canonical packed-file unit credit and whole-product source exactness remain unchanged; whole-game percentage is unknown.

MAINL current decoded source acceptance: 4 functions / 210 bytes. Current native ownership/ABI, two source-only cold builds and 4,800 guest cases per image pass. Canonical packed-file unit credit and whole-product source ownership remain unchanged.

ZUN current -2/-3/-4/-5 decoded source acceptance: 29 extents / 37 procedures / 2,656 CODE bytes. Twelve authored functions retain 1,621 CODE bytes; the complete original-ASM init owns 607 CODE + 783 DATA bytes and adds zero authored credit. Sixteen bounded library driver services add 428 CODE bytes with zero private DATA/BSS. Their actual include slots, eight absolute and eight relative native fixups are checked. Nine natural CODE contributions and EVEN replace 71 explicitly sized intergroup zero bytes and the row-copy NOP. Both source alignment controls fail equality. Twelve reserved DATA bytes and the other driver procedures remain unaccepted. Reviewed producer DATA totals 1,105 bytes. Native logo word alignment and resident SDK bindings remain checked. Two current source builds pass; logo 5,111, resident 3,548 and init 70,116 and driver scalar 8,428 guest cases per image reject 61 total mutations. All 65,536 init conversion inputs execute. Canonical packed-file unit credit and whole-product source ownership remain unchanged.
