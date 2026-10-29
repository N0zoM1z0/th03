# Character-selection declarations and storage

`src/op/menu/selection_state.inl` recovers the tail TU's complete declaration
prefix: consumed compatibility headers, character filename pointers, stats,
cursor glyphs, coordinates, initialized input flags and original state widths.
It is a bounded include. The real functions remain in
`src/op/menu/character_selection.inl`, with the existing preceding unlock helper
and score loader compiled separately.

The maintained selected producer includes this prefix and the actual literal
function tail. It emits the complete2858 CODE/227 DATA/23 BSS geometry, all17
original procedure/public boundaries and every native external/fixup record
identically to the retained baseline producer. The only OMF differences are
compiler comments recording the new source include. This is genuine TC4 output;
objects and executables are never patched.

## Replacing the old dummy state bytes

The frozen scaffold names unused BYTE objects `padding_1` and `padding_2`.
Those names are not evidence of original variables. Three focused native
controls establish the actual compiler choice:

| Declaration/compiler choice | CODE | DATA | BSS | resident / input_mode offsets |
| --- | --- | --- | --- | --- |
| Remove both dummy objects, original flags | 2858 | 227 | 21 | 1 / 10 |
| Remove dummies, whole TU `-a2` | 2874 | 227 | 23 | 2 / 12 |
| WORD alignment only while declaring state, restore BYTE for functions | 2858 | 227 | 23 | 2 / 12 |

The final source uses scoped `#pragma option -a2` then `-a-`. It reproduces the
entire CODE/DATA byte streams, segment/group records, all publics, all externals
and all literal ordered FIXUPP records. There are no dummy variables, reserve
arrays, emitted bytes or explicit filler in the maintained prefix. This recovers
a natural source representation; the original spelling of compiler directives
is not known. Ordinary function alignment cannot be changed globally: that
would insert16 bytes and move real procedure boundaries.

The real BSS declarations are:

| Object | Offset | Size | Alignment |
| --- | --- | --- | --- |
| curve_cycle | 0 | 1 | 1 |
| resident | 2 | 4 | 2 |
| sel | 6 | 2 | 1 |
| sel_confirmed | 8 | 2 | 1 |
| page_shown | 10 | 1 | 1 |
| input_mode | 12 | 4 | 2 |
| fadeout_frame_third | 16 | 2 | 2 |
| curve_unused | 18 | 2 | 2 |
| curve_trail_count | 20 | 2 | 2 |
| playchars_available | 22 | 1 | 1 |

The compiler supplies uninitialized alignment holes at1 and11. `func_t_near`
means a near variable holding the model-default far Pascal function pointer;
its stored value is four bytes. Preserve both halves and the original callbacks.
The23-byte BSS contributes zero file-backed bytes. The existing BYTE/WORD
operations and unchecked menu behavior remain unchanged.

## Complete initialized DATA

DGROUP0D7F:0A0E contains227 initialized bytes:

| Local range | Source meaning |
| --- | --- |
| 0..35 | Nine ordinary far filename pointers |
| 36..62 | Nine rows of three character stats |
| 63..68 | Two cursor top rows, each two glyphs plus an implicit zero |
| 69..74 | Two cursor bottom rows, each two glyphs plus an implicit zero |
| 75..76 | Two explicitly false input-lock BYTEs |
| 77..223 | Nine filename-macro strings and seven function literal strings |
| 224..226 | Three unused text colors from the function include |

The verifier evaluates the actual declarations and consumed filename/glyph/color
macros. It checks every byte against native LEDATA, then independently resolves
all nine far fields at32,28,...,0. Their segment words produce the literal ordered
MZ entries at DATA+34,30,...,2. All target/candidate bytes and ordered entries
match, with no straddling relocation. Following0AF1 is outside ownership.

## Affected native build

`scripts/build_th03_op_selection_work.py` is the maintained selected producer.
It uses the one existing TH03OP tree, temporarily substitutes the actual tail
wrapper with real includes, compiles the one affected TU and links it at its
unchanged position against29 validated context objects. Two independent rounds
produce identical complete raw OBJ/EXE/MAP vectors. Both whole linked files equal
the pinned Japanese decoded target, including its header and ordered relocation
table; both MAPs equal the retained native MAP exactly.

The original cold source graph/recipe and all32 retained outputs are unchanged.
The selected builder restores its wrapper and removes temporary staged inputs
and outputs. Its new maintained source/driver/input/command/output bindings are
verified separately. The frozen full-cold builder still carries its old contextual
prefix: this review does not silently relabel that recipe as a new cold build.
It grants227 new initialized DATA bytes and reviews BSS layout; the previously
accepted function CODE is not counted twice.

```sh
# Recompile/relink only after maintained source/tool changes:
.venv/bin/python scripts/build_th03_op_selection_work.py
# Current read-only source/native/layout proof:
PYTHONPATH=scripts .venv/bin/python -m lib.op_select_storage
```

The live receipt and actual selected OBJ/EXE/MAP pairs are retained under
`.analysis/work/selection-*`. No full cold rebuild, DIET replay, emulator matrix
or ancestor runtime chain is required for this bounded source change. Whole OP
source exactness and canonical packed-file unit credit remain open.
