# MAINL generated switch tables and native compiler alignment

After551 accepts **90 inline table bytes and one compiler alignment byte** in
two existing C++ producers. These are initialized data inside CODE segments:
**zero new instructions or procedures**. No product source or recipe changes.

| Owner | Original address | Initialized bytes | Partition |
| --- | --- | ---: | --- |
| Cutscene switch bank | `095F:1635` | 73 | 1 compiler alignment +72 table bytes |
| Stage-intro switch table | `095F:06AF` | 18 | 9 near WORD destinations |

The maintained sources are `src/mainl/cutscene.cpp` and
`src/mainl/root/complete_data.cpp`. The actual compiler generates the tables
from their existing switches. No literal machine-code arrays, manual filler or
object/executable patches are introduced.

## One bounded native compiler question

The previous cutscene review established that the zero at object offset2807,
decoded `095F:1635`, was real compiler LEDATA. It had not established why that
byte existed. Three isolated compiler invocations now retain the exact GAME3/L
flags, headers and same `cutscene.cpp` TU basename:

1. An unchanged source clone with the existing `#pragma option -a2` emits3195
   CODE bytes. All bytes, all236 full ordered fields, every public, and the
   entire non-comment OMF record stream equal the retained cold producer.
2. A second clone changes only that pragma to `-a1`. Native output is3194 bytes;
   the first table starts one byte earlier, without the zero. The72-byte bank
   remains identical, and all236 fields/publics follow exactly that address
   change. Every instruction kind and width remains the same. Two actual table
   operands and five near CALL displacements account for the instruction-byte
   changes; all five calls retain their original destinations.
3. Unmodified compiler `-S` output identifies the20 symbolic switch destinations
   and the sixteen WORD keys. It has word labels here without an explicit
   alignment directive. The direct-OBJ control supplies the alignment evidence;
   the assembly listing is diagnostic, not a product backend.

This identifies the zero as compiler word alignment before the generated table
bank under the already maintained `-a2` option. The `-a1` result is never linked
or accepted. Its coordinate comparison explains the control's layout change;
acceptance always uses complete unmodified original/default bytes and literal
ordered fields. No target normalization or byte exclusion establishes equality.

All artifacts remain in `TH03ML/probe/af551a/{a2,a1,s2}`: six source/wrapper
files, two raw native objects and the compiler ASM. The private driver, three
compiler logs and pinned probe report remain under
`.analysis/work/probe/cutscene551/`. The report SHA256 is
`46c1751097f40a9046441635aaa1e64c0dc33c5d4ac494bcc513eeb3225f5c26`.
`config/mainl_work/switch_tables_after551.json` binds these inputs. The original
source, full cold graph, tool identities and Japanese targets are unchanged.

## Complete source and relocation partition

Cutscene has four font destinations, sixteen keys `$=@bcefgkmnpstvw`, and
sixteen opcode destinations. All20 destinations enter previously reviewed
instruction boundaries inside `script_op`; both actual indirect dispatch
operands address these tables. Stage intro has nine entries for its original
five enemy-image choices, including shared destinations for cases0/1/6,2/4 and
3/5. Its real near dispatch and all destination boundaries are checked.

All **29 literal native destination fields** keep original CODE-group frames,
targets, addends and emission order. The three dispatch fields are also checked
in the complete producer proofs. Scoped MZ vectors are literally empty: near
WORD offsets do not invent segment relocations.

Cutscene's complete3195 bytes now partition into3122 instruction bytes,72 inline
table bytes and one demonstrated compiler alignment byte. Root's2458 CODE bytes
partition into2440 instruction bytes and18 inline table bytes. Its separate
DATA112/BSS186 remain uncredited context.

The decoded publication grows from214 to **216 extents /37,175 source bytes**.
Procedure count stays290 and instruction CODE credit stays34,431 bytes;
initialized-data credit becomes2738, including these91 bytes inside CODE.
The six previously identified uninitialized file-data bytes stay separate.
Ownership-gap audit now leaves **716 CODE-allocation bytes across9 project
contributions**, down from807/11. This is an ownership queue, not a function or
whole-game denominator.

## Verification and retained evidence

`PYTHONPATH=scripts .venv/bin/python -m lib.decoded_mainl_switch_native --current-cold`
checks the native controls and complete source-bound producer layouts. The main
publication also enforces disjointness from every earlier owner and all eleven
required gates. The unchanged938-output cold pair is validated and reused;
no cold build, product link, packing run or ancestor runtime suite is repeated.
Active shared runtime root remains after548. Preserve all prior native DAGs and
`.analysis/work/mainl-switch-tables-after551-preserved/`; no cleanup ran.

Affected validation is the scoped review, current publication, existing gate/SVG
checks, tracking/progress consistency, ownership audit and `git diff --check`.
Whole-product source acceptance, Factory credit and whole-game percentage remain
open.
