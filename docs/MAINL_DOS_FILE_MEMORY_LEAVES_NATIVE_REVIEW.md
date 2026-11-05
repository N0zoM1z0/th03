# Eight complete DOS file, time and memory original CRT routines

This increment reconstructs **eight entire original Japanese Borland DOS
CRT members** in real native 8086 source, rather than patching OBJ bytes or
claiming source ownership for a mixed library carrier. Each file in
`src/mainl/crt/<member>.asm` preserves the far API convention, exact
CODE/DATA/BSS original segment and DGROUP layout, Borland error handling
and DOS INT 21h register setup, including the original unchecked behavior.

| Member | Original CODE | Original public ABI and complete DOS function |
| --- | ---: | --- |
| `dosread` | 40 bytes | `__dos_read`: AH=3Fh, far buffer and far count output, restore DS and return error |
| `doswrite` | 40 bytes | `__dos_write`: AH=40h, same complete far count/error convention |
| `dosseek` | 45 bytes | `__dos_seek`: AH=42h, far 32-bit seek result on success |
| `dosgftim` | 39 bytes | `__dos_getftime`: AX=5700h, original far time/date outputs |
| `dossftim` | 33 bytes | `__dos_setftime`: AX=5701h with DOS carry-error path |
| `dosfree` | 26 bytes | `__dos_freemem`: AH=49h, original segment-release ABI |
| `dosalloc` | 40 bytes | `__dos_allocmem`: AH=48h with maximal free-block failure return |
| `doskeep` | 24 bytes | `__dos_keep`: call C runtime exit, INT 21h AH=31h terminate-stay-resident |

The selected original members are 33, 39, 35, 30, 36, 164, 163, and 344.
All eight have the original one-public, one-external ABI, zero initialized
DATA/BSS, exact original CODE and exactly one imported relocation field
per member. Members `dosread`, `doswrite`, `dosalloc` retain the original
`DGROUP` group order `08ff03ff02`; the remaining five use `08ff02ff03`.
The far import is `__cexit` for `doskeep`, while all other members retain
near `__DOSERROR` error forwarding.

**Known OMF distinction:** `dosseek`, `dosgftim`, `dossftim` and `dosfree`
use original Borland TARGET frame5 for the near `__DOSERROR` fixup; native
TASM uses CODE frame0. The site, width, target and addend are still identical
and the linked program is exact. The other four members' ordered FIXUPP
fields match literally. Whole original OMF serialization is not inferred
from equality of the code or its native linked result.

`scripts/build_th03_mainl_after333_work.py dos-file-memory-leaves` extends
the source/receipt-validated **344-member** CRT carrier, including its
entire previous real native OBJ/LIB/EXE/MAP rounds. Two independent
TASM/TLIB/TLINK rounds reproduce the complete original Japanese MAINL
**67,372-byte EXE and MAP**, with **677 ordered MZ relocations**. The full
CRT now has **352** complete source providers and **541** contextual
original members, yielding **114,907 original-equal CODE bytes** — an
increase of **287 bytes**. The source, original member and inherited receipt
hashes, raw two-round OBJ/LIB/EXE/MAP vectors and writer logs are retained
under `.analysis/work/after333-*` and reviewed by
`scripts/review_th03_mainl_after333_work.py` and
`tests.test_mainl_after333_work`. No new full cold replay was used and no
Factory accepted or packed-file unit credit is claimed.
