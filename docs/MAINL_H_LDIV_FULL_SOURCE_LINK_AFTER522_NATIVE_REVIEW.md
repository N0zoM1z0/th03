# Complete h_ldiv source link and original MAP aliases — after522

Original Japanese CL.LIB slot **67, h_ldiv**, is now a complete source-linked
CRT member: **174 CODE bytes, no DATA, no BSS, zero FIXUPPs**, and twelve
original near/far quotient/remainder exports. The maintained
[8086 arithmetic source](../src/mainl/crt/h_ldiv.asm) preserves near-to-far
return conversion, restoring division, signed adjustment, modulus selection,
and the original short-divisor path.

The earlier TASM-only experiment matched every code byte and public offset,
but its complete MAP reversed the same-address LDIV@/F_LDIV@ and
F_LUMOD@/LUMOD@ pairs. TASM 5 enumerates PUBLIC symbols through its hash table;
changing PUBLIC or label declaration order did not change that output.

The source now declares its twelve PUBLIC names in original OMF chronology.
The existing pinned **JWasm v2.12pre** compatible emitter preserves those
declarations in native OMF. The **entire 130-byte ordered name/offset/type
payload** matches the original twelve PUBDEF records, while JWasm groups it
into one PUBDEF record. There is no OBJ rewriting, MAP sorting, target-code
array, or padding. Original raw OBJ program-record identity is **not** claimed.

The explicit [MAINL emitter profile](../config/th03_mainl_h_ldiv_jwasm.toml)
reuses the source revision, binary hash and version already pinned by the ZUN
tool profile. The producer and independent reviewer attest those tool bytes
and bind the MAINL scope/flags and attestation code hash. This is compatible
assembler evidence, not identification of the original Borland assembler.

The [after522 producer](../scripts/build_th03_mainl_after522_work.py) extends
the unchanged after521 source-bound pair. Two independent JWasm/TLIB/TLINK
rounds reproduce the complete **67,372-byte Japanese MAINL EXE and original
MAP**, including all **677 literal ordered MZ relocations**. All earlier 729
source members and 163 remaining vendor members are preserved in the original
893-member order. The twelve public offsets, segment/GROUP layout, complete
CODE, empty relocation population and ordered public payload are checked
against the original library member in each round.

The [independent reviewer](../scripts/review_th03_mainl_after522_work.py)
checks source/recipe/tool hashes, parent receipt, actual writer logs, both
entire OBJ/LIB/EXE/MAP vectors and complete original EXE/MAP equality. All raw
rounds, logs and scratch remain retained. No full cold replay, new runtime
model, or redundant input matrix was used.

Current working-source CRT: **730/893 complete members, 196,413 original-equal
CODE bytes**. This resolves the old uncredited arithmetic helper and adds one
complete member / 174 CODE bytes. Formal Factory canonical packed-file unit
acceptance remains **0/250**; whole-game completion is unknown.

Receipt: `.analysis/work/mainl-after522-long-divmod-original-public-order-build.json`

SHA-256: `e581b1a20a5eca64b3cf1524f8e8b53fa6327ab1fbfb7d4efd68452b6fdecaca`.

The old after520 storage guard remains blocked by after521+ source stages;
no cleanup is authorized without a fresh source-DAG/SHA-256 audit.
