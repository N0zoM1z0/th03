# OP sound, polar and hflip helpers

The four complete native procedures add142 CODE bytes. Their original unchecked
behavior and far C ABI are preserved. All bodies are densely emitted by their
actual current OMF producers and match the pinned Japanese target and current
candidate over the complete raw extent. Each has an empty literal ordered MZ
relocation vector, with no straddling entry.

| Procedure | SHARED offset | CODE bytes | Native producer | CODE alignment |
| --- | --- | --- | --- | --- |
| snd_determine_mode | 004A | 29 | th02/snd_mode.c | WORD |
| snd_pmd_resident | 0068 | 57 | th02/snd_pmdr.c | BYTE |
| polar | 0155 | 26 | th03/polar.cpp | BYTE |
| hflip_lut_generate | 0CB8 | 30 | th03/hfliplut.asm | WORD |

SHARED is0BEB; DGROUP is0D7F. The three C/C++ producers have empty DATA/BSS
segments. The ASM producer has only SHARED. Segment/group records, both MAP
public tables, entire containing allocations, literal include chains and every
consumed dependency are checked by `lib.op_leaf_native`. Generic inventory still
labels the three historical outer wrappers as frozen context; actual maintained
ownership follows their verified two-hop include chains. The builder is unchanged.

Mode calls INT60 with AH09. On the non-FF driver branch it sets FM possible and
returns1; on FF it returns the zero-extended raw MIDI active BYTE. It does not
clear FM possible on that branch. Its three ordinary DGROUP offset WORD fixups
are emitted in order24(active),20(MIDI active),13(FM possible).

PMD first sets interrupt-if-MIDI to60 and clears the three capability/active
bytes. It reads the actual INT60 vector at0000:0180 and compares ISR bytes+2,
+3,+4 against P,M,D. It retains the short-circuit comparisons, both RETF exits
and original ES/BX effects. Its four DGROUP fields are17(MIDI possible),12(FM
possible),7(MIDI active),2(interrupt-if-MIDI), in emitted order.

Both sound sources still contain an explicit legacy trailing NOP at0067/00A1.
These bytes receive no ownership. The new scoped compiler diagnostic removes
only that pragma from temporary copies and compiles each body twice with the
actual C/GAME2/O flags. Both complete raw objects repeat identically;29/57 CODE
bytes and all native fields equal their current producer's function prefix.
The stripped inputs, four actual objects, commands and receipt are retained in
`.analysis/work/sound-body*` and `sound-bodies.json`. No instruction patch,
padding replacement, full link, packing or whole-product cold rebuild was used.

Polar takes center/radius/ratio as three signed16 C arguments. The real386
MOVSX/IMUL/SAR sequence computes a signed32 product and arithmetic right shift8,
then adds center through AX, preserving16-bit wrap. RETF leaves six argument
bytes to the caller. There are no external references or private storage.

The LUT generator stores zero first, then reverses each nonzero8-bit value by
eight ROL AL/RCR DL steps. Its real LOOP and wrapping INC AL terminate after256
stores. DI is saved/restored. Its sole offset WORD field at4 uses external
target-derived frame method56 for `_hflip_lut` at DGROUP:1E70; it has no segment
fixup or MZ entry. The external256-byte BSS table receives no file-backed credit.

Run the affected read-only proof with:

```sh
PYTHONPATH=scripts .venv/bin/python -m lib.op_leaf_native
```

Only rerun `scripts/probe_th03_op_sound_bodies.py` when its input/tool bindings
change. The proof revalidates the unchanged full current native cold graph.
No emulator matrix or historical ancestor runtime replay is required.

The initial character-selection DATA ownership gap is now resolved separately
by [the maintained prefix/storage review](OP_SELECTION_STORAGE_REVIEW.md).
Its real selected compiler/linker pair consumes `selection_state.inl`; the
frozen full-cold prefix stays contextual. CODE acceptance alone did not transfer
that ownership, and the new227-byte DATA owner does not duplicate function credit.
