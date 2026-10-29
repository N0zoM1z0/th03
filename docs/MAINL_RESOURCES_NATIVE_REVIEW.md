# MAINL SUPER and generated rotation table

Two complete library ranges add2032 source bytes: SUPER1008 CODE and a1024-byte
pixel-rotation table stored in CS. The table is initialized DATA,not instructions
or256 functions. The old source-presence aggregates are reused without duplicate
credit. Original master/super library attribution is preserved and their former
authored classifications are corrected to library.

## Complete SUPER range

Decoded0000:237E..276D contains six public far Pascal APIs,four private near
drawing procedures,one private near tail dispatcher and shared error exits:

| Procedure | Start | Bytes | Return cleanup |
| --- | --- | --- | --- |
| SUPER_FREE | 237E | 48 | Far0 |
| SUPER_ENTRY_PAT | 23C2 | 171 | Far8 |
| SUPER_ENTRY_AT | 246E | 116 | Far6 |
| SUPER_ENTRY_BFNT | 24E2 | 137 | Far4 |
| SUPER_CANCEL_PAT | 256C | 79 | Far2 |
| SUPER_PUT | 25BC | 240 | Far6 |
| SUPERPUT_DISP1 | 26AC | 35 | Near0 |
| SUPERPUT_DISP2 | 26D0 | 45 | Near0 |
| SUPERPUT_DISP3 | 26FE | 54 | Near0 |
| SUPERPUT_DISP4 | 2734 | 49 | Near0 |
| SUPERPUT_DISP | 2766 | 8 | Tail-jumps to a drawing helper |

The20 bytes at23AE are borrowed-frame error exits,not two independent callable
procedures. Six ordinary outer EVEN bytes at246D/256B/25BB/26CF/26FD/2765 complete
the range. Internal macro EVENs and original instruction templates remain in
their natural source positions. All1008 bytes have dense native LEDATA coverage.

All50 native fields resolve independently through the actual root layout:
own-CS offsets use root CODE base0272; own DATA uses0112; BSS uses13F6. Native
group1 contains BSS/DATA. The explicit DATA-segment frames of BSS references
therefore resolve through the same DGROUP,with both MAP tables confirming the
pattern DATA/SIZE addresses. No field contributes an MZ segment relocation.
The complete literal ordered native field stream is retained,including its
explicit group/segment frame forms.

Thirteen real CS operand writers target ten complete instruction operands:
mask/height word2769,dispatch displacement276C,and four pairs of row-add/count
BYTE immediates. Each destination is verified as the exact immediate/displacement
of its consuming MOV/ADD/JMP instruction,with matching width. All four written
dispatch displacements enter the real26AC/26D0/26FE/2734 near procedures. The
original dispatcher MOV BX,1234h and jump template remain real assembler output;
the program changes them itself at runtime.

Preserve original behavior. ENTRY_AT clears SIZE entries during lazy allocation
without clearing DATA/count,and stores the allocation result before checking CF.
Cancellation tail search uses DATA; an empty SIZE tail can leave FREE looping.
BFNT loading ignores extension-analysis carry and keeps its native close/status
behavior. PUT retains DF,unchecked indices,16-bit coordinate arithmetic and signed
imm8 row additions; zero BYTE dimensions can run256 iterations. It selects four
address/width-parity variants and renders the mask plus four color passes. This
review claims native source/ABI identity,not physical GRCG/VRAM execution.

## Natural table source

`src/mainl/resources/pixel_rotation_table.inl` generates all256 DWORD entries
with assembler REPT and bit operations. For input BYTE v,plane b receives:

```text
((v >> b) & 1) | (((v >> (b + 4)) & 1) << 1)
```

Those four plane BYTEs form the little-endian DWORD. The source contains no
literal byte table,instruction dump,reserve array or filler. All1024 generated
bytes equal an independently evaluated semantic image,native LEDATA and both
target/candidate images at0000:1AAA. RotTbl's actual public and both MAP entries
are checked. It has no native fields or MZ relocations.

## Affected build and boundaries

`scripts/build_th03_mainl_resources_work.py` temporarily changes only the real
root's table include,assembles that one producer,and relinks at its original
position against35 unchanged project objects and the existing validated CRT
library. Two rounds produce identical raw OBJ/EXE/MAP vectors. Whole decoded
EXEs equal the pinned Japanese target and both MAPs equal the retained MAP.

Additional symbolic equates change TASM's PUBDEF emission order. Every complete
public record and its multiplicity remains identical; every other non-COMENT
native record,including the full FIXUPP sequence,is literally unchanged. This
metadata permutation is not relocation normalization. Actual objects and
executables are never patched. The raw selected objects repeat exactly.

The frozen cold wrapper,938 outputs and full source/tool/library/target graph
are restored and revalidated. The new selected recipe/source/commands/output
pair is bound separately; no new whole-product cold rebuild or DIET replay is
claimed. The original literal-table provider remains frozen context until that
full recipe is deliberately updated. External DATA/BSS,allocator/device behavior
and whole-product source exactness remain open.

```sh
# Only when selected source/tool bindings change:
.venv/bin/python scripts/build_th03_mainl_resources_work.py
# Read-only complete current proof:
PYTHONPATH=scripts .venv/bin/python -m lib.decoded_mainl_resources_native
```

Preserve `.analysis/work/mainl-resources-build.json`,all six selected
`resources-roundN.obj/.exe/.map` outputs and `resources-root.asm/.lnk`. The
current native receipt is `.analysis/work/mainl-resources-native.json`.
