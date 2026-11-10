# PMD sound effects: exact positive selection and frame dispatch

`src/main/sound/se.cpp` now expresses both original sound services as
positive state gates. `snd_se_play()` only enters its selection logic
while the PMD driver is active. If no effect was previously selected,
it installs the new effect directly; otherwise the original priority
ordering can replace the current effect and reset its frame counter.
The two original `snd_se_priorities[]` index reads remain in their
exact historical order; these are not interchangeable on original TC4.

`snd_se_update()` now enters only when the PMD driver is active **and**
a real effect is selected, in that short-circuit evaluation order.
Only effect frame zero loads AH=PMD_SE_PLAY and AL=the effect number
and invokes the original fixed `INT 60h` hardware service. The next
byte-memory frame operation remains **postfix** `snd_se_frame++`, and
the priority-indexed duration resets the playing state only when the
original frame becomes *strictly greater* than its limit. This keeps
all original software interrupt, timer and clobber behavior.

Original native TC4/TLINK `af1346a` proved the first-selection/priority
`if/else if`; `af1346b` proved the combined idle guards and explicit
zero-frame gate; `af1346c` and `af1346d` proved the active-only nested
scheduling in both sound services. Final current-source `af1346f`
matched the complete **120 CODE bytes, 18 ordered fields and two PUBLICs**
in two rounds. Joint `af1346g` also recompiled the existing Kaja PMD/MIDI
interrupt dispatcher: **150 CODE bytes, 20 ordered fields and three
PUBLICs** matched both complete Japanese MAIN links. Consumer joint
`af1346h` added the current Rikako BOSS: **1,827 CODE bytes, 235 ordered
native fields and eleven PUBLICs**; both normal full MAIN links,
normalized MAPs and ordered MZ relocations remained exact. Neither
joint compiled any other original owner or invoked cold replay.

Counterexample `af1346e` reversed the two sound priority operands to
`priorities[new] >= priorities[old]`. This is semantically equivalent
for ordinary values, but original TC4 emitted **121 instead of 120
CODE bytes**, including different register and branch traffic. The
original operand order was restored, just as earlier tests rejected
prefix increment for the byte frame counter.

Read-only current source proof:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1346g af1346h
```

The physical owners were already tracked; this is a source-control and
ABI exactness improvement, not 120 newly recovered bytes or canonical
Factory packed-file acceptance.
