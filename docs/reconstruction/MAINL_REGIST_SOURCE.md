# MAINL maintained registration and score-data checkpoint

Two opt-in owners, `src/mainl/regist.cpp` and `src/mainl/scoredat.cpp`, preserve
all tokens of the reviewed frozen ReC98 bodies apart from explicit include
routing and comments. Nine maintained inputs own registration/menu rendering,
score load/save, encryption/checksum/recreation, glyph IDs and declarations.
The original BINARY='L' branches remain intact; shared headers remain guarded
as originally written. Fifteen explicit compatibility inputs expose frozen
interfaces. Their transitive headers and libraries remain outside ownership.

The scope is 17 complete bodies: 095F:17B9/229 and 095F:189E/2720 (2,949 bytes).
No DATA/BSS ownership is claimed: `hi`, entered-place, default names, mutable
rank filename and related storage stay in the original generated assembly.

Unchecked reads/writes, stale-buffer acceptance, all-rank clear flags, unsigned
name-cursor wrap, invalid character reads, mutable filename accumulation and
16-bit seek multiplication are deliberately retained. This is reconstruction,
not a bug-fix pass. No target bytes, invented padding or object rewriting are used.

Run `scripts/stage_th03_mainl_regist.py --output .analysis/NEW_REGIST_OVERLAY`
to create a fresh source-only overlay. Merge its source trees into a fresh
archive of revision b6ba5b0a529edbb31efdf8c0e939263804f8ee47; compile the original
`th03/scoredat.cpp` and `th03/regist.cpp` slots, never compile the owner twice.
Keep the original MAINL flags: `-c -I. -O -b- -3 -Z -d -DGAME=3 -ml
-DBINARY='L' -nobj/th03/`. Preserve module order and group_01 pragmas.

Focused source-token/staging/progress tests bind the frozen source. Independent
baseline/maintained TCC compiles now prove all ordered nondependency OMF records
equal for both slots. A second independent maintained compile of each slot
produces raw-identical objects, with source timestamps declared from the first
materialization before compiling. Two fresh hybrid TLINK runs use these two
owned objects plus 31 retained others and preserve the entire carrier EXE/MAP.
This is source-present evidence, not a whole-program cold build or exact credit.
The SVG now counts both extents: MAINL 38/145 source units, 9,845 source bytes.

`python3 scripts/replay_th03_mainl_regist.py --output .analysis/NEW_REGIST_SOURCE_REPLAY.json`
rechecks retained source/phase/product identities and reruns the selected CPU
models without invoking any native tool. Two linked images and the decoded
target each execute 152 calls: 151 terminal plus one deliberate budget case.
All 456 observations agree (453 terminal, three budget observations). File,
input, graphics, RNG, timing and sound interfaces remain explicit models.

Earned object hashes: scoredat 1,335 bytes, dec2723fc4e7d9d178cb9ce16a479430134ce00d12529d750a62825b8ec50649;
regist 7,269 bytes, bf0d49d2125c6fde80d5f2c3faa7ece9ef29f311cf7f46f6b0ef6977fa44493f.
Both EXEs are 67,372 bytes, ff315af6f9cd197f78292d8c834a90afad7b4d6c9bda0a9f8b09d4bdbc12a1ad;
both MAPs are f262e1d8e78d353f29e5f2d9a1cd39be91f934d48b0839b5ab55be6d9e033568.
All 677 ordered image relocations remain unchanged. This separately retained
success does not erase historical failures or grant whole-file source acceptance.

Fresh linked score-data bytes match the decoded target; registration still differs
at six PI operand bytes: 19E2, 19EC, 22D8, 22E2, 230F and 2319. All 54 ordered
registration relocations agree in the existing candidate. These facts do not
establish canonical exact acceptance. Do not patch callers or invent PI padding.
Canonical packaging, full DATA/BSS, physical devices and whole-game proof remain open.
