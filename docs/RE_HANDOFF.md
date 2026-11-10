# TH03 — active agent handoff (2026-11-10)

Start with [AGENTS.md](../AGENTS.md), then this page. Use
[generated progress](PROGRESS.md) for the **complete current** per-owner
stage list and product counts, [the workflow](RE_WORKFLOW.md) for native
verification, and [storage policy](STORAGE_HANDOFF_CURRENT.md) before any
cleanup. Focused `MAIN_*` reviews and source comments retain useful compiler
findings; Git history holds older chronology.

## State to inherit

- Work on the existing `main` worktree; inspect `git status -sb` and
  `git log -8 --oneline` first. Do not discard dirty or untracked changes.
  Every new commit subject starts `gpt-web: `. Local commits are not pushes.
- All four products remain unfinished as **whole-game source reconstruction**.
  OP, MAINL (ending) and ZUN have retained decoded acceptance/publications;
  MAIN's separate ledger records 106 extents / 78,737 bytes and 459 exact
  function entries. Neither a ledger entry nor source presence certifies
  the current build, and the game's completion percentage is unknown.
- As of this handoff, `scripts/status.py` selects **65** separately verified
  native MAIN stages covering **75 distinct physical OBJ owners** and
  **74,585 CODE bytes**. This is a total for selected, non-overlapping owners,
  **not new work completed in a session**, and the stages are independently
  linked against retained unchanged inputs, **not** one all-source build.
  For the current exact stage IDs and scopes, consult `scripts/status.py`
  (`native_source_reviews`) or the generated [progress table](PROGRESS.md)
  instead of copying old stage IDs from historical reviews.
- Native receipts reproduce complete owned CODE/initialized DATA, ordered
  OMF fields/PUBLICs/segment layout, and two original TC4/TLINK MAIN links
  with target-equal Japanese program image and ordered MZ relocations.
  Local evidence is separate from canonical Factory Oracle acceptance;
  do not claim whole-product or packed-file acceptance from these scopes.

## Current reconstruction checkpoints

These are **examples of current source-bound stages**, not another exhaustive
list. The full selection lives in the generated progress table.

| Owner / area | Stage | Focus |
| --- | --- | --- |
| MAIN entry + frame scheduler | `af1314c` | Full 3,050-byte scheduler; explicit render/VSYNC phase gates and independent victory checks, with original PC-98 page OUT order |
| Reimu BOSS | `af1312g` | Complete 2,020-byte owner; signed 256-unit radial distribution, byte-angle compound steering and cloud pattern guards |
| Kotohime / Yumemi / Mima BOSS | `af1195d` / `af1315h` / `af1197d` | Full controllers; Yumemi seek boundaries, ring/aimed warnings, and render exit state now use exact positive/nested guards |
| Ellen BOSS | `af1310g` | 1,675-byte owner; natural post-volley short-circuit exit, original first-phase branch polarity |
| Enemy formations / ENEDAT VM | `af1310h` | Four original objects, 3,325 CODE bytes; segmented formation-script block-first indexing and original unchecked interpreter behavior |
| Explosion collision / Fireball | `af1198g` / `af1177g` | Original hit-chain rules, 24-slot movement/collision; retain original uninitialized state |
| Kotohime / Yumemi Extra Attack | `af1199e` / `af1200c` | Complete entity/render states |
| Rikako / Kana / Mima Extra Attack | `af1301f` / `af1302f` / `af1306e` | Full allocators, updates and rendering; first-use locals tested independently |
| Input modes / wait | `af1313c` | All nine interface, joystick and wait functions; natural positive joystick branches and exact release/press loops |
| Hitbox + HitCircle | `af1194c` | Two complete physical owners; collision and skip-state guards |
| MAINL Staff + root | `af942s` / `af944r` | Retained source scopes; decoded MAINL publication refreshed at `af1055m` |

Other complete BOSS, Bullet, Chargeshot, Bomb, HUD and player owners are listed
in [PROGRESS.md](PROGRESS.md), not repeated here. When updating one, verify
its **entire physical owner and consumers**, not only the changed function.
Successful C++ simplifications in one owner do not imply equal TC4 codegen in
another: byte/word signedness, local lifetime, `goto` layout, far pointers,
register effects and RNG consumption matter. Preserve proven original quirks
rather than adding defensive product fixes or manufactured byte padding.

## Open blocker: BIOS keyboard scanner `input_s`

`input_s` is the **only** owner in the 76-unit mapped MAIN source inventory
excluded from the 75-owner current normal-link selection. Both the original
OBJ and freshly compiled maintained C++ have 417 bytes of initialized CODE,
42 ordered native fixup fields and the same PUBLIC/segments. But the frozen
normal MAIN parent used an older **418-byte** experimental object with a
trailing `90` after the final `RET`. A fresh normal TLINK using the **actual
original 417-byte OBJ** (`af1305a`) still differs from the frozen parent
at only **file offset 68,141** (`90` versus `00`); all ordered MZ relocations
match. File-scope `asm { even }` did not compile under TC4 (`af1193b`).
This is an unresolved **historical parent-link padding/provenance issue**,
not permission to append NOP bytes or claim complete native link acceptance.
See [the input gap analysis](MAIN_INPUT_S_LINK_GAP_AFTER744_REVIEW.md).

Investigate the old linker response, segment alignment, original compiler
behavior and frozen parent provenance. Keep the original target and both
link/object outputs untouched. New source and link experiments need fresh,
unique stage names and isolated outputs.

## Good next work

1. Investigate that one-byte `input_s` link gap without generating or
   inserting target padding. The original C++ function body already matches
   its OBJ; do not endlessly rewrite the two BIOS scan passes just to hide
   a historical linker mismatch.
2. Continue substantive natural C/C++ recovery in large BOSS and ENEDAT
   controllers **and** small helpers, using isolated negative/positive TC4
   trials. Review the actual source before assuming old comments were right.
3. For truly new ownership in OP, MAINL, ZUN or uncovered library/ASM
   contributions, consult `config/units.csv`, `config/evidence.csv` and
   focused analysis. Decoded publication, scoped native evidence and
   Factory acceptance remain separate.

## Working commands and preservation

Use an unused DOS-safe stage `afNNNNx` (digits, then a letter); substitute
only the original physical `--units` actually affected:

```sh
git status -sb
.venv/bin/python scripts/preflight.py   # before native work or tool/target change
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/probe_th03_main_exatt_layout.py --stage afNNNNx --units ba_mima
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage afNNNNx
git diff --check
# After changing status/progress selection, not after ordinary prose edits:
.venv/bin/python scripts/progress.py --check
```

Use an actual fresh stage ID matching the probe's validation pattern; the
placeholder is not executable verbatim. **Never routinely replay the cold
build or run all 65 source reviewers for a small source change.**

Keep original targets, tools, analyzer projects and current build/compare
inputs. Record useful conclusions briefly. Historical archives, duplicate
trial output and cleanup reports need no retention; documentation references
alone do not make a file necessary. The `input_s` context above remains useful
until its linker discrepancy is resolved. See the short
[storage guidance](STORAGE_HANDOFF_CURRENT.md).
