# TH03 — active handoff to the next reconstruction agent

> Current workflow: follow the **Highest priority** section in `AGENTS.md`.
> Prefer affected exact comparisons and useful Markdown knowledge. Ordinary
> notes do not require full CI, native replay or document-hash/pin refreshes.
> Older broad validation instructions apply only when their impact is relevant.


**Checked 2026-11-08 · current maintained-source native MAIN proof: `af1004a`.**
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
- **Earlier nine-major-BOSS cadence integration: `af993d`.**
  Two independent original TC4 4.02 rounds rebuilt all nine complete BOSS
  physical owners together: ba_mima, ba_reimu, ba_yumem, ba_ellen, ba_kana,
  ba_koto, ba_maris, ba_rikak and ba_chiyu. The simultaneous objects preserve
  **17,451 CODE bytes, 2,434 ordered OMF FIXUPPs and 85 PUBLICs**; both
  complete normal MAIN links reproduce all 124,642 Japanese loaded bytes
  and 1,553 ordered MZ relocations, reusing the other 90 original game
  objects and Borland CRT. Twenty-four periodic attack/render predicates
  now use natural explicit remainder comparisons or low-bit masks. See
  [Nine-BOSS cadence recovery after993](MAIN_NINE_BOSS_NATURAL_CADENCE_PREDICATES_AFTER993_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af993d/report.json,
  SHA-256 32c364c85247438b143a39b5f22d54c9163caa1aceccfd5faa76b399dd214854.
- **Earlier simultaneous twelve-owner MAIN integration: `af1001e`.**
  Two independent original TC4 4.02 rounds rebuilt all nine major BOSS
  owners together with the complete Hitbox, HitCircle and explosion-chain
  owners: **18,792 CODE bytes, 2,546 ordered OMF FIXUPPs and 91 PUBLICs**.
  Both complete normal MAIN links reproduce all 124,642 Japanese loaded
  bytes and 1,553 ordered MZ relocations, reusing the other 87 original
  game objects and Borland CRT. This integrates the current Mima trail-byte
  and hit-render changes, HitCircle self-division/named VRAM stride, the
  nine-BOSS cadence work, Hitbox combined guard and natural Explosion
  for-header. See
  [Twelve-owner integration after1001](MAIN_TWELVE_OWNER_INTEGRATION_AFTER1001_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af1001e/report.json,
  SHA-256 139acc3f4f193d073a638043e0d1f2323b8e7ff83b9612bd8c0844988d54eeb6.
- **Latest twelve-owner MAIN integration: `af1004a`.**
  Two independent original TC4 4.02 rounds rebuilt all nine major BOSS
  owners with complete Hitbox, HitCircle and explosion-chain owners:
  **18,792 CODE bytes, 2,546 ordered OMF FIXUPPs and 91 PUBLICs**. Both
  complete normal MAIN links reproduce all 124,642 Japanese loaded bytes
  and 1,553 ordered MZ relocations, reusing the other 87 original game
  objects and Borland CRT. This rechecks the latest natural attack-phase
  chains across Mima, Reimu, Yumemi, Ellen, Kana and Marisa alongside the
  previously recovered collision owners. See
  [Six-BOSS phase chains after1004](MAIN_SIX_BOSS_NATURAL_PHASE_CHAINS_AFTER1004_REVIEW.md)
  and [Earlier twelve-owner integration after1001](MAIN_TWELVE_OWNER_INTEGRATION_AFTER1001_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af1004a/report.json,
  SHA-256 958570ce186dc75e33a10d0b63d6a90edfd8c7ef1f63defbc2626e41c4b646c9.
- **Earlier explosion-chain collision source proof: `af997e`.**
  The complete far-__cdecl e_expl owner was rebuilt in two independent
  original TC4 4.02 rounds and complete normal MAIN links: **630 CODE
  bytes, 49 ordered OMF FIXUPPs and one PUBLIC**. The six duplicated
  continue-path index/pointer updates are now a natural for-header, and
  all state/player/frame prefilters share one ordered short-circuit guard.
  Both links reproduce all 124,642 Japanese loaded bytes and 1,553 ordered
  MZ relocations, reusing the other 98 original game objects and CRT. See
  [Explosion for-loop and guard recovery after997](MAIN_EXPLOSION_NATURAL_FOR_AND_GUARDS_AFTER997_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af997e/report.json,
  SHA-256 f33b52becbfbd8f817265fd118158fb8568e5477f8975fd7a7bb1d938e9f13f0.
- **Earlier Hitbox source proof: `af998d`.** The complete
  hitbox_hittest() physical owner was rebuilt in two original TC4 4.02
  rounds with the complete normal MAIN link: **266 CODE bytes, 33 ordered
  OMF FIXUPPs and one PUBLIC**. The negative-Y and banner early returns
  now share one ordered short-circuit guard; the two-player far Chargeshot
  dispatch remains explicit because direct indexed callback invocation
  changed CODE. Both links reproduce all 124,642 Japanese loaded bytes and
  1,553 ordered MZ relocations, reusing the other 98 original game objects
  and CRT. See
  [Hitbox combined guards after998](MAIN_HITBOX_NATURAL_COMBINED_GUARDS_AFTER998_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af998d/report.json,
  SHA-256 71e32d8a441ad584c96ac721e90e6852b867b751bd82e761278a627deec203b3.
- **Current HitCircle cel source proof: `af1000d`.** The complete
  hitcirc owner preserves all **445 CODE bytes, 30 ordered OMF FIXUPPs
  and four PUBLICs**. Its cel division uses a natural self-assignment and
  its scale derives from the six-byte VRAM width through a named constant.
  Both original compiler/normal MAIN rounds match. See
  [HitCircle cel register and stride recovery](MAIN_HITCIRCLE_NATURAL_CEL_REGISTER_AFTER976_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af1000d/report.json,
  SHA-256 f04fd95708946cb4c0dd0c9a904154eae504188b9dc64307d1064ea5f3db04c2.
- **Earlier Mima BOSS source proof: `af1001c`.** The complete
  ba_mima owner preserves all **1,922 CODE bytes, 277 ordered OMF FIXUPPs
  and nine PUBLICs**. The trail remainder now explicitly narrows to its
  original byte local, and the damaged-sprite branch uses a natural hit
  truth test. Both original compiler/normal MAIN rounds match. See
  [Mima trail-byte and hit rendering after1001](MAIN_MIMA_NATURAL_TRAIL_BYTE_AND_HIT_RENDER_AFTER1001_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af1001c/report.json,
  SHA-256 4b7eaaa3c29f789db710be4ee69912f271644e60a766ae812bc25662c4073137.
- **Earlier eight-major-BOSS source-current integration: `af988b`.**
  Two independent original TC4 4.02 rounds rebuilt all eight major BOSS
  physical owners together: ba_mima, ba_reimu, ba_yumem, ba_ellen, ba_kana,
  ba_koto, ba_maris and ba_rikak. The simultaneous objects preserve
  **14,797 CODE bytes, 2,053 ordered OMF FIXUPPs and 74 PUBLICs**; both
  complete normal MAIN links reproduce all 124,642 Japanese loaded bytes
  and 1,553 ordered MZ relocations, reusing the other 91 original game
  objects and Borland CRT. All eight global 16-bit BOSS frame increments
  now use natural prefix form. See
  [Eight-BOSS frame-clock integration after988](MAIN_EIGHT_BOSS_NATURAL_GLOBAL_FRAME_PREFIX_INTEGRATION_AFTER988_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af988b/report.json,
  SHA-256 409055acc70a43c445e26039d863ee9da88f40f7897a5ac58468178d61bc355e.
- **Earlier Kana major-BOSS source-current follow-up: `af976a`.** The
  complete nine-function ba_kana owner was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,874 CODE bytes, 274
  ordered OMF FIXUPPs and nine PUBLICs**. The sixteen-pellet staged volley
  now uses postfix increment in its natural for header; both rounds preserve
  the complete 124,642-byte Japanese MAIN image and all 1,553 MZ relocations.
  See [Kana postfix loop after976](MAIN_KANA_BOSS_NATURAL_FOR_POSTFIX_AFTER976_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af976a/report.json,
  SHA-256 45c0d81edc7473d3014ff4343c7049c867cd117cdd8d2dd7fb49bb0756c96fd3.
- **Earlier Marisa major-BOSS source-current follow-up: `af975d`.** The
  complete nine-function ba_maris owner was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,431 CODE bytes, 199
  ordered OMF FIXUPPs and nine PUBLICs**. The four-frame flicker uses a
  natural low-bit mask, the intro split radius uses multiplication by two,
  and the SI/DI split local is typed as screen_x_t while preserving its
  declaration order. See
  [Marisa flicker/split after975](MAIN_MARISA_BOSS_NATURAL_FLICKER_AND_SPLIT_AFTER975_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af975d/report.json,
  SHA-256 138823acc2036573271773d98d3cd367e96c092c8dde16e8c65b6501d0b420e5.
- **Earlier Kana major-BOSS source-current follow-up: `af974c`.** The
  complete nine-function ba_kana owner was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,874 CODE bytes, 274
  ordered OMF FIXUPPs and nine PUBLICs**, with all 124,642 Japanese loaded
  bytes and 1,553 ordered MZ relocations exact. Its 16-pellet staged volley
  now uses natural byte-field assignment and a for loop while preserving
  emit/angle/speed/index order. See
  [Kana staged volley after974](MAIN_KANA_BOSS_NATURAL_STAGED_VOLLEY_AFTER974_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af974c/report.json,
  SHA-256 ac9f32893af05350b6880577f39229e1e8a3e4dc06b2746d324706aa084dc206.
- **Earlier Hitbox source-current follow-up: `af986b`.** The complete
  hitbox_hittest() physical owner was rebuilt in two original TC4 rounds
  with the complete normal MAIN link: **266 CODE bytes, 33 ordered OMF
  FIXUPPs and one PUBLIC**. The shotpair loop uses prefix index/pointer
  updates, the bomb clock uses a low-bit test, and the two early exits are
  separate natural guard clauses. See
  [Hitbox scan and bomb clock after983](MAIN_HITBOX_NATURAL_SCAN_AND_BOMB_CLOCK_AFTER983_REVIEW.md)
  and [Hitbox early guards after986](MAIN_HITBOX_NATURAL_EARLY_GUARDS_AFTER986_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af986b/report.json,
  SHA-256 f9fb84eddb743fa3f2ff961eb11e87362ec1ba5ef09703310f25d1ec1755d2e5.
- **Earlier HitCircle source follow-up: `af985b`.** The complete
  four-function hitcirc owner was rebuilt in two original TC4 rounds with
  the complete normal MAIN link: **445 CODE bytes, 30 ordered OMF FIXUPPs
  and four PUBLICs**. Both thirteen-slot lifetime traversal and twelve-slot
  enemy rendering now use natural for headers with prefix index-before-pointer
  updates; the player sprite remains a separate final draw. See
  [HitCircle lifetime/render loops after985](MAIN_HITCIRCLE_NATURAL_LIFETIME_AND_RENDER_FOR_AFTER985_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af985b/report.json,
  SHA-256 000fc1edb8af9c71f4daa3c91f14a9c64825f8fb4b06e89c1b25853d804641a1.
- **Latest Chiyuri major-BOSS source-current follow-up: `af973b`.** The
  complete eleven-function ba_chiyu owner was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **2,654 CODE bytes, 381
  ordered OMF FIXUPPs and eleven PUBLICs**, with all 124,642 Japanese
  loaded bytes and 1,553 ordered MZ relocations exact. Lifecycle byte
  predicates are explicit, and the sixteen-sprite ring renderer now uses
  natural named multiplication for its radius and sprite-frame scales.
  See [Chiyuri ring scaling after973](MAIN_CHIYURI_BOSS_NATURAL_RENDER_SCALE_AFTER973_REVIEW.md)
  and [Chiyuri lifecycle after972](MAIN_CHIYURI_BOSS_NATURAL_LIFECYCLE_PREDICATES_AFTER972_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af973b/report.json,
  SHA-256 2b41bf9a0c0fc3bca5b88b9bc8c02b0ac27e73559b225beaa7ed7574772d3bb4.
- **Earlier Marisa major-BOSS source-current follow-up: `af971b`.** The
  complete nine-function ba_maris owner was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,431 CODE bytes, 199
  ordered OMF FIXUPPs and nine PUBLICs**, with all 124,642 Japanese loaded
  bytes and 1,553 ordered MZ relocations exact. The ring attack now uses
  natural byte-angle assignment; render hit/state predicates are explicit.
  See [Marisa ring angle after971](MAIN_MARISA_BOSS_NATURAL_RING_ANGLE_AND_RENDER_AFTER971_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af971b/report.json,
  SHA-256 14348b7868d9a8af655daf93999adbf3d4fcdd13dfb756568d8d7f4a72cd23d6.
- **Earlier Marisa major-BOSS source-current follow-up: `af969a`.** The
  complete nine-function ba_maris owner was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,431 CODE bytes, 199
  ordered OMF FIXUPPs and nine PUBLICs**, with all 124,642 Japanese loaded
  bytes and 1,553 ordered MZ relocations exact. The other 98 original game
  objects and CRT were reused. The template, scheduler/render states and
  six level parameters now use semantic C++ names. See
  [Marisa BOSS native C++ after969](MAIN_MARISA_BOSS_TEMPLATE_AND_LEVEL_AFTER969_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af969a/report.json,
  SHA-256 ac37d9c2b6f5877c19e0aa15af96eee017ddddd4fa1ddeafe089ed4a8e97e3c2.
- **Earlier Kana major-BOSS source-current follow-up: `af966a`.** The
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
- **Earlier Kotohime major-BOSS source-current follow-up: `af968c`.** The
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
- **Earlier Ellen major-BOSS source-current follow-up: `af964a`.** Both
  independent radial Extra Attack volleys in the complete nine-function
  `ba_ellen` controller now use natural byte-angle addition/assignment,
  preserving the runtime 256/count division and spawn order. Two original
  TC4 rounds match **1,675 CODE bytes, 213 ordered OMF FIXUPPs and nine
  PUBLICs**, with complete normal MAIN and all 1,553 MZ relocations exact.
  See [Ellen radial Extra angle after964](MAIN_ELLEN_BOSS_NATURAL_EXTRA_ANGLE_AFTER964_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af964a/report.json`,
  SHA-256 `d0d4384d45de700bbe3f9fd7a0ff71a2b6d1684467331d41cb90e21bbca2b1fe`.
- **Earlier Ellen major-BOSS source-current follow-up: `af962a`.** The
  complete nine-function `ba_ellen` BOSS was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,675 CODE bytes, 213
  ordered OMF FIXUPPs and nine PUBLICs**, with all 124,642 Japanese
  loaded bytes and 1,553 ordered MZ relocations exact. The other 98 original
  game objects and CRT were reused. See [Ellen BOSS native C++ after962](MAIN_ELLEN_BOSS_LEVEL_AND_CADENCE_AFTER962_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af962a/report.json`,
  SHA-256 `0d4c188c64c0a551c2fa4c43cadf65f2ddfc7f2ae5bda69d6ad0a5cfaa5d7b71`.
- **Earlier Rikako major-BOSS source-current follow-up: `af963a`.** The
  complete eight-function `ba_rikak` BOSS was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,677 CODE bytes, 215
  ordered OMF FIXUPPs and eight PUBLICs**, with all 124,642 Japanese
  loaded bytes and 1,553 ordered MZ relocations exact. The other 98 original
  game objects and CRT were reused. See [Rikako signed-angle native C++ after963](MAIN_RIKAKO_BOSS_NATURAL_SIGNED_ANGLE_AFTER963_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af963a/report.json`,
  SHA-256 `78fa528372b3450e59d4b9ae5467e04018390feb3601f56fc76b8f6d677302ff`.
- **Earlier Rikako major-BOSS source-current follow-up: `af961c`.** The
  complete eight-function `ba_rikak` BOSS was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,677 CODE bytes, 215
  ordered OMF FIXUPPs and eight PUBLICs**, with all 124,642 Japanese
  loaded bytes and 1,553 ordered MZ relocations exact. The other 98 original
  game objects and CRT were reused. See [Rikako BOSS native C++ after961](MAIN_RIKAKO_BOSS_TEMPLATE_LEVEL_RENDER_AFTER961_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af961c/report.json`,
  SHA-256 `9fcbae796cef4dca161be6373e8d97e0c6d34c65c6243e717a2438929ffb5987`.
- **Earlier Ellen major-BOSS source-current follow-up: `af960a`.** The
  complete nine-function `ba_ellen` BOSS was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,675 CODE bytes, 213
  ordered OMF FIXUPPs and nine PUBLICs**, with all 124,642 Japanese
  loaded bytes and 1,553 ordered MZ relocations exact. The other 98 original
  game objects and CRT were reused. See [Ellen BOSS native C++ after960](MAIN_ELLEN_BOSS_TEMPLATE_RENDER_AFTER960_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af960a/report.json`,
  SHA-256 `448760cfd873930a2e15b3b61fa692fbf5145c9dbca62f20a4d862950f7abc5c`.
- **Earlier Chiyuri major-BOSS source-current follow-up: `af959b`.** The
  complete 11-function `ba_chiyu` BOSS was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **2,654 CODE bytes, 381
  ordered OMF FIXUPPs and eleven PUBLICs**, with all 124,642 Japanese
  loaded bytes and 1,553 ordered MZ relocations exact. The other 98 original
  game objects and CRT were reused. See [Chiyuri BOSS native C++ after959](MAIN_CHIYURI_BOSS_TEMPLATE_RENDER_AFTER959_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af959b/report.json`,
  SHA-256 `2a3f864b74ed5c01b6b0217833ce46ecb04ea8930cd8af301503658329baba69`.
- **Earlier Yumemi major-BOSS source-current follow-up: `af983a`.** The
  complete ten-function ba_yumem BOSS was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **2,358 CODE bytes, 343
  ordered OMF FIXUPPs and ten PUBLICs**. Its rain volley uses a natural
  for-loop with verified prefix increment; all four arrival raster loops
  are also natural for loops. Both links reproduce the 124,642-byte Japanese
  MAIN image and all 1,553 MZ relocations. See
  [Yumemi rain increment after980](MAIN_YUMEMI_BOSS_NATURAL_RAIN_INCREMENT_AFTER980_REVIEW.md)
  and [Yumemi rain/arrival loops after979](MAIN_YUMEMI_BOSS_NATURAL_RAIN_AND_ARRIVAL_LOOPS_AFTER979_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af983a/report.json,
  SHA-256 53a363645f48f4b17ef8cae6c119812b4fa6737504fc8249f88a2bd581645c9b.
- **Earlier Mima major-BOSS source follow-up: `af984b`.** The
  complete nine-function ba_mima BOSS was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **1,922 CODE bytes, 277
  ordered OMF FIXUPPs and nine PUBLICs**. The spread and medium-pellet
  byte-angle updates now use ordinary addition/assignment; the separate
  signed orbit-steering byte retains its compound update. See
  [Mima spread-angle assignments after984](MAIN_MIMA_BOSS_NATURAL_SPREAD_ANGLE_ASSIGNMENTS_AFTER984_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af984b/report.json,
  SHA-256 01f13a472e8979f2a4b67f35a8c38e38d5c1672bb391632873fb24f80147ad75.
- **Earlier Reimu major-BOSS source-current follow-up: `af986a`.** The
  complete nine-function ba_reimu BOSS was rebuilt in two original TC4
  rounds with the complete normal MAIN link: **2,020 CODE bytes, 270
  ordered OMF FIXUPPs and nine PUBLICs**. All five loops use prefix
  increments; the intro comma-expression keeps index-before-angle order.
  The cloud direction predicate is explicit and its negative byte angle
  uses an explicit unsigned-byte conversion. See
  [Reimu prefix loops and cloud byte wrap after986](MAIN_REIMU_BOSS_NATURAL_PREFIX_AND_CLOUD_BYTE_AFTER986_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af986a/report.json,
  SHA-256 95dca00485bf6eec6b02c95caa377fe7264be5e0727270c6b72122e26553102c.
- **Earlier Reimu source-current follow-up: `af944a`.** The complete
  nine-function BOSS was rebuilt in two original TC4 rounds with its normal
  MAIN link: 2,020 CODE bytes, 270 ordered OMF FIXUPPs and nine PUBLICs.
  See [Reimu cloud semantics after944](MAIN_REIMU_BOSS_CLOUD_NATURAL_AFTER944_REVIEW.md).
  Protected report: .analysis/work/exatt-layout-af944a/report.json,
  SHA-256 2691ea3727c53fc41646c5d7c9408324d2e874c8f2a38aae79efa946f9cf99c6.
- Both independent multi-object scopes are **current-source native normal MAIN proof**,
  **not** vendor packet-identical OMF, full original source ownership or
  canonical packed-file Factory acceptance. The 7,886 and 7,833 CODE bytes
  were already historically source-covered; do not award new distinct
  original CODE bytes or add these overlapping historical proof scopes.

## Native proof receipts and current-source binding

These genuine two-round native compiler/linker reports document
independent complete physical-object scopes and simultaneous integrations.
The latest source-current integration is listed first; older snapshots are
kept as historical receipts below:

| Native proof stage | Complete physically rebuilt original owners | Original CODE bytes |
| --- | ---: | ---: |
| `af1004a` | 12 | 18,792 |
| `af1003f` | 1 | 1,431 |
| `af1003e` | 1 | 1,874 |
| `af1003d` | 1 | 1,675 |
| `af1003c` | 1 | 2,358 |
| `af1003a` | 1 | 2,020 |
| `af1002d` | 1 | 1,922 |
| `af1001e` | 12 | 18,792 |
| `af1001c` | 1 | 1,922 |
| `af1000d` | 1 | 445 |
| `af997e` | 1 | 630 |
| `af998d` | 1 | 266 |
| `af993d` | 9 | 17,451 |
| `af988b` | 8 | 14,797 |
| `af976a` | 1 | 1,874 |
| `af973b` | 1 | 2,654 |
| `af975d` | 1 | 1,431 |
| `af968c` | 1 | 1,840 |
| `af985b` | 1 | 445 |
| `af966a` | 1 | 1,874 |
| `af964e` | 1 | 1,555 |
| `af964a` | 1 | 1,675 |
| `af963a` | 1 | 1,677 |
| `af959b` | 1 | 2,654 |
| `af983a` | 1 | 2,358 |
| `af986b` | 1 | 266 |
| `af986a` | 1 | 2,020 |
| `af984b` | 1 | 1,922 |
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
The older explosion-chain source receipt af902e is historical after
current e_expl proof af997e; the original while-based traversal is retained
in that historical note, not the current source.
Hitbox af986b and earlier af983c are historical after current source proof
af998d; the split early-return form remains in its historical review.
The twelve-owner integration af1001e is now historical after the current
twelve-owner integration af1004a. The latter includes natural attack
phase-chain improvements across six complete BOSS owners and rechecks all
twelve owners together. The nine-owner integration af993d and earlier
individual BOSS receipts remain useful historical compiler trials.
The older explosion and Hitbox source receipts are likewise superseded as
current-source bindings by af1004a.

Compiler-sensitive negative results remain important. Reimu af981b/af981d
loop variants and unary negative-angle form changed complete CODE; the
prefix comma-expression and explicit unsigned-byte subtraction are the
current native-exact forms. The direct cloud-speed assignment in af982d
also changed complete BOSS CODE; the original postfix increment remains.
HitCircle af985c pointer-first for-header order changed complete CODE.
Hitbox af983d pointer-first scan update and af984d direct explosion call
also changed complete CODE; the index-first scan and explicit far/near
bridge remain. Mima af980a/af980c/af980d control-flow and frame/angle
variants, plus af984c explicit signed-orbit cast, are preserved negative
compiler results. HitCircle cel local/register arithmetic trials af976b-f, af987a/af989a-b
and af993e changed complete CODE; retain the verified BX sequence.

Current source bindings: af1004a for all nine major BOSSes, Hitbox,
HitCircle and e_expl; af964e remains the current Fireball source proof.
HitCircle af931b and
older af919g/af921a receipts are historical after af985b. Hitbox af983c
and af986b are historical after af998d. Marisa af935a/af930e, the prior individual BOSS
receipts and the eight-owner af988b integration are historical after
af993d. Fireball af964d is the source snapshot before geometry naming in
af964e; af964b/af964c are earlier predicate experiments and af964f is a
failed direct-call trial. The older af903a bullet, af896a enemy-consumer,
af883a and af881i Marisa receipts no longer bind to changed maintained
sources; af935a preserves their historical native outputs. Never add
overlapping receipts as distinct CODE ownership.

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
- [Current twelve-owner MAIN integration and six-BOSS phase chains](MAIN_SIX_BOSS_NATURAL_PHASE_CHAINS_AFTER1004_REVIEW.md)
- [Earlier twelve-owner MAIN integration](MAIN_TWELVE_OWNER_INTEGRATION_AFTER1001_REVIEW.md)
- [Current Mima trail-byte and hit-render source](MAIN_MIMA_NATURAL_TRAIL_BYTE_AND_HIT_RENDER_AFTER1001_REVIEW.md)
- [Current HitCircle cel register and VRAM stride](MAIN_HITCIRCLE_NATURAL_CEL_REGISTER_AFTER976_REVIEW.md)
- [Current explosion for-loop and guard recovery](MAIN_EXPLOSION_NATURAL_FOR_AND_GUARDS_AFTER997_REVIEW.md)
- [Current Hitbox combined early guard](MAIN_HITBOX_NATURAL_COMBINED_GUARDS_AFTER998_REVIEW.md)
- [Earlier nine-BOSS cadence integration](MAIN_NINE_BOSS_NATURAL_CADENCE_PREDICATES_AFTER993_REVIEW.md)
- [Earlier eight-major-BOSS frame-clock integration](MAIN_EIGHT_BOSS_NATURAL_GLOBAL_FRAME_PREFIX_INTEGRATION_AFTER988_REVIEW.md)
- [Earlier Reimu prefix loops and cloud byte wrap](MAIN_REIMU_BOSS_NATURAL_PREFIX_AND_CLOUD_BYTE_AFTER986_REVIEW.md)
- [Earlier Hitbox split early guard clauses](MAIN_HITBOX_NATURAL_EARLY_GUARDS_AFTER986_REVIEW.md)
- [Earlier HitCircle lifetime and render for loops](MAIN_HITCIRCLE_NATURAL_LIFETIME_AND_RENDER_FOR_AFTER985_REVIEW.md)
- [Earlier Mima spread-angle assignments](MAIN_MIMA_BOSS_NATURAL_SPREAD_ANGLE_ASSIGNMENTS_AFTER984_REVIEW.md)
- [Earlier Reimu orbit and intro loops](MAIN_REIMU_BOSS_NATURAL_ORBIT_AND_INTRO_LOOPS_AFTER982_REVIEW.md)
- [Earlier Yumemi rain-loop prefix increment](MAIN_YUMEMI_BOSS_NATURAL_RAIN_INCREMENT_AFTER980_REVIEW.md)
- [Earlier Mima random-bomb quarter clock](MAIN_MIMA_BOSS_NATURAL_QUARTER_CLOCK_AFTER980_REVIEW.md)
- [Earlier Yumemi rain and arrival for-loop source work](MAIN_YUMEMI_BOSS_NATURAL_RAIN_AND_ARRIVAL_LOOPS_AFTER979_REVIEW.md)
- [Earlier Mima split-angle and even-frame clock source work](MAIN_MIMA_BOSS_NATURAL_SPLIT_AND_CLOCK_AFTER977_REVIEW.md)
- [Earlier Kana postfix for-loop source work](MAIN_KANA_BOSS_NATURAL_FOR_POSTFIX_AFTER976_REVIEW.md)
- [Earlier Marisa flicker and split renderer](MAIN_MARISA_BOSS_NATURAL_FLICKER_AND_SPLIT_AFTER975_REVIEW.md)
- [HitCircle cel register allocation experiments](MAIN_HITCIRCLE_NATURAL_CEL_REGISTER_AFTER976_REVIEW.md)
- [Earlier HitCircle natural spawn stores](MAIN_HITCIRCLE_NATURAL_SPAWN_AFTER931_REVIEW.md)
- [Earlier Kana staged-volley natural C++ work](MAIN_KANA_BOSS_NATURAL_STAGED_VOLLEY_AFTER974_REVIEW.md)
- [Current Chiyuri natural ring-render scaling](MAIN_CHIYURI_BOSS_NATURAL_RENDER_SCALE_AFTER973_REVIEW.md)
- [Current Chiyuri lifecycle predicates](MAIN_CHIYURI_BOSS_NATURAL_LIFECYCLE_PREDICATES_AFTER972_REVIEW.md)
- [Earlier Marisa natural ring-angle assignment](MAIN_MARISA_BOSS_NATURAL_RING_ANGLE_AND_RENDER_AFTER971_REVIEW.md)
- [Earlier Marisa BOSS template/level work](MAIN_MARISA_BOSS_TEMPLATE_AND_LEVEL_AFTER969_REVIEW.md)
- [Earlier Kotohime phase-reload native C++ work](MAIN_KOTOHIME_BOSS_NATURAL_PHASE_RELOAD_AFTER968_REVIEW.md)
- [Earlier Kana BOSS native C++ work](MAIN_KANA_BOSS_NATURAL_TEMPLATE_LEVEL_AND_RENDER_AFTER966_REVIEW.md)
- [Kana cloud SUB AL codegen finding](MAIN_KANA_CLOUD_BYTE_SUBTRACTION_AFTER967_REVIEW.md)
- [Current Fireball byte-predicate native work](MAIN_FIREBALL_NATURAL_BYTE_PREDICATES_AFTER964_REVIEW.md)
- [Current Fireball explosion-geometry native work](MAIN_FIREBALL_EXPLOSION_GEOMETRY_AFTER964_REVIEW.md)
- [Earlier Ellen radial Extra angle native work](MAIN_ELLEN_BOSS_NATURAL_EXTRA_ANGLE_AFTER964_REVIEW.md)
- [Earlier Ellen BOSS level/cadence native work](MAIN_ELLEN_BOSS_LEVEL_AND_CADENCE_AFTER962_REVIEW.md)
- [Earlier Rikako signed-angle source/native follow-up](MAIN_RIKAKO_BOSS_NATURAL_SIGNED_ANGLE_AFTER963_REVIEW.md)
- [Rikako BOSS template/level/render follow-up](MAIN_RIKAKO_BOSS_TEMPLATE_LEVEL_RENDER_AFTER961_REVIEW.md)
- [Earlier Ellen BOSS source/native follow-up](MAIN_ELLEN_BOSS_TEMPLATE_RENDER_AFTER960_REVIEW.md)
- [Earlier Chiyuri BOSS source/native follow-up](MAIN_CHIYURI_BOSS_TEMPLATE_RENDER_AFTER959_REVIEW.md)
- [Earlier Yumemi BOSS render/template work](MAIN_YUMEMI_BOSS_NATURAL_RENDER_AND_TEMPLATE_AFTER956_REVIEW.md)
- [Earlier Mima BOSS render/state work](MAIN_MIMA_BOSS_NATURAL_RENDER_AND_STATE_AFTER952_REVIEW.md)
- [Earlier Reimu cloud-angle work](MAIN_REIMU_BOSS_CLOUD_NATURAL_AFTER944_REVIEW.md)
- [Seven-object integration snapshot (historical for Marisa)](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER935_REVIEW.md)
- [Earlier five-object source/native integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER927_REVIEW.md)
- [Historical source and compiler trials through after927](RE_HANDOFF_ARCHIVE_AFTER927.md)
- [Storage policy and prior safe cleanup audits](STORAGE_HANDOFF_CURRENT.md)
- [After928 applied Git/cache storage recovery](STORAGE_HANDOFF_AFTER928.md)
- [Current MAINL Staff source/native work](MAINL_STAFF_NATURAL_CPP_AFTER942_REVIEW.md)
- [Current MAINL root controller source/native work](MAINL_ROOT_CONTROLLER_NATURAL_CPP_AFTER944_REVIEW.md)
- [MAINL original CRT/source recovery index](MAINL_WORKING_CRT_RECOVERY_INDEX.md)
- [Generated source/acceptance progress](PROGRESS.md)
