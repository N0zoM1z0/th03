# Japanese Borland C++ `ios::sync_with_stdio`: entire original stream bridge

The genuinely selected original Japanese large-model CRT member **886**,
`stsync`, exports `@ios@sync_with_stdio$qv` at CODE+96. Its full native
layout is **761 `_TEXTA` CODE bytes**, **2 initialized DATA bytes**, zero
BSS, 19 original ordered EXTDEF imports, and `08ff02ff03` DGROUP.

`src/mainl/crt/stsync.asm` reconstructs the complete original **516-byte
executable C++ stream synchronizer** (CODE+96..611) as real symbolic 8086
instructions. It flushes `cout`/`clog`, tears down prior stream buffers,
allocates three genuine `stdiobuf` objects for the original C `__streams`
`FILE` entries at base +0/+20/+40, connects the returned buffers to
`cin`, `cout`, `cerr` and `clog` through Borland's near/far stream assignment
operators, and restores the original output flags and C++ destructor counts.
Original error/unchecked behavior is preserved; no modern libc substitute.

CODE+0..95 contains **three typed non-executable C++ exception-unwind
frames**; CODE+612..760 contains class RTTI and destructor far pointers,
including authentic `stdiobuf *`, `stdiobuf` and `streambuf` names. These
regions are real `dw`/`dd` fields and readable strings, not executable
machine byte arrays or arbitrary padding. The DATA+0 `sync_enabled dw 0`
flag has its original segment/group relocation identity.

The original far virtual `FF 5F 24` at CODE+160 initially assembled as a
near indirect call when untyped; an explicit `call dword ptr [bx+24h]`
restores the original 8086 instruction without byte patching. The original
BCC direct `cin/cout/cerr/clog` and `___stdin/stdout/stderr_streambuf`
GROUP-relative references, including +2 far-pointer segment halves, are
restored as named `DGROUP:` symbols. Original `__streams+20` and +40
addends are preserved, not invented data addresses.

Native TASM 5.0 `/m /mx /kh32768 /t` reproduces **all 761 original CODE
bytes**, **both original DATA bytes**, the entire C++ PUBLIC/EXTDEF ABI,
all original segment sizes/classes, and **all 66 OMF relocation sites,
targets, addends, relocation kinds and frame methods**. BCC and TASM still
serialize the FIXUPP records in a different *order*: complete original
literal OBJ record identity is therefore **not claimed**.

`scripts/build_th03_mainl_after168_work.py stsync` extends the full
source-bound 168-member original Japanese CRT at its actual selected slot,
performs two independent normal TASM/TLIB/TLINK rounds and reconstructs the
**entire original 67,372-byte decoded Japanese MAINL EXE and MAP byte-for-
byte**, preserving **all 677 ordered MZ relocations** and **724 untouched
vendor CRT member records**. Working source rises to **169 members / 72,814
original-equal CODE bytes**. This is working-source evidence, not new formal
accepted-ledger credit or complete whole-game source ownership. No full cold
replay was performed.

Proofs: `review_th03_mainl_after168_work.py stsync`,
`tests.test_mainl_after168_work`, source/driver/parent-hash-bound receipts,
actual native writer phase logs and raw OBJ/LIB/EXE/MAP pairs under
`.analysis/work/mainl-after168-*` and `.analysis/work/after168-*`.
