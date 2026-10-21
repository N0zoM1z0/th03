# ZUN initialization standalone reconstruction checkpoint

This checkpoint localizes the complete semantic initialization producer at
`src/zun/init.asm`. It does not connect that source to the default build graph,
change the launcher producer or promote wrapper/whole-game acceptance. The
2026-10-21 standalone proof below has two independently staged and assembled
materializations, completed through a retained first-round continuation.
Standalone payload byte equality remains separate from acceptance.

The maintained UTF-8/LF source is byte-identical to the reviewed semantic v03
proposal: SHA256 078525c35dfa4b499feb661980733964e16fa5654e8403ee55b0de221e828dc2.
Strict `scripts/stage_th03_zun_init.py` transforms it to Shift-JIS/CRLF, SHA256
6f35dcba455a9d9ab9bb9545e55141da7ca25186749df6749d8ac4c3c43a1e55.
The helper rejects malformed UTF-8, CR, BOM, replacement characters, unmappable
or non-bijective mappings, and a missing final LF. It exclusively creates its
output. It never compiles, patches, normalizes or substitutes target bytes.
The U+301C wave dash remains Shift-JIS 81 60.

`config/th03_zun_init_labels.json` records the invertible 59-label naming
correspondence to the retained reference; it is evidence, not a build dependency.
The live Shift-JIS/CRLF reference SHA256 is
f5506af2546a2fb66fb51b1ac7e2e468b83de9f1d1d205007f33859fcdd7a999.
Its exact CRLF-to-LF transform has SHA256
72281210345c697384157bb46216a0f313cf99893b6b4aa21026481462fa93e5.
Static tests compare complete label-insensitive instruction/directive tokens,
all 783 initialized data bytes, full target boundaries and encoding rejection.
They require the pinned private reference and decoded target; absent evidence
fails the test rather than fabricating a replacement. No Ghidra claim is added.

## Retained single-attempt evidence

The parent-owned fresh standalone assembly and tiny link used the exact staged
source under `src/zun/init.asm`, with no cached object input. The retained run is
`.analysis/th03-zun-init-native/zun-init-feasibility-20261020-utc` and the owned
work directory is `.analysis/toolchain/wineprefix/drive_c/ZIE1CBB0`.
Both native phases completed with certain owned cleanup. The original run failed
its output verifier because that verifier incorrectly rejected TLINK's two
public tables and its displayed zero-length DATA segment at 066E. That failure
remains immutable; it was not rewritten as a passing native receipt.

The strict supplemental MAP verifier accepts only the observed finite summary,
detail and two public-table structures, cross-checked against complete OMF
ownership. It does not add padding, normalize output, or accept arbitrary rows.
The read-only supplement is `.analysis/zun-init-retained-supplement-20261020-v03`.
Its final full historical guard and retained-output proof are recorded in
`.analysis/zun-init-retained-finalguard-20261020-v02/completion.json`, SHA256
 a862e306c8be51f39d1c34bcc9320c7682af3a8cca274fa6ba192bc37d80fd2d.
The earlier 180-second guard timeout is retained in the v01 finalguard tree;
its certain-cleanup incident was separately archived before the unchanged
read-only guard ran with a 360-second ceiling. No compiler was rerun.

The full raw 1390-byte COM has SHA256
27fe52738878c1fa267c5dc82b0d70957d72dca5a6da375620a74d163b61e2d8,
matching the complete decoded TH03 -2 target. Nine procedures cover 607 code
bytes and initialized declarations cover 783 data bytes. The ORG 100h address
gap is uninitialized OMF address space, not emitted COM padding. All 48 fixups,
exact MODEND, segments, publics and MAP storage are checked without modifying
object or output bytes. The supplemental guard preserved all 19 generated-input
identities and the original failed receipt. Registry transitions use the
separately reviewed exact raw-delta policy with explicit child TZ=UTC, complete
snapshots and certain cleanup; no registry normalization is used.

## Two independent standalone materializations (2026-10-21)

The maintained recipe `scripts/build_th03_zun_init.py` exclusively stages the
semantic source, preserves its explicitly declared mtime, and specifies one
TASM assembly followed by one tiny TLINK link. It delegates native supervision
to the reviewed parent adapter; invoking the recipe directly never runs tools.
The strict verifier and exact 48-fixup schema are now maintained under
`scripts/verify_th03_zun_init_standalone.py` and
`config/th03_zun_init_fixups.json`. They are byte-identical to the proven inputs.
No default build graph, launcher source or outside payload is changed.

Round 1 was freshly staged and assembled in
`.analysis/toolchain/wineprefix/drive_c/ZC9467D4`; its assembler exited zero
with certain owned cleanup. The original attempt then rejected only Wine's
UTC DriverDate rollover from 10-20-2026 to 10-21-2026. Its failed receipt and
complete raw hive snapshots remain unchanged under
`.analysis/zun-init-cold-output-20261021-v01`. A narrowly reviewed UTC-day rule
revalidated that exact transition. The parent, while holding the shared lock,
checked the current hive bytes and owned cleanup, archived the two matching
markers, and linked the exact retained freshly produced object. It did not
rewrite the object, rerun the first assembly, or turn the failed receipt green.
Round 2 was independently staged, assembled and linked in fresh
`.analysis/toolchain/wineprefix/drive_c/ZCC3A129`, without reusing any object.

The three-command continuation completed with all native exit codes zero,
certain owned cleanup, no survivors, and owned lock release. It retained the
original full preguard, ran consumed guards before each remaining native phase,
and completed a final historical guard: 262,362 paths / 15,445,179,202 bytes,
every path hashed without digest reuse. New and old receipts remain separate.
The outer Factory transport result was not recovered, so its exit status is
**unknown**, not asserted as zero. The durable post-release completion is:

`.analysis/zun-init-cold-continuation-output-20261021-v01/completion.json`

SHA256 `4fb3cf03ef57da9ae3da738f0f650da385b546abb3fff35975760d75449f70c8`.

Both raw OBJ, COM and MAP files are pairwise identical, with no normalization.
Each 1,390-byte COM equals the complete decoded TH03 -2 payload; strict OMF,
MAP and all nine procedure boundaries cover 607 CODE bytes plus 783 data bytes.
The 1,841-byte OBJ SHA256 is
`6ce552017d1c177b5066d1d656007cf1542870d2df2bf5677240933afa357ef8`.
The expected COM SHA256 remains
`27fe52738878c1fa267c5dc82b0d70957d72dca5a6da375620a74d163b61e2d8`.
This demonstrates reproducibility under the explicitly observed environment.
The approved Git/libXtst host update has unverified package provenance; old
host-byte continuity is not claimed. Compiler/linker, source and target pins
remain strict. Registry observations are runtime evidence, never executable
normalization or a permission to accept arbitrary changes.

## Remaining gates

Wrapper -2-only composition, caller/interrupt/TSR/device obligations and separate
outer DIET/MZ packing remain open. The known ten differing -4 bytes are untouched.
Complete decoded target-wrapper equality is not claimed. Neither this checkpoint
nor either standalone proof changes accepted units/functions, whole-game
percentages, target provenance or the >=95% whole-game goal.

Focused source-only check:
`python3 -B -m unittest discover -s tests -p test_zun_init_source.py -v`

`python3 -B -m unittest discover -s tests -p test_zun_init_standalone_build.py -v`

No native command is wired into this test or the default build by this checkpoint.
