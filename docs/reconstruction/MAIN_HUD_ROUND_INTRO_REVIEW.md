# MAIN complete HUD round-introduction owner — exact

Scope: Original Japanese TH03 MAIN target load-image 0x0BB12..0x0C0D8,
PLAYER_M_TEXT / MAIN_01, original MAP 096E:2432..29F8.
The complete owner has **1478 CODE bytes and four complete functions**,
including both large animation/gameplay functions, not just helper leaves.

| Original body | MAP start | Bytes | Maintained source | ABI |
| --- | --- | ---: | --- | --- |
| hud_start_anim_update | 096E:2432 | 688 | src/main/hud/start_anim.cpp | near, RET |
| hud_start_sprite_strip_put | 096E:26E2 | 104 | src/main/hud/start_lowlevel.asm | near Pascal, RET 8 |
| hud_start_particle_pixel_put | 096E:274A | 51 | src/main/hud/start_lowlevel.asm | near Pascal, RET 4 |
| hud_start_anim_render | 096E:277D | 635 | src/main/hud/start_render.cpp | near, RET |

The 688-byte update includes 16-column intro animation, setup for
64+64 randomized particles, polar movement, off-playfield clipping and
phase shutdown. The 635-byte renderer has dual-screen Story/versus
sprites, GRCG output and 128-particle dot effects. The two 104/51-byte
hardware helpers are whole symbolic TASM routines, not frozen game-byte
carriers. Both natural Turbo C++ 4.02 functions have independent complete
instruction-shape, function-size and ABI probes:

    python3 scripts/probe_th03_main_hud_start_cpp.py --run-id gpt-web-hud-intro-shape-v10-20261008
    python3 scripts/probe_th03_main_hud_render_cpp.py --run-id gpt-web-hud-render-shape-v07-20261008

The original far Pascal IRAND ABI and the near Pascal device-helper
X/Y argument order were corroborated against the original instructions.

## Full physical producer, OMF and negative controls

The initial three-object attempt recreated every original HUD byte, the
exact physical MAP contributions and all 20 relocation sites, but
**failed** the unchanged ordered-MZ comparison. The original TASM puts
HUD relocation 874 before 565, 532, 413, 395, 320 and 302, then the
renderer tail locations in descending order. Three separate objects and
a naive single TASM assembly did not reproduce that historical order.
These c03–c11 were rejected compiler/link experiments. Following the
guarded owner-authorized analysis cleanup, some **unreferenced duplicate
cold worktrees/receipts were pruned**; the successful complete c12 and
latest default receipts and the maintained negative-control tests remain.
Do not assume every old c03–c11 intermediate tree is still present.

The maintained source-to-OMF recipe in scripts/lib/hud_tc4_bridge.py
now regenerates the entire physical owner in **each fresh cold build**:

1. Pinned TC4J compiles both natural C++ functions to independent -S
   assembler sources. No checked-in generated .asm snapshot is used.
2. Compiler-produced bodies are stitched with the full 155-byte
   maintained symbolic TASM hardware helpers in their original
   four-function order. Compiler-private branch labels are separated
   without rewriting the instructions or external symbol targets.
3. Pinned TASM50 assembles one physical PLAYER_M_TEXT object. It emits
   exactly two LEDATA/FIXUPP records of 1007 and 471 CODE bytes.
4. A fail-closed calibration reverses only 87 and 57 independent FIXUPP
   descriptors inside those records. Their location fields, target and
   frame methods, non-FIXUPP OMF records, source CODE bytes and byte
   counts do not change. OMF checksums are regenerated and validated;
   unknown record dialects abort instead of being guessed.

Raw **native** and **calibrated** TASM OMF SHA-256 digests for both cold
builds remain independently recorded in the replay receipt. They
are different; this is not a claim that the unmodified TASM object
already had the historical FIXUPP order. The negative controls are in
tests/test_hud_tc4_bridge.py. Original exact raw-byte, physical MAP,
ordered MZ and DOS comparisons were not weakened.

The previous score_add bounded-include MAP covered the original frozen
carrier from 096E:2432 to 096E:3FF4. After physical HUD replacement,
the residual carrier contribution is exactly 096E:29F8..3FF4
(size 15FC); score_add itself remains unmoved at 096E:3ED0.
Historical particle history storage, its destination-X word alias,
phase pointer and resident globals remain at their original DGROUP
addresses with no duplicated private BSS allocation. Physical DATA/BSS
compiler-producer attribution is still open.

The successful candidate two-round receipt is:

    .analysis/th03-main-exact/gpt-web-hud-natural-stitch-link-c12-20261008/receipt.json

This archived candidate manifest is now merged into the default manifest.
The first no-candidate two-round default replay passed:

    python3 scripts/replay_th03_main_exact_units.py --run-id gpt-web-hud-main-default-p01-20261008

Receipt:

    .analysis/th03-main-exact/gpt-web-hud-main-default-p01-20261008/receipt.json

Both full cold rounds match all 1478 HUD raw linked bytes with
**zero differences**, one MAP contribution at 096E:2432 size 05C6,
all **20 ordered MZ relocation sites**, all previously exact owners,
20 product outputs, 391 game objects, 457 generated OMF objects and
DOS behavior. This extends the scoped reviewed MAIN aggregate to
**334 exact functions / 52199 function bytes / 53122 owned bytes**,
**74 CODE extents / 67 maintained semantic source owners**.

The live target-first frontier now excludes the exact HUD/Hyper owners:
Marisa charge/hyper/hitbox prefix (1958 B, 30 relocations) and P_SHOT
producer prefix (173 B, 12 relocations) remain **unreviewed**.

The result is scoped CODE exactness, not full game source closure,
independently pristine original provenance, physical historical
DATA/BSS origin, exact unmodified TASM OMF, or Factory Truth Kernel
acceptance. OP, MAINL, ZUN still require independent mapping.

## Final post-ledger acceptance and CI limitation

    python3 scripts/replay_th03_main_exact_units.py --run-id gpt-web-hud-main-default-final-p02-20261008

Receipt:
.analysis/th03-main-exact/gpt-web-hud-main-default-final-p02-20261008/receipt.json

The final two serial cold links were run after promotion to all nine
exact evidence records and four authored-function/boundary ledger rows,
with strict original raw CODE, MAP, **ordered** MZ relocations, product
vector and DOS behavior retained. Result: **PASS**, 334 functions,
52199 function bytes and 53122 owned bytes.

Full CI was attempted (643 tests, 125 errors importing missing host
Python unicorn, 167 skips); log:
.analysis/th03-hud-ci-final-20261008.log.
Full CI does not pass on the current Factory host. All available
post-unittest CI controls pass separately, including Ghidra and
negative Oracle controls; log:
.analysis/th03-hud-postgates-final-20261008.log.
