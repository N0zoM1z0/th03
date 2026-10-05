# MAIN MRS owner review

`src/main/formats/mrs.asm` maintains the complete SHARED contribution
0E8F:05F2–07FD. The 524 bytes contain five complete functions (520 bytes)
and four assembler-produced alignment bytes outside function bodies. This
replaces frozen `th03/mrs.cpp` and `th03/formats/mrs.cpp` for MAIN.

Same-process-attested Ghidra queries and the replayable raw review bind Japanese
MAIN SHA-256 `f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`:

```sh
python3 scripts/review_th03_main_code.py --owner th03-main-mrs \
  --output .analysis/th03-main-exact/sol-mrs-target-review/raw-review.json
```

| Function candidate | Offset | Bytes | Observed ABI/return |
| --- | --- | ---: | --- |
| mrs_load | 05F2 | 58 | far Pascal; word slot, four-byte filename; RETF 6 |
| mrs_free | 062C | 41 | far Pascal; word slot; RETF 2 |
| mrs_put_8 | 0656 | 173 | far Pascal; three words; RETF 6 |
| mrs_put_noalpha_8 | 0704 | 177 | far Pascal; four word slots, bool read as byte; RETF 8 |
| mrs_hflip | 07B6 | 71 | far Pascal; word slot; RETF 2 |

Ghidra's five contiguous bodies agree with the raw boundaries. Observed direct
caller counts are 1, 1, 1, 8 and 1; unique direct callee counts are 4, 1, 1,
0 and 0. Names, format dimensions, plane meanings and port meanings derive
from the frozen candidate source/MAP. Numeric operands, access widths,
branch conditions and stack effects are target observations. No image asset
or runtime observation is claimed.

Load passes the four-byte filename at BP+6 to its open call, allocates 8160h
bytes and stores the returned AX as the segment of the indexed far pointer.
The offset is explicitly zero. The pointer array is at DGROUP:1D64 with
four-byte slot stride. It passes that far pointer and size 8160h to the read
call and closes the file; no error/null check is present. Far callees are
0000:0896, 22BC, 07E2 and 07D2. Free loads AX from the segment word and ORs
the offset into the incoming DX, then ORs AX into DX. It skips freeing only
when the resulting zero flag is set. A nonzero incoming DX therefore affects
the branch even for a zero pointer. It passes AX to 0000:23C0 and clears both
pointer words using the post-call BX. This behavior is retained, including
its dependence on the external callee and incoming register state.

The source's 288*184/8 plane size is 19E0h; five planes occupy 8160h bytes.
Both blitters compute DI from signed left >>3 plus 3930h, and compute a
segment delta from unsigned top >>1 multiplied by five. They preserve SI,
DI and DS, change ES/FS/GS, and use 16-bit memory addressing with genuine
386 EAX/dword instructions. Neither executes CLD; MOVSD retains the ambient
direction flag dependence. No additional clipping or input checks are added.

The alpha blitter calls 0000:0F5C with words 00C0/0000, sets ES/FS/GS to
A800h plus the delta and successive 0800h increments, saves DS, and loads
DS:SI from the selected image. Its first loop copies nine dwords per row,
subtracts 74h from DI and repeats while carry is clear. It outputs zero to
port 7Ch, resets SI to zero, and adds 3980h to DI. Each later nine-dword row
tests its alpha dword and, if nonzero, ORs the corresponding four plane
dwords into ES/FS/GS, temporarily changing GS by 2800h for the fourth plane.
SI/DI advance by four for each dword; the row termination again uses carry
from subtracting 74h. The source interpretation of clearing/plane operations
is distinct from observing their actual runtime graphics effects.

Noalpha loads DS from the slot but replaces SI with 4DA0h, disregarding the
loaded offset. FS/GS/ES select the first three destination planes; BX holds
the fourth segment. BP+6 is tested as an unsigned byte. The altered branch
writes NOT(alpha) OR first-plane data to FS; the regular branch writes the
first-plane data directly. Both write the second plane to GS and MOVSD the
third to ES. Each then resets DI from DX, changes ES to BX and copies the
fourth plane in its own nine-dword loop. The target's negative source offsets,
LOOP counters, carry-based row bounds and branch-local duplicate loops remain.

Horizontal reversal loads ES:DI from the slot and XLATs exactly 8160h bytes
through DGROUP:1C64. It then disregards the loaded offset: BX and each row's
DI start at zero, SI starts at 35, and it swaps pairs until DI passes 17.
There are 0398h rows of 36 bytes. This second stage retains the offset-zero
assumption established by load, without adding a generalized pointer rule.

The stock C++ reproduced all owner bytes but emitted ordered relocation sites
113,83,52,47,18,10; the target order is 10,18,47,52,83,113. Sorted equality
was insufficient. Complete symbolic TASM source naturally reproduced the
target's ascending order in the diagnostic build, with no relocation-table
rewrite or manufactured OMF records. Every instruction is symbolic, including
the dword operations formerly expressed through codegen emission macros.

Normal EVEN directives replace the four upstream codestring NOPs, producing
owner-relative bytes 99,273,451,523. EVEN also word-aligns the first blitting
loop at 069A, producing the internal NOP at 0699 formerly written explicitly
in upstream inline assembly. That byte remains inside the 173-byte body.
There are no raw instruction emissions, target-byte arrays or authored padding.
The BYTE PUBLIC contribution retains TASM alignment warnings; MAP/raw checks
verify actual placement. Zero-byte DATA/BSS contributions are at
1D56:0BEE / 1D56:8DFA. The header's PC-98 dependency is an explicit compatibility
forwarder. Image storage, reversal table, file/heap/graphics callees, header/data
acceptance, other products and whole-product closure remain separate.

`sol-mrs-probe-20261006` passed two independent complete cold builds:
79 functions / 30 CODE extents / 10329 owned bytes, comprising 10199 function
bytes and 130 producer-owned bytes. Full raw equality, original ordered
relocations, MAP ownership, all 417 OMF outputs and the deterministic
20-product / 351-game-object vector passed with every earlier accepted owner.
Scoped evidence promotes this complete owner locally to exact. Independent
pristine-dump attestation remains unknown; whole-product closure remains open.

The final accepted-state `sol-mrs-final-20261006` replay also passed both
cold rounds with promoted ledger inputs frozen at build start.
