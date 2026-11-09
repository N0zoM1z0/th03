# TH03 MAIN Kotohime radial burst: center-angle initialization and byte-phase constraints (af1084l)

This pass revisits the complete 302-byte near-cdecl
`kotohime_pattern_radial_burst()` at `1f1f:2b2a` (`0x21D1A`). The function
contains a nested center-count by burst-count bullet traversal, two signed
16-bit divisions per center/bullet coordinate, byte-angle truncation, sound
and render/mode completion transitions. The goal was to recover more natural
C++ without disturbing the original AL/DI/SI behavior.

## Current source and loop shape

At the start frame, the function resets the expanding render state, effect
radius and warning frame. It then advances the byte movement phase by the
original AL-mediated `+0xFC` operation. During the expanding phase it moves
the sine target and increases radius. After the expansion threshold it enters
WARNING, grows the radius and advances the warning frame. Once release is
reached, it initializes the bullet template and emits the nested radial burst:

```cpp
for(register int center_i = 0; center_i < kotohime_orbit_count; ++center_i) {
    register int x;
    register int y;
    register unsigned char center_angle = (
        boss_move_phase +
        ((KOTOHIME_FULL_TURN_STEPS * center_i) / kotohime_orbit_count)
    );
    x = polar(
        boss_center_x,
        boss_effect_radius,
        CosTable8[center_angle]
    );
    y = polar(
        boss_center_y,
        boss_effect_radius,
        SinTable8[center_angle]
    );
    bullet_template.center.x.v = x;
    bullet_template.center.y.v = y;

    for(register int bullet_i = 0; bullet_i < kotohime_burst_count; ++bullet_i) {
        bullet_template.angle = (
            KOTOHIME_BURST_CENTER_ANGLE_OFFSET +
            center_angle +
            ((KOTOHIME_BURST_HALF_TURN_STEPS * bullet_i) / kotohime_burst_count)
        );
        bullet_template.speed.v = (
            KOTOHIME_BURST_SPEED_BASE +
            ((KOTOHIME_BURST_SPEED_SCALE * bullet_i) / kotohime_burst_count)
        );
        bullets_add();
    }
}
```

The central byte angle is now initialized at declaration. It is computed once
per center from the current byte movement phase plus a signed 16-bit
`256 * center_i / orbit_count` division, then truncated to a byte. The inner
loop retains signed 16-bit divisions for the half-turn angle and speed scale;
these are not replaced with shifts or byte arithmetic. The x/y polar values
remain separate register locals and assignments.

## Native experiments

- Stage `af1084e` moves `center_angle` initialization into its declaration.
  The complete `ba_koto` owner still matches in two original TC4 rounds.
- Moving x/y declarations after center-angle calculation changes CODE
  (`af1084i`); their declaration order remains before `center_angle`.
- Initializing x or y directly from its polar call changes CODE
  (`af1084g`, `af1084h`); retain the separate assignments.
- Replacing the initial AL-mediated phase update with
  `boss_move_phase -= 4`, `boss_move_phase = boss_move_phase - 4`, or
  `boss_move_phase += (unsigned char)0xFC` changes CODE
  (`af1084c`, `af1084j`, `af1084k`). Keep the explicit `_AL` load/add/store.
- Replacing the warning-frame postfix increment with prefix increment
  changes CODE (`af1084d`). Keep `boss_render_frame++`.

These tests are scoped to the complete `ba_koto` owner, not only the radial
function's apparent instruction sequence.

## Original disassembly cross-check

Ghidra identifies the function at `0x21D1A`, near-cdecl, 302 bytes. The
instruction stream confirms the frame-start reset, AL byte phase add of
`0xFC`, signed comparisons and threshold transition, warning radius/frame
updates, pre-tested DI/SI loops, `IDIV` before byte-angle truncation, the
polar calls, inner angle/speed division, bullet emitter, sound and final
mode/frame reset. The current source keeps the signed arithmetic and
side-effect order intact.

## Complete original-owner verification

Stage `af1084e` rebuilt the complete `ba_koto` physical owner in two
independent original Turbo C++ 4.02 rounds: all 1,840 CODE bytes, 262 ordered
native fields and eleven PUBLIC offsets match. Both normal Japanese MAIN
links reproduce the original loaded image and ordered MZ relocations. The
source overlay checked the maintained `kotohime.cpp` producer and compiler
input dependency.

Report: `.analysis/work/exatt-layout-af1084e/report.json`

SHA-256: `9b0eb1ec1040a5fd53ce0adc2eb267bc2deface5343a49aa00d001052982906d`

Current `ba_koto` source SHA-256:
`d0aa332d55322f8e7bfa21d5fe93a82a0859d1794f4d2278472b346b5b54c5b3`

## Six-owner integration

Stage `af1084l` rebuilt `ba_koto`, `ba_reimu`, `ba_yumem`, `ba_chiyu`,
`ex_rfly` and `ex_reup` together in two independent original TC4 rounds:
10,028 CODE bytes, 1,329 ordered native fields and 51 PUBLIC offsets match.
Both normal Japanese MAIN links reproduce the original loaded image and
ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1084l/report.json`

SHA-256: `7fc3be1cb249f6b092f253f5a2f947a3ff30abad91e66704cc36628213673f62`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.
