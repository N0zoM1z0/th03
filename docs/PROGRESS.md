# TH03 reconstruction progress

| Artifact | Target bytes | Source-present units | Exact units | Exact functions | Exact owned bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| th03-op | 36041 | 33 | 0 | 0 | 0 |
| th03-main | 130882 | 87 | 86 | 403 | 65198 |
| th03-mainl | 37975 | 145 | 0 | 0 | 0 |
| th03-zun | 16242 | 3 | 0 | 0 | 0 |

Reviewed authored-byte coverage is scoped to currently reviewed file-backed unit extents; the whole-product authored denominator remains unknown.
Infrastructure and reference builds do not count as game reconstruction.

Historical MAINL PI composition: 6,144 owned decoded bytes and 110 scoped ordered relocation words match target. Nine PI operand gaps close in this composition; historical failures remain preserved. That image retained 21 other byte differences and relocation-order differences. This historical composition did not change source or exact counts.

MAINL CRT source promotion: six existing units / 628 bytes added, now source 145/145 (28,381 bytes), exact 0. Six fresh semantic ASM producers replace only six members in the original893-member private library order;887 contextual members remain unchanged. Independent repeated producers/library/link yield nine raw-identical products. All24,680 scoped maintained CODE bytes and93 CRT DATA bytes match target; DATA is not extra CODE ledger credit. Fresh target and final-repeat candidate runtime runs each passed7,858 scenarios and277 instruction positions; first/repeat EXE identity avoids a redundant third run. Fast replay retains the two actual model receipts without rerunning. Known DATA linear60473 (90 to00),461 global relocation-order differences and canonical packed/full cold aggregate gates remain open. Source145/145 is not whole-game exact completion.

MAINL DIET diagnostic: default DIET packs the decoded target twice to the exact canonical37,975-byte stored image, validating the packing control. The maintained-source MCO02 image packs twice to38,048 bytes, with2,259 packed differences; both source roundtrips restore its exact input. The461 decoded relocation-order differences and one DATA byte remain. Same-tool restoration is a separate invocation, not an independent decoder proof. Source145/145 and28,381 bytes remain unchanged; formal exact credit stays0.
