# MAIN state and shot source-link checkpoint, 2026-10-22

The maintained five-function state candidate and five-function shot candidate
now participate together in an actual native MAIN link. PSTL245 freshly
compiles both C++ objects, assembles the root and score objects, and links
against 83 explicitly retained context objects. All five native commands exit
zero. The resulting two source ranges remain 1,716 bytes at `DA43..E0F7` and
1,497 bytes at `E266..E83F`.

Every one of the 87 previously accepted scopes / 66,843 bytes retains complete
raw target equality and literal relocation order. Every other nonzero MAP
contribution, existing public symbol, and program byte outside the two new
ranges is unchanged. The new ranges are **not exact**: 17 unrelaxed far calls
account for all 85 program-byte differences against the retained mixed baseline.
No whole-program, behavior, cold-build or new acceptance claim is made.

## Reproducible source staging

`scripts/stage_th03_main_playerstate.py` composes the existing hash-guarded
shot staging with the complete state transfer. It removes exactly five near
procedures, replaces the six outside state caller references, exports aliases
for the two existing lose-animation bodies, and inserts the new state object
before the retained `main_010.obj`. The shot and score transformations retain
their existing original-source hash guards.

The release-counter symbol is a view within the existing BSS reserve:

| Item | DGROUP offset | Storage |
| --- | --- | ---: |
| `_collmap_pid` | 4B9A | existing byte |
| unchanged reserve | 4B9B | 1 byte |
| `_shot_release_frames` | 4B9C | 2 bytes |
| unchanged reserve | 4B9E | 2 bytes |
| `_collmap` | 4BA0 | existing array |

The original five reserved bytes become 1+2+2 bytes. The native root's BSS and
all other segment sizes are unchanged; only its complete MAIN_010 and P_SHOT
CODE contributions disappear. The linker confirms the new counter's address,
all previous public addresses, and the existing defeated-player byte at DS:38DD.
Both inferred animation names resolve to the real C0D8 and C248 entries, and
`player_shots_add` resolves to the actual E737 body. No wrapper, padding,
new counter allocation or ABI substitute is introduced.

Replay staging with a fresh ignored output directory:

```sh
python3 scripts/stage_th03_main_playerstate.py \
  --baseline .analysis/th03-main-exact/gpt-dots-yumemi-charge-default-cold-v01/round1/source \
  --output .analysis/NEW_MAIN_STATE_STAGE
```

`maintained-stage-equality.json` proves all three maintained staged outputs
(root, score, response) equal the files consumed by the original native run.
Nine focused tests cover provenance, complete procedure ownership, outside
callers, hidden allocations, reserve size, alias collisions and object order.

## Native evidence and failure history

Evidence is retained under `.analysis/codex-main-state-link-20261022-v01/`.
The work began clean at `3bf8f30`, with preflight and a fresh headless MAIN
database check passing. The canonical Japanese target and its
candidate-local-attested provenance are unchanged.

PSTL244 / `native-v01` stops before any native process creation: the inherited
800-second work budget cannot satisfy five guarded phase reserves. That
zero-invocation failed receipt remains unchanged. PSTL245 / `native-v02` uses
1,000 seconds of work allowance inside 1,100 seconds externally; every native
phase still has its original 90-second runtime and 15-second cleanup limit.
Both packages pass 13 preparation controls. The native supervisor, process
inventory, poison handling, registry and writer-lock code are unchanged.

PSTL245 stages 340 explicitly pinned files, including 83 context objects.
Its C++ closure has 81 files including vendor headers and 125 literal include
edges; assembler closure has 179 files and 177 edges. Four project objects and
the EXE/MAP are freshly produced. The state object is byte-identical to PSTA243's
original source-only producer. This is a mixed incremental link, not a cold
whole-source build. Native work takes 27.51 seconds, peak RSS 110,628 KiB,
one CPU/nice 10, zero swaps.

The original `native-v02-output/completion.json` is **false**, with five native
invocations and a released lock: the aggregate correctly rejects complete
program equality. `object-verification.json` preserves all individual pass/fail
checks. `post-audit.py` / `post-diagnostic-audit-v01.json` separately recheck all
original inputs and tracked source bytes, staged inputs/outputs, tool membership
and mtimes, final registry state, process cleanup and released lock. They do not
rewrite the failed receipt or perform another native call. The newly authored
stage script and tests are explicitly outside that historical manifest.

## Remaining byte and relocation differences

`diagnose.py` / `call-diagnosis-v01.json` compare the actual linked EXE with the
canonical target and retained baseline. All 17 far-call pointers resolve to the
same load address as the target's relaxed `NOP; PUSH CS; CALL near` sequence.
The candidate bytes are not changed or normalized into an acceptance artifact.

| Source range | Unrelaxed calls | Differing bytes | Extra segment sites | Remaining literal order |
| --- | ---: | ---: | ---: | --- |
| State, DA43..E0F7 | 4 | 20 | 4 | 7 sites match target |
| Shot, E266..E83F | 13 | 65 | 13 | 26 sites have equal membership, unequal order |

State's four unresolved calls are the player hit circle, half-heart HUD,
bomb HUD and bomb explosion APIs. Three calls to the playfield-X converter
**do** relax in the actual link, even though its provider uses PLAYFLD_TEXT and
the caller uses MAIN_010_TEXT. Therefore same-SEGDEF membership is not a
necessary condition for every observed relaxation. FCAL226 remains evidence
for its specific same/cross-segment controls, not a universal linker rule.
The 21,010-byte original physical-producer proposal remains a hypothesis.

`metadata-intake.py` / `metadata-intake-v01.json` pin the actual state, playfield,
HUD and earlier calibration-cross objects. Both real playfield and HUD providers
have PUBDEF group index zero; the calibration-cross provider uses group index
one. That single field alone therefore cannot explain the two real outcomes.
The metadata snapshot includes SEGDEF, GRPDEF, publics and non-dependency
comments; no object is modified. A useful next control varies the provider's
explicit group membership and whether its segment is first in the caller's
code group, while keeping real far-return bodies and source-only producers.

Next distinguish the relevant group/frame/public metadata and physical producer
composition with a bounded native control, then reproduce the real linked call
bytes and literal relocation stream. Do not rename segments or patch object
records solely to manufacture a match. Full ownership/ABI/layout, behavior,
independent cold rounds and the complete Oracle set remain required. No ledger
or exact counter changes in this checkpoint.

## Verification

Nine focused staging tests, tracking validation and whitespace checks pass.
Full CI passes 2,323 tests in 300.145 seconds with two existing skips, all four
database attestations and Oracle/toolchain checks. `ci-v01.log`, `ci-v01.exit`
and `ci-v01-resources.txt` record exit zero, outer time 7:18.81, peak RSS
665,016 KiB, one CPU/nice 10, 768 MiB Java heap cap and zero swaps. All owned
jobs are terminal. The native equality diagnostic remains failed as described
above; green repository CI does not promote either new range to exact.
