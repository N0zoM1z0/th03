# MAIN far-call group controls, 2026-10-22

Eight fresh native controls isolate a group/layout condition behind the current
MAIN call mismatch. For the measured TC4/TASM/TLINK commands, a call relaxes when
its target belongs to the first physical CODE segment of the caller's effective
code group; an ungrouped caller instead uses its own segment. The independent
read-only replay fits all 16 control calls and all 20 relevant actual MAIN calls.
This is a bounded compiler/linker observation, not a universal rule or proof of
the original physical producer.

The result explains the actual mixed link: MAIN_01 starts with PLAYFLD_TEXT,
so the three playfield converter calls relax. The other 17 targets lie in later
segments and retain far calls. Both new source ranges remain unaccepted. Their
85 differing program bytes, extra segment sites and shot relocation-order
mismatch are unchanged by these controls.

## Controlled native cases

All cases start from four tiny text inputs: a C++ caller making two genuine far
calls, two TASM providers with real `RETF` bodies, and a linker response. There
are no target inputs, retained objects, output seeds, artificial near aliases,
patched objects or generated target bytes. The controls are not executed as game
runtime tests. They use the original pinned compiler, assembler and linker.

Evidence is `.analysis/codex-main-farcall-groups-20261022-v01/`, starting from
clean `ada7c2c`. Preflight and a fresh headless MAIN database check passed. Each
native capsule passes ten preparation controls, then performs four serial native
commands with the original process, registry and writer-lock safeguards.

| Case | Carrier | Deliberate source change | SAME | CROSS |
| --- | --- | --- | --- | --- |
| 1 | FCAL246 | Cross provider omits its own group; layout names A,B | relaxed | far |
| 2 | FCAL247 | Layout object precedes caller; otherwise case 1 | relaxed | far |
| 3 | FCAL248 | Group member list becomes B,A; otherwise case 2 | relaxed | far |
| 4 | FCAL249 | Cross provider declares its group; otherwise case 3 | relaxed | far |
| 5 | FCAL250 | B segment declaration precedes A; otherwise case 3 | far | relaxed |
| 6 | FCAL251 | Cross provider declares its group; otherwise case 5 | far | relaxed |
| 7 | FCAL252 | Caller omits the group in its codeseg pragma; otherwise case 6 | far | relaxed |
| 8 | FCAL253 | Layout group contains only B; otherwise case 7 | relaxed | far |

Changing the group member list alone does not change the physical segment order.
Cases 1–4 keep A first. Declaring B first in case 5 changes the linked layout:
CROSS is at load 0, SAME at 1 and CALLER at 2. Cases 5–8 retain those exact public
addresses. Cases 7 and 8 differ only in the layout provider's group declaration;
A remains grouped in case 7 through the other object, and is ungrouped in case 8.
Their opposite call results at identical addresses isolate effective membership
rather than call distance or byte placement. The eight original source filesets
and seven single-file delta checks are preserved in the replay report.

Thus neither same-SEGDEF membership alone nor the caller's own GRPDEF declaration
alone predicts these results. FCAL226's original two-call observation remains
valid, but its same/cross-segment contrast did not isolate this condition.
The template README labels in the later private capsules describe their generic
lineage; the actual pinned sources, MAP membership and this matrix establish the
specific case 8 group containing B only.

All 32 new native commands exit zero, all eight completion receipts are true,
and every writer lock is released. Each phase retains the 90-second runtime and
15-second cleanup allowance, inside 800-second work / 900-second outer limits.
Each carrier uses one CPU/nice 10. Individual outer runs take 19.00–24.68 seconds;
maximum native RSS is 109,656 KiB and swaps are zero. Preserve every capsule,
including its actual objects, EXE/MAP, source, manifest and registry receipts.

## Read-only replay and limits

`scripts/review_th03_farcall_groups.py` checks each frozen manifest digest,
consumed input identity, native exit/cleanup/registry result and output digest.
It decodes the actual compiler object's two far calls and external OMF fixups,
then reads each real linked five-byte call window and far-return destination.
It derives segment membership and physical order from MAP contributions.
The complete control call count and matching relocation count are required.

For the actual PSTL245 MAIN link it verifies the original five successful native
phases while retaining that run's false aggregate equality receipt. It rechecks
the actual executable, distinct 20-call cohort and canonical target callees.
Only three calls relax; all destinations agree. The effective-frame classifier
matches every one of the 36 observed outcomes. This classification performs no
native call, byte rewrite, acceptance promotion or original-producer attestation.

```sh
.venv/bin/python -B scripts/review_th03_farcall_groups.py \
  --controls .analysis/codex-main-farcall-groups-20261022-v01 \
  --main-link .analysis/codex-main-state-link-20261022-v01 \
  --output .analysis/NEW_FARCALL_GROUP_REVIEW.json
```

`group-review-v03.json` is the final replay including independent compiler-call
and fixup checks. Earlier v01/v02 reports are retained. Six focused tests cover
physical versus input order, unchanged-address membership reversal, absent or
overlapping ownership, signed near displacement, far-pointer decoding, malformed
call windows and zero-length MAP contributions.

`composition-intake.py` / `composition-intake-v01.json` also bind the current
20 MAIN_01 contributions to their actual objects. The root still supplies three
CODE spans totaling 8,772 bytes (3,050 + 5,058 + 664). Every non-root contribution
in this group has zero private DATA/BSS. The root's full 25,270-byte non-CODE
allocation belongs to the larger mixed root and must remain separately owned;
it is not a new group denominator. The original one-byte inter-contribution gap
and all existing addresses remain part of the composition review.

Next use this evidence to review a coherent source/physical composition that
preserves all current CODE and DATA/BSS addresses and literal relocation order.
Simply changing caller group spelling does not resolve the measured condition;
case 7 demonstrates that limitation. The 21,010-byte MAIN_01 span is still a
geometry hypothesis, not proved original authored TU ownership. Any composition
must use real native producers and preserve ABI; raw byte equality, behavior,
independent cold rounds and the full Oracle set remain open. Exact counters and
the unknown whole-authored denominator are unchanged.

## Verification

The final 36-call replay, six focused tests, tracking and whitespace checks pass.
Full CI passes 2,329 tests in 350.786 seconds with two existing skips, all four
database attestations and Oracle/toolchain checks. `ci-v01.log`, `ci-v01.exit` and
`ci-v01-resources.txt` record exit zero, outer time 8:02.09, peak RSS 666,240 KiB,
one CPU/nice 10, 768 MiB Java heap cap and zero swaps. All owned native jobs and
CI are terminal. Original proof files and registry snapshots remain retained;
this compiler observation does not change product source or acceptance ledgers.
