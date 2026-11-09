# Player core: natural movement retry, glow guard and skill leaf

The full player core owner includes the human/CPU movement, hit and charged
shot state machine, Hyper callback dispatch, and skill decrement. The human
invalid-direction retry now uses a natural unbounded `for` loop with its
original one-retry semantics. At the end of the complete state update, a
non-background page returns after resetting the glow pattern; invincibility
and Hyper glow still have their original priority on the back page. The
story-mode skill decrement recognizes player zero with natural truthiness.

The final two-round original TC4/TLINK stage `af1191e` matched all **3,135
CODE bytes**, 260 ordered native fields, 21 PUBLICs, and the Japanese MAIN
loaded image and ordered MZ relocations. The sequence `af1191a` (retry),
`af1191d` (glow), and `af1191e` (skill leaf) isolated successful changes.

Independent alternatives were rejected on compiler evidence: merging the
repeated base-damage assignments before a conditional CPU penalty (`af1191b`)
and inverting the Hyper standby callback check into an early return
(`af1191c`) both changed CODE. The original expressions remain.
