# MAINL historical VSync DATA alignment

ReC98 commit 287d7ea554cc33cf3fe7067f491210c63954e8c0 (2014-08-26,
[Reduction] #197: VSync-related global data) explicitly records a binary change:
NOP to zero after these declarations. Its predecessor stores the original alignment
byte after vsync_OldMask. This is source-history evidence for restoring the alignment
producer, not a claim about a particular historical assembler version.

The maintained complete VSync provider uses a named parity-conditional mnemonic NOP,
relative to a private zero-storage label at the start of DATA. There is no target offset,
raw opcode array, executable patch, or extra code-function ownership. The first real
root/link attempt exposed TASM's downstream alignment-state effect: two ordinary DATA
alignment sites also became NOP. That failed verifier and its products remain preserved.

A complete traversal of initialized root DATA has exactly three alignment producers:
the VSync producer, CDG ALIGN 2, and EVEN after CUTSCENE_KANJI. The latter two are now
explicit EVENDATA, an existing native TASM directive also used by reference initialized
cutscene DATA. Declaration/public boundaries, segment classes and DGROUP stay unchanged.
The odd fixture genuinely leaves a one-byte LEDATA hole; it does not emit a zero byte.
The actual TLINK result, not synthesized OMF coverage, establishes the final zero fill.

Actual root assembly/link and an independently assembled repeat preserve raw root OBJ,
EXE and MAP identity. The 63,276-byte loaded image now equals the decoded target, and
only the intended VSync alignment byte differs from the previous source image. Header,
MAP and literal relocation sequence remain unchanged from that previous build. The
677 relocation members match the target, but 461 ordered indices still differ.
The aligned EXE SHA-256 is ab825a2cd14eb41310b6a71ebb5952f534bdd5913f597293fc03e2183d6a18e4.

Two independent DIET compressions produce identical 38,050-byte packed files and both
restore the complete aligned EXE. The packed result is still 75 bytes larger than the
37,975-byte canonical target and has 1,212 absolute differences including size. No
canonical raw equality, fresh runtime matrix, post-alignment full 35-object cold build,
or formal exact acceptance is claimed. Source counts and exact0 remain unchanged.

The source-only cold stager now consumes these maintained providers. Its historical
proof.json is intentionally unchanged: that receipt proves the earlier source snapshot,
not the new stage. Toolchain CRT library integration likewise remains a separate lane.

Replay: python3 -B scripts/replay_th03_mainl_vsync_alignment.py. The source-only
cold stage retains its CRLF policy; MVA03/MVA04 used the composer's LF outputs.
They have identical source statements, not identical raw source files. This is
another reason the existing full-cold receipt is not extended to the new stage.
