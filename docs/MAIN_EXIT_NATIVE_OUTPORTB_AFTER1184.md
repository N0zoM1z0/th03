# PC-98 shutdown: natural Borland outportb is byte-exact

All four original VRAM port writes in `game_exit()` can be expressed as
native C++ `outportb(port, value)` calls from Borland `<dos.h>`. TC4 4.02
lowers the intrinsic to the exact original DX/AL/OUT instructions, without
an extra function call or changed OMF relocations. The order is essential:
select display page 1, clear, select page 0, clear, **select page 0 again**,
then select access page 0 before stopping VSYNC, memory, text and joystick
services and restarting EGC. The repeated display-page write is not removed.

The independent scoped stages `af1184a` (first OUT), `af1184b` (second OUT),
`af1184c` (all four), and final `af1184d` all passed two original TC4 and
normal MAIN TLINK rounds, matching all 67 CODE bytes, eight ordered native
fields, one PUBLIC and the complete Japanese MAIN loaded image and ordered
MZ relocations. This improves on the historical explicit `_DX/_AL` source
without padding, a handwritten instruction replacement, or a new helper ABI.
