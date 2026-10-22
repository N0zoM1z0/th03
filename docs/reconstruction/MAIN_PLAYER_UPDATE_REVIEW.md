# MAIN player-state update source checkpoint, 2026-10-22

`src/main/player/update.inl` now supplies the complete target-derived candidate
for load `DA43..DE95`. It is included first by `state.cpp`, before the four
previous tail bodies. The PSTA243 original-toolchain producer emits
1,106 + 131 + 209 + 151 + 119 = **1,716 CODE bytes**, with no private DATA/BSS.
All five lengths and instruction shapes agree with the canonical target.
This remains outside the default product graph and acceptance ledgers.

## Target and compiler evidence

Evidence lives in `.analysis/codex-main-player-update-20261022-v01/`.
Preflight and a fresh headless MAIN database attestation passed from clean
commit `a30b70b`. The canonical Japanese MAIN SHA-256 remains
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`, with
candidate-local attestation and independent pristine provenance still unknown.

Thirteen serial native compiler capsules retain their original inputs, logs,
process/registry audits and sole-writer lock receipts. Every capsule passed
11 preparation controls and released its lock with certain cleanup. The first
failed because reference headers were included repeatedly; the second lacked
the existing `page_back` declaration. Later successful process receipts are
compiler observations, including mismatching outputs:

| Capsule | Update bytes | Observation |
| --- | ---: | --- |
| PSTA233 | 1,105 | Input stayed on stack; movement occupied DI |
| PSTA234 | 1,110 | Explicit subtraction matches the damage sequence |
| PSTA235 | 1,265 | `-rd` disables the desired register allocation |
| PSTA236 / PSTA237 | 1,109 | Local input/player copies; register ordering reviewed |
| PSTA238 | 1,112 | Expanded movement assignment adds instructions |
| PSTA239 | 1,108 | Cached previous movement uses DX and an extra copy |
| PSTA240 | 1,109 | Signed movement local does not remove the extra load |
| PSTA241 | 1,112 | Reusing the charged local does not match |
| PSTA242 | 1,106 | Retry-branch structure matches, but one jump operand differs |
| PSTA243 | 1,106 | Boss fallback branch also matches raw non-fixup bytes |

The final natural C++ candidate keeps a local player pointer and local input
word. Initializing input before the pointer matches the observed DI/SI loads;
local declarations retain the observed six-byte stack. The movement retry
performs its retry in the unequal branch. The full-gauge case jumps directly
to the bullet attack when the current player already owns the boss. This is
an observed shared branch destination, expressed with a source label; the prior
conjunction instead jumped to a redundant gauge threshold check. PSTA242's
length/shape equality alone did not detect that single raw branch-byte mismatch.
No target arrays, padding, binary patching or substitute ABI are used.

The final capsule stages 60 source files and four vendor headers, with 96
literal include edges. Its object has 7,143 bytes, SHA-256
`238001c822cf40dbea4a93ba2c019b1f14bc05e61ec83fdb6803f79bcaf0d907`.
The frozen manifest is `native-v13/manifest.json`, SHA-256
`3af32870f8fcf64dbd31dea8a7a14384342012fab9d3fe2870ebde51acbf5479`.
Installed source bytes equal the original consumed inputs. Peak native RSS
across all thirteen capsules is 108,920 KiB, one CPU/nice 10, with zero swaps.

## Independent raw diagnostic and operand observations

`review-playerstate-v13.py` verifies the original native completion, all pinned
inputs, unchanged object and actual OMF fixup operands. There are 110 fixups:
96 two-byte and 14 four-byte operands. Excluding their 248 operand bytes plus
seven possible far-call relaxation opcodes leaves **1,461 raw bytes, all equal**
to the canonical target. The negative controls reject both a changed non-fixup
byte and a changed far-call opcode. The earlier diagnostic failed on PSTA242's
branch displacement; it was not added to the exclusion set.

Hypothetically removing only those seven relaxed segment sites leaves
`[511, 1684, 1559, 1467, 1438, 1336, 1229]` relative to `DA43`, matching the
literal target order. This is not an actual native link or complete equality.
`unlinked-review-v13.json` and `installed-review-v13.json` preserve the reports.
Replay against installed source with a fresh output path:

```sh
.venv/bin/python -B .analysis/codex-main-player-update-20261022-v01/review-playerstate-v13.py \
  --installed --output .analysis/NEW_PLAYER_UPDATE_REVIEW.json
```

`bind-operands-v13.py` and `operand-bindings-v13.json` associate every external
fixup with the actual target call destination or DGROUP base plus compiled
addend. The retained compiler MAP is hash-bound, and its names remain compiler
corroboration. Important bindings include `target_formation_marker` at DS:38E8,
`gba_boss_launched_by` at DS:063E, and the 16-bit
`combo_points_for_boss_attack` at DS:3ED4. Five names lack a retained public at
the target destination: the two inferred lose-animation APIs, `player_shots_add`,
`round_defeated_player`, and `shot_release_frames`. Their physical caller/storage
aliases still need integration; no successful symbol resolution is claimed.

`lose-update-abi-v02.json` isolates target `C0D8..C1E6`, 270 bytes: BP+4 is loaded
into SI and `RET 2` occurs at C1E3. The wider v01 observation also contains the
following function and is preserved. The update API's source name and pointer
type remain inferred. The previously reviewed render auxiliary uses an unused
stack slot; these two contracts are distinct.

## Next physical composition work

The candidate's `shot_release_frames[2]` references DS:4B9C, inside the retained
root BSS reserve after `_collmap_pid` at DS:4B9A and before `_collmap` at DS:4BA0.
It declares no allocation. A reviewed two-byte symbol view must preserve the
original five-byte reserve and every downstream offset. The defeated-player
byte is DS:38DD; `player_shots_add` is load E737.

`physical-intake.py` / `physical-intake-v01.json` pin the retained root and MAP:
20 contributions cover `96E6..E8F8`, a 21,010-byte group span with one existing
byte gap at `A377..A378`. The proposed five-byte BSS reserve partition is
one unchanged byte, the two-byte counter view, then two unchanged bytes.
It is recorded only as a layout proposal and has not been applied. The three
CODE aliases correspond to `sub_C0D8`, `sub_C248`, and `sub_E737`; the defeated
player's retained storage label is `byte_20E3D`.

Next compose these five bodies with the neighboring maintained MAIN_01 code,
review all root aliases and storage views, and perform a real link. The previous
P_SHOT far-call/layout mismatch still requires coherent physical segment
ownership. Complete raw equality, literal relocations, layout/ABI, behavior,
independent cold rounds and the complete Oracle set remain required. MAIN stays
at 87 exact extents / 413 functions / 66,843 scoped bytes. No whole-authored
percentage or new OP/MAINL/ZUN acceptance is claimed.

## Verification

Installed-source comparison, tracking validation and whitespace checks pass.
Full CI passed 2,314 tests in 308.085 seconds with two existing skips, plus all
four database attestations and Oracle/toolchain checks. `ci-v01.log`,
`ci-v01.exit` and `ci-v01-resources.txt` record exit zero, outer time 7:22.83,
peak RSS 665,424 KiB, one CPU/nice 10, Java heap cap 768 MiB and zero swaps.
All owned jobs are terminal. The proof/candidate histories remain retained;
no cleanup removed an input or evidence file.
