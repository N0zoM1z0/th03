# TH03 MAIN Kotohime BOSS update: active-player PID and frame lifetime (af1084b)

This pass revisits the complete 332-byte far-cdecl
`gba_boss_update_kotohime()` controller at `1f1f:2c58` (`0x21E48`). It does
not stop at a small arithmetic leaf: the entire `ba_koto` physical owner was
rebuilt in two original Turbo C++ 4.02 rounds after the update changes.

## Controller order

The update first refreshes all seven difficulty-derived parameters when
`boss_update_start()` is true. The inactive-player guard then returns before
target tracking, bullet PID selection, frame advancement, pattern dispatch,
collision-map updates or hitbox/HP processing. On the active player, the
controller updates the target and bullet PID, advances the global boss frame,
executes the complete mode switch (INTRO, SELECT, Random Ring, Aimed Ring,
Pellet Arc, Radial, DESCEND and EXPLODE), and then performs the collision tail
unless a mode's early return applies.

## Natural local lifetime

The `pid_other` local is now created only after the inactive-player return and
initialized at its first use:

```cpp
if(pid_current != gba_boss_launched_by) {
    return;
}

pid_t pid_other = 1 - pid_current;
boss_target_update();
bullet_template.pid = pid_other;
++boss_frame;
```

This is the same useful lifetime boundary as the Reimu controller: the
inactive-player path never needs an opponent PID local. The target update and
bullet PID assignment remain in their original order.

The word frame counter uses prefix increment. Original disassembly has a
single `INC word ptr [boss_frame]`; the prefix form reproduces that operation
and is verified in isolation after the PID-scope change.

## Native experiments

- Stage `af1084a` moved `pid_other` below the inactive-player guard and
  initialized it in the declaration. The full 1,840-byte `ba_koto` owner
  matched in two original TC4 rounds.
- Stage `af1084b` changed `boss_frame++` to `++boss_frame` with the PID local
  change retained. The full owner still matched in two independent rounds.
- The switch dispatch, all seven level formulas, INTRO/EXPLODE returns,
  collision-map writes, hitbox setup, HP subtraction and `boss_hittest_end()`
  remain unchanged.

## Original disassembly cross-check

Ghidra identifies the controller at `0x21E48`, with far-cdecl calling
convention. The disassembly confirms the seven level assignments, the
launched-player comparison, opponent PID calculation, target update, bullet
PID assignment, word frame increment, switch-table dispatch and collision
setup. The source retains the existing direct inactive-player return rather
than converting the whole function into a positive branch; the current
naturalization only shortens the PID local lifetime.

## Complete original-owner verification

Stage `af1084b` rebuilt the complete `ba_koto` physical owner in two
independent original Turbo C++ 4.02 rounds: all 1,840 CODE bytes, 262 ordered
native fields and eleven PUBLIC offsets match. Both normal Japanese MAIN
links reproduce the original loaded image and ordered MZ relocations. The
source overlay independently checked the maintained `kotohime.cpp` producer
and its compiler dependency.

Report: `.analysis/work/exatt-layout-af1084b/report.json`

SHA-256: `e81732a00d7ff78519f52ee50afb4f337e015a1aa9c61dc4b3fa0d7825c152d5`

Current `ba_koto` source SHA-256:
`48954fcec81024d01b344dd9f25faad734764a1c08b9cac4e364bb40fc178559`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.
