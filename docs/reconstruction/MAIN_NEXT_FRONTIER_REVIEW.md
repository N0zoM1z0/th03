# TH03 MAIN next gameplay owner frontier — target-first intake

Status: **five provisional, non-exact CODE intervals**. No new source owner,
function boundary, DATA/BSS owner or exact byte credit is assigned here.
The 320/320 exact MAIN count covers only the 72 already reviewed CODE
extents, not the entire game.

## Reproducible immutable target review

    python3 scripts/review_th03_main_next_frontier.py

Receipt:

    .analysis/th03-main-next-frontier/target-review-v1.json

Source of truth: original TH03 MAIN.EXE with SHA-256
f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b.

The script verifies target binding, whole bounded 16-bit linear decode,
terminal return, original MZ relocation containment and ordered sites,
and rejects overlap with every already accepted CODE extent. Old ReC98
labels and automatic Ghidra boundaries are hypotheses only.

All offsets in this table are raw MAIN load-image offsets, **not** a
synthetic zero-based owner coordinate system.

| Provisional subsystem interval | Target bytes, end exclusive | Size | Ordered MZ sites | Last instruction |
| --- | --- | ---: | ---: | --- |
| PLAYER_M HUD intro/state prefix | 0x0BB12..0x0BE5D | 843 | 6 | near RET 4 |
| PLAYER_M HUD render | 0x0BE5D..0x0C0D8 | 635 | 14 | near RET |
| MAIN_010 hyper/input dispatch | 0x0D7F0..0x0DA43 | 595 | 4 | near RET |
| HITBOX Marisa character prefix | 0x142D0..0x14A76 | 1958 | 30 | far RETF |
| P_SHOT ordinary-shot producer prefix | 0x0E266..0x0E313 | 173 | 12 | near RET |

All five intervals together contain 4204 non-overlapping target bytes,
with no overlap against the current exact manifest. Linear decode alone
does not prove internal function boundaries, complete semantic or physical
owners, historical global storage, or any compiler/binary-exact acceptance.

## Next owner priorities

1. MAIN_010 hyper dispatch. This 595-byte, ten-provisional-handler prefix
   connects the existing input, math, state and per-character gameplay code.
   Review near function-pointer ABI, player speed/shot-mode storage and
   direct boss/charge-shot calls. Ghidra did not recognize a function at
   0x1D7F0, even though target 0x0D7F0 starts with a valid BP prologue:
   the absence of an automatic function must not override raw target CODE.
   TH04 player-update code is a reference hypothesis, not inherited exactness.

2. HUD state/intro and render as a complete 1478-byte subsystem, rather
   than just leaf functions. The first interval includes a 688-byte HUD
   animation/update and two smaller routines; the adjacent 635-byte render
   function is itself large. Existing resident/HUD globals, sprite and DOS
   calls need reviewed physical ownership and ABI. Ghidra identifies
   contiguous bodies at 0x1BB12..0x1BDC1 and 0x1BE5D..0x1C0D7;
   raw boundaries still take precedence.

3. Marisa charge/hyper/hitbox prefix (1958 bytes, 30 relocations).
   This is a larger gameplay and boss/shot dependency graph. Establish its
   true logical and physical owner partitions before recovering natural
   source; do not accept automatic function names as owner evidence.

4. P_SHOT producer dependency (173 bytes, 12 relocations). It contains
   low-level graphics I/O. Review alongside the full ordinary-shot call
   graph rather than satisfying the roadmap with only small leaves.

Acceptance before any promotion: target-first complete function boundaries
and shared tails, near/far ABI, historical DATA/BSS and relocations, natural
C++ or symbolic TASM source, exact MAP, original **ordered** MZ relocations,
two serial full cold links and DOS behavior with every existing exact
owner retained. Do not weaken OMF normalization for this new frontier.
Full MAIN source closure and pristine-target origin remain unresolved.

Negative controls are in tests/test_main_next_frontier_review.py.
