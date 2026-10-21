# ZUN launcher source and decoded-component review

The maintained candidate contains three natural assembler translation units:
`src/zun/launcher.asm` (223 bytes), `transfer_call.asm` (3 bytes), and
`transfer_helper.asm` (8 bytes). The 234 source-owned bytes match the decoded
target at their reviewed positions. They remain **source-present**, not exact.
No canonical stored-file offset is assigned to these decoded extents.

The entry stub contains 202 CODE bytes and 21 real data bytes (the saved name
pointer and DOS error string). The transfer units contain eleven CODE bytes.
The separate 324-byte directory is generated as actual structured metadata by
`scripts/lib/zun.py`; it is not credited as product CODE or a maintained data TU.
There are no target-byte arrays, fake ABI substitutions or inserted alignment.
The empty name/entry slots are fields of the observed 32-slot directory format,
not padding used to force code equality.

## Inputs and replay limits

The canonical Japanese target remains the pinned DIET MZ image. The selected
stored Ghidra database was re-attested before this review; packed automatic
functions were not treated as decoded game code. The private flat COM input
comes from guarded `sol-diet-restoration-20261006-b` and retains that receipt's
complete stored/decoded hash binding. The compiler fixture is the two-round
`sol-main-randring-probe-20261006` scaffold, with its maintained MAIN overlays.
Neither fixture is an authored ZUN build or an independent pristine dump.

`config/th03_zun_launcher.toml` pins both receipts, the decoded file, both full
scaffold products, four paired compiled subprogram inputs, and the frozen binary
`libs/kaja/ongchk.com` by hash. All five payloads remain externally owned private
inputs. None was copied into product source or accepted as reconstructed code.
The ZUN binary input was missing from the conservative intake queue; it is now
present as metadata only, expanding the queue from 504 to 505 files.

The default replay assembles each source TU in two fresh directories, links
tiny COM modules, composes the real directory and payloads, validates OMF,
checks unmodified bytes, and runs bounded CPU dispatch observations:

```sh
python3 scripts/replay_th03_zun_launcher.py --run-id NEW_UNIQUE_ID
```

The first attempts exposed runner/output-format mistakes and failed before
acceptance. Run `sol-zun-launcher-20261006-final` produced both source-bound
sets of 223/3/8-byte modules and full compositions, then failed while preparing
the report because `PSP_SIZE` was not imported. That reporting error is fixed.
After the execution environment changed, the next fresh replay failed toolchain
attestation: all three Wine banner probes returned `-31` (SIGSYS). There is no
successful final cold-wrapper receipt in the current environment.

The distinct cached review reads both existing snapshots, checks their source
files against the maintained TUs, validates their OMF and complete compositions,
re-runs the wrapper runtime checks, and guards every consulted input. The launcher
snapshot differs only by two tabs removed from one empty line during whitespace
verification. Its original SHA and this single transformation are explicitly
pinned and recorded; both transfer-source snapshots match exactly. This cached
source association grants no fresh-build acceptance:

```sh
python3 scripts/replay_th03_zun_launcher.py \
  --run-id NEW_CACHED_REVIEW_ID \
  --review-cached-run sol-zun-launcher-20261006-final
```

The recorded cached receipt is
`.analysis/th03-zun-launcher/sol-zun-launcher-cached-final-20261006/receipt.json`.
It explicitly reports `cached_candidates_checked=true`,
`cold_wrapper_checks_pass=false`, and `exact_acceptance=false`. Cached object
equality and source snapshots cannot replace a complete successful frozen cold
replay. Restore the execution environment and run the default command before
considering stronger acceptance. Stored packaging and complete product Oracles
also remain open.

## Complete decoded partition

The 22812-byte decoded image has the following contiguous file partition.
COM runtime addresses add 0100h while embedded; each payload is copied back to
0100h before entry, so its own MAP addresses must not be used as outer positions.

| Region | Decoded file offset | Size | Source/fixture and observed result |
|---|---:|---:|---|
| Entry stub, including real local data | 0000h | 223 | Maintained launcher candidate; bytes match |
| Count, 32 names, 33 entry words | 00DFh | 324 | Structured directory; bytes match |
| Near CALL across payloads | 0223h | 3 | Maintained transfer-call candidate; bytes match |
| `-1` | 0226h | 926 | Frozen ongchk.com binary; bytes match, no source credit |
| `-2` | 05C4h | 1390 | th02_zuninit scaffold; bytes match, ownership open |
| `-3` | 0B32h | 10096 | th01/zunsoft.cpp plus linked runtime/library; bytes match, ownership open |
| `-4` | 32A2h | 4224 | libs/sprite16/sprite16.asm driver; ten differing bytes |
| `-5` | 4322h | 5618 | th03/res_yume.cpp plus included/linked code; bytes match, ownership open |
| Trailing relocation helper | 5914h | 8 | Maintained helper candidate; bytes match |

The six used directory words are 0326h, 06C4h, 0C32h, 33A2h, 4422h and 5A14h.
The other 27 entry words are zero; the other 27 eight-byte names are spaces.
The near CALL's displacement is the complete sum of payload lengths. It is
assembled symbolically from that measured input size, rather than emitted as
an opaque code string. The Python composer writes directory fields and joins
the separately owned compiled modules and private payloads.

## ABI and bounded runtime observations

The stub clears DF, reads the procedure count and PSP command tail, lists the
five names for an empty tail, and reports the real DOS error string for an
unknown FCB name. Selection compares all eight bytes of PSP FCB1's filename;
the wrapper does not implement DOS's argument-to-FCB parsing itself.

For a selected procedure it copies the 16 bytes of FCB2 at 006Ch into FCB1 at
005Ch, removes the first command token, retains the separating space in the
remaining tail, writes the new byte length and CR terminator, and sets
SI=payload start, DI=0100h and CX=complete payload length. It jumps to the near
CALL, whose helper uses REP MOVSB, discards its own return word with POP AX,
pushes 0100h and returns to the copied payload.

The successful name comparison leaves its pushed CX on the stack. With the
probe's initial SP=FFFEh, payload entry therefore has SP=FFFCh and remaining
counts 5/4/3/2/1 for options -1/-2/-3/-4/-5. That word must not be silently
removed in a rewrite. The helper's AX value at entry is 0100h. DS/ES/SS/CS share
the COM segment in this observation; no MZ relocation or far ABI is invented.

The cached review runs seven cases on each image: empty command, unknown name,
and each option with multiple leading spaces and a remaining argument. It
checks the complete selected payload copy, FCB bytes, tail, terminator, stack
word and cleared DF, then stops before executing any payload instruction.
Unicorn's module banner reports 1.0.2 (the installed distribution is 1.0.2rc4),
and Capstone reports 5.0.6. The private replay requires Unicorn; its synthetic
portable regression is explicitly skipped on hosts without that optional
runtime. DOS stdout/exit services
are modeled; DOS return-register details, game/hardware execution, resident
initialization and original DIET self-extraction are not proved by this probe.

The installed Unicorn uses ctypes callbacks. A wrong-return-address control
initially exposed that callback exceptions could be ignored, allowing execution
to continue. Hooks now record the error, stop the emulator, and raise after the
FFI call returns. A synthetic regression test requires clean rejection before
the wrong payload entry and no ignored-callback output. The target-derived
negative control changes the helper's return address to 0101h in a private
copy and is also rejected. Canonical bytes are never modified.

## Raw failure retained

Every decoded-file difference belongs to the externally owned `-4` payload:

| Decoded file offset | Driver address after copy | Instruction | Target | Candidate |
|---|---:|---|---|---|
| 353Ah | 0398h | CMP AX,0 | 83F800 | 3D0000 |
| 35AEh | 040Ch | AND AX,FFFEh | 83E0FE | 25FEFF |
| 35BFh | 041Dh | AND AX,000Fh | 83E00F | 250F00 |
| 3A53h | 08B1h | MOV DL,CS:[EDX+08DCh] | 672E8A92DC080000 | 2E678A92DC080000 |

The decoded mnemonic and operands agree for these equal-length instruction
pairs. That observation is separate from raw equality, which still fails by
ten bytes. No mask, reordered-prefix normalization, equality-maximizing search,
or opaque instruction bytes are used to claim acceptance. The frozen driver
was labeled as TH04 material upstream; that label does not attest its TH03
encoding. Review its complete code/data/TSR boundary and natural TASM forms
before promoting any driver source. The other matching payloads likewise still
need their own source, library, layout, runtime and Oracle review.

The earlier restricted sandbox also failed the Ghidra headless-usage execution probe, so a
new selected-database check cannot complete. Prior stored-database attestation
remains historical evidence. Current cached review verifies complete stored and
decoded hashes directly and does not use database observations. Git metadata
was mounted read-only; staging this batch failed to create `.git/index.lock`.
The worktree and a pending patch preserve the review until the required execution
and repository-write capabilities are restored.

## Fresh replay after execution restoration

On 2026-10-06, unrestricted execution and repository writes were revalidated.
Full CI passes343 tests, pinned Wine compiler/linker probes, headless analysis
tools and all four stored-database/Oracle checks. Historical failure receipts
remain unchanged. A new selected MAINL database attestation also passes; this
does not convert the packed database into an unpacked analysis database.

```sh
python3 scripts/replay_th03_zun_launcher.py --run-id sol-zun-wrapper-fresh-20261006
```

New receipt: `.analysis/th03-zun-launcher/sol-zun-wrapper-fresh-20261006/receipt.json`,
SHA-256 `57d65896bb4c25cd9a4e752fd70919adf9128776861e5002136639b785bc94ad`.
Its25 source/target/lineage inputs remain frozen throughout two independent
compiler directories. All twelve TASM5/TLINK commands exit0. The three
complete maintained TUs are223/3/8 bytes; both composed22812-byte candidates
and dependency-timestamp-normalized OMF objects agree with each other and
the pinned scaffold. Fourteen wrapper executions cover listing, error and
all five dispatches with PSP/FCB/argument moves, REP copy and native return;
execution still stops before each payload. Wrong-transfer controls reject.

`cold_wrapper_checks_pass=true` now reflects fresh execution, while prior
cached receipts retain `false`. Scoped wrapper/directory/helper raw equality
passes. Full decoded equality still fails the same ten unowned `-4` encoding
bytes. Payload source, full runtime, canonical stored-file ownership/DIET
packaging and complete Oracles remain open; exact stays false. This fresh
wrapper result is separate from a complete game build.

## Maintained -2 retained integration (2026-10-21)

The opt-in `--compose-maintained-init` route takes the two independently produced
TH03 initializer outputs from the 2026-10-21 standalone proof and composes them
with the source-bound retained launcher/transfer modules using the existing
`compose_launcher` operation. It does not patch a target or rerun native tools.
The four other private payloads are taken unchanged from the hash-bound retained
scaffold; legacy full-build payload paths are not required by this opt-in route.
The ordinary replay route remains unchanged.

Opt-in invocation:

`python3 -B scripts/replay_th03_zun_launcher.py --run-id zun-init-wrapper-minus2-20261021-v01 --review-cached-run sol-zun-launcher-20261006-final --compose-maintained-init`

This is a retained composition/runtime diagnostic, not a new full-wrapper cold
build or acceptance. All bytes outside -2 must remain identical, both complete
22,812-byte compositions must match the prior scaffold, and the exact ten target
differences must remain inside -4. The 16,242-byte packed original, DIET rebuild,
real DOS/device/TSR behavior and whole-game denominator remain separate. The parent executed this diagnostic successfully with no native invocations.
The two composed outputs are raw-identical to the retained scaffold. Fourteen
wrapper-only observations pass, including all five dispatches, and the deliberate
wrong-transfer negative control rejects. Owned shared-lock release is complete.

Receipt: `.analysis/zun-init-wrapper-composition/zun-init-wrapper-minus2-20261021-v01/receipt.json`

SHA256 `39490223a696083e6729e01c7855da1b4f84ba5a3ecb380e33f0aa2da760f924`.

Post-release completion SHA256
`ce41829b6e038dd881e4f09e2a49cac05284d21676f3fbbdd3c043cb39a076a1`.
The short parent Factory command completed exit0; the earlier standalone
continuation's unrecovered outer transport status remains unknown.


## Maintained initializer and driver composition (2026-10-21)

The opt-in `--compose-maintained-init-driver` route consumes the two actual
maintained initializer COMs and two independently assembled/linked maintained
driver COMs. The 55-procedure driver owns all 4,224 bytes (2,844 procedure bytes
plus 1,380 layout/data bytes) through ten maintained inputs, without a retained
reference-source producer. Its two raw OBJ, COM and MAP files match. The second
materialization declares the first run's observed source timestamps as inputs;
the first run was not a predeclared cold pair. No output normalization or object
reuse is used.

Composition replaces only -4 in each already maintained -2 composition. The
three other payloads, directory, launcher and transfer scaffold remain retained
and byte-identical. Both actual produced inputs are required; target fallback
is forbidden. The full decoded candidate remains 22,812 bytes with the same
ten target differences in four natural TASM instructions in -4. This is not
full-wrapper cold provenance, DIET packaging, DOS device/TSR proof, or an exact
acceptance change. The default replay and initializer-only option are unchanged.

Eight focused positive/negative tests pass. The parent-owned short composition
check also passes: both 22,812-byte outputs have SHA-256
`c036f2df54f81ff9e9950d2a397576a4c6c08314ed601c8f972fc83e5bf384b8`.
All fourteen wrapper dispatch observations and the wrong-transfer negative
control pass; observations stop before payload entry, not DOS device execution.
The retained receipt is
`.analysis/zun-driver-wrapper-composition/zun-init-driver-wrapper-20261021-v01/receipt.json`
(SHA-256 `3830777630d3c719765a7ab522a068203e10e452e4e7f6072f140995ed31469b`),
with successful owned release and no errors. No compiler or Wine was invoked.

Replay the opt-in retained composition with:
`python3 scripts/replay_th03_zun_launcher.py --run-id UNIQUE_ID --review-cached-run sol-zun-launcher-20261006-final --compose-maintained-init-driver`.
The required actual retained output inputs are deliberately explicit and must
remain available; this is not a standalone distribution build command.
