# TH03 MAIN Enemy controller: real chain-ring state updates

The complete `enemy_hittest` controller now explicitly advances the original
chain ring at both distinct starting events: global enemy damage and a lethal
non-explosion hit. The previous `chain_start_next_in_ring(pid)` expression
macro deceptively expanded into multiple separate assignments and an index
wrap; it was **not** a function call. In each branch the natural C++ code now
loads the selected ring index, stores it into the enemy, initializes that
slot's hit count and charged value, and *then* advances/wraps the index.
The existing explosion-continuation branch deliberately does not start a
new slot. No out-of-range guard, invented state or gameplay fix was added.

`af932b` genuinely recompiled the entire original four-function `eupdb`
physical object in two independent original TC4 rounds and relinked
complete normal Japanese MAIN both times: **1,160 CODE bytes**, **103
literal ordered OMF fixup fields**, four PUBLICs and full original
124,642-byte loaded program/1,553 relocations match. The other 98 project
objects and original CRT were reused, not cold replayed. Report:
`.analysis/work/exatt-layout-af932b/report.json`, SHA-256
`cef593f8d4a6fdaab19495e837dac6d95186b87f108a39cc2dfcb10215034375`.

A rejected alternative extracted these operations into a typed inline
C++ function. In trial `af930c`, the physical object expanded to 1,187
instead of 1,160 bytes, changed PUBLIC offsets and fixups. The direct
statements preserve original TC4 register lifetime and store order while
eliminating the expression macro. This is source quality and provenance
progress within historically covered CODE, not new distinct product bytes.
