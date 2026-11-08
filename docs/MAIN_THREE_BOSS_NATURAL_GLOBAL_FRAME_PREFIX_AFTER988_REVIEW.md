# TH03 MAIN: natural prefix updates for three major BOSS frame clocks

The unused-result increment of the shared 16-bit boss_frame now uses
prefix form in the complete Mima, Reimu and Yumemi BOSS source owners:

    ++boss_frame;

This is a natural C++ spelling for an increment whose old value is not
consumed. Genuine original Turbo C++ 4.02 builds confirm that it emits the
same complete physical CODE, OMF relocations and PUBLIC layout in each
owner. This result is specific to the 16-bit global frame clock; it does
not generalize to byte animation counters, whose prefix/postfix choices
have separately demonstrated different machine code.

## Independent complete-object verification

| Physical owner | Stage | CODE | Ordered FIXUPPs | PUBLICs |
| --- | --- | ---: | ---: | ---: |
| ba_mima | af987c | 1,922 | 277 | 9 |
| ba_reimu | af987d | 2,020 | 270 | 9 |
| ba_yumem | af988a | 2,358 | 343 | 10 |

Each stage used two independent original TC4 4.02 compiler rounds and two
complete normal MAIN links. Each preserves the 124,642-byte Japanese MAIN
loaded image and all 1,553 ordered MZ relocations while reusing the other
98 original game objects and Borland CRT.

Protected reports:

- .analysis/work/exatt-layout-af987c/report.json,
  SHA-256 ca0b3baec60340356dc999028f19b7f1214d7ea8ef4dbdba89a490d5691d8465
- .analysis/work/exatt-layout-af987d/report.json,
  SHA-256 60ef9a74359c42783ea8d34d5c41226f0388bcd46f6ca5c648b5c30fdeb3ea3d
- .analysis/work/exatt-layout-af988a/report.json,
  SHA-256 7b845961ff327892799064adc8654d78ca2f83ea34837119586a4edb779af6f1
