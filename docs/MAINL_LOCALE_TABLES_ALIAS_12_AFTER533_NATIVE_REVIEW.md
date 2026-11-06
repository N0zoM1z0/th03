# Six DATA tables and six metadata-only members — after533

Twelve original Japanese CL.LIB members now have complete maintained source
programs in the incremental CRT carrier:

| Slot / member | Initialized DATA bytes | Ordered FAR fields | Ordered ALIAS records |
| --- | ---: | ---: | ---: |
| 124 / `clocale` | 2,657 | 14 | 0 |
| 125 / `clower` | 256 | 0 | 0 |
| 126 / `cupper` | 256 | 0 | 0 |
| 127 / `ctype` | 257 | 0 | 0 |
| 318 / `syserrls` | 699 | 48 | 0 |
| 585 / `MBCTYPE` | 257 | 0 | 0 |
| 18 / `delf` | 0 | 0 | 0 |
| 19 / `delfarry` | 0 | 0 | 0 |
| 179 / `nearheap` | 0 | 0 | 0 |
| 358 / `nheapchk` | 0 | 0 | 0 |
| 584 / `MBCS` | 0 | 0 | 6 |
| 645 / `JSTR` | 0 | 0 | 67 |

Total: **4,382 initialized DATA bytes, 62 literal ordered FAR fields and
73 literal ordered aliases**. These members add **zero CODE, BSS or INITDATA**
bytes and no reconstructed executable functions. Original segment attributes,
GROUP membership, public offsets, imports and module-end semantics are checked
for every member, including modules with no segments.

## Typed C locale object

[clocale.asm](../src/mainl/crt/clocale.asm) declares the original 0x99B-byte
locale object, category-name pointer vector, current-locale pointer, 81-byte
locale-library name and all eight category-name strings. Existing source
consumers corroborate its layout: `locale.asm` allocates 0x99B bytes and copies
bounded categories; `lconv.asm` exposes actual monetary/numeric string offsets;
`lsetlocl.asm` consumes the aggregate locale name at +4Eh. Those previously
proved source files remain unchanged.

The source uses fixed-capacity strings and typed WORD/DWORD fields. It owns
the C names, monetary CHAR_MAX flags, decimal point, weekday/month names,
AM/PM names, original date/time formats and yes/no responses. The original
serialized LC_TIME category includes a 1,000-byte zero-filled extension;
it remains a named DATA field within the proven 0x709-byte copied category,
without inventing unsupported runtime behavior. Neutral header/format fields
retain their original values rather than guessed feature semantics.

Fourteen symbolic FAR pointers preserve original targets, addends, frames
and order. The first five select transformer, comparator, uppercase, lowercase
and ctype tables in original compiler chronology; the remaining nine bind
the current locale and eight category-name strings. Existing
[locale field declarations](../src/mainl/crt/locale_fields.inc) are unchanged
and hash-bound. Every initialized byte and the complete absence of storage
holes are checked after materializing native LEDATA/LIDATA records.

## Character tables from classification rules

The bounded [DATA table rules](../src/mainl/crt/char_tables.inl) expand into
four separate original owners. Lowercase/uppercase folding changes only ASCII
A–Z/a–z and preserves all other 8-bit values. C ctype uses the original eight
flag values, whitespace/control overlap, ASCII blank/digit/hex/letter/
punctuation classes and EOF sentinel. Its high-byte classifications remain
zero; no host locale or Unicode rules are substituted.

The multibyte table preserves the original Shift-JIS lead/trail ranges,
7Fh exclusion, half-width kana punctuation/alphabet classes and EOF sentinel.
All 1,026 resulting bytes are compared in full against the original table
members. These are semantic table declarations, not copied instruction arrays.

## Error strings and alias semantics

[syserrls.asm](../src/mainl/crt/syserrls.asm) owns forty-eight FAR pointers and
their original NUL-terminated strings. Every empty error slot keeps its own
one-byte string owner; empty values are not merged. The source preserves the
original descending pointer-field order, all 48 target offsets and all 699
DATA bytes. The previously proved error count remains 48.

`MBCS` and `JSTR` are **alias modules**, not empty functions. Their native
ALIAS directives preserve all 73 original alias/target pairs and their exact
record order, including near/far multibyte/Japanese compatibility names.
The four other zero-payload modules retain their original empty segment/GROUP
shape and no imports, publics, aliases or entry point. Their zero CODE sizes
receive no executable progress credit. No object-record serializer, object
patch, MAP edit or target-byte instruction array is used.

## Scoped native evidence

The [producer](../scripts/build_th03_mainl_after533_work.py) validates the
unchanged after532 carrier: twenty-one TU hashes, both FILE includes, compatible
emitter/profile attestation and all five original ordered PUBLIC payloads.
The earlier source DAG and both complete native rounds remain retained.
Pinned compiler CL.LIB identity is independently bound from the carrier.
Only these twelve affected TUs are assembled with headless TASM 5.0; writers
remain serialized on one CPU at nice10.

Two TLIB/TLINK rounds reproduce the complete **67,372-byte Japanese MAINL EXE,
retained original MAP and all 677 ordered MZ relocations**. Both full
OBJ/LIB/EXE/MAP vectors agree between rounds. All 877 earlier incremental
source members, four context members and original 893-member order are
preserved. The [independent reviewer](../scripts/review_th03_mainl_after533_work.py)
checks source/include/recipe/parent/tool bindings, actual writer logs, complete
storage coverage, all 62 literal fields, every ordered ALIAS record, module-end
semantics and all 197 iostream members at slots 696–892. There are **zero new
frame exceptions**. Original Borland OBJ identity remains a separate claim
and is not asserted.

Current incremental CRT: **889/893 source member receipts, 209,016 original-equal
CODE-segment bytes**. The remaining four context members (`h_llsh`, `h_padd`,
`ioerror`, `lseek`) already have source files and older evidence; they require
owner/receipt review rather than duplicate source or automatic new credit.
Formal Factory canonical packed-file acceptance stays **0/250**, and whole-game
completion remains unproved. Targets remain `candidate-local-attested`.
The first integrated compile caught two case-insensitive local-name collisions
with existing locale EQU declarations. Only the private labels were renamed;
public symbols and fields are unchanged. Its source/include/recipe/receipt
snapshots and SHA inventory remain in
`.analysis/work/probe/locale-table-local-name-correction/`, alongside the
original `TH03ML/probe/after533` scratch and logs. The corrected stage uses
`TH03ML/probe/af533b` and **af533b-** raw output/log paths bound in the receipt.
All outputs, logs and candidate branches are retained. No full CI, cold replay,
new runtime model or redundant input matrix was run.

Receipt: `.analysis/work/mainl-after533-locale-tables-aliases-twelve-build.json`

SHA-256: `45912144bddb0d0910472133f85055d3b16825bc0130affabebdd1b8e115d450`.
