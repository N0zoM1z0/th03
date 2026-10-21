# TH03 reconstruction progress

| Artifact | Target bytes | Source-present units | Exact units | Exact functions | Exact owned bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| th03-op | 36041 | 33 | 0 | 0 | 0 |
| th03-main | 130882 | 87 | 86 | 403 | 65198 |
| th03-mainl | 37975 | 51 | 0 | 0 | 0 |
| th03-zun | 16242 | 3 | 0 | 0 | 0 |

Reviewed authored-byte coverage is scoped to currently reviewed file-backed unit extents; the whole-product authored denominator remains unknown.
Infrastructure and reference builds do not count as game reconstruction.

MAINL contextual composition: 6,144 owned decoded bytes and 110 scoped ordered relocation words match target. Nine PI operand gaps close in this composition; historical failures remain preserved. Whole decoded image retains 21 other byte differences and relocation-order differences. This historical composition did not change source or exact counts.

MAINL PI decoder source promotion: one existing 1,524-byte unit added, now source 51/145 (17,196 bytes), exact 0. Two fresh include-consuming root assemblies and hybrid links have equal raw root OBJ/EXE/MAP. All 13,495 scoped maintained bytes match target; four ordered PI relocations match. One DATA byte and 461 global relocation-order differences remain. Full decoder models passed and are retained by complete EXE identity in fast replay, not rerun. Other objects remain contextual, not a cold aggregate.
