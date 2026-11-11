# TH03 — active agent handoff (2026-11-11)

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
- As of this handoff, MAIN has **76 independently verified stages**, covering
  **97 non-overlapping physical objects** and **89,269 executable CODE bytes**.
  This includes **10,570 bytes of original ReC98 `master.lib` CODE**, not
  newly recovered authored gameplay code. VSYNC storage, the master DATA/BSS carrier and
  two segment-order scaffolds contribute no CODE bytes. The stage list and
  counts are generated in [PROGRESS.md](PROGRESS.md); use that instead of
  historical stage IDs from older notes.
- Each selected owner is independently compiled in two original TC4/TASM
  rounds and linked against retained unchanged inputs. This is **not** one
  end-to-end cold all-source rebuild, and its physical CODE total is not a
  whole-game completion percentage.
- Native receipts compare complete owned CODE/initialized DATA, ordered OMF
  fields/PUBLICs/segment layouts, and two original TC4/TASM + TLINK MAIN links,
  including the Japanese program image and ordered MZ relocations.
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
| Reimu BOSS | `af1336i` | 2,020-byte owner; three true orbit phases, cadence-gated spreads and mirrored attack ending; original signed radial arithmetic retained |
| Rikako BOSS | `af1345e` | Complete 1,677-byte owner; three orbit phases, four entity/pellet phases and terminating alternating volley use exact mutually exclusive branch gates |
| Kana BOSS | `af1323f` | Complete 1,874-byte owner; staged and rotating emission windows, two cadence gates, byte-angle/speed increments, and intro flicker |
| Chiyuri BOSS | `af1349a` | Full 2,654-byte owner; positive four-way/ring cadence gates, 48-shot release, mutually exclusive horizontal/vertical fans; native joint `af1347h` |
| Marisa BOSS | `af1325h` | Complete 1,431-byte owner; positive active-attack renderer, narrow-column completion, original high-level ring branch |
| Kotohime / Yumemi / Mima BOSS | `af1343i` / `af1334f` / `af1339d` | Kotohime's random, aimed and nested radial releases now use original exact positive phase gates; Mima and Yumemi remain source-bound |
| Ellen BOSS | `af1331h` | Complete 1,675-byte owner; original extra-attack/paired-pellet byte-angle advances, intro flicker, spread phase and renderer codegen constraints |
| Enemy formations / ENEDAT VM | `af1310h` | Four original objects, 3,325 CODE bytes; segmented formation-script block-first indexing and original unchecked interpreter behavior |
| Bullet engine | `af1318f` | Complete 2,685-byte owner; independent spawn bounds, slot-state/clip guards, and collision-map eligibility; jointly linked with Mima at `af1318g` |
| Explosion collision / Fireball | `af1198g` / `af1325i` | Original hit-chain rules; Fireball free-slot filtering, three falling-removal gates and original transfer labels; retain uninitialized state |
| Kotohime / Yumemi Extra Attack | `af1199e` / `af1200c` | Complete entity/render states |
| Rikako / Kana / Mima Extra Attack | `af1301f` / `af1302f` / `af1306e` | Full allocators, updates and rendering; first-use locals tested independently |
| Q8 polar / PI reload / DOS handoff | `af1322h` / `af1322i` / `af1322j` | Explicit signed Q8 center addition, far PI slot pointers and far DOS executable arguments; joint scope `af1322g` |
| VSYNC storage-only ASM | `af1337i` | Original `VS.ASM`: 0 CODE, 8 initialized DATA, 8 BSS and 12 aliases; only one tied PUBLIC pair needs MAP-order normalization |
| Original master.lib CODE | `af1338c` | Original external library carriers, 10,570 CODE bytes / 464 ordered fields / 103 PUBLICs; two exact native links and pinned vendor includes, not game-authored code |
| Master DATA/BSS tail | `af1340d` | Original `mst_tail` source carrier: 1,566 initialized DATA bytes, 1,606-byte DATA segment, 22,250-byte BSS segment, 414 PUBLICs and 0 CODE; generated sprite and vendor dependencies pinned |
| MAIN aggregate root | `af1341b` | Original 32-segment `main.obj` bound: 896 executable CODE, 1,289 initialized DATA, 64 fixups and 127 PUBLICs; three repaired bounded includes pinned |
| Native segment-order scaffolds | `af1342c` | Original `bo_shim` / `ex_ord` (19 + 11 zero-length SEGDEFs), exact raw OMF alignments and complete normal links; zero CODE/DATA/PUBLIC |
| Native frame delay / DOS initializer | `af1316e` / `af1316f` | Volatile VSYNC polling and nonzero allocation failure; joint native proof `af1316d` |
| Shared sound ASM leaves | `af1328b` | Three newly source-bound original TASM owners: PMD mode detection, resident probe and SE reset; 100 CODE bytes, native link/relocs exact |
| Graphics/resource ASM leaves | `af1330f` | Six source-bound TASM owners, 1,622 CODE bytes; HUD score aliases, sprite16, MRS, palette, flip LUT and fill carrier; includes now bound |
| Vector/playfield/collision ASM | `af1332c` | Three newly source-bound TASM objects: 160-byte vectors, 118-byte playfield geometry, 432-byte collision-map generator |
| Demo transition control | `af1333a` | 663-byte source-bound TC4 stage wipe, triangle mask, two phase callbacks and frame transitions |
| Round RNG / collision reset | `af1333c` | 82-byte TASM carrier, source-bound RNG macros, fill loop, collision reset, three maintained includes |
| PMD/MIDI audio services | `af1346g` | Two complete audio owners: active-only Kaja interrupt, positive SE priority/first-selection and frame-zero PMD dispatch; Rikako joint proof `af1346h` |
| Input modes / wait | `af1344d` | Nine native interfaces; explicit joystick availability, signed bounded wait and release/press empty-input gates; CPU/VSYNC joint stage `af1344e` |
| Hitbox + HitCircle | `af1348j` | Whole 711-byte collision pair; short-circuited spawn/bomb gates, explicit DGROUP near-pointers, live-age sprite rendering; Chiyuri/Bullet join `af1348k` |
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

## Open blocker: original `input_s` source versus historical linker carrier

The original TC4 `input_s.obj` and the fresh maintained C++ object each have
**417 CODE bytes**, **42 ordered OMF fixup fields**, and identical PUBLICs
and segments (`af1320c`/`af1320d`). The frozen normal MAIN link instead
used an older **418-byte assembler carrier**. When linked with the genuine
417-byte TC4 object (`af1305a`), the result differs at only file offset
**68,141** (`0x90` versus `0x00`), with the same ordered MZ relocations.

The maintained `src/main/hardware/input_scan.asm` naturally emits the
extra `0x90` through a TASM `EVEN` alignment. Independent stage `af1335b`
proves the 418-byte carrier and both complete normal TLINK images. This
**explains historical parent-link provenance** without a hand-inserted NOP,
but does not prove that the original **417-byte TC4 source object** can
reproduce that normal link. Keep those two claims separate; the alternative
assembler carrier is intentionally absent from current original-OBJ source
coverage. Full diagnostics: [input alignment review](MAIN_INPUT_S_LINK_GAP_AFTER744_REVIEW.md).

The original CRT `c0l.obj`, canonical packed-file/Factory acceptance and
whole-product source composition remain separate unfinished gates.

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
placeholder is not executable verbatim. **Do not routinely replay the cold
build or run every selected source reviewer for a small change.**

Keep original targets, tools, analyzer projects and current build/compare
inputs. Record useful conclusions briefly. Old trial artifacts may be pruned.
**Historical stage IDs in focused notes are observations, not a promise that
an output directory still exists.** Use generated current selections for
live rechecks and fresh stage IDs for new experiments. Documentation references
alone do not make old output necessary. The `input_s` context above remains useful
until its linker discrepancy is resolved. See the short
[storage guidance](STORAGE_HANDOFF_CURRENT.md).
