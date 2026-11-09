# Reimu Chargeshot: complete natural creation, homing and collision traversals

All reset/shot/Hyper, deceleration-homing update, history shifting, collision
and sprite passes in the ten-function original `cs_reimu` owner use natural
bounded C++ `for` loops. All 24 real physical slots reset; ordinary launches
initialize four projectiles with seven X/Y history positions each; Hyper
preserves its first-free early break. Update moves twelve projectiles, but
hittest still sees only six and skips inactive/offscreen projectiles through
the same for-header index/pointer advance. Rendering retains the PC-98
SPRITE16 monochrome service call between original cels.

Sequential original TC4/full MAIN TLINK stages `af1136a` through final
`af1136f` each reproduced the complete 1,448 CODE bytes, 138 ordered native
fields, ten PUBLICs and original Japanese MAIN image/relocations across two
independent rounds. Both collision and rendering signed indices proved safe
to declare in their respective for headers. No shared DATA/ABI ownership is
changed.
