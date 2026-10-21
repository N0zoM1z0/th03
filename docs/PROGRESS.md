# TH03 reconstruction progress

| Artifact | Target bytes | Source-present units | Exact units | Exact functions | Exact owned bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| th03-op | 36041 | 33 | 0 | 0 | 0 |
| th03-main | 130882 | 87 | 86 | 403 | 65198 |
| th03-mainl | 37975 | 116 | 0 | 0 | 0 |
| th03-zun | 16242 | 3 | 0 | 0 | 0 |

Reviewed authored-byte coverage is scoped to currently reviewed file-backed unit extents; the whole-product authored denominator remains unknown.
Infrastructure and reference builds do not count as game reconstruction.

Historical MAINL PI composition: 6,144 owned decoded bytes and 110 scoped ordered relocation words match target. Nine PI operand gaps close in this composition; historical failures remain preserved. That image retained 21 other byte differences and relocation-order differences. This historical composition did not change source or exact counts.

MAINL root-tail source promotion: 16 existing units / 722 bytes added, now source 116/145 (25,988 bytes), exact 0. Two independent include-consuming root assemblies and hybrid links have equal raw root OBJ/EXE/MAP. All 22,287 scoped maintained bytes match target; root-tail scopes have empty relocations. The 722 bytes are 701 bodies plus 21 actual source-traced producers, with no duplicate archive body credit. Target and candidate models each passed 3,895 scenarios / 8,445 calls, including 10 actual DIV stops. SAJOUT remains private/unreferenced and structural-only. Fast replay retains models, not reruns. One DATA0849 byte and 461 global relocation-order differences remain; retained objects are contextual, not a cold aggregate.
