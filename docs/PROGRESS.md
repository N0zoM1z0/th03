# TH03 reconstruction progress

| Artifact | Target bytes | Source-present units | Ledger exact units | Exact functions | Ledger exact owned bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| th03-op | 36041 | 48 | 0 | 0 | 0 |
| th03-main | 130882 | 98 | 98 | 445 | 75317 |
| th03-mainl | 37975 | 145 | 0 | 0 | 0 |
| th03-zun | 16242 | 71 | 0 | 0 | 0 |

These are recorded ledger scopes, not a whole-game completion percentage.
Historical private verification outputs were removed at the owner's request.
Regenerate source builds and verification before any new exact acceptance.
See [current work](RE_HANDOFF.md) and [workflow](RE_WORKFLOW.md).

OP decoded publication: installed.

OP current decoded source acceptance: 18 functions / 1,172 bytes. Fresh source-only cold pair, native ownership/ABI and bounded instruction models pass. Canonical packed-file unit credit and whole-product source exactness remain unchanged; whole-game percentage is unknown.

MAINL current decoded source acceptance: 15 functions / 703 bytes. Current native ownership/ABI, two source-only cold builds, 4,800 lifecycle, 2,218 shared input and 3,378 ending wait guest cases per image pass. Canonical packed-file unit credit and whole-product source ownership remain unchanged.

ZUN current -2/-3/-4/-5 decoded source acceptance: 68 extents / 76 procedures / 5,072 CODE bytes. Twelve authored functions retain 1,621 CODE bytes; the complete original-ASM init owns 607 CODE + 783 DATA bytes and adds zero authored credit. Fifty-five bounded library driver procedures own 2,844 CODE bytes with zero private DATA/BSS. Scalar include slots and sixteen native fixups remain checked. Nine command procedures add thirty literal native fixups, including seven relative calls. Their 6,678 guest cases per image cover all 361 bytes and reject nineteen mutations. Ten formatter/print procedures add 677 CODE bytes and four native fixups: 666 instruction bytes execute and eleven bytes are proved CFG-unreachable. Their 6,106 cases per image cover signed padding, DWORD slots, width wrap and saved-BP buffer overflow; twenty-four mutations fail. Twelve graphics procedures add 814 CODE bytes and 62 WORD fixups: 810 bytes execute, four clipping jump bytes are CFG-unreachable. Their 512 cases per image validate register/port/page-memory interfaces and reject 26 mutations. EGC raster/latch effects remain unproved. Eight lifecycle procedures add 564 CODE bytes and 69 WORD fixups (27 relative): 549 bytes execute and fifteen remain unreachable after terminal DOS calls. Their 1,826 cases per image compose real parser/formatter/graphics helpers, cover all 256 vector bytes and reject 25 mutations. Uninstall preserves the target zero-offset restoration and four-free order. Nine natural CODE contributions and EVEN replace 71 explicitly sized intergroup zero bytes and the row-copy NOP. Both source alignment controls fail equality. The driver header, other DATA ownership and twelve reserved DATA bytes remain unaccepted. Reviewed producer DATA totals 1,105 bytes. Native logo word alignment and resident SDK bindings remain checked. Two current source builds pass; logo 5,111, resident 3,548 and init 70,116, driver scalar 8,428, command 6,678, formatter 6,106, graphics 512 and lifecycle 1,826 guest cases per image reject 155 total mutations. All 65,536 init conversion inputs execute. Canonical packed-file unit credit and whole-product source ownership remain unchanged.
