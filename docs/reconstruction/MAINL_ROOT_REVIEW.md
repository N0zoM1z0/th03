# Complete MAINL root CODE candidate review

The frozen `th03_mainl.asm` contribution to CUTSCENE_TEXT has nine complete
procedures (2470 bytes / 810 instructions) and an 18-byte switch table. They
partition all 2488 bytes at decoded `095F:0186..0B3D`. This covers the win
animation, story dispatch, next-stage setup, continue menu and main entry,
including the handwritten `cdg_free_all` include. The separate compiled
cutscene TU begins at 0B3E and receives no duplicate credit here.

```sh
python3 scripts/review_th03_mainl_root.py --output .analysis/NEW_ROOT_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_root_review.py -v
```

Receipt: `.analysis/sol-mainl-root-review-20261006.json`. It inherits the pinned
staff/snow/cutscene lineage, checks canonical Japanese MAINL identity and
decoded/cached image hashes, and associates nineteen consulted frozen
providers with both old compiler trees. Assembly differs only by LF-to-CRLF
conversion; other providers are byte-identical. Source procedure bodies, the
handwritten include, relevant filename/pointer declarations, resident layout,
input and character constants were read. Cached source associations do not
establish a fresh compiler or maintained source. Ghidra headless-usage fails
before database attestation; no database observations are used.

| Decoded entry | Body | Bytes | Return |
| --- | --- | ---: | --- |
| 0186 | Free all CDG slots | 23 | near |
| 019D | Win animation | 250 | near |
| 0297 | Story dispatch / opponent update | 133 | near |
| 031C | Load next-stage presentation | 288 | near |
| 043C | Present next stage and load sound | 627 | near |
| 06C1 | Load shot pair, mutate caller filename | 111 | near RET 6 |
| 0730 | Construct shot filename on stack | 93 | near RET 2 |
| 078D | Main orchestration | 528 | far, caller cleanup |
| 099D | Continue menu | 417 | near |

All direct branches resolve to instruction boundaries within their body;
near calls resolve to complete root entries or declared external interfaces.
Every return, including interior early returns, has the reviewed cleanup.
The indirect jump at 05A2 addresses nine words at 06AF, selecting five actual
instruction entries in the enemy-file paths. The complete table is checked
separately from CODE. No disassembler function discovery or comment supplies
an independent Oracle.

## Raw and relocation failures

Both cached products retain ten raw call-operand differences at
0412/0436/0457/0573/05DB/0695/06E1/0719/0B07/0B11. Actual root callers establish
PI palette/put/interlace target entries `0C7E:052A/054F/05D7`; cached callers
use `0529/054E/05D6`. These are separate declared interfaces in the probe.
The prior palette/put body observations remain separate; this review does
not execute or establish ownership of the interlace helper. No byte search,
entry normalization, padding or operand repair is used for equality.

Five bodies have cached raw equality: free-all, win animation, dispatch,
shot-load and main (1027 bytes). The remaining four bodies retain the ten
differences. Original ordered relocations also fail over the whole contribution
(114 sites), with different interleaving. Free-all's one site agrees; dispatch
and shot-load have none. Win animation / next-load / next-put / shot-pair /
main / continue retain order failures over 22/8/32/6/25/20 sites respectively.
Per-body raw hashes and complete original lists are retained in the receipt.
Raw identity or CPU agreement does not close these independent gates.

## CPU and interface scope

All nine root bodies execute actual decoded instructions in target and both
cached images. External libraries, CDG/PI/font rendering, file I/O, palette,
sound, configuration, initialization/exit, win-loading/text, registration,
ending/staff and cutscene interpreter calls are explicit models. Clock updates
are injected at the next-stage polling instruction. The probe checks segment
aliases, Pascal cleanup, actual near/far returns, callee-saved state and every
callback error. It uses no memory-read hook; actual far RET preserves the main
caller's argument words. Modeled `execl` distinguishes a stopped handoff from
a returning failure. Neither case is a real process launch.

Per image there are 455 observation records and 456 top-level invocations
(the accumulated filename case calls twice): 452 terminal returns, three
nonterminal budgets and one modeled exec handoff. Across three images this is
1368 invocations: 1356 terminal, nine budgets, three handoffs. Eight adversarial
controls reject branch operands, neighboring bodies, wrong interior returns,
unknown calls/switch expressions, callback failures, stale terminal state,
incorrect cleanup and physically equivalent interface/terminal segment aliases.

The matrix contains 384 dispatch, fourteen shot, five next-load plus one
two-call accumulation, twelve next-put, five clock, twenty continue, one
continue-budget, ten complete main, one missing-config and one modeled exec
handoff records, plus one free-all record per image. Root calls use constructed
resident state; main cases supply nine opponent bytes plus a deliberate stage9
sentinel outside that array. These are bounded interface contracts, without
loaded assets, physical devices, real interrupt schedules or whole-game runtime.

## Retained observed behavior

Free-all requests slots 0..31 in order, without testing free results. Win
animation clears both pages, requests CDG slots 0..4 then 6/5, changes tone,
frees all slots and waits for any interface input. Its foreign graphics, sound
measure and timing operations remain request models.

Dispatch returns 1 outside story mode or when winner is nonzero. Otherwise it
reads `story_opponents[story_stage]` before testing stages 7/8/9, updates the
second resident character and returns 3/4/5 for those stages. No array bounds
guard precedes the read. Stage9 reads the following unused byte; larger stages
read farther resident/adjacent memory. Other stages return 0 and clamp character
IDs >=7 to Reimu. Optional value0 undergoes signed `(0-1)/2` truncation to zero
in this check, so it is not rejected. The matrix compares all 512 constructed
resident bytes, preserving alias effects when the selected address is itself
another field. These invalid-state cases do not establish normal reachability.

Next-load uses byte palette packing for CDG requests and modifies the fifth
byte of `stnx1.pi`: non-story adds4, character7 adds2, character8 adds1, and
story stage6 adds3; otherwise it loads a separate stage-number CDG. Two
non-story calls request `stnx5.pi` then `stnx9.pi`. Load returns are ignored;
the model's zero result creates no real resource or metadata.

Shot-load copies all twelve template bytes onto the stack, subtracts1 from
the resident optional character and adds decimal quotient/remainder to its
first two filename bytes without validation. Shot-pair then writes `ex` into
bytes2/3 of the caller's far filename between the two PI loads. Constructed
optional0 produces `0/16.pi` then `0/ex.pi`; optional255 produces `I416.pi`
then `I4ex.pi`. Coordinates are PID*320 with top200/208. The source template
remains unchanged because this caller supplies its local stack copy; direct
callers of shot-pair still require writable far storage. Actual libraries,
files and interlace pixels are not proved.

Next-put formats the mutable global `00mm.m` prefix using the opponent's
character ID, without restoration; stage6 instead requests `dec.m`. Its clock
gate busy-polls until unsigned count>32 before reading input, then leaves on
count>96 or any nonzero input. Counts33/96 need one constructed input call;
count97 needs none. A fixed count32 or absent clock remains nonterminal even
with held input. The separate clock interface is not a real interrupt source.

Continue first zeroes all sixteen recent-score digits, including the no-credit
early return. With credits it adds the count to a mutable ASCII digit, starts
with Yes selected and toggles once per LEFT/RIGHT press until released.
OK/SHOT is tested before CANCEL. Yes decrements credit and the digit; No or
Cancel does not. Every nonzero-credit terminal branch, including cancellation,
decrements story stage (0 wraps to255), sets lives2, fades and requests the
game-over picture. No-credit early return performs none of those later effects.
The no-input budget retains the menu loop. Repeated calls can accumulate the
mutable digit; only the tested single-call credit vectors are asserted here.

Main calls the configuration interface first and returns far when it reports
zero. A score-menu request calls registration, exits and requests `op`; if
the modeled exec returns, it continues through the remaining root code.
The constructed story-stage5 case therefore requests `op` then `main`.
Stage0 prepares the next stage directly; stage8 skips win animation; stage7/8
request the cutscene interfaces; stage9 requests staff then the win/continue
path. Accepted continue returns to MAIN, while no credits or cancellation
requests ending then OP. Non-story win returns to OP. Sound-mode selection
is conditional on resident BGM, and all foreign failures remain unchecked
where the actual caller has no branch. The ten root cases check these routes
and actual internal entries, without claiming CRT/startup or external-body
execution.

This adds one decoded boundary-reviewed module row, with no maintained source,
canonical stored-file offset or exact acceptance. Complete `_TEXT` libraries,
shared game dependencies, DATA/BSS/resources, cold localized producers,
original relocation/encoding ownership and DIET packaging/complete Oracles
remain open, as does the broader frozen TH03 intake.
