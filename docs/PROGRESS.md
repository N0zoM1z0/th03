# TH03 reconstruction progress

| Artifact | Target bytes | Source-present units | Exact units | Exact functions | Exact owned bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| th03-op | 36041 | 33 | 0 | 0 | 0 |
| th03-main | 130882 | 87 | 86 | 403 | 65198 |
| th03-mainl | 37975 | 84 | 0 | 0 | 0 |
| th03-zun | 16242 | 3 | 0 | 0 | 0 |

Reviewed authored-byte coverage is scoped to currently reviewed file-backed unit extents; the whole-product authored denominator remains unknown.
Infrastructure and reference builds do not count as game reconstruction.

Historical MAINL PI composition: 6,144 owned decoded bytes and 110 scoped ordered relocation words match target. Nine PI operand gaps close in this composition; historical failures remain preserved. That image retained 21 other byte differences and relocation-order differences. This historical composition did not change source or exact counts.

MAINL archive/file source promotion: 19 existing units /2,479 bytes added, now source 84/145 (23,150 bytes), exact 0. Two independent include-consuming root assemblies and hybrid links have equal raw root OBJ/EXE/MAP. All 19,449 scoped maintained bytes match target; the archive scope has one matching ordered relocation. Eight fresh model phase receipts and the buffer1754 contract are retained by complete EXE identity, not rerun by fast replay. FILE outer model terminal statuses are unknown after transport timeout; durable successes are verified. One DATA byte and 461 global relocation-order differences remain; no gap/DOSopen/close/STR_IEQ/heap double credit or cold aggregate.
