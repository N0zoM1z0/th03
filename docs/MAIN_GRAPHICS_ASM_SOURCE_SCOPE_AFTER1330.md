# Six graphics and asset owners: exact source-bound native MAIN assembly

Six previously unselected original MAIN physical objects now assemble
from the maintained symbolic ASM under the original TASM 5.0 and link
under the unchanged 99-object TLINK 6.10 response:

| Original object | Maintained source | CODE bytes | Native fixup fields | PUBLICs |
| --- | --- | ---: | ---: | ---: |
| `hfliplut` | `src/main/formats/hfliplut.asm` | 30 | 1 | 1 |
| `sprite16` | `src/main/graphics/sprite16.asm` | 268 | 11 | 4 |
| `stg_pal` | `src/main/graphics/stage_palette.asm` | 130 | 10 | 5 |
| `mrs` | `src/main/formats/mrs.asm` | 524 | 17 | 5 |
| `score_hud` | `src/main/hud/score.asm` | 454 | 22 | 11 |
| `gf_ctx` | `src/main/graphics/round_fill_context.asm` | 216 | 1 | 10 |
| **Total** | | **1,622** | **62** | **36** |

The score HUD required an actual source change: its CODE and fixups
were already exact, but the native object lacked two original PUBLIC
aliases. `_score_hud_render` now labels the same near entry as
`score_hud_render`; `@ROUND_RESULT_HIGH_DIGITS_PUT$QIIUIUC` labels the
same far entry as `score_bonus_digits_put`. Neither adds instructions,
DATA nor a second function body. The full original PUBLIC map now matches.

The final source-bound `af1330e` assembled all six physical objects twice.
Every CODE byte, literal ordered fixup, PUBLIC, native segment and OMF
module/source identity matched. Both complete normal MAIN executables
were **byte-identical** to the unchanged historical link; the full
normalized MAP and ordered MZ relocation vector matched as well. An
earlier `af1330c` link also independently combined all six candidates.
The retained graphics-fill includes were checked against the maintained
source tree before the final build. The other 93 project objects and CRT
were reused unchanged, not cold-replayed.

Earlier physical comparison `af1330a` identified the two missing HUD
PUBLIC names. This is newly selected **native physical source coverage**,
not a claim about recovered historical authorship, complete gameplay
semantics or canonical packed-file acceptance.

Read-only current-source verification:

```
PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_graphics_asm.py --stage af1330e --check
```
