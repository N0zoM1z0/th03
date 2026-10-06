# MAINL interpreter-loop CPU diagnostics

The complete 315-byte `cutscene_animate` body executes on selected synthetic
scripts through the actual snapshot, parameter, `script_op`, cursor, restore
and free bodies. Target and both cached images agree on ninety terminal cases
and three explicitly nonterminal budget observations. This adds runtime-model
evidence to the existing cutscene candidate; it does not accept source or exact
bytes, all command branches or the physical graphics/input/timing devices.

```sh
python3 scripts/review_th03_mainl_animate.py --output .analysis/NEW_ANIMATE_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_animate_review.py -v
```

Receipt: `.analysis/sol-mainl-animate-review-20261006.json`. The prior box
receipt is SHA-256 pinned; all inherited cutscene inputs are checked before and
after execution. Canonical Japanese MAINL is separately read through its target
manifest. Three additional complete frozen headers (`th03/hardware/input.h`,
`th01/hardware/grppsafx.h`, `th02/hardware/frmdelay.h`) bind byte-identically to
both cached trees. Their declarations/constants support this scope, without
granting whole-header dependency or compiler acceptance. Ghidra headless-usage
still fails; no database observation is used.

## Root execution and explicit substitutes

The relocated images use load segment 2000, CS=295F, DS=2E3F, SS=4000. Actual
root instructions initialize cursor 80/320, interval 1, color 0F, weight 20,
zero the speedup byte and allocate/snapshot the text box. They run the entire
interpreter loop and normal cleanup. All input sense, ASCII tolower, font,
frame delay, input wait, allocation and free calls are explicit models.
Allocation supplies segment 6000; free returns AX=FFFF/CF=1 without DOS effects.
Other model register effects are controlled and distinct from the real ABI.

Input sense supplies a constructed sequence of 16-bit words at DS:1D0C; the
last value repeats once the sequence ends. Frame and input waits record their
word arguments and return immediately. Actual held-key detection, joystick,
interrupts, VSync duration and wait termination are not executed or proved.

The four VRAM pointers address the same flat 32-KiB B/R/G/E regions used by
the box review. A6 byte writes are logged; physical page banks are unmodeled.
The font model captures its actual five-word far-call arguments, including
the three bytes at the supplied string pointer, and writes a synthetic marker
into one cell per flat plane. It does not emulate glyph shapes, font ROM,
effects, string traversal or hardware. Normal exit restores all four entire
regions to their original patterns, proving cleanup over these constructed
markers rather than rendered pixels or two real pages.

Every ordered snapshot/restore word access, final rectangle/outside bytes,
script pointer, near cleanup and BP/SI/DI preservation is checked. A6 order
is checked through each pair of font calls and each full-box dual restore.
Unrecognized ports/imports, interrupts and segment aliases fail. Callback
errors leave the FFI boundary before raising. The default terminal budget is
five million instructions; budget exhaustion is not a terminal return.

## Thirty terminal cases per image

| Cases | Observed behavior |
| --- | --- |
| Empty explicit STOP | `\$` returns through actual box restore/free; no font/delay call |
| NUL, space, tab, CR, LF before AB | Each is skipped; input is sensed again for every skipped byte |
| A followed by NUL or backslash | Both bytes are consumed as one ordinary pair without validating the second byte |
| Script at offset FFFC | `AB\$` wraps the offset to zero, leaving segment 5000 unchanged |
| CANCEL followed by no input | Fast-forward is recomputed, so release resumes the normal delay |
| Mixed key/no-key/CANCEL | Only a non-CANCEL, nonzero-input glyph advances the speedup byte |
| Inputs 0/1/20/2000/1000/3000 | Zero delays every glyph; nonzero without CANCEL accelerates; CANCEL suppresses text delays |
| Intervals 0/1/2/3/4/999 with zero/held input | Zero-input passes the exact interval, including zero; held input uses signed division by three, with odd-cycle one-frame fallback when the quotient is zero |
| Color 260 and weights 1/3/9/0 | Color truncates to 4; effect bits become 10/30/unchanged-30/00; no font-effect correctness is inferred |
| 110 glyphs, no input | One full box waits with argument zero and restores twice; final cursor is 112/320 |
| 257 glyphs, held input | Two full-box waits/restores; 128 one-frame requests; byte speedup counter wraps to 1; final cursor is 320/336 |
| 110 glyphs, CANCEL | Full-box wait and text delays are skipped; ordered restores still execute |

The actual byte speedup local at SS:FFEC is checked against the count of
nonzero, non-CANCEL glyph inputs. No-input glyphs and CANCEL glyphs leave it
unchanged, and full-box reset does not reset it. This distinction matters when
keys change partway through a text run. The target's opcode `99h` before IDIV
is CWD in this 16-bit execution, despite Capstone's CDQ display.

The font calls pass bytes at DS:0902 and its trailing zero at 0904. Actual root
code writes both consumed bytes, selects page 1, passes color OR effect, then
selects page 0 and repeats. Near script advancement changes only its word
offset. STOP is AL=FF from the actual `$` command; the interpreter then calls
box restore once and free, clears the backup pointer and returns near.

## Missing STOP is explicitly nonterminal

A separate constructed segment contains `AB` followed by zero-filled memory,
without `\$`. After 500000 instructions each image remains in the loop:
31174 input calls/script byte reads, final script offset 31174, segment 5000,
two font calls and a still-live `6000:0000` backup. There is no free or return.
NUL is classified by the actual target ctype table as control and skipped.
This is a bounded nontermination observation for the constructed segment, not
a proof about all malformed scripts, real allocation boundaries or watchdogs.

Seven synthetic controls reject budget-as-return, return-as-nonterminal,
stale return sentinels, model-requested delay termination, callback errors,
aliased imports and invalid constructed input words. All other opcode paths,
picture/EGC and font/input/timing implementations, assets/data/BSS ownership,
natural PI entry producer, cold maintained build and packed-file Oracles remain
open. The whole cutscene still has its three raw PI call-operand differences.
