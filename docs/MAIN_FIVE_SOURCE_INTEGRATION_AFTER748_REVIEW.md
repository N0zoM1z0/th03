# TH03 MAIN after748: five changed physical source units rebuilt together, with input_s blocker separately diagnosed

The **as-of-after748 current-source two-round original Turbo C++ 4.02/TLINK proof**
compiles five genuinely modified original 16-bit physical translation
units together. It does **not** rerun the full 99-project-object cold
compiler workflow: the other **94 original project objects and original
CRT** are reused from the unchanged after596 normal MAIN source-native
parent. The real maintained C++ sources are bound through compiler-emitted
original OMF dependency comments, not silently substituted older worktree
copies or manually patched object bytes.

| Original physical TU | Complete source reconstruction changed in this turn | Original initialized CODE | Ordered OMF FIXUPPs | PUBLICs |
| --- | --- | ---: | ---: | ---: |
| `ba_chiyu` | **Full Chiyuri major BOSS**, original attack cadence, full update, signed ring/intro radius shifts and both sprite renderers | 2,654 | 381 | 11 |
| `e_fireb` | **Full Fireball engine**, 512-frame target selection mask, 8-frame sprites, natural spawn/transfer/hittest/render indices; **one initialized DATA and one BSS byte retained** | 1,555 | 115 | 10 |
| `ba_maris` | **Full Marisa major BOSS**, period masks, BOSS update, main/split intro renderer and native signed frame shift | 1,431 | 199 | 9 |
| `ex_ellen` | **Full six-function Ellen Extra Attack** slots, seven-point trail and collision/render state, native C++ local loops | 1,129 | 79 | 6 |
| `e_expl` | **Complete 630-byte explosion chain/collision controller**, 4-frame test, three charge tiers, native signed bonus and collision-count loop | 630 | 49 | 1 |
| **Five original source objects rebuilt together at after748** | | **7,399** | **823** | **37** |

## Original compiler and full normal MAIN integration

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af748a --units ba_chiyu,e_fireb,ba_maris,ex_ellen,e_expl
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af748a

**Both independent real TC4 compiler/full original TLINK rounds** match
every original initialized CODE byte, the original Fireball's initialized
DATA and BSS ownership, **823 literal ordered original OMF FIXUPP fields**,
**37 PUBLIC names and offsets**, original segment definitions and
compiler-consumed maintained source path dependencies. Both full normal
MAIN EXE and path-normalized MAP match the immutable source-native parent.
The original Japanese **124,642-byte loaded program** and **all 1,553
ordered MZ relocation words** also match. Independently serialized
standard DOS MZ exactly reproduces the **130,882-byte original Japanese
MAIN.EXE**; this post-link serialization is separate from the historical
vendor direct TLINK header. No cold replay or source/object byte patch.

Primary immutable source-bound writer receipt:
`.analysis/work/exatt-layout-af748a/report.json`, SHA-256
`9200b878dd4beeecb6c79b17c07773a36f522aed322c32ed7d5b8c05c7572f84`.
The five actual original native OBJ variants per round, complete full
EXE/MAP, compiler/linker writer logs and all source/OMF dependency
snapshots are retained intact in protected ignored evidence. Distinct
historical receipts from after741, after730 and earlier builds are not
rewritten, repinned or overwritten.

## Native-negative tests and remaining input_s problem

Actual separately compiled negative controls showed that apparently
natural but byte-unequal C++ can change 16-bit TC4 codegen:

- `af742c`: Chiyuri's unsigned-byte `speed / 4` cannot be a C++ `>> 2`
  without changing machine code; the three signed intro shifts and
  ring-radius shifts **are** original native-exact (`af742f`).
- `af743a`: Fireball explosion `frame / 4` cannot be reduced to `>> 2`
  without changing the original CODE length; the independent 512/8-frame
  masks and `++i/--i` loops are exact (`af743d`).
- `af745b`: Marisa's unsigned-byte bullet speed division ` / 2`
  cannot become `>> 1`; the split sprite intro's signed `<< 1` and
  the full attack-period bit masks **are** native-exact (`af745d`).
- `af746b`: Ellen Extra Attack's mutable local `added++` cannot use
  prefix `++added`; the loop/clip and entity-state improvements are exact
  (`af746d`).
- `af747c`: explosion bonus `bonus += bonus` cannot be replaced with
  `bonus <<= 1`; named charge thresholds and collision-count prefix
  are exact (`af747e`).

**Separate and intentionally not included in the five passing units**:
The current `input_s` BIOS keyboard scanner source (now with natural
`for(;;)` two-pass polling) recompiled to exactly the original **417
CODE bytes, 42 ordered fixups and one PUBLIC** in separate actual TC4
trials `af744c` and `af744d`. However the frozen normal MAIN parent
uses an **418-byte** historical alternative object whose extra byte
at original CODE offset 417 is a `0x90` NOP. Without that historical
byte, the normal full linked EXE has exactly one byte different at
raw file offset **68,141**. This **fails** complete original full-link
source-native proof. The original code is not modified with a filler
NOP, and no acceptance or source-completion credit is claimed.
Read [the read-only input_s negative proof](MAIN_INPUT_S_LINK_GAP_AFTER744_REVIEW.md)
and run `scripts/review_th03_input_s_link_gap_after744.py` to verify the
blocker explicitly. Do not treat a successful diagnostic return as full
MAIN equality: it returns `normal_MAIN_exact=false` by design.

## Historical receipt state and limits

The unaffected `af741b` and `af730a` live-source reviewers still pass;
`af724a`, `af721a` and `af715a` now **correctly reject current-source
input hashes**, since their Marisa/Chiyuri revisions precede this turn.
They remain valid **historical native compiler/linker snapshot evidence**,
not current-source revalidations. Earlier after736/709 are likewise
historical after source changes. No reviewer was weakened to turn stale
inputs or the `input_s` one-byte NOP into passing provenance.

This current success attests the original compiler and full-link behavior
of **five already existing physical original CODE owners**, **not** newly
accepted canonical Factory packed-game units, historical vendor raw OMF
packet identity, independent pristine target provenance or complete
99-owner product source reconstruction. The after709 cumulative 58-owner
union was not recomputed or increased using these overlapping bytes.
