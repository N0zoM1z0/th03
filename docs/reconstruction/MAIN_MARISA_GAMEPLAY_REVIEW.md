# TH03 MAIN Marisa character charge/hyper/hitbox prefix — target-first review

**State: ten original logical function bodies now verified against target;
not exact, not a completed natural-source or physical DATA/BSS producer.**

This review continues the MAIN_04 dependency graph from the exact
MAIN_010 Hyper dispatcher and the exact HUD/gameplay CODE. The original
Japanese MAIN target contains a continuous 1958-byte Marisa character
prefix at load-image offsets **0x142D0..0x14A76**, segment
HITBOX_TEXT in the MAIN_04 group, starting at original 139D:0900.
The frozen root assembler contains multiple subsequent Reimu/Mima
routines in the same HITBOX_TEXT physical MAP contributor, so the
present review is a **complete logical module prefix hypothesis**, not
evidence that it was one distinct historical compiler object.

Reproduce original immutable-body boundaries and 30 MZ sites via:

    python3 scripts/review_th03_main_marisa_gameplay.py --run-id UNIQUE_ID

Pinned current receipt:

    .analysis/th03-main-marisa-gameplay/gpt-web-marisa-gameplay-target-v01-20261008.json

The script independently checks the target SHA-256, parses the original
MZ load-image, linearly decodes every instruction in all 10 functions,
requires the exact original terminal near/far RET ABI, forbids
relocations crossing function edges, confirms no gaps or overlap and
refuses overlap with the **334 previously exact** functions' CODE owners.
The ReC98 labels and provisional Ghidra pseudocode are corroboration,
not evidence that source code is reconstructed.

| Complete original function | Original load-image interval | Bytes | MZ sites | Returns |
| --- | --- | ---: | ---: | --- |
| marisa_chargeshot_state_reset | 0x142D0..0x142DF | 15 | 0 | far RETF |
| chargeshot_add_marisa | 0x142DF..0x14340 | 97 | 1 | far RETF 4 |
| marisa_hyper_14340 | 0x14340..0x143BE | 126 | 1 | far RETF |
| chargeshot_update_marisa | 0x143BE..0x14487 | 201 | 0 | far RETF (two exits) |
| chargeshot_hittest_marisa | 0x14487..0x14511 | 138 | 1 | far RETF |
| chargeshot_render_marisa | 0x14511..0x146AF | **414** | **15** | far RETF |
| gauge_pattern_marisa | 0x146AF..0x14885 | **470** | 2 | near Pascal RET 2 |
| gba_gauge_pattern_pellet_marisa | 0x14885..0x1489D | 24 | 0 | far RETF |
| gba_gauge_pattern_bullet_marisa | 0x1489D..0x148B5 | 24 | 0 | far RETF |
| marisa_bomb | 0x148B5..0x14A76 | **449** | **10** | far RETF |

These ten bodies account for all **1958 bytes / 30 original MZ
relocation entries**. An important negative control: the original
chargeshot_update_marisa contains an **early RETF at 0x14464**
inside one 201-byte routine; blindly splitting at every RETF produces
11 false functions. The near Pascal gauge_pattern_marisa uses a
two-byte caller-argument cleanup, not far cdecl.

## Recovered semantic relationships and risks

- The leading 15-byte reset clears a pair of charge status bytes.
  Marisa charge add and Hyper setup use a **50-byte per-player history
  structure**, with 12 X words from slot offset +2 and 12 Y words
  from +0x1A. The mutable pointer and two per-player frames must
  continue to alias the original historical DGROUP.
- marisa_hyper_14340 is **already called by the accepted exact native
  TC4 MAIN_010 Hyper dispatcher**; its current far external alias
  resolves into the frozen carrier. Any physical carve must replace
  that export without shifting the existing Hyper owner.
- The 201-byte charge update rolls the twelve-point history, updates
  gauge/shot-active player state, and returns early during its active
  phase. The 138-byte hittest routine touches shot/collmap structures.
- The **414-byte renderer** calls PC-98 EGC/GRCG and pattern draw
  functions; it contains fifteen original relocation sites, so full
  MAP, far ABI and FIXUPP order need review together.
- The **470-byte gauge-pattern** chooses pellet/bullet behavior from
  per-player flags, advances a vertical gauge position and frame,
  calls the existing random/math/ordinary-shot producer dependencies,
  and uses four different modulo-24 pattern branches. The original
  source has an unusual word-width near Pascal call containing a local
  byte pair; use immutable target disassembly and the original stack
  discipline rather than Ghidra type guesses.
- The **449-byte Marisa bomb function** spans multiple timed phases,
  palette/GRCG and bullet/hitbox helpers with ten relocations. It is
  required for complete gameplay, not a leaf that can be deferred.

Ghidra independently corroborates the full 201-byte update, 414-byte
renderer, 470-byte gauge pattern and 449-byte bomb graph, but its
provisional local variable recovery is not a source-of-truth ABI.
TH04/ReC98 provide hypotheses only. The existing natural
charge/gauge character sources in MAIN_09_TEXT establish useful
TC4 calling patterns, but do not prove Marisa field offsets.

## Next acceptance milestones

First, recover one complete maintainable Marisa logical source module
covering *all ten* functions, including the two large renderer/gauge
and bomb functions. Independently confirm the 50-byte historical
per-player buffers, external palette/device routines, near/far
Pascal ABI, calls into the exact Hyper dispatcher and physical segment
placement. The candidate is in the *beginning* of HITBOX_TEXT;
do not assume the later Reimu/Mima code belongs to the same original
physical producer.

Only after the complete source and producer graph exist: run the
pinned TC4 shape/ABI oracle for all ten functions, restore original
TLINK MAP and ordered MZ FIXUPP, then run **two serialized cold
builds** containing every previously exact owner and DOS probes.
Update evidence, knowledge, progress and handoff and commit with the
gpt-web: prefix **only on real progress**. This target-only logical
boundary proof does **not** add any exact function or byte credit,
nor Factory Truth Kernel acceptance.
