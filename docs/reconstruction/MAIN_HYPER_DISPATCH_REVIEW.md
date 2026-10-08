# MAIN_010_TEXT complete Hyper/character-state dispatcher — exact

**Scope:** TH03 Japanese MAIN, target load-image 0x0D7F0..0x0DA43;
original segment MAIN_010_TEXT in group MAIN_01, map at 096E:4110,
length 0x0253 = **595 bytes**, ten complete near Pascal callbacks.

All ten functions are reconstructed in the maintained natural source
src/main/player/hyper.cpp, with declarations in hyper.hpp. A standalone
pinned Turbo C++ 4.02 source-shape probe attests complete function starts,
sizes, instruction shapes and returns. Existing character state, per-player
near Hyper function pointers and speed globals remain historical external
DATA/BSS; this CODE object creates no private BSS.

| Original function | Relative start | Size | Caller-facing behavior |
| --- | ---: | ---: | --- |
| hyper_standby | 0x000 | 25 | Normal shot mode, restore configured Hyper callback |
| hyper_reimu | 0x019 | 62 | Special Hyper shots and faster aligned/diagonal movement |
| hyper_mima | 0x057 | 66 | Paired shots, frame block and speed changes |
| hyper_marisa | 0x099 | 67 | Far Marisa Hyper helper, slow movement |
| hyper_ellen | 0x0DC | 47 | Far Ellen Hyper on selected round frames |
| hyper_kotohime | 0x10B | 62 | Four shot pairs and faster movement |
| hyper_chiyuri | 0x149 | 62 | Four shot pairs and faster movement |
| hyper_yumemi | 0x187 | 62 | Four shot pairs and faster movement |
| hyper_kana | 0x1C5 | 62 | Four shot pairs and faster movement |
| hyper_rikako | 0x203 | 80 | Gauge-gated charge call, cancellation and slow movement |

These are the target-reviewed **complete** boundaries, not a set of short
functions selected to increase the exact count. Three important far
dependencies are Marisa Hyper, Ellen Hyper and Rikako charge/hyper.
The frozen carrier preserves the original Marisa far helper export;
the existing fully exact Ellen/Rikako source owners supply the other calls.
The original ASM's near pointer initializers for P1/P2 remain in the frozen
DATA/code carrier, resolved by exported symbols from the new object.

## Critical TC4 layout and ABI discovery

The first direct-C++ candidate reproduced all 595 target instruction
*shapes*, exact MAP, all four ordered MZ relocations and prior owners, but
nine near function-pointer operands remained 0000 instead of the actual
MAIN_01 group offset 0x4110. Another rejected experiment added a codegroup
option and OMF GRPDEF patch but shifted player_stuff_t field displacements
(e.g., original shot_mode at 0x0D became 0x12), causing 98 linked byte
differences. Both failure receipts are retained, and the OMF workaround was
**not** integrated.

The accepted solution uses **unmodified original TC4J OMF**, generated
from this source prologue before historical player headers:

    #pragma codeseg MAIN_010_TEXT main_01
    #pragma option -a1

The player_stuff_t declarations are thereby parsed using the original
one-byte field packing (shot_mode at 0x0D, near hyper pointer at 0x64).
After those includes, #pragma option -a2 restores normal compilation
alignment for subsequent source. This also places the live CODE SEGDEF
in the correct MAIN_01 code group without any OMF edit. The existing
frozen TASM carrier's residual MAIN_010_TEXT contribution is marked
BYTE aligned after the newly emitted odd-length 595-byte object;
otherwise TLINK inserts one spurious byte and moves all downstream
accepted MAP contributions. No comparison expected value is changed.

The direct natural compiler-shape probe is:

    python3 scripts/probe_th03_main_hyper_cpp.py --run-id gpt-web-hyper-natural-final-shape-v14-20261008

Receipt:
.analysis/th03-main-hyper-cpp/gpt-web-hyper-natural-final-shape-v14-20261008/receipt.json

Two serial candidate cold compilations and links passed **all** prior
accepted CODE, immutable target raw bytes, exact MAP for p_hyper at
096E:4110 0253, the exact original ordered MZ relocation positions
184, 263, 536 and 559, and the DOS behavior probe:

    python3 scripts/replay_th03_main_exact_units.py --candidate-manifest config/th03_main_hyper_dispatch_candidate.toml --run-id gpt-web-hyper-main010-link-c11-20261008

The candidate TOML was merged into the default manifest and retired;
that invocation is historical. Its receipt stays at
.analysis/th03-main-exact/gpt-web-hyper-main010-link-c11-20261008/receipt.json.

First default, no-candidate replay:

    python3 scripts/replay_th03_main_exact_units.py --run-id gpt-web-hyper-main010-default-p01-20261008

Receipt:
.analysis/th03-main-exact/gpt-web-hyper-main010-default-p01-20261008/receipt.json

Both cold rounds pass **330 accepted functions / 50721 function bytes /
51644 owned CODE bytes**, 73 CODE extents and 66 maintained semantic
source owners. All 20 outputs, 390 game objects and 456 generated OMF
objects reproduce the accepted game vector with no earlier owner
regressions. The previously known nine Research-only diagnostics remain
separate from the accepted game vector. The current review count is not
a denominator for the whole MAIN program.

## Next dependency closure

The original target-first exploratory v1 interval review included Hyper
among five candidates. After this source promotion, v2 deliberately
excludes Hyper and reviews only four non-exact intervals (3609 bytes):
the two contiguous HUD intro/render blocks, the 1958-byte Marisa
charge/hyper/hitbox prefix and the low-level P_SHOT prefix. See
MAIN_NEXT_FRONTIER_REVIEW.md.

Independent pristine-original provenance, whole-game source closure,
historical physical DATA/BSS ownership, full CI on a host with unicorn,
and Factory Truth Kernel exact acceptance remain open.

## Final post-ledger acceptance and CI limitation

    python3 scripts/replay_th03_main_exact_units.py --run-id gpt-web-hyper-main010-default-final-p02-20261008

Receipt: .analysis/th03-main-exact/gpt-web-hyper-main010-default-final-p02-20261008/receipt.json

The **post-ledger** no-candidate replay passes in both serial cold rounds
with all 330 exact reviewed functions and the complete earlier exact scope.
Source, manifest, Oracle, unit/evidence ledger and progress snapshot hashes
were checked against the receipt and remain identical.

Full CI was attempted (638 tests, 125 import errors for missing Python
unicorn, 167 skips): .analysis/th03-hyper-ci-20261008.log. It does not pass
on the current host. All available post-unittest gates were independently
executed and PASS, with retained
.analysis/th03-hyper-postgates-20261008.log. Factory Truth Kernel
replay and the full game product still remain open.
