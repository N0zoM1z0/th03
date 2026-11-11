# Chiyuri BOSS: exact cardinal cadence, trail release and fan selection

The historical `af1347g` `ba_chiyu` controller contained a positively gated
four-cardinal-bullet phase: the **unsigned 16-bit frame remainder must
be one** before the four axis warnings, mutable byte steering and
four quarter-turn bullet spawns. Off-cadence ticks never touch the
bullet template or consume RNG. The related 32-shot ring family uses
a separate positive one-remainder gate; it retains its original
axis warning, post-terminal state update and unconditional common
ring, followed by four additional eight-pellet rings at high difficulty.
The order of the terminal state update and emissions is preserved even
on the last original attack frame.

The trailing 48-shot ring uses an exact positive release frame rather
than an early return; its independent eight-frame warnings still happen
first. The horizontal and vertical fan passes now form an actual
mutually exclusive `if/else if` phase pair. All four nested signed
16-bit index/division loops, per-shot byte speed increments/decrements,
`polar()` paths, BOSS flags and the final mode reset keep the original
sequence. The cardinal byte reverse-rotation is explicitly tested for
zero, without reversing branch polarity.

Original TC4 4.02/TLINK staged trials `af1347a` (trail release),
`af1347b` (horizontal/vertical fan selection), `af1347c` (whole cardinal
cadence), `af1347d` (whole ring cadence) and `af1347e` (explicit byte
steering guard) all reproduced **2,654 bytes** of physical BOSS CODE
and complete Japanese MAIN normal links in two independent rounds.
After documenting the native guard constraints, final source-bound
`af1347g` matched **2,654 CODE bytes, 381 literal ordered OMF fields
and 11 PUBLICs** in two native rounds. Joint `af1347h` compiled Chiyuri,
Bullet, both shared BOSS owners and Hitbox: **6,554 CODE bytes, 716
ordered native fields, 40 PUBLICs** with both entire Japanese MAIN
images, normalized MAPs and ordered MZ relocation vectors exact. Only
these selected physical owners were compiled, not cold replay.

Counterexample `af1347f` inverted Chiyuri's forward/reverse cardinal
byte steering to the opposite comparison and swapped the two arms. This
kept exactly 2,654 CODE bytes and 381 OMF fields but changed **nine
original CODE offsets** in the cardinal controller. The attempted
rewrite was reverted; source-level behavioral equivalence is not the
native-exact criterion.

Current source and related owner reviews:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1347g af1347h
```

This improves a previously selected source-exact BOSS physical owner;
it does not represent first-time ownership of 2,654 gameplay bytes or
Factory canonical packed-file acceptance.

## 2026-11-11: early return for the two largest attack clocks

The maintained `chiyuri_pattern_cardinal()` and `chiyuri_pattern_rings()`
now explicitly return whenever their independent unsigned-word script
remainder is **not one**. Their larger bodies are no longer enclosed in
single-use positive gates. This preserves warning effects, cardinal
forward/reverse byte steering, four shot calls, ring RNG consumption,
mode reset before the last 32-shot release and four optional high-level
pellet groups. The intro renderer also short-circuits its global odd
frame and animation cutoff. The large update uses natural nonzero byte
predicates for the palette countdown and rendering stage while retaining
the original post-decrements and palette-call order.

A separate attempt to express the first intro AL-carried phase step as a
volatile byte load plus natural assignment (`af1357d`) changed native
CODE and was reverted; the explicit AL carriers remain necessary.
Stages `af1357a`, `af1357b`, `af1357c` and current `af1357e` rebuilt
the complete **2,654-byte**, **381-field**, **11-PUBLIC** Chiyuri owner
in two original TC4 rounds. Consumer joint `af1357f` compiled Chiyuri,
Bullet, both shared BOSS objects, Hitbox, HitCircle and Chiyuri Extra:
**7,977 CODE bytes, 801 ordered fields, 48 PUBLICs**, with both normal
Japanese MAIN links and all ordered MZ relocations exact.

Current receipt: `.analysis/work/exatt-layout-af1357e/report.json`, SHA-256
`5d872fa923e0fa02a4defb5ce7ce2638cbc9e3f0bbc38d35ff093e6dd20b6085`.
Consumer receipt: `.analysis/work/exatt-layout-af1357f/report.json`, SHA-256
`6f8542fbb999c713b79f8655472442495719e47dcdce9dcc22a5a8d76ce94f6e`.
