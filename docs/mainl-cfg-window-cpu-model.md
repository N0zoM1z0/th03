# MAINL CFG/window CPU contracts

The model executes 387 actual linked bytes: CFG resident loading at 095F:0003
(49 bytes), win_load at 095F:0034 (282), and win_text_put at 095F:014E (56).

## API and replay
scripts/review_th03_mainl_cfg_windows.py exposes analyze(program_image) and
matrix(mz), where mz is produced by lib.pc98.parse_mz. Compare complete returned
matrices directly; no normalization is required. Analyze separately checks full
near-return bodies, instruction boundaries, branches, and reviewed foreign calls.

The matrix has 489 scenarios and 4,723 foreign calls per image: 76 CFG, 407 window,
and 6 text scenarios. Focused tests retain nine actual CPU mutation controls for
return value, resident destination, near/far return, palette, message selection,
NUL termination, text pointer, and text geometry.

Use the existing virtualenv, one allowed CPU, nice >=10, and bytecode disabled.
tests/test_mainl_cfg_windows.py defaults to the retained original decoded image;
TH03_MAINL_CFG_TEST_EXE can select a newly linked candidate. Missing retained input
is reported as a skip, never as successful CPU verification.

Runtime repository dependencies are the model helper and lib/pc98.py for parsing.
The focused tests add only their own file. External dependencies are Unicorn and
Capstone (observed versions 1.0.3 and 5.0.6). Standard-library imports add no
repository dependencies. Source reconstruction providers are separately owned.

## Oracle and limits
Expected behavior uses independent scalar expectations informed by frozen source
b6ba5b0a529edbb31efdf8c0e939263804f8ee47. Disassembly establishes instruction and
ABI coordinates, not expected candidate behavior.

Foreign functions are explicit memory-only contracts with far Pascal stack
cleanup. File reads write scenario-controlled prefixes; other imports perform no
memory or device operations and return AX. Error-like values, short reads, and
no-write reads preserve the original unchecked behavior. CFG propagates untouched
or partially overwritten stack bytes into its returned resident segment.
win_load always adds all three NUL terminators.

Distinct synthetic near PIC_FN and far WIN_MESSAGE_FN tables test selection and
pointer ABI, not filename contents. Cases cover every valid paletted-character
pair, special stages 6/7, nonzero winner selection, palette bits, CF/DF seeds,
partial reads, and selected invalid loser bytes. Invalid winner/table indices are
not comprehensively validated. Text expectations check x=80, y=272/288/304,
effect/color=47, and three far text pointers.

Checks cover call order and arguments, near-return stack balance, BP/SI/DI and
DS/SS preservation, declared CPU memory writes, and complete 16-KiB DATA snapshots.
Stack locals and volatile flags/registers are not exhaustively asserted.
This does not validate real DOS, devices, library implementations, filename
content, whole-program execution, or exact reconstruction acceptance.

## Evidence reuse
Retained results may be reused only when each full executable SHA-256, the exact
model/helper dependencies, relevant runner identity, and external model versions
match the recorded receipt. Matching only these 387 code bytes is insufficient.
A newly installed or changed executable requires replay after its native build.
The retained standalone runner is not identical to these focused tests; its
results do not claim that the focused test file itself has executed.
