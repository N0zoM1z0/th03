# Japanese TH03 CRT: full `fstreambase` / `strstreambase` far destructors

Two separate, actually selected Borland large-model CRT members now have
complete human-readable symbolic 8086 assembly source: original slot **723
`fsdtr`** has **388 CODE + 20 initialized DATA**, and slot **852 `srdtr`**
has **396 CODE + 20 DATA**. Both export their original mangled C++ far
destructor at CODE+0 and preserve five ordered original EXTDEF imports,
`_TEXTA` CODE, `_DATA`, empty `_BSS` and `08ff02ff03` DGROUP.

Each source implements the entire 120-byte far destructor body, including
real Borland C++ `ios`/`streambuf` and owned buffer destruction, reference
bookkeeping and original conditional far delete. CODE+120..131 contains a
**real executable 8086 multiple-inheritance adjustor thunk**, not RTTI:
`mov bx,sp`, native stack-offset `add`, and far `jmp` to the destructor.
`ASSUME CS:NOTHING` ensures TASM does not shorten the self-targeted native
far `EA` transfer to a near `E9`. The remainder of CODE contains typed
`dw`/`dd` class-destructor records with original class names, and the
20-byte DATA segment has original far unwind pointers. There are no raw
executable machine-CODE arrays, artificial padding or modified OBJ bytes.

Standalone TASM `/m /mx /kh32768 /t` reconstructs **784/784 original CODE
and 40/40 DATA bytes**, every original public offset/ordered import, and
**34/34 original OMF fixup sites, kinds, targets, addends, widths and frame
methods**. BCC and TASM emit these same fixups in different record order:
original literal whole-OBJ equality is **not** claimed.

`build_th03_mainl_after299_work.py base-destructors` uses the source-bound
299-member Japanese CRT and replaces both selected slots in **two
independent normal TASM/TLIB/TLINK rounds**. Both rebuild the **entire
67,372-byte decoded original Japanese MAINL EXE and original MAP byte-for-
byte**, preserving all **677 original ordered MZ relocations** and **592
unchanged original vendor CRT member program records**. The working CRT is
**301 source-built members / 99,916 original-equal CODE bytes**. These are
working-source results, not formally accepted-ledger credit. No historical
full cold replay was run.

Verify with `review_th03_mainl_after299_work.py base-destructors` and
`tests.test_mainl_after299_work`, plus source/driver/parent-hash-bound raw
OBJ/LIB/EXE/MAP receipts and original writer logs under
`.analysis/work/after299-*` and `.analysis/work/mainl-after299-*`.
