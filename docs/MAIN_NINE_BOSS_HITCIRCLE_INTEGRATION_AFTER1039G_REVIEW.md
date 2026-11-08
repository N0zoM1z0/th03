# TH03 MAIN nine BOSS + HitCircle integration after1039g

The current nine complete BOSS physical owners and the complete four-function
HitCircle physical owner were rebuilt simultaneously at stage `af1039g`:

| Scope | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| Nine complete BOSS owners | 17,451 | 2,434 | 85 |
| Complete `hitcirc` owner | 445 | 30 | 4 |
| **Ten complete owners** | **17,896** | **2,464** | **89** |

Two independent original Turbo C++ 4.02 rounds reproduced all ten owners'
CODE, ordered native fields and PUBLIC offsets. The complete normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Only these ten physical owners were rebuilt; unaffected original game
objects and CRT were reused.

This integration includes the current Mima/Yumemi, Chiyuri Fans, Kotohime
Radial/Update, Chiyuri Update and HitCircle spawn pointer/coordinate source
refinements. No full cold replay was run.

Protected report: `.analysis/work/exatt-layout-af1039g/report.json`

SHA-256: `299f5f7815f5e0e878129caad1981f7445feb9ea02c7617b24c218c8971a9cb2`
