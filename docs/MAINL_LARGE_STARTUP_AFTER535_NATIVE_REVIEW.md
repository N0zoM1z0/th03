# MAINL source-generated large-model startup after535

`src/mainl/startup/c0.asm` replaces the prebuilt `C0L.OBJ` in a bounded native
MAINL link. It specializes the installed supplier startup to the DOS large
model with a separate stack. Supplier attribution is preserved; this is
**zero authored-game credit**. Neither the frozen cold graph nor the CRT
library is rebuilt or changed.

| Original startup scope | Native result |
| --- | --- |
| 17 ordered segments, alignment/combine flags, DGROUP | Literal equality |
| CODE extent | 625 bytes |
| Initialized CODE | 623 bytes: 621 instruction bytes and 2-byte model word |
| Uninitialized CODE cache | 2 bytes, sites 621–622, written by startup |
| Initialized runtime DATA | 144 bytes, complete equality |
| Initial STACK reservation | 128 uninitialized bytes |
| Literal relocation fields | 58; every full field agrees at its original site |
| PUBLIC definitions, including absolute constants | Same complete multiset |
| Entry MODEND and module name | Literal equality, including `c0.ASM` spelling |
| Complete native pair | OBJ/EXE/MAP byte-identical between rounds |
| Complete decoded Japanese EXE / retained MAP | 67,372 / 80,893 bytes, byte-exact |
| Complete MZ relocation table | Original 677 ordered entries |

The cache word is genuinely uninitialized, not zero padding. The model word
is the original `C004h` large-code/large-data descriptor. DATA retains the
null-check header, diagnostic strings, four saved interrupt vectors, process
and environment fields, errno/exception storage and heap boundaries. Empty
segments and the reserved stack preserve original ownership and layout.

The startup retains the PSP-derived environment scan, original minimum-stack
selection and memory release, protected SS:SP switch, BSS clear, conditional
DOS handle-table expansion, exception initialization, arguments and normal
main/exit calls. It saves/restores INT 0/4/5/6 and installs the original divide
handler. The typed six-byte startup/exit records preserve near/far dispatch:
initialization selects ascending priority with first-entry ties; cleanup
selects descending priority with last-entry ties. Selected entries are marked
used before calling them. No defensive behavior is added.

The installed `C0.ASM`, `RULES.ASI` and `BUILD_C0.BAT` were hypotheses, checked
against the independently pinned installed C0L object and actual target link.
Their hashes, original object and native options are pinned in
`config/th03_mainl_startup.json`. The maintained TU resolves the relevant
model choices and naming/pointer macros into ordinary instructions, typed
storage, EQU aliases and explicit segment declarations. No private source
include, instruction byte array, object patch or output rewrite supplies it.

TASM 5 retains all individual literal fields but emits them in a different
order from the original startup object. PUBLIC record order also differs.
Both full original/native profiles and their literal streams are retained;
the reviewer pins the emitted field sequence and reports ordered equality
**false**. No original OMF-program identity or formal source-exact acceptance
is claimed. Final EXE/MAP equality includes the complete original ordered MZ
relocations, not a normalized or sorted executable comparison.

Producer: `scripts/build_th03_mainl_after535_work.py`.
Reviewer: `scripts/review_th03_mainl_after535_work.py`.
Root: `.analysis/work/mainl-after535-startup-build.json`.
SHA-256: `9a3592185b880d53d344cdd3f0cf0c0b13534d186833e7d739f673edd2e61d6b`.
The new native pair and writer logs use **af535e-startup-** paths; consumed
source, driver, config and response remain in `probe/af535e`. Both unchanged
after533 CRT libraries are retained by their original paths and hashes,
not represented as fresh TLIB output. After534 independently traces all
893 source-bound compiler-library slots, with its metadata gaps still visible.

The first link already matched the full EXE but used `c0.asm` as its OMF
module spelling. Its MAP consequently differed in those module names. The
corrected producer passes `c0.ASM` to native TASM and checks literal THEADR;
it does not edit the object or MAP. The original incomplete receipt, source,
driver, config, response, logs and raw outputs are retained, with eleven
SHA-inventoried snapshots at
`.analysis/work/probe/startup-module-name-correction/manifest.json`.
Earlier source/option probes under `probe/af535a`, `af535b` and `af535c` remain.

No cold replay, ancestor runtime models, full CI or new emulator test suite was
run. The affected independent native review, progress/tracking checks and
whitespace check pass. Canonical Factory acceptance remains **0/250**.
The current detailed MAP has no contributing EMU/MATHL member names: remaining
work should target actual product source/ownership gaps, not those unlinked
libraries merely because the link response lists them.
