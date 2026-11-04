# Japanese MAINL original C++ `strstreambuf::seekoff` and `overflow`

Two complete selected Borland large-model CRT algorithms are now real
symbolic 8086 source. Original member **846**, `srbskoff`, contains **600
CODE bytes** implementing `strstreambuf::seekoff`, including 16-bit seek
direction/buffer pointer arithmetic and far `streambuf::setg`/`setp` calls.
Original member **844**, `srboflow`, contains **512 CODE bytes** implementing
`strstreambuf::overflow`, including buffer growth/allocation, original far
`memcpy`, ownership/deletion, get/put pointer updates and virtual dispatch.
Both use genuine `_TEXTA` CODE with empty `_DATA/_BSS` and original
`08ff02ff03` DGROUP. Each exports one original C++ far public at CODE+0.

`src/mainl/crt/srbskoff.asm` and `src/mainl/crt/srboflow.asm` reconstruct
all **600/600 + 512/512 original CODE bytes** with actual 8086 instructions,
branch labels, far virtual calls expressed as `call dword ptr [...]`, and the
original ordered two/six external imports. They contain **no original
machine-CODE byte arrays, target padding or patched native objects**.

All **9/9 native OMF relocations** agree with the selected Borland members
at every original site, relocation type, target, addend and **frame method**.
The original compiler and TASM differ in the enumeration order of FIXUPP
records; complete literal object-record identity is **not** claimed. Native
C++ public offsets and selected program-record identities are checked for
both members, not inferred from file names.

`scripts/build_th03_mainl_after134_work.py strstream-bosses` extends the
retained **134-source** Japanese CRT and performs **two complete normal
TASM/TLIB/TLINK rounds**. Both produce the **entire original 67,372-byte
decoded Japanese MAINL EXE and original MAP byte-for-byte**, preserving all
**677 ordered DOS MZ relocations** and the other **757 untouched vendor CRT
program records**. Working-source CRT now has **136 members and 64,568
original-equal CODE bytes**. This is working-native source evidence, not new
formal accepted-ledger credit. No full cold replay ran.

Verify using `review_th03_mainl_after134_work.py strstream-bosses` and
`tests.test_mainl_after134_work`. Source/driver-hash-bound receipts, both raw
OBJ/LIB/EXE/MAP native pairs and actual writer logs are retained under
`.analysis/work/mainl-after134-*` and `.analysis/work/after134-*`.
