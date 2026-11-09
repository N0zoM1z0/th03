# TH03 MAIN — Mima BOSS: natural template and active-render control (af1105d)

The full physical `ba_mima` Turbo C++ 4.02 owner retains the original four
attack families, rendering, 16-bit clocks, sprite masks and two-player state.
The original shared BOSS template is now addressed with normal array indexing
and explicit `player_id != 0`. The main renderer's owner check is an early
return instead of an enclosing block. The word-sized frame advances with
`++boss_frame`, and random-bomb warning center coordinates are `const int`
locals, initialized after the inactive-warning exit.

Separate successful stages were `af1105a` (template), `af1105b` (complete
render dispatcher guard) and final `af1105d` (frame and bomb coordinates).
The final two independent native TC4/TLINK rounds reproduce the entire
1,922-byte original CODE and all 277 native relocation fields, nine PUBLICs,
complete Japanese MAIN loaded image and 1,553 ordered MZ relocations.
Original source/ABI and attack/RNG order remain bound to
`.analysis/work/exatt-layout-af1105d/report.json`.

Two natural source alternatives were independently falsified by the original
compiler: `af1105c` replaced the mode-5 `goto render_mode_2` with a combined
animated-mode condition, and `af1105e` replaced the trail's two assignment
branches with a ternary. Both changed CODE and were restored. Do not infer
that one C++ expression shape preserves TC4 register and control-flow layout.
This is local native source improvement, not canonical Factory credit.
