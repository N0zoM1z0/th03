# TH03 reconstruction progress

| Artifact | Target bytes | Source-present units | Exact units | Exact functions | Exact owned bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| th03-op | 36041 | 33 | 0 | 0 | 0 |
| th03-main | 130882 | 87 | 86 | 403 | 65198 |
| th03-mainl | 37975 | 65 | 0 | 0 | 0 |
| th03-zun | 16242 | 3 | 0 | 0 | 0 |

Reviewed authored-byte coverage is scoped to currently reviewed file-backed unit extents; the whole-product authored denominator remains unknown.
Infrastructure and reference builds do not count as game reconstruction.

MAINL contextual composition: 6,144 owned decoded bytes and 110 scoped ordered relocation words match target. Nine PI operand gaps close in this composition; historical failures remain preserved. Whole decoded image retains 21 other byte differences and relocation-order differences. This historical composition did not change source or exact counts.

MAINL resource source promotion: 14 existing units /3,475 bytes added, now source 65/145 (20,671 bytes), exact 0. RotTbl's 1,024 bytes are generated semantic table data, not functions; retained heap is not credited again. Two fresh include-consuming root assemblies and hybrid links have equal raw root OBJ/EXE/MAP. All 16,970 scoped maintained bytes match target; resource relocation sets are empty. One DATA byte and 461 global relocation-order differences remain. Ten fresh model phase receipts plus PI_FREE lifecycle proof are retained by complete EXE identity, not rerun by fast replay; no cold aggregate.
