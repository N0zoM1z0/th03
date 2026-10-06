# MAINL lifecycle candidate review

MAINL's complete initialization and two exit translation units contribute
169 decoded CODE bytes. All three complete functions and their direct
41-byte VRAM pointer helper have raw identity and equal original ordered
relocations in both cached products. This is candidate analysis, without a
new cold build, maintained MAINL source or canonical stored-file acceptance.

```sh
python3 scripts/review_th03_mainl_lifecycle.py --output .analysis/NEW_LIFECYCLE_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_lifecycle_review.py -v
```

Receipt: `.analysis/sol-mainl-lifecycle-review-20261006.json`. It inherits the
pinned root/decoded/canonical lineage and separately verifies all inputs.
Ghidra headless-usage fails before selected database attestation; no database
observations are used. All addresses below belong to the decoded namespace.

| Entry in 0C7E | Complete body | Bytes / instructions | Return | Original relocations |
| --- | --- | ---: | --- | ---: |
| 0002 | VRAM planes helper | 41 / 8 | far | 0 |
| 01B0 | General game exit | 67 / 23 | far | 8 |
| 0700 | Game initialization | 62 / 21 | far RET 4 | 6 |
| 098F | Exit from MAINL to MAIN | 40 / 14 | far | 5 |

The root bodies total 169 bytes / 58 instructions; the helper is a separate
41-byte diagnostic dependency. Both cached MAPs show each complete TU's
contribution exactly at these boundaries. Branches resolve to instructions
within their body, every interior return has the same cleanup, and each far
call has a declared interface. The sole near call at 0718 targets the complete
helper at 0002, immediately preceded by PUSH CS. The helper's actual far RET
consumes the constructed segment/offset return frame and resumes at 071B.
The observed NOP at 0716 is part of initialization's body; no padding is added
or encoding producer inferred from that observation alone.

## Compiler and source association

Seventeen frozen providers were consulted. Fourteen match both cached source
trees byte-for-byte. Three cached top-level includes instead forward to the
maintained MAIN sources already used by the aggregate replay:

| Frozen carrier | Cached include destination |
| --- | --- |
| th03/initmain.cpp | src/main/core/initmain.cpp |
| th03/exit.cpp | src/main/core/exit.cpp |
| th01/vplanset.cpp | src/main/hardware/vram_planes.cpp |

These remaps are checked as exact single includes. Eight consulted localized
implementation/header/compat providers match the current repository and both
cached trees. The original included implementations remain separately pinned
candidate material; their presence in a tree does not mean the compiler used
them. The exit-to-MAIN TU uses its unchanged frozen implementation. Cached
producer identity is therefore mixed and explicit, rather than a claim that
all seventeen frozen files compiled unchanged.

The maintained MAIN declarations explicitly preserve far/Pascal library
contracts and far filename pointers. The frozen large-model declarations,
game-specific preprocessing and actual caller/return instructions corroborate
the observed ABI. MAIN's prior exact acceptance does not transfer to MAINL.
No product dependency is added across artifact folders; cold localization or
proved shared ownership remains required before a maintained MAINL owner.

## Actual operations and modeled interfaces

All four bodies execute actual decoded instructions. The twelve imported
library bodies are explicit interfaces: memory assignment/unassignment,
vsync start/end, EGC start, 400-line mode, joystick start/end, archive start/end,
graph clear and text clear. Models record word arguments, supply controlled
AX/CF values, preserve nonvolatile state and emulate far Pascal return cleanup.
The actual port OUT instructions are recorded without a physical device.
There are no real allocations, files, interrupt hooks, clears or page banks.

The helper writes four actual DGROUP dwords at 1C60/1C64/1C68/1C6C, installing
`A800:0000`, `B000:0000`, `B800:0000`, `E000:0000`. The replay independently
checks each write and all 65536 bytes of the constructed DGROUP window:
only those sixteen bytes may change. DF remains inherited, without affecting
the scalar MOV stores. No VRAM pixels are touched by this helper.

Initialization requests 18000 paragraphs (288000 bytes). Its branch tests AX,
returning1 for any nonzero assignment result, regardless of modeled CF. It
performs no later initialization in that case and leaves the plane pointers
unchanged. On zero AX it executes the actual helper, then requests vsync,
EGC, 400-line, joystick and archive initialization in order. The far filename
pointer is passed unchanged, including the tested NULL and offset-FFFE values;
no filename dereference is modeled. Other controlled library returns remain
unchecked, and initialization finally returns0.

General exit requests archive end, clears access pages1/0, selects access0
and show0, then ends vsync, unassigns memory, clears text, ends joystick and
starts EGC. The special exit-to-MAIN selects access0/show0 without graph/text
clear requests, then ends vsync, unassigns memory, ends joystick and starts
EGC. Both use the TH03 vsync-before-memory order. The GAME>=4 alternate order
and BGM operations are not executed or inherited. Caller/source intent does
not supply physical pixel preservation or complete teardown proof.

The replay also executes the actual `_main` prefix at `095F:078D..07A2`,
modeling only the prior configuration call as successful. Actual initialization
then returns0/1 for the selected memory results. In all cases execution reaches
the next `respal_exist` call at 07A3, with the root stack intact; `_main` does
not branch on initialization's result. This checks the real caller and callee
together, rather than substituting initialization's result alone. It stops
before that next library call and does not prove the remainder of failed-init
execution, CRT or process startup.

Per image: 36 initialization calls (six AX results × two CF states × three
far pointers), twelve helper/exit calls (three entries × two DF states × two
library results), and three actual caller-prefix stops. Across three images:
153 invocations, comprising 144 terminal returns and nine intentional prefix
stops. Six adversarial controls cover truncation/interior return contracts,
PUSH-CS requirements, operand/neighbor edges, unknown calls, callback errors,
interface aliases, stale terminal state and actual near-call/far-return cleanup.

Three new decoded boundary-reviewed function rows grant no maintained source,
file-backed extent or exact credit. Canonical DIET packaging, cold source and
link layout, DGROUP/BSS ownership, complete libraries/devices/CRT and the full
Oracle set remain open alongside the broader ReC98 intake.
