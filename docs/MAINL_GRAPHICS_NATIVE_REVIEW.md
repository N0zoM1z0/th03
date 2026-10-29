# MAINL graphics, heap and native far calls

This review adds18 disjoint owners,26 procedures and2,209 bytes:2,143 CODE and
66 initialized DATA. The no-Y-clip packed-pixel variant202 is authored ZUN code;
the remaining2,007 bytes are library code/storage. Existing131 owners remain
unchanged. BSS8 receives zero file-byte credit.

## Native production

`build_th03_mainl_graphics_work.py` replaces five root DATA/BSS includes with
maintained clip geometry,generated masks and heap declarations at their original
positions. Two actual GAME3 TASM/TLINK rounds rebuild the root and reuse35 project
objects/current CRT. Complete raw OBJ/EXE/MAP vectors repeat. Both EXEs equal the
pinned Japanese decoded target; both MAPs equal the retained MAP. Complete native
payload/public records and literal FIXUPP order agree with the retained root.
Generator equates may change PUBDEF emission order; complete records/multiplicity
are checked. This does not reorder relocations.

The original root and938 cold outputs/source/recipe are restored and validated.
No full cold/DIET or ancestor runtime replay is needed. Source provenance remains
the pinned local candidate and original library/game providers; no reference-game
binary is substituted. No object or executable is patched.

## Ordinary far calls reproduce the page-copy bytes

The old page-copy provider used two `nopcall` compatibility macros. New
`page_copy.inl` uses ordinary calls with no explicit NOPs. An independent native
copy TU declares SMEM_WGET/SMEM_RELEASE as external far procedures outside CODE.
Declaring them inside the same CODE segment lets TASM optimize the calls early
to four bytes; the correct external declarations emit ordinary five-byte9A calls
and two literal FAR-pointer OMF fields. A separate real memory TU supplies the
actual heap628/stack-memory76 and original state. No fake callee is introduced.

Two actual TLINK rounds consume these fields and naturally emit
`NOP / PUSH CS / near CALL`, exactly matching the product's108-byte copy owner.
The independent comparison resolves the DATA WORD and both far calls for the
mini MAP and product MAP. Both complete native OBJ/EXE/MAP vectors repeat. All44
mini memory fields also resolve independently; no MZ segment entry survives.
The carrier's32-byte stack and8-byte BSS are uninitialized and add no source
credit. The frozen root retains its compatibility calls as contextual transport;
future full recipe work must integrate the demonstrated independent TU boundary.

## Complete ownership and ABI

| Owner | CODE | Procedures | Additional layout |
| --- | ---: | ---: | --- |
| GRCG rectangle bank | 366 | 2 | Shared6-byte return, two outer EVEN bytes |
| Clipped packed-pixel writer | 212 | 1 | Shared6-byte clip return |
| No-Y-clip packed-pixel writer | 202 | 1 | Shared6-byte clip return |
| Glyph writer | 148 | 1 | One outer EVEN byte |
| Scroll / show / GDC writer | 105 | 3 | Show includes one outer EVEN |
| Screen mode / clear / page copy / extended mode | 308 | 5 | Copy has a private21-byte near helper |
| EGC bank | 98 | 3 | EGC_END aliases EGC_START; three outer EVEN bytes |
| Heap | 628 | 8 | HMEM_ALLOCBYTE tail-enters HMEM_ALLOC; three outer EVEN |
| Stack memory | 76 | 2 | Shared6-byte ASSIGNALL continuation; two outer EVEN |

Shared error exits/continuations borrow the owning frame and add no procedures.
Every complete body,local branch,near/far return and Pascal cleanup is checked.
The heap free path can borrow the allocation unwind. MEMHEAD has three WORD
fields within a16-byte allocation paragraph; it is not a six-byte allocation.
All93 root native fields resolve in their literal order; scoped MZ vectors are
empty. Sixteen actual WORD memory operands read the previously accepted CS RotTbl
at base/base+2. These are table reads,not self-modifying writes or segment fields.

## State and generated data

`clip_initialized.inl` owns eight WORDs/16 bytes:inclusive640x400 bounds,A800 VRAM
segment scalar and399*80 bottom address. `edge_masks.inl` uses REPT17 and a
cumulative-bit recurrence with byte swapping to generate34 bytes in VRAM order.
`byte_masks.inl` generates eight successive right-shift masks fromFF. Complete
native LEDATA equals independent semantic formulas,with no literal target tables.
BYTE_MASK needs no procedure or execution claim merely because it is present.

`heap_initialized.inl` owns four WORDs/8 bytes (0,0,0,256),with all eight aliases.
`heap_uninitialized.inl` retains four BSS WORDs and aliases without initializers.
All four initialized owners have no native fixups or MZ entries. Their original
containing segment/group allocations and all MAP aliases are checked.

Preserve signed clipping,16-bit wrapping,caller DF where original code assumes
it,and CLD where the packed writers execute it. GRCG_BOXFILL retains CLI/stack
argument extraction/STI; it does not restore a previously cleared IF. GAME3 glyph
conversion retains ADC BP,5680h and its caller-CF quirk. Original BIOS/port waits,
heap coalescing,overflow and allocation behavior are unchanged. No defensive
product fixes or physical graphics/DOS/heap execution are claimed.

Current inputs under `.analysis/work/`: `mainl-graphics-build.json`,
`mainl-graphics-native.json`,both `graphics-roundN.obj/.exe/.map` vectors,
`graphics-root.asm/.lnk`,both `graphics-mini-roundN-*`/EXE/MAP vectors,and actual
`graphics-mini-memory.asm`, `graphics-mini-copy.asm`, `graphics-mini.lnk` inputs.
The verifier is `scripts/lib/decoded_mainl_graphics_native.py`.
