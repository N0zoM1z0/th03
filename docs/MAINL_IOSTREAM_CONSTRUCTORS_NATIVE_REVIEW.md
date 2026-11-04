# Japanese TH03 CRT: complete iostream constructors and withassign variant

Three selected original Borland C++ large-model CRT members are now whole
symbolic 8086 source: original slot **741 `iostctr1`** (**478 CODE**), slot
**742 `iostctr2`** (**460 CODE**) and slot **743 `iostctr3`** (**527 CODE**).
Each owns **28 initialized DATA bytes**, zero BSS and a far C++ constructor
PUBLIC at offset +0. Both `iostream` overloads and the
`iostream_withassign` constructor are covered, with their original ordered
EXTDEF inventories and `_TEXTA/_DATA/_BSS` plus `08ff02ff03` DGROUP.

All complete far constructor bodies reconstruct genuine Borland
`ios`/`istream`/`ostream` initialization, streambuf binding and native
exception cleanup. After each `RETF` the source contains **two executable
12-byte 8086 multiple-inheritance destructor-adjustor thunks** with
`mov bx,sp`, native stack adjustment and a **far `EA` destructor jump**.
The remainder of CODE contains *nonexecutable* RTTI type strings and typed
`dw`/`dd` descriptors (including the separate `iostream_withassign` class).
All original 28-byte DATA sections are authentic far unwind/class records.
No executable machine-CODE arrays, padding or binary patches were used.

Native TASM 5.0 `/m /mx /kh32768 /t` reconstructs **1,465/1,465 original
CODE bytes**, **84/84 DATA bytes**, original public offsets/imports,
segment layout and **all 72 original OMF relocation sites, types, targets,
addends and frame methods**. The literal BCC-vs-TASM FIXUPP record ordering
differs, so full original OMF OBJ serialization is **not** claimed.

`scripts/build_th03_mainl_after301_work.py iostream-constructors` extends
the verified actual **301-source Japanese CRT** at three selected slots in
**two independent normal TASM/TLIB/TLINK rounds**. Both reproduce the
**entire 67,372-byte decoded original Japanese MAINL EXE and original MAP
byte-for-byte**, keeping all **677 original ordered MZ relocations** and
**589 unchanged original vendor member program records**. The working
source CRT becomes **304 members and 101,381 original-equal CODE bytes**.
This is working-source evidence, not accepted-ledger promotion, and no
full cold replay was performed.

Proof: `review_th03_mainl_after301_work.py iostream-constructors`,
`tests.test_mainl_after301_work` and source/driver-hash-bound native
OBJ/LIB/EXE/MAP pairs plus actual writer logs under `.analysis/work/after301-*`.
