# MAINL input scan after549: complete function, open product boundary

The natural assembly candidate recovers the complete 417-byte held-key scan:
115 instructions and all 42 ordered native fields. Two OBJ/EXE/MAP vectors
repeat and the independent reviewer passes this instruction scope. The whole
product candidate remains unaccepted: omitting the adjacent unowned byte moves
later code and produces 323 EXE byte differences. The active runtime root stays
after548; no acceptance publication or canonical-unit credit changes.

## Function and native ownership

Live candidate: `src/mainl/hardware/input_scan.asm`. Its far no-argument public
is `@input_reset_sense_key_held$qv`. MAINL MAP allocates it at C7E:0388,
decoded-load CB68..CD09, with RETF at CD08. The following target byte at CD09
is 90 and is explicitly outside this instruction owner.

The independent oracle is the pinned Japanese decoded executable, retaining
`candidate-local-attested` provenance. Independent pristine-dump attestation
remains unknown. The baseline OBJ is the actual reconstructed TC4 cold object
`obj/th03/input_s.obj`, not a claimed original vendor object. Its four imports,
all complete 42 field tuples and sole PUBLIC entry are preserved in order.
Both actual linked candidate bodies match the entire target function without
masking or output patches. Every instruction byte is emitted exactly once;
all direct edges close on real instruction boundaries. There are no private
DATA/BSS bytes or extra exports, and original WORD/public segment flags remain.

The candidate uses the pinned compatible JWasm profile. Ordinary source spans
preserve the actual native field chronology. Original assembler identity is
not claimed. Mutable word state remains external: js_stat[0], input_mp_p1,
input_mp_p2 and input_sp. Their surrounding storage receives no new ownership.

## Recovered behavior and source limits

The function clears exactly those four words and ORs two BIOS keyboard samples.
Arrow, numpad, letter, escape, return and space mappings retain the original
single-player / two-player combinations. BL is the real sample counter;
between samples CX counts 1,024 OUT 5Fh iterations. ES is set to zero, while
DS remains the caller DGROUP. AX/BX/CX/ES and flags retain original effects;
SI/DI/BP and the far no-argument return frame are unchanged. Physical keyboard
or timing behavior is not claimed from a host simulation.

The actual short entry transfer, including its zero displacement, remains an
ordinary JMP to the original following boundary. No invented timing explanation
is assigned to it. The candidate has no register self-assignment and no
`codestring` or hand-filled trailing NOP. Historical
`src/mainl/linked_game/input_sense.cpp` remains frozen in the accepted cold graph;
this candidate has not silently replaced it.

That historical compiler object has 418 CODE bytes, including the manually
supplied final 90. The new function has exactly 417. Native linking does not
recover that byte as automatic inter-contribution alignment. Full EXE lengths
are both 67,372, but later addresses and related fields change. Complete raw
differences remain recorded; no broad MAP normalization or one-byte masking
turns the product candidate into an exact result. The byte's source/layout
provenance is the next boundary question.

## Actual affected checks and retained outputs

The unchanged current source-only cold pair is validated, including all 1,912
staged inputs, original first-use compiler slot and 938 outputs per round.
Only one separate assembly candidate is produced per round; none of those
retained C++ objects is recompiled. Two native TLINK runs consume the actual
after548 C0 and unchanged library pair. No old after535 startup is substituted.

All six fresh raw outputs and four writer logs remain under
`mainl-input-scan-*`; consumed source/config/driver, C0/library copies and both
linker responses remain in `TH03ML/probe/af549h`. No cold replay, ancestor
runtime chain, emulator matrix, DIET run or output cleanup occurs.

Root: `.analysis/work/mainl-input-scan-build.json`, SHA-256
`fb67e160ba2f75e21e13e9252b1e96ac8959f5f45753348ae83d964bb0afde82`.
Producer/reviewer: `scripts/build_th03_mainl_input_scan_work.py` and
`scripts/review_th03_mainl_input_scan_work.py`. Independent review transcript:
`mainl-input-scan-independent-review.txt`. The existing active root remains
`.analysis/work/runtime-after548-build.json`, SHA-256
`b0bed460844c39c51a1496b312ac0b94120cfff2ccd7e202e6abdb01db9ed773`.

## Project ownership queue

`scripts/audit_th03_mainl_ownership_gaps.py` verifies all 211 published decoded
owner extents against the actual current target bytes and maps the 36 actual
project objects. It finds 905 CODE bytes across 13 contributions outside those
published scopes. These are not automatically missing functions or absent
source. The input contribution accounts for 418; four sound wrappers account
for 128, vector_far for 160 and regdata's remaining span for 68. The remaining
131 require separate table/alignment/instruction classification, including the
already identified 18-byte root switch table. BSS and initialized DATA stay
separate and do not become CODE credit.

Report: `.analysis/work/mainl-ownership-gap-audit.json`, SHA-256
`cc7c394e808e0f9d2f1c34338f6932085110f5ec344c8036438e629f7f6f6a74`.
Its `--check` path recomputes the saved diagnostic without executing native
writers or promoting any acceptance. The 417-byte candidate is not subtracted
from the published queue before publication. No whole-game denominator or
percentage is inferred.

## Other producer questions retained

af549a's TASM /ml probe does not restore C0 PUBLIC order. af549b/c preserve
setvbuf bytes and per-site attributes, but its two operand pairs still differ
with both early and late external declarations. These are not adopted changes.

An isolated candidate from the official
[Turbo C museum archive](https://altd.embarcadero.com/download/museum/tc201.zip)
is retained privately. Archive SHA-256 is
`2c87f988605ae9ed70e5fef35b9854de87e36ccdb021caec35ab2424ca4b5553`;
TCC.EXE is `19650666dcaa03e3f68efd9beeb57821ba4ed4d84c88a52b0e989bbfc97e07ba`.
Its banner reports Turbo C 2.01. Both tested register settings emit a 16-byte
abort probe, rather than the original 20, and do not establish producer identity.
It is not used for product outputs; TC4, installed CL.LIB and targets are intact.
Preflight passes after installation.

All af549a–g probes, recipes, tool provenance and preflight are preserved in
the 60-file `.analysis/work/probe/input-scan549/manifest.json`, SHA-256
`55552dda2102f468726774b427709670c844883ffce19180c34dd273e8968677`.
Existing C0 PUBLIC order and setvbuf pair gaps remain open. Displays are empty,
writers serialized, and heavy work uses one CPU at nice10.
