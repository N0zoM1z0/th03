# OP CDG drawing native source review

2026-10-29: the actual OP TASM producers have complete module ownership:
`cdg_put.obj`382 CODE and `cdg_p_na.obj`114 CODE. Three complete far Pascal pop6
procedures occupy493 bytes; three ordinary outer EVEN bytes are accounted
separately within the496-byte module extents. All19 native fields, two literal
ordered MZ relocations and12 self-modifying WORD destinations match the target.

| Procedure | OP CS-relative offset | Function body | Outer EVEN after body |
| --- | --- | --- | --- |
| Alpha plus colors | 0170 | 179 | 0223 |
| Horizontal flip | 0224 | 201 | 02ED |
| Colors without alpha | 0C46 | 113 | 0CB7 |

The CODE figure is a physical segment extent, not a pure-instruction total.
The three outer bytes follow existing source EVEN directives; they are not
extra procedures. Internal loop alignment stays within the complete bodies.
MAINL's earlier function-only acceptance remains unchanged and excludes its
corresponding outer bytes.

## Actual native source and ownership

The wrappers are literal ASM includes with declared CRLF transport. Every
consumed source/include is checked against the current native source graph and
staged file. TASM5.0 identity, whole segments/publics and WORD/PUBLIC/USE16
alignment are checked. The alpha/hflip object also has its genuine empty
CDG_PUT_TEXT and DATA contributions; these add no bytes or storage ownership.
Neither producer has private DATA/BSS.

The shared MAINL module supplies native field grammar and SMC metadata. Its
comparison image is discarded. OP begins with its own native CODE and resolves
every field again using both OP MAP public tables:12 own-CS WORD references,
five external DGROUP references and two far GRCG calls. Complete pristine CODE,
including the three outer EVEN bytes, is compared with the pinned Japanese
target and current candidate. The two far-call MZ entries retain emitted order.
No object or executable is patched.

Every CS writer is checked as a full MOV whose destination is the immediate
WORD of a MOV instruction in its own procedure. The placeholders, including
the original hexadecimal/decimal distinction in the flip color width, remain
as source instructions. They are overwritten by the original setup code,
rather than replaced by prebuilt target bytes.

## Original drawing behavior

The alpha blitter prepares width, stride, source-segment and bottom-left
operands, then copies the mask with REP MOVSD under GRCG RMW. It disables GRCG
and ORs colors into each plane. The flip blitter keeps DS for the external
bit-reversal LUT, uses FS for source bytes and XLAT to reverse each byte while
moving the destination left. Its setup rewrites the original row widths,
strides and restart coordinates. The noalpha blitter writes color DWORDs
directly, with its own rewritten width operand.

All three keep their original WORD coordinates/slot argument and RETF6.
Preserve the source's segment-register handling, CLD behavior, short jumps
around SMC setup and unchecked slot/geometry/VRAM accesses. The external slot
array, LUT, GRCG service and physical VRAM behavior receive no new source credit.
Native equality resolves this scope without a new emulator or flag/input matrix.

## Input scanner investigation: no new acceptance

The current scanner source ends with explicit `#pragma codestring "\x90"`.
One isolated, serialized TC4 compile removed only that line in a temporary TU,
using the original flags. Its complete CODE record shrank from418 to417 bytes.
Every remaining CODE byte and the complete EXTDEF/FIXUPP streams stayed equal
to the maintained producer's prefix. Segment alignment attributes also stayed
the same. Thus the extra byte is pragma output, rather than automatic compiler
alignment. This finding is based on actual new output, not the old source note.

The probe is `.analysis/work/input-nostring.json`; its OBJ/log/script are
retained locally. It is one fresh compile, not a cold pair. It changed no product
source or existing native product outputs. No scanner or trailer credit is
added. Current whole-file equality cannot establish legitimate source ownership
of that explicit trailer. Its provenance/layout must be resolved before a clean
producer/layout change can be accepted; the byte must not be replaced with
another arbitrary padding mechanism.

## Checks

```sh
PYTHONPATH=scripts .venv/bin/python -m lib.op_cdg_draw_native
.venv/bin/python -m unittest tests.test_op_cdg_draw_native tests.test_op_work_acceptance
.venv/bin/python scripts/publish_th03_op_work_scopes.py
```

Use one CPU, nice10 and empty displays. These drawing scopes reuse the verified
unchanged cold pair; they were not reassembled or relinked. Focused controls
reject identical corrupted SMC fields, identical wrong EVEN bytes and swapped
MZ entries. The separate input experiment is the only new native compilation.
