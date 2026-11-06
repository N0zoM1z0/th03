# MAINL picture filename table — after553

`src/mainl/root/picture_files.c` replaces the generated-only `rootpre.asm`
18-byte filename table with a maintained natural C TU. Nine symbolic `near`
character pointers preserve the callers' two-byte ABI and the independent
original DATA contribution. The native compiler's supported `-u-` option retains
the existing assembler string names; the table exports the callers' `_PIC_FN`
symbol. No address constants, target bytes, padding or object patches are used.

## Native result and limits

Two real TCC4.02/TLINK6.10 rounds produce identical complete raw OBJ/EXE/MAP
vectors. Only this one game TU is compiled: the actual after552 root OBJ,
after548 source C0/retained library pair and 34 unchanged cold game objects are
reused. There is no TLIB, packing, cold replay or ancestor runtime-suite run.
All six fresh outputs and four writer logs remain under
`.analysis/work/picture-files-after553-*`; consumed source, recipes, responses
and native inputs remain in `TH03ML/probe/af553h`.

| Output per round | Bytes | SHA-256 |
| --- | ---: | --- |
| Complete C OBJ | 396 | `86f30c8e1a9771ee8bf4be77a71590ba1c291fbecadcae4f6710d16ec9d8f020` |
| Original-equal decoded EXE | 67,372 | `92600c8858bb407516cac6a9d77538ebdf0c33522c4f6bd9194d569eb927134a` |
| Complete new MAP | 81,039 | `3e595d670346db13abeb3edf6b9a1896cdf790123815f229d47bd1912f573c90` |

The table occupies **0E3F:0090–00A2**, with `_PIC_FN` at its first byte. All
nine native fixups have two-byte offset location type1, segment-relative=true,
DGROUP frame1, external target method2 and zero addend. Their literal emitted
sites descend **16,14,…,0** and external indices descend9…1. Existing external
strings are `00sl.cd2`, `02sl.cd2`, …, `16sl.cd2`; independent MAP addresses and
actual linked strings determine the pointer values. The complete LEDATA writes
each of the18 bytes once. CODE and BSS segments both have zero extent.

The retained generated ASM object has ascending sites0,2,…,16 and target-frame
method5. **Its OMF stream is explicitly different.** No original-game standalone
OBJ is available, so no original compiler identity or original OBJ equality is
claimed. The new native field stream is checked literally and repeats; final
target bytes and all **677 literal ordered MZ relocations** agree. This near
pointer table has no MZ relocation. Whole-product source acceptance remains open.

The MAP differs from after552 only in the explicit contribution rows below;
every other raw MAP byte is identical. Empty CODE alignment/position changes
emit no bytes. The DATA contribution retains its exact address, extent and
attributes; the new empty BSS contribution adds no storage.

```text
old 0000:0272 0000 C=CODE S=_TEXT G=(none) M=rootpre.asm ACBP=48
old 0E3F:0090 0012 C=DATA S=_DATA G=DGROUP M=rootpre.asm ACBP=48
new 0000:0271 0000 C=CODE S=_TEXT G=(none) M=rootpre.c ACBP=28
new 0E3F:0090 0012 C=DATA S=_DATA G=DGROUP M=rootpre.c ACBP=48
new 0E3F:133C 0000 C=BSS  S=_BSS  G=DGROUP M=rootpre.c ACBP=48
```

Build receipt `.analysis/work/picture-files-after553-build.json`, SHA-256
`1b4c3f0d4d82364afea5d1fb78fdab81b7d9ddd6de3ef4b0bcac88ca4f3a771b`.
Review receipt `.analysis/work/picture-files-after553-review.json`, SHA-256
`7df4f518559fb18933e84dd1a340f3a6f181f6e4c01e8cf50c8804846eff4129`.
Producer/reviewer: `build_th03_mainl_picture_files_work.py` /
`review_th03_mainl_picture_files_work.py`. Both validate the unchanged cold
pair and actual inherited source/native evidence. The selected reviewer
preserves after552's immutable native-input audit rather than replaying the
obsolete live211 publication gate. Japanese provenance remains
`candidate-local-attested`; independent pristine-dump identity is unknown.

## Ownership and continuation

One disjoint initialized DATA owner adds **18 bytes**, zero CODE, procedures or
BSS. MAINL publication reaches **218 extents / 37,305 bytes / 290 procedures**:
34,431 CODE, 2,868 initialized DATA and six existing file-backed uninitialized
bytes. Authored ownership is17,054 bytes; library ownership remains20,251.
These are reviewed scopes, not a whole-game denominator. Canonical Factory
acceptance remains0/250. Future MAINL source links must retain this C OBJ,
the after552 root OBJ and actual after548 C0/library references.

The old217-owner publication, ledgers and ownership audit are preserved in
`.analysis/work/picture-files-after553-preserved/`. Remaining unowned project
CODE is unchanged:716 allocation bytes across9 contributions. DATA18 is removed
from the ownership queue, without treating diagnostic counts as source credit.

## Retained MAIN linker investigation

The unchanged MAIN candidate has124,642 load-image bytes: only offset**EC2D**
differs (target90, native00), immediately after the complete input routine. All
1553 ordered MZ relocations agree. Its MZ header is7680 bytes (480 paragraphs,
relocation-table offset62); the original header is6240 bytes (390 paragraphs,
offset28). Neither header normalization nor a hand-filled NOP is accepted.

The actual current TLINK6.10 `/i` probe preserves that difference and header,
but extends the file to164,464 bytes by initializing further segments. It is
not adopted. The authentic TC2.01 package supplied a separate TLINK2.0 candidate
(`821a862e71bdfea977a2fddbe58d1127047eecbfe8d1b6eb82830cd8f493c140`);
default tools/prefix remain intact and environment-change preflight passed.
Initial MSDOS bridge probes failed with AX0006; this does not establish object
format incompatibility. A subsequent actual headless DOSBox-X run reads all
unchanged objects in their original order, but reports **29 fixup overflows**
and writes `FAILED`. Its partial132,322-byte EXE has4724 load-image differences,
1867 relocations and EC2D still00. It is rejected. No game was executed.

Preserve all help/recipes/bridge logs, DOSBox inputs and partial raw outputs in
`probe/link553/`, including `dos/LINK.LOG` and `STATUS.TXT`. The unsuccessful
C++ pragma-restore probe and its actual inputs/logs remain in
`probe/pictures553/` and af553f/g. The successful independent C TU avoids
changing the frozen root TU's compilation boundary. The private after553
diagnostic manifest also binds these branches and the prior publication.
No native evidence, tools or targets were deleted.

## Affected checks

The scoped native reviewer and publication validate the unchanged cold inputs;
all217 prior owner records remain identical. Seven existing gate/presentation
tests, tracking validation, ownership-audit `--check`, progress `--check` and
`git diff --check` pass. The expensive live-audit test is covered by publication
and is not repeated. Full CI, cold replay and historical runtime suites are not
run for this bounded DATA change.
