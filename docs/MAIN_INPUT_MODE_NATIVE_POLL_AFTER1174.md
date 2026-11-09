# Input modes: joystick guards and keyboard wait polling

The full nine-PUBLIC `inp_m_w` physical owner handles the interface,
two-player keyboard/joystick pairings, CPU modes and keyboard wait phases.
Both joystick-versus-keyboard modes now return immediately when no joystick
exists; the original key reset and conditional joystick read stay in order.
The wait-for-change controller uses natural zero checks for release/press
sensing and its zero-duration request. The original unsigned input values,
9999-frame sentinel, VSync calls and two independent CANCEL/OK bit tests
remain unchanged.

The final `af1174e` original TC4/TLINK stage matched all 367 CODE bytes,
58 ordered native fields, nine PUBLIC offsets, and the complete Japanese
MAIN image and ordered MZ relocations in two independent rounds. `af1174b`
also verified the unchanged `initmain` physical owner alongside this module;
it is independent native evidence, not an additional modified input owner.
