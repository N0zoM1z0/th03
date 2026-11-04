# Japanese MAINL original far-heap diagnostics / walker source recovery

This is the **selected** original Borland large-model CRT member **170**
`fheapchk`, distinct from the **already accepted** `farheap` allocator member
166. We verified the chosen member against the active baseline program records
rather than treating the standalone vendor farheap object as a new provider.

`src/mainl/crt/fheapchk.asm` is a complete 665-byte real 8086 source recovery
of five original far-heap diagnostic routines, each with the original near/far
alias pair:

| CODE offset | Original public aliases | Recovery |
| ---: | --- | --- |
| 0 | `_farheapcheck`, `_heapcheck` | Walk physical heap and validate free-list links |
| 251 | `_farheapchecknode`, `_heapchecknode` | Check a selected node and its boundaries |
| 359 | `_farheapfillfree`, `_heapfillfree` | Fill free heap blocks with supplied pattern |
| 449 | `_farheapcheckfree`, `_heapcheckfree` | Verify free blocks and rings |
| 546 | `_farheapwalk`, `_heapwalk` | Walk heap and expose the next block state |

The native source retains the actual 16-bit segment arithmetic, CS-resident
heap roots `___first`, `___last`, `___rover`, `__sbrk` near call, and the
original 2-segment layout (`_TEXT`: 665 CODE, `_DATA`: empty, DGROUP contains
only `_DATA`). All five original ordered EXTDEF imports and ten public aliases
are checked. TASM initially interpreted some bare `[0]`, `[2]` heap-header
operands as immediate constants, including the `MOV ES` case; explicit
`ds:[...]` memory operands restore the correct 8086 form. Original string
instructions use native `REP STOSW` and `REPE SCASW`. No original target
CODE arrays, object manipulation or padding was introduced.

**Literal original OMF and product evidence:**

- All **665/665 original CODE bytes**, with no initialized DATA/BSS.
- All **19/19 original ordered FIXUPP records**, including site, target,
  frame method and register-segment addressing.
- Two independent normal TASM/TLIB/TLINK rounds from the complete retained
  87-source Japanese MAINL carrier, replacing the *actual selected CRT*
  members `signal` and `fheapchk` in their original positions.
- Original decoded **67,372-byte Japanese MAINL EXE** and entire **MAP**
  match byte-for-byte, retaining all **677 ordered MZ relocations**.

The new working CRT now has **89** source-built members / **37,571** original-
equal CODE bytes; **804** original vendor CRT member program records remain
unchanged. Its `fheapchk` native relocations are *literally* original-equal;
`signal` in the same native mode still has different FIXUPP **record order**,
so a claim about the combined library's universal OMF record identity would
be false. No new formal accepted-source ledger credit is claimed.

Native builder/reviewer: `scripts/build_th03_mainl_after87_work.py
signal-fheapchk`, `scripts/review_th03_mainl_after87_work.py
signal-fheapchk`, and the heap-specific regression in
`tests.test_mainl_after87_work`. Real two-round OBJ/LIB/EXE/MAP proof vectors,
writer logs and source-bound receipts are under `.analysis/work/after87-*`
and `.analysis/work/mainl-after87-signal-fheapchk-*`. The existing original
cold build was reused; **no full cold replay** ran.
