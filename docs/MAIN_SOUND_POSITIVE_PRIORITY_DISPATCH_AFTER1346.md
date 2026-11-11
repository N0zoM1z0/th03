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

## 2026-11-11: native early exits and original priority selection

The current `snd_se_play()` now rejects an inactive driver immediately,
installs the first selected sound and exits, and explicitly rejects
replacements whose previous sound has strictly greater priority. Only
an accepted replacement resets the effect frame. The original two
priority-table reads remain in their original order: swapping their
operands is not supported by old TC4 even for an equivalent comparison.

`snd_se_update()` now exits before any state change when the PMD driver
is inactive or no sound is selected. The first frame still issues
`INT 60h` with AH and AL in their original registers; a natural
`if(!snd_se_frame)` detects that frame without changing native output.
The byte-memory postfix frame increment, strictly greater expiration
and original reset order are unchanged.

Isolated complete-owner stages `af1354i` through `af1354m` proved the
incremental source changes in two original Turbo C++ 4.02 rounds.
Current two-owner `af1354n` (SE and Kaja dispatcher) reproduces
**150 CODE bytes, 20 ordered native fields and 3 PUBLICs**. Consumer
stage `af1354o` recompiles the two audio owners with the complete
Kotohime BOSS: **1,990 CODE bytes, 282 fields and 14 PUBLICs**, both
normal Japanese MAIN links and ordered MZ relocations original-exact.
No full cold replay or target-byte adjustment was used.

Current proof: `.analysis/work/exatt-layout-af1354n/report.json`, SHA-256
`ced87e4fe330687139d911a7e9947dc8aabe8aae1955338ec9db005d2df577f1`.
Joint proof: `.analysis/work/exatt-layout-af1354o/report.json`, SHA-256
`91a1f21152262ca34b6c08c37839b2192050e53718877ce259e9baad6c40408a`.

## 2026-11-11: source-exact Kaja software-interrupt exits

`snd_kaja_interrupt()` now directly returns the original AX when no
hardware music driver is active. Once active, it loads the caller's
16-bit AX value, selects PMD for every `snd_midi_active` byte other
than 1, and returns after the original INT 60h. The MIDI INT 61h
remains the final branch. A separate `af1364i` trial reversed the
PMD/MIDI conditional to select MIDI first; TC4 emitted different CODE,
so its original comparison and vector ordering were retained.

`af1364h` proved the inactive return and `af1364j` the PMD return.
Current source-bound `af1364k` recompiles **both** SE and Kaja objects:
**150 CODE bytes, 20 ordered native fields, 3 PUBLICs**, exact normal
MAIN links and relocations in both original TC4 rounds. Joint `af1364l`
recompiles those sound leaves with Kana BOSS, Kana Extra Attack,
Bullet, both shared BOSS owners and Polar: **6,347 CODE bytes,
640 ordered fields, 46 PUBLICs**, both normal links exact.

Current proof: `.analysis/work/exatt-layout-af1364k/report.json`, SHA-256
`f033cf9cd326835bf173ac6133278e8e1faf58c97ec5acbdc8f730f3abdf58c6`.
Joint proof: `.analysis/work/exatt-layout-af1364l/report.json`, SHA-256
`9c4c585173e1e1ef0f06de6311545c2cd6db874563c96e079a01b157e3ed3b34`.
