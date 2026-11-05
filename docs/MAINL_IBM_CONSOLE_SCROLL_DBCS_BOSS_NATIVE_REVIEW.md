# Original IBM scrolling and split-DBCS cleanup boss — after448

The previously contextual Japanese Borland member cibmscrl, CL.LIB
slot **529**, now has complete maintainable
[8086 source](../src/mainl/crt/cibmscrl.asm).
The complete near __IBM_SCROLL entry iterates a text rectangle,
checks for double-byte trail characters at the left and right
column boundaries, fills split-character cells using the true
near IBM helper, selects the original display attribute and calls
the IBM video BIOS adapter. It preserves 16-bit arguments,
the stack-local current column and its native callee-pop-12 ABI.

**184/184 CODE bytes**, all original segment/group layout, six
exactly ordered external imports, the near public symbol and all
**13 original relocation sites, types, targets and addends** match.
Independent OMF inspection disproved an initially plausible but
incorrect assumption: CODE+10 tests the imported wgarbage flag,
while CODE+140 actually tests **wclrnorm**. These are distinct
original external indices 2 and 1. Both now have the original
DGROUP-style frame method 1. All other global state accesses also
have the exact original frame/target semantics.

The remaining **seven precisely guarded near imported calls** use
Borland original TARGET-frame method 5, but TASM emits the CODE
segment-frame method 0. The proven CODE site -> import target pairs
are **43->4, 59->5, 68->5, 89->4, 105->5, 114->5, 174->6**.
The source-bound scope only normalizes this exact known pair set;
every site/target/kind/width/segment-relative flag/addend is checked,
as are all other original frame fields. The review independently
checks literal raw FIXUPPs and explicitly reports that literal
Borland-versus-TASM OMF equality is **false**. A trial with the CS
assumption removed failed native near-call assembly and was not
silently adopted. No original CODE arrays, object rewriting, or
arbitrary padding have been introduced.

After448 validates the previous 655-member after447 parent and runs
two independent real TASM/TLIB/TLINK native rounds with full source
hashes, writer logs and original raw OBJ/LIB/EXE/MAP output pairs
preserved. Both decoded Japanese MAINL EXE/MAP are byte-for-byte
original-equal (67,372-byte EXE, 677 ordered MZ relocations).
Working CRT reaches **656/893 source-linked original CRT members**
and **176,605 original-equal CODE bytes**; 237 original members
remain vendor context. This proves scoped working-source parity,
not full raw OBJ identity, a cold replay or new Factory credit.

Focused reviewer: scripts/review_th03_mainl_after448_work.py
(mode ibm-console-scroll-dbcs-boss);
unit tests: tests.test_mainl_after448_work.
