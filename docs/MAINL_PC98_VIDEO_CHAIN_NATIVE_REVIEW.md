# Original Japanese PC-98 video initialization and VRAM character output

Two more selected native Borland CRT members have now been recovered in
natural 8086 assembler source and linked with the existing `cibmscrn`
six-function screen core:

| Original slot | Complete member | CODE | DATA/BSS | Original entry points |
| ---: | --- | ---: | --- | --- |
| 892 | `cibminit` | 663 | 7 DATA | Seven near/far BIOS initialization and video service functions |
| 528 | `cibmputn` | 433 | 12 BSS | Four near VRAM access/output callbacks |

`src/mainl/crt/cibminit.asm` includes the original direct BIOS video
services, native ES:DI / ES:BP variants, CRT initialization, screen height
and window geometry queries, and the actual **`COMPAQ`** vendor string
stored as a semantic 7-byte DATA literal. The original four ordered
external video-state imports are retained. `src/mainl/crt/cibmputn.asm`
recovers VRAM access, cursor/DBCS checks and character output, retaining
the six near-or-far dependent routines, plus external current column and
row state, original 12-byte uninitialized BSS and all four PUBLIC offsets.
Both consist of complete original 8086 instructions, not machine-CODE
byte arrays, artificial padding or native OBJ patches.

One real 8086 trap mattered: reading PC-98 BIOS video state at absolute
`ES:[0084h]` needs the **ES segment override**. An early spelling
`ES:DS:[0084h]` caused TASM to ignore the override, producing a different
CODE extent. The corrected explicit ES operand reproduces the original
`26 A0 84 00` instruction and the precise original public offsets.
Original far `__video` pointer access also requires `LES` with typed
`dword ptr`; untyped `ptr` is not sufficient.

Normal TASM 5.0 `/m /mx /kh32768 /t` produces **663/663 + 433/433 CODE
bytes**, **7/7 initialized DATA**, and the genuine 12-byte unmaterialized
BSS. All **105 original relocation sites, types, targets and frame methods**
are equal once paired by exact native site; Borland and TASM FIXUPP record
order differs, so full literal native OBJ serialization equality is
**not** claimed. Both modules match original `08ff03ff02` DGROUP and
complete original PUBLIC/EXTDEF inventories.

`scripts/build_th03_mainl_after131_work.py video-chain` extends the
original 131-source CRT with both real selected members and normally
reassembles and links two independent TASM/TLIB/TLINK rounds. Both rounds
reproduce the **entire original 67,372-byte decoded Japanese MAINL EXE
and MAP byte-for-byte**, preserving all **677 ordered MZ relocations** and
**760 unchanged vendor CRT program records**. Working native CRT now
covers **133 source-built members / 62,902 original-equal CODE bytes**.
This is working-source evidence, not formally accepted-ledger credit;
**no full cold replay** was performed.

Proof: `review_th03_mainl_after131_work.py video-chain`,
`tests.test_mainl_after131_work`, both source-bound raw OBJ/LIB/EXE/MAP
native rounds, tool logs and receipts under `.analysis/work/after131-*`
and `.analysis/work/mainl-after131-*`.
