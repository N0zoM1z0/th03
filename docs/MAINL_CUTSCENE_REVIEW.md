# MAINL complete cutscene source ownership

Baseline: `83706b4`, reviewed 2026-10-26. This accepts existing source, not a
new implementation. The frozen aggregate replay remains historical.

## Complete producer and bounded credit

The actual GAME3/L producer is `th03/cutscene.cpp`, including maintained
`src/mainl/cutscene.cpp` and its header, script and EGC includes. Native TC86
Borland C++4.02 emits CUTSCENE_TEXT3195, DATA0/BSS0; its four contiguous LEDATA
records are1019/1019/1021/136. All13 publics,58 literal EXTDEF/MAP identities,
236 ordered native fields and56 literal ordered MZ relocations are bound.

Every native field is independently resolved in a comparison buffer from OMF
and literal MAP identities, never copied from the final executable. The entire
resolved3195-byte producer equals target and candidate at095F:0B3E..17B9.
No objects, executable bytes or relocation vectors are patched or normalized.

Thirteen complete near procedures own **3122 instruction bytes /1057
instructions**. Argument-taking entries preserve near Pascal cleanup, four-byte
large-model pointers and the BYTE opcode's WORD argument slot. Current root
`complete_data.cpp` and staff `data.cpp` call load/animate/free; historical
standalone wrappers do not add owners. No far-callback conversion is involved.

The72 inline switch bytes are required producer context, not instructions or
initialized DATA: four font destinations,16 literal WORD keys
`$=@bcefgkmnpstvw`, and16 opcode destinations. All20 destinations land on
reviewed instruction boundaries; two additional own-CODE fixups address tables.
The single zero at1635 is compiler LEDATA at objectAF7, not a linker tail.
Its causal alignment explanation is not proved and it receives no credit.
All direct branches/calls and both indirect switch dispatches close over the
complete reviewed boundaries. External global DATA/BSS remains separate.

**Current evidence supersedes the historical source comment about three open PI
call operands.** All current raw producer bytes, including these operands, match.
The comment is retained with the original compiled input rather than triggering
another comment-only native rebuild.

## Current proof and recovery boundary

`.venv/bin/python scripts/review_th03_mainl_cutscene_work.py --current-cold`
revalidates the complete existing source/SDK/recipe/tool/native-output graph and
the bounded cutscene proof. No new runtime harness was added. The prior54 owner
observations remain exactly bound;13 new owners add3122 CODE bytes, yielding
67 extents /72 procedures /9719 CODE +224 initialized DATA bytes.

A comment-only edit prompted a fresh two-round native build, which completed
and reproduced all938 outputs. The subsequent ancestor supporting-runtime chain
was interrupted during Staff single; that chain did **not** pass. Fresh and
incomplete evidence is retained separately under `.analysis/work/`.

The comment-only change was reverted to exact baseline source bytes. The entire
original cold report was recovered in memory by restoring its single changed
source-inventory entry and requiring its full serialized SHA256 to equal the
previously published
`746a2bc55f27efd72aac4fcba724baa2fec8da2f2f8b48de485ce266ffff67ef`.
All native output, tool, recipe, phase-log and comparison fields were unchanged.
Seventeen original scoped reports were likewise recovered only after exact
original report-SHA equality. Fresh/interrupted artifacts were preserved before
restoration. No historical proof hash was repinned, partial report promoted or
acceptance guard relaxed.

Unchanged current-source guards then revalidated all17 scoped reports, shared
input and the complete original938-output cold pair. The new cutscene proof
passes against this graph. The existing selected supporting traces remain their
original observations; no new executed-body or physical-device claim is made.
Whole-product source ownership and canonical packed-file credit remain open.

Full existing CI is pending at writing; its final result is reported separately.
