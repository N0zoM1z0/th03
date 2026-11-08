# TH03 — active handoff to the next reconstruction agent

> Current workflow: follow the **Highest priority** section in `AGENTS.md`.
> Prefer affected exact comparisons and useful Markdown knowledge. Ordinary
> notes do not require full CI, native replay or document-hash/pin refreshes.
> Older broad validation instructions apply only when their impact is relevant.


**Checked 2026-11-08 · current maintained-source native MAIN proof: `af969a`.**
This is the **active, intentionally short handoff**. The previous 2,713-line
handoff is preserved without substantive deletion in
[RE_HANDOFF_ARCHIVE_AFTER927.md](RE_HANDOFF_ARCHIVE_AFTER927.md). Its many
historical “Latest” headings are **not current checkout claims**.
Older archives: [after709](RE_HANDOFF_ARCHIVE_AFTER709.md),
[after596](RE_HANDOFF_ARCHIVE_AFTER596.md),
[after554](RE_HANDOFF_ARCHIVE_AFTER554.md).

## First read: what is actually proved

- Source repository is the real persistent `th03` worktree. Start with
  `git status -sb`, [AGENTS.md](../AGENTS.md),
  [RE_WORKFLOW.md](RE_WORKFLOW.md), the relevant original C++ file and
  the experiment-specific review. **Carry forward dirty work; do not
  assume another agent is concurrently editing this repository.**
- Original targets are the **pinned Japanese binaries** from
  `config/targets.toml` with `candidate-local-attested` provenance.
  Do not use translated/reference binaries as targets or alter original
  target/OBJ/compiler/CRT/linker inputs to create equality.
- **Seven-object MAIN integration snapshot: `af935a` (now historical for ba_maris).** Two
  independent original Turbo C++ 4.02 rounds recompiled **seven original
  physical project objects together**: the complete Marisa BOSS
  (`ba_maris`), HitCircle (`hitcirc`), all **four** Enemy source consumers
  (`eforna`, `efornb`, `eupda`, `eupdb`) and the complete Bullet engine.
  The normal complete **99-game-object MAIN TLINK** ran twice, reusing
  **92 unchanged original game objects and Borland CRT**. All **7,886 CODE
  bytes, 647 ordered native OMF FIXUPP fields, 52 PUBLICs**, source/header
  dependencies, 16-bit segment/ABI layout, complete MAIN EXE/MAP,
  **124,642 Japanese loaded bytes and all 1,553 original ordered MZ
  relocations** match. See [after935 integrated source](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER935_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af935a/report.json`,
  SHA-256 `924fdd7943c428064b1a26d9a3a4b4b99303d4204f7c4d7bfd682965d35c3620`.
- **Independent earlier source-current experiment: `af927a`.** Two
  original compiler and normal-link rounds rebuilt five original objects,
  reusing 94 other game objects and CRT. Their **7,833 CODE bytes,
  991 ordered OMF FIXUPPs and 34 PUBLICs** remain source-current, with
  full original Japanese MAIN and 1,553 relocations matched. A separately
  reviewed standard DOS MZ serializer also matches the original
  **130,882-byte Japanese MAIN.EXE**.
- These earlier five scopes are **complete Chiyuri major BOSS** (`ba_chiyu`,
  2,654 CODE), **complete MAIN entry/round scheduler** (`entry`, 3,050),
  **full player-effects/GRCG engine** (`effects`, 628), **Chiyuri
  Chargeshot/Gauge** (`cs_chiyu`, 1,011) and **Chiyuri Bomb** (`b_chiyu`,
  490). `entry` consumes four maintained `.inl` implementations;
  edits to them must recompile the real **`entry` physical object**.
  Review [after927 integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER927_REVIEW.md).
  Protected actual native writer receipt:
  `.analysis/work/exatt-layout-af927a/report.json`, SHA-256
  `3b64374f73e81bfedaf86227724544664f18d5b5ffe39ed5b381001c168ab6d5`.
- **Latest Marisa major-BOSS source-current follow-up: `af969a`.** The
  complete nine-function ba_maris owner was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,431 CODE bytes, 199
  ordered OMF FIXUPPs and nine PUBLICs**, with all 124,642 Japanese loaded
  bytes and 1,553 ordered MZ relocations exact. The other 98 original game
  objects and CRT were reused. The template, scheduler/render states and
  six level parameters now use semantic C++ names. See
  [Marisa BOSS native C++ after969](MAIN_MARISA_BOSS_TEMPLATE_AND_LEVEL_AFTER969_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af969a/report.json,
  SHA-256 ac37d9c2b6f5877c19e0aa15af96eee017ddddd4fa1ddeafe089ed4a8e97e3c2.
- **Latest Kana major-BOSS source-current follow-up: `af966a`.** The
  complete nine-function ba_kana owner was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,874 CODE bytes, 274
  ordered OMF FIXUPPs and nine PUBLICs**, with all 124,642 Japanese
  loaded bytes and 1,553 ordered MZ relocations exact. The other 98
  original game objects and CRT were reused. See
  [Kana BOSS native C++ after966](MAIN_KANA_BOSS_NATURAL_TEMPLATE_LEVEL_AND_RENDER_AFTER966_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af966a/report.json`,
  SHA-256 `da17ec634a93ca022f7270d58aeb53d350f05b3b5b1610c4acf4c14e07520bb2`.
  A fresh cloud-angle trial confirms that _AL -= 0x10 emits ADD AL,F0,
  not the original SUB AL,10; the explicit instruction remains. See
  [Kana cloud byte subtraction after967](MAIN_KANA_CLOUD_BYTE_SUBTRACTION_AFTER967_REVIEW.md).
- **Latest Kotohime major-BOSS source-current follow-up: `af968c`.** The
  complete eleven-function ba_koto owner was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,840 CODE bytes, 262
  ordered OMF FIXUPPs and eleven PUBLICs**, with all 124,642 Japanese
  loaded bytes and 1,553 ordered MZ relocations exact. A volatile byte
  dereference forces the original phase reload after the preceding +4,
  while retaining the native AL increment/store. See
  [Kotohime phase reload after968](MAIN_KOTOHIME_BOSS_NATURAL_PHASE_RELOAD_AFTER968_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af968c/report.json,
  SHA-256 4e85046a9c0d4a959b28e736d339392fda2732e25a086bfa0abecaee0834a598.
- **Earlier Kotohime major-BOSS source-current follow-up: `af965e`.** The
  complete eleven-function ba_koto owner was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,840 CODE bytes, 262
  ordered OMF FIXUPPs and eleven PUBLICs**, with all 124,642 Japanese
  loaded bytes and 1,553 ordered MZ relocations exact. The other 98
  original game objects and CRT were reused. See
  [Kotohime BOSS native C++ after965](MAIN_KOTOHIME_BOSS_NATURAL_STATES_AND_LEVEL_AFTER965_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af965e/report.json`,
  SHA-256 `abbd5dbaeb972d3004e973dbce9f3a7cfdd0d0383cc0c70f665ad5a74675ee2c`.
- **Latest Fireball source-current follow-up: `af964e`.** The complete
  24-projectile, ten-function `e_fireb` object was rebuilt in two original
  TC4 rounds with the complete normal MAIN link: **1,555 CODE bytes,
  115 ordered OMF FIXUPP fields, ten PUBLICs, one DATA byte and one BSS
  byte**. Both rounds reproduce the 124,642-byte Japanese MAIN loaded image
  and all 1,553 ordered MZ relocations. The other 98 original game objects
  and CRT were reused. The source now uses natural zero predicates for the
  fireball flag, HP and hitbox result, and names the distinct 64x64 explosion
  sprite / 64x48 collision geometry. See
  [Fireball predicates after964](MAIN_FIREBALL_NATURAL_BYTE_PREDICATES_AFTER964_REVIEW.md)
  and [Fireball geometry after964](MAIN_FIREBALL_EXPLOSION_GEOMETRY_AFTER964_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af964e/report.json`,
  SHA-256 `3f03d78b2808918c5377e79bb14a164d86c38d585642db79e95358fd2f287cba`.
- **Latest Ellen major-BOSS source-current follow-up: `af964a`.** Both
  independent radial Extra Attack volleys in the complete nine-function
  `ba_ellen` controller now use natural byte-angle addition/assignment,
  preserving the runtime 256/count division and spawn order. Two original
  TC4 rounds match **1,675 CODE bytes, 213 ordered OMF FIXUPPs and nine
  PUBLICs**, with complete normal MAIN and all 1,553 MZ relocations exact.
  See [Ellen radial Extra angle after964](MAIN_ELLEN_BOSS_NATURAL_EXTRA_ANGLE_AFTER964_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af964a/report.json`,
  SHA-256 `d0d4384d45de700bbe3f9fd7a0ff71a2b6d1684467331d41cb90e21bbca2b1fe`.
- **Latest Ellen major-BOSS source-current follow-up: `af962a`.** The
  complete nine-function `ba_ellen` BOSS was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,675 CODE bytes, 213
  ordered OMF FIXUPPs and nine PUBLICs**, with all 124,642 Japanese
  loaded bytes and 1,553 ordered MZ relocations exact. The other 98 original
  game objects and CRT were reused. See [Ellen BOSS native C++ after962](MAIN_ELLEN_BOSS_LEVEL_AND_CADENCE_AFTER962_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af962a/report.json`,
  SHA-256 `0d4c188c64c0a551c2fa4c43cadf65f2ddfc7f2ae5bda69d6ad0a5cfaa5d7b71`.
- **Latest Rikako major-BOSS source-current follow-up: `af963a`.** The
  complete eight-function `ba_rikak` BOSS was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,677 CODE bytes, 215
  ordered OMF FIXUPPs and eight PUBLICs**, with all 124,642 Japanese
  loaded bytes and 1,553 ordered MZ relocations exact. The other 98 original
  game objects and CRT were reused. See [Rikako signed-angle native C++ after963](MAIN_RIKAKO_BOSS_NATURAL_SIGNED_ANGLE_AFTER963_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af963a/report.json`,
  SHA-256 `78fa528372b3450e59d4b9ae5467e04018390feb3601f56fc76b8f6d677302ff`.
- **Latest Rikako major-BOSS source-current follow-up: `af961c`.** The
  complete eight-function `ba_rikak` BOSS was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,677 CODE bytes, 215
  ordered OMF FIXUPPs and eight PUBLICs**, with all 124,642 Japanese
  loaded bytes and 1,553 ordered MZ relocations exact. The other 98 original
  game objects and CRT were reused. See [Rikako BOSS native C++ after961](MAIN_RIKAKO_BOSS_TEMPLATE_LEVEL_RENDER_AFTER961_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af961c/report.json`,
  SHA-256 `9fcbae796cef4dca161be6373e8d97e0c6d34c65c6243e717a2438929ffb5987`.
- **Latest Ellen major-BOSS source-current follow-up: `af960a`.** The
  complete nine-function `ba_ellen` BOSS was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,675 CODE bytes, 213
  ordered OMF FIXUPPs and nine PUBLICs**, with all 124,642 Japanese
  loaded bytes and 1,553 ordered MZ relocations exact. The other 98 original
  game objects and CRT were reused. See [Ellen BOSS native C++ after960](MAIN_ELLEN_BOSS_TEMPLATE_RENDER_AFTER960_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af960a/report.json`,
  SHA-256 `448760cfd873930a2e15b3b61fa692fbf5145c9dbca62f20a4d862950f7abc5c`.
- **Latest Chiyuri major-BOSS source-current follow-up: `af959b`.** The
  complete 11-function `ba_chiyu` BOSS was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **2,654 CODE bytes, 381
  ordered OMF FIXUPPs and eleven PUBLICs**, with all 124,642 Japanese
  loaded bytes and 1,553 ordered MZ relocations exact. The other 98 original
  game objects and CRT were reused. See [Chiyuri BOSS native C++ after959](MAIN_CHIYURI_BOSS_TEMPLATE_RENDER_AFTER959_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af959b/report.json`,
  SHA-256 `2a3f864b74ed5c01b6b0217833ce46ecb04ea8930cd8af301503658329baba69`.
- **Latest Yumemi major-BOSS source-current follow-up: `af956a`.** The
  full ten-function `ba_yumem` BOSS was rebuilt in two original TC4 rounds
  with the complete normal MAIN link: **2,358 CODE bytes, 343 ordered OMF
  FIXUPPs and ten PUBLICs**, with all 124,642 Japanese loaded bytes and
  1,553 ordered MZ relocations exact. The other 98 original game objects
  and CRT were reused. See [Yumemi BOSS native C++ after956](MAIN_YUMEMI_BOSS_NATURAL_RENDER_AND_TEMPLATE_AFTER956_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af956a/report.json`,
  SHA-256 `418f24c6cf9c7aa8b2bb5480ef4b7fb808642da2b46ff37e052157c614b35c7a`.
- **Latest Mima major-BOSS source-current follow-up: `af952a`.** The full
  nine-function `ba_mima` BOSS was rebuilt in two original TC4 rounds with
  the complete normal MAIN link: **1,922 CODE bytes, 277 ordered OMF
  FIXUPPs and nine PUBLICs**, with all 124,642 Japanese loaded bytes and
  1,553 ordered MZ relocations exact. The other 98 original game objects
  and CRT were reused. See [Mima BOSS native C++ after952](MAIN_MIMA_BOSS_NATURAL_RENDER_AND_STATE_AFTER952_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af952a/report.json`,
  SHA-256 `d780002d0d8b5daf2756232c0b6e92d461813e045d15a9397b5478b8b7ecee13`.
- **Latest single-object source-current MAIN follow-up: `af944a`.** The
  complete nine-function Reimu major BOSS (`ba_reimu`) was recompiled in
  two original TC4 rounds with its complete normal MAIN link: **2,020 CODE
  bytes, 270 ordered OMF FIXUPPs, nine PUBLICs**, all 124,642 loaded bytes
  and 1,553 MZ relocations match. See
  [Reimu BOSS native C++ after944](MAIN_REIMU_BOSS_CLOUD_NATURAL_AFTER944_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af944a/report.json`,
  SHA-256 `2691ea3727c53fc41646c5d7c9408324d2e874c8f2a38aae79efa946f9cf99c6`.
- Both independent multi-object scopes are **current-source native normal MAIN proof**,
  **not** vendor packet-identical OMF, full original source ownership or
  canonical packed-file Factory acceptance. The 7,886 and 7,833 CODE bytes
  were already historically source-covered; do not award new distinct
  original CODE bytes or add these overlapping historical proof scopes.

## Independent current-source receipts versus historical snapshots

These genuine two-round native compiler/linker reports were rechecked against
the current checkout after `af935a`. They are **independent physical-object
scopes**, not one combined 99-original-source replay:

| Source-current stage | Complete physically rebuilt original owners | Original CODE bytes |
| --- | ---: | ---: |
| `af969a` | 1 | 1,431 |
| `af968c` | 1 | 1,840 |
| `af966a` | 1 | 1,874 |
| `af964e` | 1 | 1,555 |
| `af964a` | 1 | 1,675 |
| `af963a` | 1 | 1,677 |
| `af959b` | 1 | 2,654 |
| `af956a` | 1 | 2,358 |
| `af952a` | 1 | 1,922 |
| `af944a` | 1 | 2,020 |
| `af935a` | 7 | 7,886 |
| `af927a` | 5 | 7,833 |
| `af915a` | 5 | 6,059 |
| `af909a` | 5 | 7,582 |
| `af889a` | 5 | 4,191 |
| `af880h` | 2 | 1,245 |
| `af882e` | 1 | 49 |

The Kana `af965b` and Kotohime `af965a` receipts are earlier
source snapshots superseded by `af966a` and `af965e`, respectively.
Kotohime `af965e` is now historical after `af968c`; Marisa's
`af935a` and older single-object `af930e` receipts are now historical for
ba_maris after `af969a`. Use `af968c` and `af969a` for current
source binding. The Ellen `af962a`
receipt is now a historical source snapshot after
`af964a` changed the same physical owner; preserve it, but use `af964a`
for current source binding. Fireball `af964d` is the source snapshot before
the explosion-geometry naming in `af964e`; `af964b` and `af964c` are
earlier predicate experiments. The failed direct-call trial `af964f`
remains preserved as a negative compiler result. Use `af964e` for current
Fireball source binding. The Rikako `af961c` receipt is now a historical source snapshot after
`af963a` changed the same physical owner; preserve it, but use `af963a` for
current source binding. The older Ellen `af960a` receipt is now a historical source snapshot after
`af962a` changed the same physical owner; preserve it, but use `af962a` for
current source binding. `af961b` and `af961a` are likewise earlier Rikako
source snapshots superseded by `af961c`.
`af921a` (`hitcirc`), `af903a` (`bullet`), `af896a` (all four physical
`enemy.cpp` consumers), `af883a` and `af881i` (`ba_maris`) no longer
bind to the changed maintained source hashes. Their original native outputs
are authentic **historical** evidence; `af935a` establishes the entire
currently changed physical scope together. These independent receipts may
have related/overlapping ownership: never add their bytes as distinct
coverage or infer whole-product source exactness.
The genuine older `af877a` now **fails current maintained-source hash
binding** because both Chiyuri BOSS and Chiyuri Chargeshot changed.
`af871a` also fails after earlier Kotohime/other source changes.
`af865a`, `af859a`, `af853a`, `af847a`, `af843g`, `af842a`,
`af840a`, `af835a` and many earlier rounds are **historical evidence**,
not this checkout's source-current proof. Preserve their frozen writer
logs and reports; never rewrite old receipts or weaken binding checks.
The [after927 archive](RE_HANDOFF_ARCHIVE_AFTER927.md) and per-experiment
reviews contain the historical source/codegen trial details.

## Source-product status: avoid mixing denominators

The latest `scripts/preflight.py` (2026-11-08) reports:

- **MAIN:** real source-native normal linker comparisons above, but
  **no claim of complete game-source exactness or canonical packed-game
  acceptance**. Parent and selected original project OBJ/CRT are reused;
  a verified normal EXE does not automatically establish the vendor
  linker’s own MZ-header serialization or packet-identical OMF.
- **MAINL (ending):** current decoded source **accepted units 0/259**,
  zero current authored/library decoded acceptance and Factory
  acceptance **false**. The after587 historical original-native link
  did reproduce the **67,372-byte Japanese MAINL executable and 677
  relocations at that historic source snapshot**, but its old broad
  source publication guard no longer matches this checkout. Recertify
  current source and ownership before calling that result current.
  Historical older “0/250” uses a *different tracking population*;
  do not substitute it for the current preflight **0/259**.
- A fresh **scoped current-source MAINL Staff Roll build `af942s`** now
  recompiles the entire 19-procedure `staffdat` owner in two independent
  original TC4 rounds: **3,695 CODE + 224 DATA bytes, 342 literal ordered
  OMF FIXUPPs, six DATA PUBLICs**, with both complete normal MAINL links
  reproducing the Japanese 67,372-byte EXE and all 677 relocations. The
  other 35 original game objects and CRT were reused; no full cold replay.
  See [MAINL Staff native C++ after942](MAINL_STAFF_NATURAL_CPP_AFTER942_REVIEW.md).
  The old broad cold-source graph still pins the pre-edit `staff/data.cpp`;
  do not call it current or repin it just to satisfy cold-dependent tests.
- A separate **scoped current-source MAINL root-controller build `af944r`**
  recompiles the complete 11-function `rootdata` owner in two independent
  original TC4 rounds: **2,458 CODE + 112 DATA + 186 BSS bytes, 278 literal
  ordered OMF FIXUPPs and all 17 PUBLICs**. Both complete normal MAINL links
  reproduce the Japanese 67,372-byte EXE and all 677 relocations. The other
  35 original game objects and C0/CRT were reused; no full cold replay.
  See [MAINL root native C++ after944](MAINL_ROOT_CONTROLLER_NATURAL_CPP_AFTER944_REVIEW.md).
  The old after580 root receipt is now a historical source snapshot; this
  new report binds the edited `root/complete_data.cpp` source.
- **OP:** current decoded source acceptance **60 extents / 92
  procedures / 14,985 bytes** (13,221 CODE + 1,764 DATA), with a
  validated source-only cold pair and native ownership/ABI. This is
  separate from canonical packed-file acceptance or whole-game exactness.
- **ZUN:** current decoded source acceptance **77 extents**, with
  2,179 authored, 1,390 original-ASM and 5,066 library bytes;
  canonical packed-unit credit and complete source ownership remain open.
- Whole-game completion percentage is **unknown**. Use
  [the generated progress](PROGRESS.md) and **current preflight**,
  not old claimed percentages or summed CODE extents.

## Important unresolved issues and best next work

1. **Pursue new distinct original source ownership**, not only another
   refactor of already historically source-covered CODE. Attack real
   large BOSS/engine functions and small leaves together; use original
   codegen to confirm natural C/C++, but count new bytes only after
   formal acceptance. The newest work provides repeatable examples.
2. **`input_s` historical single-NOP parent normal-link gap** remains
   unresolved. Do not insert a synthetic NOP, alter an original OBJ or
   claim full normal MAIN acceptance for that owner. See the read-only
   `scripts/review_th03_input_s_link_gap_after744.py` diagnostic.
3. **MAINL decoded publication and source binding** require fresh
   recertification against current source and the preserved after587
   ancestry; 0/259 current accepted. The historical linker equality
   is useful evidence but **not** a current broad-source acceptance.
4. **Vendor OMF packet identity and raw MZ-header writer identity**
   remain separate from CODE, ordered FIXUPP, PUBLIC and independently
   serialized Japanese EXE equality. **Factory canonical packed-file
   acceptance remains open.** Preserve this distinction in every report.
5. **Storage:** `.analysis` includes the Wine/Borland toolchain,
   original inputs and successful two-round OBJ/EXE/MAP/writer logs.
   Never bulk-remove source-bound stages or prune by age. Only audited
   unreferenced failed trials and official regenerable caches may be
   removed. The latest bounded safe repack/cache cleanup reclaimed
   about 23.77 MiB **without deleting proof trees**; see
   [after928 applied storage audit](STORAGE_HANDOFF_AFTER928.md) and
   [current storage policy](STORAGE_HANDOFF_CURRENT.md).

## Minimal repeatable commands (no full cold replay)

```sh
# At session start; read-only, modest checks
 git status -sb
 .venv/bin/python scripts/preflight.py
 DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
   .venv/bin/python scripts/review_th03_main_source_overlay.py \
   --stage af935a af927a af915a af909a af889a af880h af882e

# If a maintained physical source or its actual .inl changed:
# replace the examples with real original TUs and a UNIQUE unused stage.
# Shared enemy.cpp has FOUR physical consumers, even if one code path changes.
 DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
   .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
   --stage afNEWa --units eforna,efornb,eupda,eupdb
 DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
   .venv/bin/python scripts/review_th03_main_source_overlay.py --stage afNEWa

# Ordinary completion checks
 .venv/bin/python -m unittest discover -s tests \
   -p test_main_source_overlay_inline_contract.py -q
 .venv/bin/python scripts/validate_tracking.py
 .venv/bin/python scripts/progress.py --check
 git diff --check
```

Use an actually unused DOS-safe `afNNNx` stage, **not** the literal
`afNEWa` example. Probe **only edited original physical TUs**, preserving
all other original game objects and CRT, and require two actual original
TC4 rounds plus two complete **normal** MAIN TLINKs. No routine full
cold replay. Do not edit another agent's reference toolchain or original
target. Preserve dirty source changes and commit meaningful progress as
`gpt-web: xxx` (local commits; no push unless asked).

## Reference map

- [Workflow](RE_WORKFLOW.md) · [Architecture](ARCHITECTURE.md) ·
  [Original fixed targets](../config/targets.toml)
- [Current Marisa BOSS native C++ work](MAIN_MARISA_BOSS_TEMPLATE_AND_LEVEL_AFTER969_REVIEW.md)
- [Current Kotohime phase-reload native C++ work](MAIN_KOTOHIME_BOSS_NATURAL_PHASE_RELOAD_AFTER968_REVIEW.md)
- [Current Kana BOSS native C++ work](MAIN_KANA_BOSS_NATURAL_TEMPLATE_LEVEL_AND_RENDER_AFTER966_REVIEW.md)
- [Kana cloud SUB AL codegen finding](MAIN_KANA_CLOUD_BYTE_SUBTRACTION_AFTER967_REVIEW.md)
- [Current Fireball byte-predicate native work](MAIN_FIREBALL_NATURAL_BYTE_PREDICATES_AFTER964_REVIEW.md)
- [Current Fireball explosion-geometry native work](MAIN_FIREBALL_EXPLOSION_GEOMETRY_AFTER964_REVIEW.md)
- [Current Ellen radial Extra angle native work](MAIN_ELLEN_BOSS_NATURAL_EXTRA_ANGLE_AFTER964_REVIEW.md)
- [Earlier Ellen BOSS level/cadence native work](MAIN_ELLEN_BOSS_LEVEL_AND_CADENCE_AFTER962_REVIEW.md)
- [Latest Rikako signed-angle source/native follow-up](MAIN_RIKAKO_BOSS_NATURAL_SIGNED_ANGLE_AFTER963_REVIEW.md)
- [Rikako BOSS template/level/render follow-up](MAIN_RIKAKO_BOSS_TEMPLATE_LEVEL_RENDER_AFTER961_REVIEW.md)
- [Latest Ellen BOSS source/native follow-up](MAIN_ELLEN_BOSS_TEMPLATE_RENDER_AFTER960_REVIEW.md)
- [Latest Chiyuri BOSS source/native follow-up](MAIN_CHIYURI_BOSS_TEMPLATE_RENDER_AFTER959_REVIEW.md)
- [Latest Yumemi BOSS source/native follow-up](MAIN_YUMEMI_BOSS_NATURAL_RENDER_AND_TEMPLATE_AFTER956_REVIEW.md)
- [Latest Mima BOSS source/native follow-up](MAIN_MIMA_BOSS_NATURAL_RENDER_AND_STATE_AFTER952_REVIEW.md)
- [Latest Reimu BOSS source/native follow-up](MAIN_REIMU_BOSS_CLOUD_NATURAL_AFTER944_REVIEW.md)
- [Seven-object integration snapshot (historical for Marisa)](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER935_REVIEW.md)
- [Earlier five-object source/native integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER927_REVIEW.md)
- [Historical source and compiler trials through after927](RE_HANDOFF_ARCHIVE_AFTER927.md)
- [Storage policy and prior safe cleanup audits](STORAGE_HANDOFF_CURRENT.md)
- [After928 applied Git/cache storage recovery](STORAGE_HANDOFF_AFTER928.md)
- [Current MAINL Staff source/native work](MAINL_STAFF_NATURAL_CPP_AFTER942_REVIEW.md)
- [Current MAINL root controller source/native work](MAINL_ROOT_CONTROLLER_NATURAL_CPP_AFTER944_REVIEW.md)
- [MAINL original CRT/source recovery index](MAINL_WORKING_CRT_RECOVERY_INDEX.md)
- [Generated source/acceptance progress](PROGRESS.md)
