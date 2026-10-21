# TH03 reconstruction progress

| Artifact | Target bytes | Source-present units | Exact units | Exact functions | Exact owned bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| th03-op | 36041 | 33 | 0 | 0 | 0 |
| th03-main | 130882 | 87 | 86 | 403 | 65198 |
| th03-mainl | 37975 | 139 | 0 | 0 | 0 |
| th03-zun | 16242 | 3 | 0 | 0 | 0 |

Reviewed authored-byte coverage is scoped to currently reviewed file-backed unit extents; the whole-product authored denominator remains unknown.
Infrastructure and reference builds do not count as game reconstruction.

Historical MAINL PI composition: 6,144 owned decoded bytes and 110 scoped ordered relocation words match target. Nine PI operand gaps close in this composition; historical failures remain preserved. That image retained 21 other byte differences and relocation-order differences. This historical composition did not change source or exact counts.

MAINL linked-game source promotion: 23 existing units / 1,765 bytes added, now source 139/145 (27,753 bytes), exact 0. Two actual rounds each rebuilt 15 C/C++ providers plus root and link: 34 successful native phases and 18 raw-identical repeat products. Nineteen contextual objects per round remain retained, not a cold whole program. All 24,052 scoped maintained bytes match target. Six model families cover 3,496 cases per image and nine CFG/window mutants; fast replay retains results without rerunning matrices. STAFF music/ending retain relocation membership but seven/thirteen ordered positions differ. Four original sound producer bytes are owned; scanner NOP remains context. One DATA byte and 461 global relocation-order differences, full cold aggregate and canonical packing remain open.
