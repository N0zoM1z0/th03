# Original Japanese DOS directory/raw-write and stdio finalizers: two proven native layers

The four complete original 8086 source implementations below were independently
recompiled against their real **Japanese CL.LIB members**. They were not
accepted merely because an `.asm` file or older review already existed.

| Original library member | Complete CODE | Original native 16-bit operation |
| --- | ---: | --- |
| `getdcwd` (239) | 157 | `__getdcwd`: DOS drive/current-directory lookup, range errors and optional far buffer allocation |
| `writea` (332) | 91 | `__rtl_write`/`__write` at +0/+63: raw DOS file write with mode/EOF flag handling |
| `flushall` (223) | 76 | `_flushall`: iterate original open FILE slots, invoke `_fflush` |
| `xfflush` (335) | 63 | `__xfflush`: CRT shutdown flush across the original standard stream slots |

Together these members reconstruct **387 original CODE bytes**, with the
original ABI, original segment/class/group ordering, full public and imported
symbol identities, and **13 original relocation fields** including frame,
site, target and *literal FIXUPP order*. All four have zero initialized
DATA/BSS. The source retains the original `stdio_layout.inc` constants;
the included file's exact SHA256 is bound in both native layer receipts.

## Two separate source-bound checkpoints, not one overwritten driver

The live provenance is a deliberate **two-stage native source chain**:

1. `scripts/build_th03_mainl_after349_work.py directory-and-raw-write`
   takes the original 393-source parent, adds `getdcwd` and `writea`
   (**248 CODE**, eight relocations), and proves the complete **395-source**
   Japanese EXE/MAP in two independent native rounds. The original
   `getdcwd` **entire CL.LIB program record** is reproduced byte-for-byte
   in both native rounds; `writea`'s complete OMF program differs in
   nonsemantic metadata although its full FIXUPPs match.
2. `scripts/build_th03_mainl_after350_work.py stdio-flush-finalizers`
   inherits **both** SHA-bound native 395-member producer rounds unchanged,
   then compiles `flushall` and `xfflush` (**139 CODE**, five relocations).
   Both new TASM/TLIB/TLINK rounds reproduce the exact **397-source**
   Japanese EXE/MAP. Their source-produced complete OMF programs differ
   from the originals outside their byte-equal CODE and ordered FIXUPPs.

The separate `vendor/flushall.obj` and `vendor/xfflush.obj` have the same
logical relocation population as the real pinned CL.LIB members, but emit
FIXUPPs in another order. Source objects match the actual library, not the
standalone vendor. The real original CODE and original 13 ordered FIXUPPs
are verified directly in `tests.test_mainl_after349_work` and
`tests.test_mainl_after350_work`; reviewers verify retained full raw
OBJ/LIB/EXE/MAP and writer logs.

The combined **397** complete source-backed CRT members leave **496**
original contextual library members intact. The full **893-member** carrier
recreates the pinned decoded Japanese MAINL **67,372-byte EXE and MAP**
byte-for-byte in each independent round, including **677 DOS MZ
relocations in original order**, and totals **127,393 original-equal logical
CRT CODE bytes**. The original linked binary evidence is retained under
`.analysis/work/after349-*` and `.analysis/work/after350-*`, together with
parent/source/driver hashes and all native tool logs. No full cold replay,
patched OMF/EXE, Factory-accepted extent or packed-game ownership is claimed.
