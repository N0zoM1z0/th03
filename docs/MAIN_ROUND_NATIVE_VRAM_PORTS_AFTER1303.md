# Frame scheduler: native C++ PC-98 VRAM page registers

The complete round-loop controller now writes the PC-98 display and access
page ports through Borland's native `outportb()` intrinsic rather than a
handwritten assembly block. Both ports retain their physical addresses
`0xA6` and `0xA4`, and the calls preserve the original DX/AL/OUT sequence.
The following `page_front = _AL` still consumes the AL value left by the
**second** port write, before the XOR page toggle. This matters because a
new source-level memory reload would change the hardware-visible frame
scheduler's original instruction stream.

Original TC4/TLINK stages `af1303a` (both port writes) and `af1303b` (named
ports) each match all 3,050 CODE bytes, 433 ordered native fields, eight
PUBLIC offsets and the complete Japanese MAIN loaded image and ordered MZ
relocations in both independent compilation rounds. The full controller,
including its match/game-over exits, VSync waits and page-swap sequence, was
recompiled as one original physical owner (`entry`).
