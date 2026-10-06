# TH03 OP Music Room carrier

This review covers all fourteen functions in the original Music Room CODE
carrier, decoded `0990:0C1E..14E2`, 2244 bytes. The frozen wrapper is
`th03/op_music.cpp`, including `th02/op/m_music.cpp` at ReC98 revision
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`. The Japanese packed OP remains
candidate-local-attested; independent pristine-dump provenance is unknown.
Decoded observations do not supply stored-file offsets or exact acceptance.

| Function | Decoded start | Bytes | Return / argument cleanup |
|---|---:|---:|---|
| track_put_both | 0990:0C1E | 114 | near Pascal / 4 |
| tracklist_put_both | 0990:0C90 | 39 | near Pascal / 2 |
| nopoly_B_snap | 0990:0CB7 | 49 | near / 0 |
| nopoly_B_free | 0990:0CE8 | 14 | near / 0 |
| nopoly_B_put | 0990:0CF6 | 30 | near / 0 |
| polygon_build | 0990:0D14 | 143 | near Pascal / 12 |
| polygons_update_and_render | 0990:0DA3 | 502 | near / 0 |
| music_update_render_and_flip | 0990:0F99 | 54 | near / 0 |
| cmt_bg_snap | 0990:0FCF | 315 | near / 0 |
| cmt_load | 0990:110A | 73 | near Pascal / 2 |
| cmt_bg_free | 0990:1153 | 41 | near / 0 |
| cmt_unput | 0990:117C | 285 | near / 0 |
| cmt_load_unput_and_put | 0990:1299 | 109 | near Pascal / 2 |
| musicroom_menu | 0990:1306 | 476 | far / 0 |

The native IRAND42 and far cdecl POLAR26 execute as helper context, without
additional unit/byte credit. Near/far frames, original complete function
boundaries, call sites, saved BP/SI/DI/DS, stack segment and cleanup are checked.
The independent scalar model compares ordered calls, port writes, native
stores, bulk load operands, external input writes and the complete physical
memory image outside the 64 KiB stack.

The comment reader performs signed 16-bit multiplication by 840 before
promoting the file offset to a signed long. For example, track40 seeks -31936.
It ignores the file operation replies and short-read lengths; stale comment
bytes remain, except that byte40 of each of twenty 42-byte lines is cleared.
Byte41 remains unchanged. Snapshot/restore visits ten DWORDs on each of 320
rows, separately copying all four planes; the allocated size is 12800 per
plane. Near point coordinates and their closing duplicate retain 16-bit
arithmetic and the original signed subpixel conversion.

The B-plane copy uses REP MOVSW without CLD. DF=1 attempts a backward copy
through offsets 0, FFFE, FFFC, etc. The fixture permits writable flat memory
to observe those attempts; it establishes no actual plane banking or ROM
write behavior. Its thirty-byte body retains two raw encoding inequalities
at decoded 0990:0D06/0D08 (target31/candidate33), while complete ordered
relocations agree. It remains an unowned candidate between the prospective
216-byte prefix and 1998-byte tail owners. No byte arrays, synthetic padding
or forced register encoding resolve that failure.

Polygon initialization is never reset by the Music Room. Independent cases
check zero-velocity/speed replacements, bounce and reset ordering, angle and
coordinate wrap, closure, and repeat calls. The native radii are64..112;
the original reset Y remains -100 pixels. The source preserves these values
and removes the reference comment claiming a maximum radius of96. Input cases cover both directional
bits, the empty line, wrap, held-key release loops, no-input animation, song
confirmation followed by cancel and the quit selection. Confirming a track
issues STOP, load and PLAY before a simultaneous cancel is processed. The
exit frees five buffers without stopping the chosen song or clearing their
stored pointers. These are native caller observations; actual DOS, allocator,
file, graphics, sound, keyboard filtering and clock behavior are foreign
reply fixtures.

Unicorn1.0.2rc4 misexecutes a far return when a memory-read hook is installed,
even if that hook is empty and restricted outside the stack. The independent
control `scripts/probe_th03_unicorn_far_return.py` runs the same original
26-byte POLAR body with and without that hook. Music Room uses no memory-read
hooks: bulk load operands are recorded at the audited original instruction
boundaries, and every original far return executes normally. This is a tool
observation, separate from target facts; no replacement return is emulated.

Diagnostic receipt: `.analysis/sol-op-music-review-20261006.json`; SHA-256
`22dc12eb9cb250c6bcd1f6febcd98198d651ac4c9f551572324c8e471350f1f2`; 244 guarded inputs. Three images each pass276
cases/all807 native instruction positions. Maintained-source verification is
pending the two fresh cold builds. The exact state remains open, including the whole
OP's six raw unequal bytes, original relocation order, CRT/root/library/header/
DATA/BSS/resource ownership, physical runtime and canonical packing Oracles.
MAIN, MAINL and ZUN acceptance do not change.

Replay with `scripts/review_th03_op_music.py --output .analysis/NEW_OP_MUSIC.json`
and, after source verification, `scripts/replay_th03_op_music.py --run-id NEW_OP_MUSIC`.
