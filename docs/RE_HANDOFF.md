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
- As of this handoff, `scripts/status.py` selects **71** separately verified
  native MAIN stages covering **90 distinct physical OBJ owners** and
  **77,803 CODE bytes**. This is a total for selected, non-overlapping owners,
  **not new work completed in a session**, and the stages are independently
  linked against retained unchanged inputs, **not** one all-source build.
  For the current exact stage IDs and scopes, consult `scripts/status.py`
  (`native_source_reviews`) or the generated [progress table](PROGRESS.md)
  instead of copying old stage IDs from historical reviews.
- Native receipts reproduce complete owned CODE/initialized DATA, ordered
  OMF fields/PUBLICs/segment layout, and two original TC4/TASM + TLINK MAIN links
  with target-equal Japanese program image and ordered MZ relocations.
  Local evidence is separate from canonical Factory Oracle acceptance;
  do not claim whole-product or packed-file acceptance from these scopes.

## Current reconstruction checkpoints

These are **examples of current source-bound stages**, not another exhaustive
list. The full selection lives in the generated progress table.

| Owner / area | Stage | Focus |
| --- | --- | --- |
| VRAM plane initializer | `af1326e` | Newly source-bound original TH01 shared 41-byte hardware owner; four far plane pointers, complete normal MAIN link |
| Shared BOSS controller and ring | `af1326i` | Two physical owners, 949 bytes; exact HP, edge turns, descent, pattern-count transitions, retained native RNG rejection loop |
| MAIN entry + frame scheduler | `af1314c` | Full 3,050-byte scheduler; explicit render/VSYNC phase gates and independent victory checks, with original PC-98 page OUT order |
| Reimu BOSS | `af1312g` | Complete 2,020-byte owner; signed 256-unit radial distribution, byte-angle compound steering and cloud pattern guards |
| Rikako BOSS | `af1321h` | Complete 1,677-byte owner; independent signed spin limits and 8-frame clocks, positive intro flicker, exact render byte-angle steps |
| Kana BOSS | `af1323f` | Complete 1,874-byte owner; staged and rotating emission windows, two cadence gates, byte-angle/speed increments, and intro flicker |
| Chiyuri BOSS | `af1329l` | Full 2,654-byte owner; higher-level rings, four signed-index fans with exact speed steps, positive vertical phase and natural intro/ring guards |
| Marisa BOSS | `af1325h` | Complete 1,431-byte owner; positive active-attack renderer, narrow-column completion, original high-level ring branch |
| Kotohime / Yumemi / Mima BOSS | `af1319e` / `af1334f` / `af1317k` | Complete controllers; Yumemi's ring, aimed, cross, chase, rain terminal states now use positive gates; original full-player-header EXTDEF ordering still open |
| Ellen BOSS | `af1331h` | Complete 1,675-byte owner; original extra-attack/paired-pellet byte-angle advances, intro flicker, spread phase and renderer codegen constraints |
| Enemy formations / ENEDAT VM | `af1310h` | Four original objects, 3,325 CODE bytes; segmented formation-script block-first indexing and original unchecked interpreter behavior |
| Bullet engine | `af1318f` | Complete 2,685-byte owner; independent spawn bounds, slot-state/clip guards, and collision-map eligibility; jointly linked with Mima at `af1318g` |
| Explosion collision / Fireball | `af1198g` / `af1325i` | Original hit-chain rules; Fireball free-slot filtering, three falling-removal gates and original transfer labels; retain uninitialized state |
| Kotohime / Yumemi Extra Attack | `af1199e` / `af1200c` | Complete entity/render states |
| Rikako / Kana / Mima Extra Attack | `af1301f` / `af1302f` / `af1306e` | Full allocators, updates and rendering; first-use locals tested independently |
| Q8 polar / PI reload / DOS handoff | `af1322h` / `af1322i` / `af1322j` | Explicit signed Q8 center addition, far PI slot pointers and far DOS executable arguments; joint scope `af1322g` |
| Native frame delay / DOS initializer | `af1316e` / `af1316f` | Volatile VSYNC polling and nonzero allocation failure; joint native proof `af1316d` |
| Shared sound ASM leaves | `af1328b` | Three newly source-bound original TASM owners: PMD mode detection, resident probe and SE reset; 100 CODE bytes, native link/relocs exact |
| Graphics/resource ASM leaves | `af1330f` | Six source-bound TASM owners, 1,622 CODE bytes; HUD score aliases, sprite16, MRS, palette, flip LUT and fill carrier; includes now bound |
| Vector/playfield/collision ASM | `af1332c` | Three newly source-bound TASM objects: 160-byte vectors, 118-byte playfield geometry, 432-byte collision-map generator |
| Demo transition control | `af1333a` | 663-byte source-bound TC4 stage wipe, triangle mask, two phase callbacks and frame transitions |
| Round RNG / collision reset | `af1333c` | 82-byte TASM carrier, source-bound RNG macros, fill loop, collision reset, three maintained includes |
| PMD/MIDI audio services | `af1320b` | Two complete owners; native active-only Kaja interrupt and source-exact sound-effect service |
| Input modes / wait | `af1313c` | All nine interface, joystick and wait functions; natural positive joystick branches and exact release/press loops |
| Hitbox + HitCircle | `af1317l` | Two complete physical owners; independent shot ownership/bomb cadence checks and active-age animation updates |
| CPU movement/dodge controller | `af1327h` | Full 1,077-byte controller; floor escape, nine-direction retries, separate hit/safety gates; current joint source `af1327i` |
| Gauge / shared Extra Attack | `af1324e` | Near DGROUP player pointer, Hyper/full-gauge short circuit and native saturation, two full owners |
| MAINL Staff + root | `af942s` / `af944r` | Retained source scopes; decoded MAINL publication refreshed at `af1055m` |

Other complete BOSS, Bullet, Chargeshot, Bomb, HUD and player owners are listed
in [PROGRESS.md](PROGRESS.md), not repeated here. When updating one, verify
its **entire physical owner and consumers**, not only the changed function.
Successful C++ simplifications in one owner do not imply equal TC4 codegen in
another: byte/word signedness, local lifetime, `goto` layout, far pointers,
register effects and RNG consumption matter. Preserve proven original quirks
rather than adding defensive product fixes or manufactured byte padding.

## Open blocker: BIOS keyboard scanner `input_s`

`input_s` is the **only** owner in the 91-unit scoped MAIN source inventory
excluded from the 90-owner current normal-link selection. Both the original
OBJ and freshly compiled maintained C++ have 417 bytes of initialized CODE,
42 ordered native fixup fields and the same PUBLIC/segments. But the frozen
normal MAIN parent used an older **418-byte** experimental object with a
trailing `90` after the final `RET`. A fresh normal TLINK using the **actual
original 417-byte OBJ** (`af1305a`) still differs from the frozen parent
at only **file offset 68,141** (`90` versus `00`); all ordered MZ relocations
match. Fresh independent native negative stages `af1320c` and `af1320d`
confirm the same object and gap. Other one-byte SHARED alignment holes are
zero in both links, so this is not a general TLINK NOP-fill rule. File-scope
`asm { even }` did not compile under TC4 (`af1193b`).
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
