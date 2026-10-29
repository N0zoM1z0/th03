# MAINL resident, integer angle, text and joystick

This review adds 9 disjoint owners and 13 procedures: 559 CODE +18 DATA bytes.
The TH03-modified joystick start/sense APIs account for 76 authored CODE bytes;
the other 501 bytes are library code/storage. Previous 172 owners remain
unchanged. Four joystick BSS bytes add no file credit.

## Natural native production

Six actual modules assemble and link twice: context, resident scan/set, resident
create, sound/text, joystick, and joystick end. Context supplies the real
DOS_KEYCLEAR and IATAN2 providers, palette/console state and existing angle table.
No stub callee is used. Complete six-OBJ/EXE/MAP vectors repeat. All 18 native
module fields resolve independently for the actual mini layout and the product
layout; complete code contributions match the pinned Japanese target/current
candidate. The mini has a real uninitialized stack and BSS, with no extra credit.

`respal_create.inl` removes the old compatibility NOP guard and uses ordinary
CALL. RESPAL_EXIST is declared external far outside CODE, so TASM emits an
actual five-byte 9A call and FAR-pointer field. Actual TLINK naturally produces
the target NOP/PUSH CS/near CALL at 27AC. The same method replaces JS_END's
`nopcall DOS_KEYCLEAR` at 17CA. Neither source adds NOP padding. The new MCB
include retains the original offsets 0/1/3 and signature length 10.

Private SOUND_I/O are real near providers exported by the sound module wrapper.
The three joystick calls to these providers have genuine native self-relative
fields. Their real mini and product destinations are checked. Original same-TU
near calls, local branches and compiler/assembler output remain intact.

The unchanged root is contextual transport for the old compatibility calls.
The maintained includes and independent TU boundary now demonstrate the natural
producer. A future deliberate full recipe integration must use that boundary.
All 938 cold outputs, source, recipe and tools remain validated and unchanged;
no full cold, DIET or ancestor runtime replay is required.

## Complete source and ABI

| Scope | CODE | Procedures | Origin |
| --- | ---: | ---: | --- |
| IATAN2 / JS_END | 114 | 2 | Library |
| SOUND_O / SOUND_I / TEXT_CLEAR / TEXT_FILLCA | 116 | 4 | Library |
| RESPAL_EXIST / CREATE / SET_PALETTES | 226 | 3 | Library |
| JS_START | 42 | 1 | Authored TH03 variant |
| SOUND_JOY | 18 | 1 | Library |
| JS_SENSE | 34 | 1 | Authored TH03 variant |
| SAJOUT | 9 | 1 | Library |

Every complete physical body, private near return, far Pascal cleanup, local
branch and genuine outer EVEN is checked. All 13 root native fields are offset
WORDs; the complete scoped literal MZ vectors are empty. IATAN2 keeps its signed
magnitude/overflow behavior and both real angle-table references. The existing
AtanTable8 is contextual DATA here and gains no table credit.

Resident scan traverses DOS MCBs and compares the ten-byte signature. Creation
preserves allocation strategy handling, its unchecked fallback allocation and
the original owner/state writes. SET_PALETTES preserves packed RGB conversion.
No new allocation checks or timeout behavior is introduced.

Sound busy waits remain potentially unbounded. TEXT_CLEAR retains the INT29h
escape sequence. TEXT_FILLCA keeps the BIOS row count, BP-via-BX frame and caller
DF assumption. Joystick detection retains 256 attempts and PUSHF/CLI/POPF.
When no joystick exists, JS_SENSE still ORs the caller's SI into js_stat and
does not synthesize a valid AX result. Private SAJOUT remains in the output;
no execution or reachability claim is made for that body.

## Corrected joystick boundary and state

The old 105-byte joystick aggregate included zero bytes at 2AAD and 2B15.
The actual four bodies and three ordinary EVEN bytes occupy 103 bytes from
2AAE through 2B14. The ledger now separates the two TH03 variants from SOUND_JOY
and SAJOUT. Neither surrounding zero belongs to a code owner. The independent
103-byte WORD module naturally creates a zero gap before its following module;
the old root's two explicit zero providers remain uncredited context.

The ten-byte `pal98 grb` identifier, including NUL, has its actual ResPalID public
and native DATA owner. Four original zero joystick WORDs own eight bytes, with
all C/ASM aliases. js_stat remains two uninitialized WORDs. The new source files
use genuine signature/state declarations, not target-byte arrays.

Actual private inputs: `mainl-resident-build.json`, `mainl-resident-native.json`,
both `resident-mini-roundN-NAME.obj`/EXE/MAP vectors, six actual
`resident-mini-NAME.asm` wrappers and `resident-mini.lnk` in `.analysis/work/`.
The verifier binds the whole generated source/dependency closure and output
vectors. Physical hardware behavior and whole-product source ownership remain
open. Current acceptance reuses unchanged historical runtime observations.
