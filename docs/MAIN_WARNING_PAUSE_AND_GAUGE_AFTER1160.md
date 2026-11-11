# Warning/Gauge HUD: exact native pause and flash control

The historic `af1160e` version of the complete `warning` physical owner
used natural `while` loops for both key-release polls and the pause/quit
command loop. Four word-frame gauge predicates used remainder truthiness.
The 27-frame palette flash scoped its register index to a `for` header;
warning text clearing used prefix advancement of both row and index.
The byte warning-flag parity retained its explicit unsigned promotion.

Two original TC4/TLINK rounds at `af1160e` matched all 1,560 CODE bytes,
125 ordered native fields, seven PUBLICs and the Japanese MAIN image plus
ordered relocations. Hardware GRCG and far-return assembly entry sequences
remain unchanged; the warning completion still executes the first active
Gauge update during the same call.

## Current pause, warning flash and text-clearing source (2026-11-11)

The current controller uses direct nonzero input tests for both
key-release polls, and `for(;;)` for its unbounded command loop. Each
poll retains the original key sensing, quit-before-cancel priority and
one-frame VSYNC delay. The portrait display helper uses direct byte
player truthiness for the second playfield. The four unsigned word-frame
Gauge flash predicates and the 27-frame palette tone now test their
actual low bit with `& 1`, leaving hardware GRCG and palette writes in
place. The original multiply-by-tone-increment stays after that parity
read: an equivalent ternary color selection (`af1362m`) changed full
CODE from **1,560 to 1,563 bytes** and was rejected.

The palette flash and six-row text-clear loops now use pre-tested `while`.
The palette loop increments its signed frame index only after input,
VSYNC, tone assignment and display; the text-clear loop advances its
unsigned index and row independently, both **after** each text draw.
The original same-frame warning completion/active-Gauge update remains.

Stages `af1362h`–`af1362l` proved these local transformations in two
original TC4 rounds. Current-source `af1362n` rebuilds **1,560 CODE
bytes, 125 ordered native fields and 7 PUBLICs** in the complete
`warning` object, with both normal Japanese MAIN links and relocations
exact. Integration stage `af1362o` recompiles Warning, input modes,
VSYNC delay, sound, static HUD, Reimu BOSS and CPU: **5,704 CODE bytes,
555 native fields and 39 PUBLICs**, both normal links original-exact.

Current proof: `.analysis/work/exatt-layout-af1362n/report.json`, SHA-256
`fea00b02c17918aadad7222d1a75089b74b6910fb6bee9003dea7c914dc560cd`.
Joint proof: `.analysis/work/exatt-layout-af1362o/report.json`, SHA-256
`a1f7952038791f7b18296ebf4549812b0f3f73f6f3bf8de34c652f2c8116dbe4`.
