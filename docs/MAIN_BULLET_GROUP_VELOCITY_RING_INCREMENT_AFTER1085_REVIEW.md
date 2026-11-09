# TH03 MAIN Bullet group velocity: natural ring-count increment (af1085v)

This pass targets the complete 819-byte near-Pascal
`group_velocity_set(int i)` dispatcher inside the original 2,685-byte Bullet
physical owner. It handles the ordinary and aimed 2/4/8/16/32-ring groups,
randomized ring groups, shared TH02/TH03 groups, constrained-angle groups and
single aimed bullets. The dispatcher writes the shared byte angle and returns
the completion flag consumed by `bullets_add()`.

## Accepted C++ improvement

Both ordinary and aimed ring fallthrough chains accumulate the number of
remaining ring positions. The terminal one-count increment now uses prefix
increment:

```cpp
case BG_32_RING: ring_remaining = 16; ring_i_shift--;
case BG_16_RING: ring_remaining += 8; ring_i_shift--;
case BG_8_RING:  ring_remaining += 4; ring_i_shift--;
case BG_4_RING:  ring_remaining += 2; ring_i_shift--;
case BG_2_RING:
    ++ring_remaining;
    ring_i_shift--;
    i_angle = (i << ring_i_shift);
    // completion test and no-aim velocity path
```

The same change is present in the aimed ring family. The value produced by
`++ring_remaining` is not consumed; it only updates the byte count. The
compiler nevertheless had to be tested against the complete physical owner,
not inferred from C++ equivalence.

## Rejected alternatives

The following seemingly natural rewrites changed the complete original
`bullet` CODE and were restored:

- Initialize `done` at declaration instead of at its original statement
  (`af1085g`).
- Replace the ten `ring_i_shift--` operations with prefix decrement or
  compound subtraction (`af1085i`, `af1085s`).
- Move `aim_x`/`aim_y` initialization to their declarations, or replace the
  pair with a `PlayfieldPoint` (`af1085j`, `af1085r`).
- Narrow `bullet_i`, `trail_i` or `group_i` to their loop scopes
  (`af1085k`, `af1085l`, `af1085m`).
- Move transfer-only locals or the group completion flag into their
  conditional branch (`af1085n`, `af1085o`, `af1085p`, `af1085q`).

The existing ring-shift postfix decrements, function-scope aim coordinates,
and bullets_add allocator locals remain as they are. The accepted prefix
increment is intentionally narrow; it does not imply that all local
postfix operations can be changed.

## Complete original-owner verification

Stage `af1085u` rebuilt the entire Bullet physical object in two independent
original Turbo C++ 4.02 rounds. All 2,685 CODE bytes, 196 ordered native fields
and 20 PUBLIC offsets match. The original 9,500-byte BSS extent is preserved,
and both normal Japanese MAIN links reproduce the original loaded image and
ordered MZ relocations. The source overlay checked the maintained
`bullet.cpp` producer.

Report: `.analysis/work/exatt-layout-af1085u/report.json`

SHA-256: `b99d55bfe35577aa32e4b441b049d1882246eb5e9f41cccde23934119606f619`

Current `bullet.cpp` SHA-256:
`8c8ddaa4d24e514152f9e235f3a2399853e924cc28d31cf175dc45f6b8b381cc`

## Eight-owner integration

Stage `af1085v` rebuilt the current Bullet owner together with
`ba_koto`, `ba_reimu`, `ba_yumem`, `ba_chiyu`, `ex_rfly`, `ex_reup` and
`hitcirc` in two independent original TC4 rounds: 13,158 CODE bytes, 1,555
ordered native fields and 75 PUBLIC offsets match. Both normal Japanese MAIN
links reproduce the original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1085v/report.json`

SHA-256: `c3d5f5ba9b80eef6462e1c8ac33779c6b588779dd4cd08d4824f0e138d8e0ba3`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.
