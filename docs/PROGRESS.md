# TH03 reconstruction progress

| Artifact | Target bytes | Source-present units | Exact units | Exact functions | Exact owned bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| th03-op | 36041 | 33 | 0 | 0 | 0 |
| th03-main | 130882 | 87 | 86 | 403 | 65198 |
| th03-mainl | 37975 | 49 | 0 | 0 | 0 |
| th03-zun | 16242 | 3 | 0 | 0 | 0 |

Reviewed authored-byte coverage is scoped to currently reviewed file-backed unit extents; the whole-product authored denominator remains unknown.
Infrastructure and reference builds do not count as game reconstruction.

MAINL contextual composition: 6,144 owned decoded bytes and 110 scoped ordered relocation words match target. Nine PI operand gaps close in this composition; historical failures remain preserved. Whole decoded image retains 21 other byte differences and relocation-order differences. This historical composition did not change source or exact counts.

MAINL staff/graphics source promotion: 11 existing units / 3,339 bytes added, now source 49/145 (13,184 bytes), exact 0. Two fresh include-consuming root assemblies and hybrid links have equal raw root OBJ/EXE/MAP; second link retains the first two graphics objects and 32 contextual objects, not a cold aggregate. All 9,483 scoped maintained bytes match target. Existing 112 ordered relocation words remain equal; new snow/staff relocation membership matches but ordering differs. One DATA byte and 461 global relocation-order differences remain. Full runtime models are retained by complete EXE identity, not rerun in fast replay.
