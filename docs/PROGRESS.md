# TH03 reconstruction progress

| Artifact | Target bytes | Source-present units | Exact units | Exact functions | Exact owned bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| th03-op | 36041 | 33 | 0 | 0 | 0 |
| th03-main | 130882 | 87 | 86 | 403 | 65198 |
| th03-mainl | 37975 | 38 | 0 | 0 | 0 |
| th03-zun | 16242 | 3 | 0 | 0 | 0 |

Reviewed authored-byte coverage is scoped to currently reviewed file-backed unit extents; the whole-product authored denominator remains unknown.
Infrastructure and reference builds do not count as game reconstruction.

MAINL contextual composition: 6,144 owned decoded bytes and 110 scoped ordered relocation words match target. Nine PI operand gaps close in this composition; historical failures remain preserved. Whole decoded image retains 21 other byte differences and relocation-order differences. Source 38/145 (9,845 bytes), exact 0 remain unchanged.

MAINL opt-in linked graphics: 355 target-equal bytes and two scoped ordered relocations preserve the earlier 6,144 bytes / 110 relocations, totaling 6,499 scoped bytes / 112 relocations. One decoded DATA byte remains; all 677 relocation entries retain membership with 461 order differences. One mixed-source link with 32 retained objects, not two cold products; original segment identity is not preserved. Source and exact counts remain unchanged.
