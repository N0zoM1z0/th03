# MAIN entry source and actual link — 2026-10-23

`src/main/core/entry.cpp` recovers the complete 146-byte far C entry at load
96E6..9778. It initializes the game, resolves resident state, loads the gaiji
font, starts the stage/background, runs rounds, transfers the round counter to
the resident random seed, and dispatches to OP or MAINL. Existing strings and
callback storage remain external views. The original source spelling is unknown.

## Native result

Evidence is `.analysis/main-resume-20261023/`. Preflight and the fresh headless
MAIN database attestation pass. The Japanese target remains locally attested.

The first standalone TC4J compile (MENT263) emits 146 CODE bytes and no DATA/BSS.
The first mixed-link attempt (MENT264) fails on the historical `GameExecl`
symbol spelling: the compiler's Pascal spelling differs from that assembly
label. The next candidate declares the genuine far Pascal interface as
`MAIN_EXEC`, exported directly on the existing B454 body ending RETF 4.
There is no wrapper, alternate body or changed stack convention.

MENT266 performs six successful native commands: entry/state/shot compilation,
root/score assembly, and one actual MAIN link with 83 declared context objects.
Each phase retains its process, registry and sole-writer checks. Peak RSS is
111,220 KiB, one CPU/nice 10, zero swaps. The original aggregate receipt remains
**false** because its strict ordered-relocation check fails; it is not rewritten.

The maintained staging script removes exactly the original far entry, inserts
its compiler object immediately before the root, and exports nine views of
existing code/storage. All other MAP contributions, every outside program byte,
and all 87 accepted scopes / 66,843 bytes retain their prior results. The entry
has 23 genuine OMF fixups; all 83 remaining non-fixup object bytes equal target.

The actual linked entry has **141/146 raw bytes equal**. Its only difference is
9770..9775: a real far call to B454 versus target NOP/PUSH CS/near CALL to the
same destination. Outside-entry relocation membership is unchanged, but its
literal global order differs. These are unresolved physical-producer/link-order
questions. Existing state/shot mismatches remain unchanged. No exact, cold-build
or whole-game promotion follows from this mixed incremental link.

## Bounded behavior

The replay executes both real entry byte streams in Unicorn for 293 scenarios:
all return-byte values, resident lookup failure, repeated continuation, BGM
selection and story-stage wraparound. Every entry byte is executed. It checks
foreign call order/arguments, stack cleanup, callee-save registers, resident
seed/ending selection, ordered data writes and memory changes across DGROUP,
the resident record and the entry stack window. Five mutations of the resident
branch, palette tone, continuation test, OP filename and story increment fail.

Foreign callees are bounded stubs. This does not execute the game loop or devices.
One unrelated initial DGROUP byte (05A5) already differs in the retained mixed
baseline; it stays unchanged and is not normalized into byte equality. Unicorn
reports far-CALL stack writes differently from PUSH CS/near CALL, so the replay
compares final stack effects and checks all write bounds, rather than claiming
identical stack-write hook events. Full callees/runtime Oracles remain open.

```sh
.venv/bin/python -B scripts/review_th03_main_entry.py \
  --output .analysis/NEW_MAIN_ENTRY_REVIEW.json
```

`entry-review-v03.json` checks original native inputs/exits, installed-source
identity, all current layout assertions and bounded runtime/negative controls.
The source-only stager can reproduce the root/response consumed by MENT266:

```sh
python3 scripts/stage_th03_main_entry.py \
  --baseline .analysis/codex-main-state-link-20261022-v01/maintained-stage-v01 \
  --output .analysis/NEW_MAIN_ENTRY_STAGE
```

Six focused tests pass. Evidence and knowledge ledgers record this source/link
observation separately from bounded runtime. The OP33 and MAINL145 publications
are refreshed only for evidence/knowledge ledger bindings; owner scope is unchanged.

Full CI passes 2,335 tests in 327.075 seconds (two existing skips), target and
Oracle/toolchain checks and all four database attestations. Total wall time
7:54.19; peak RSS660,052 KiB, CPU19/nice10, zero swaps. `ci.log` and
`ci-resources.txt` retain the result. `entry-baseline-audit.json` separately
checks all five original PSTL245 native phases and their retained output hashes.
Unused publication candidates and regenerated Python caches were removed;
current native proof trees and installed publication inputs remain retained.
