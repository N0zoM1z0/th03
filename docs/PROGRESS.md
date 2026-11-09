# TH03 reconstruction progress

All counts describe tracked scopes. The whole-game completion percentage is unknown.

| Product | Source-present / tracked extents | Current accepted scope | Stored target bytes |
| --- | ---: | --- | ---: |
| th03-op | 61/62 | Decoded: 60 extents / 14,985 bytes | 36,041 |
| th03-main | 106/106 | Ledger: 106 extents / 78,737 bytes | 130,882 |
| th03-mainl | 259/259 | **Pending revalidation** | 37,975 |
| th03-zun | 77/78 | Decoded: 77 extents / 8,635 bytes | 16,242 |

Source-present means a maintained source path exists; it does not grant exact acceptance. Tracked extents can be functions, modules or DATA owners. All chart bars use these extents.

MAIN's separate function ledger records 459/459 exact entries. The other products have no equivalent function ledger; a zero function count would be misleading. Ledger acceptance is distinct from revalidation against current source; selected current native reviews follow below.

Stored target sizes are original file sizes, including DIET packing for OP/MAINL/ZUN. They are not decoded CODE denominators. OP/MAINL/ZUN canonical packed-unit credit remains zero; that does not erase decoded or scoped native work.

## Current source-native reviews

These read-only checks validate maintained source bindings, both original compiler rounds, complete physical owners, ordered native fields and normal target-equal links. Other link inputs are reused; these results do not grant broad decoded publication or whole-product ownership.

| Product / scope | Stage | Current check | Physical owners | CODE bytes | Initialized DATA bytes |
| --- | --- | --- | ---: | ---: | ---: |
| th03-main / BOSS and HitCircle | af1053k | Verified | 12 | 18,845 | — |
| th03-mainl / Staff Roll | af942s | Verified | 1 | 3,695 | 224 |
| th03-mainl / Root controller | af944r | Verified | 1 | 2,458 | 112 |

th03-main BOSS and HitCircle: `.analysis/work/exatt-layout-af1053k/report.json`.

th03-mainl Staff Roll / 19 procedures: `.analysis/work/mainl-staff-af942s-native-build.json`.

th03-mainl Root controller / 11 procedures: `.analysis/work/mainl-root-af944r-native-build.json`.

## Decoded publication status

OP current decoded source acceptance: 60 extents / 92 procedures / 14,985 bytes (13,221 CODE + 1,764 initialized DATA). Validated source-only cold pair and complete native ownership/ABI pass; older runtime observations remain historical support. Canonical packed-file unit credit and whole-product source exactness remain unchanged; whole-game percentage is unknown.

MAINL broad decoded acceptance is **pending**, rather than zero reconstruction. The retained publication does not bind the current complete source graph. The independent Staff Roll and root-controller reviews above remain visible.

Current blocker: `current MAINL acceptance: proof verifier input drift: src/mainl/root/complete_data.cpp, scripts/lib/decoded_mainl_acceptance.py; native audit: staff_data cpp src/mainl/staff/data.cpp: pin mismatch bb4dc75429e41d750e63eea09c1c8488ab426ee590bb1eba183eacf06122fda4`.

Revalidate the changed native dependency scopes and compose their retained evidence before publishing again. Do not update historical hashes to imply a new compiler run.

ZUN decoded source acceptance: 77 extents / 89 procedures or entries / 6,179 CODE + 2,456 DATA bytes. Origins: 2,179 authored, 1,390 original ASM and 5,066 library bytes. Twelve reserved DATA bytes and physical devices remain open.

Factory whole-product acceptance remains open for every product. See the [current handoff](RE_HANDOFF.md) and [workflow](RE_WORKFLOW.md).
