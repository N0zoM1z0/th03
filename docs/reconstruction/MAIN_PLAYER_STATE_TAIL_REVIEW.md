# MAIN player-state tail: source candidate, 2026-10-22

Four natural C++ bodies now live in `src/main/player/state.cpp`, its declaration
headers and bounded `render.inl`, `overlay.inl`, `knock.inl`, and `bomb.inl`.
The original-toolchain PSTA230 producer emits 610 CODE bytes, no private DATA/BSS,
and four complete procedure publics. This is an unlinked compiler observation,
not source-ledger promotion or exact acceptance. The default product graph is
unchanged; original physical TU composition and the full authored denominator
remain open.

| Candidate | Canonical MAIN load interval | Bytes |
| --- | --- | ---: |
| `player_render` | `DE95..DF18` | 131 |
| `player_overlay_render` | `DF18..DFE9` | 209 |
| `player_knockback_update` | `DFE9..E080` | 151 |
| `player_bomb` | `E080..E0F7` | 119 |

These boundaries retain their provisional target/database association. All four
compiled lengths and instruction shapes agree with the target. Field assertions
bind the packed player record, byte flags, character wrapper, gauge, animation
and knockback offsets. Existing HUD, sound, vector, movement and effect APIs
supply the real types. `player_bomb` uses the existing near-Pascal near-pointer
signature in `cpu.hpp`; its available-gauge test uses offset `0x1A`, and the
character byte is `playchar_paletted.v`.

The auxiliary target entry `C248` returns with `RET 2` at `C2F6`; this body ends
at `C2F9`, before another function. Its passed stack slot is unused. The new
`player_lose_anim_render` name and pointer interpretation are inferences from
the caller; no maintained callee body, original source name or accepted ownership
is claimed. `lose-render-abi-v01.json` retains the earlier wider observation;
`lose-render-abi-v02.json` isolates the first body without rewriting it.

## Compiler observations and retained failures

Evidence is preserved under `.analysis/codex-main-player-state-20261022-v01/`.
The starting worktree was clean at `0ec0f97`; preflight and a fresh headless MAIN
database check passed. `main-database-check.log` retains that check. The canonical
Japanese target remains candidate-local-attested, SHA-256
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`.

- PBMB227 (`native-v01`) failed compilation because the character wrapper was
  assigned directly to a byte. Its original source, error and terminal receipt
  remain unchanged.
- PBMB228 (`native-v02`) accesses the wrapper's actual `.v` field and compiles
  the 119-byte bomb body successfully.
- PSTA229 (`native-v03`) compiles three bodies totaling 476 bytes. Its overlay
  is 206 instead of 209 bytes: multiplying the movement frame by three produces
  a different register calculation. Its successful process receipt does not
  imply a matching candidate.
- PSTA230 (`native-v04`) expresses the observed two-stage pattern-index addition
  and includes the base sprite pass. All four bodies total the expected 610
  bytes. The actual object is 4,481 bytes, SHA-256
  `cccf780057a171bf75a0c0a846aba1ec56ffe97aae2bdcf83567c68a802f0c09`.

Each capsule has eleven preparation controls and retains the same process,
registry, source/tool and sole-writer guards. Four native compiler invocations
ran serially; all ended with certain cleanup and released locks, including the
compiler failure. The final capsule materializes 52 source files plus four
vendor headers, with no retained object or binary seed. Its outer time is
13.18 seconds and peak RSS 108,904 KiB; the largest of the four peaks is 108,940
KiB. One CPU/nice 10 and zero swaps are recorded in the resource reports.

## Raw-byte and fixup diagnostic

`review-playerstate-v04.py` reads the actual object, the canonical target, the
original native receipt and every pinned input. Its installed-source mode also
requires the maintained product/compatibility bytes to equal the actual compiler
inputs. The installed seven files are byte-identical to the successful producer.

All 35 fixups are decoded from the unchanged OMF. Their locations must be actual
displacement/immediate fields; four-byte fixups must belong to five-byte far
calls. Excluding 92 operand bytes and five observed linker-relaxation opcode
positions leaves **513 raw bytes, all equal to target**. The two negative
controls reject a non-fixup target mutation and a changed far-call opcode.
This is a diagnostic exclusion, not complete linked raw equality.

Five compiler far calls still require native linker relaxation: two bomb-path
calls and three playfield-X conversion calls. Removing only those hypothetical
segment sites from the observed OMF traversal leaves
`[578, 453, 361, 332, 230, 123]`, equal to the target's six literal sites relative
to `DE95`. No actual linked relocation order has been produced; the report marks
it unknown, and exact acceptance remains false. No OMF or MZ bytes are rewritten.

Replay the current-source diagnostic without native tools:

```sh
.venv/bin/python -B .analysis/codex-main-player-state-20261022-v01/review-playerstate-v04.py \
  --installed --output .analysis/NEW_PLAYER_STATE_REVIEW.json
```

`unlinked-review-v04.json` and `installed-source-review-v01.json` retain the
original observations. A separate parser correction in
`bind-main010-calls-v02.py` recognizes Capstone's `0, 0x26ca` as a direct far
call. Exactly two of the prior 29 call observations change, both to the existing
`SUPER_PUT` entry; the other 27 and all other report fields are unchanged. The
original call-intake report is preserved.

## Remaining proof work

Recover the preceding 1,106-byte state-update body at `DA43..DE95`, then measure
the coherent MAIN_01 source composition. A private uncompiled draft is retained
as `player-update-candidate-v01.inl`; `update-next-intake-v01.json` binds its hash
and target observations. The input word is at BP+6, the player pointer at BP+4,
and the exit is RET 4. The two-byte release-counter view at DS:4B9C lies within
the existing root BSS reserve following `_collmap_pid`; a reviewed symbol binding
is still needed. The existing `target_formation_marker` is DS:38E8 and is declared
by the maintained Yumemi gameplay API. The boss owner at DS:063E is
`gba_boss_launched_by`, not `boss_active`. These names follow current source/MAP
bindings; the draft has not been compiled or installed. Original physical ownership, root caller
migration, real linked callee bindings, all raw bytes and literal relocations,
selected behavior, independent cold builds and the complete acceptance gates
remain required. The prior 21,010-byte physical-producer hypothesis is still
open. MAIN remains 87 exact extents / 413 functions / 66,843 scoped bytes; OP,
MAINL and ZUN acceptance counters are unchanged.
