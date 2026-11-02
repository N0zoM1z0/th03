# Complete original DOS open: 459-byte native source, 20 FIXUPPs and 40-source link

The original Borland C/C++ 4.5 large-model DOS CRT open
member267 is now maintained as real 8086 assembler source
in src/mainl/crt/open.asm. The original is substantially more
than a syscall wrapper. A 31-byte private near Create helper
and a 22-byte near zero-length/truncate helper precede the
406-byte public far-cdecl _open at CODE+53. The source preserves
the actual DOS INT 21h creation/truncation paths, default
text/binary mode, original umask rules, errno/DOS error handling,
descriptor and IOCTL flags, close/chmod fallbacks, and process
exit cleanup hook. It retains the original unchecked error and
stack behavior, not a modernized file-opening implementation.

Actual TASM 5.0 emits **all 459 original CODE bytes** and
**all 20 original literal ordered OMF FIXUPPs** byte-for-byte,
including their exact field sites, widths, segment-relative
kind, frame/target methods and indices, addends and original
record order. The paired fields at sites392/394 and398/400
store the exit cleanup pointer via distinct GROUP-framed
and TARGET-framed native relocation types in the original
instruction sequence. Unlike the older fopen experiment, the
actual TASM emission order of these paired OMF fields matches
the historical original here. The source preserves the one
public _open at offset53, all **12 original CRT imports** in
their original EXTDEF order, empty DATA/BSS and literal
BSS-before-DATA GRPDEF 08ff03ff02.

Initial native assembly contained two unsymbolized original
absolute references (DOS error variable and exit hook) that
TASM correctly rejected. Replacing those instructions with
genuine DGROUP + named original data symbols restored the
original CODE and relocation fields naturally. Defining the
real DATA/BSS segment group before emitting the code permits
the original PUSH DS/POP DS and far LES/LDS behavior, without
adding NOP bytes, inserted PUSH CS instructions or patches.
The maintained source is instruction-level reconstruction:
real 8086 control-flow and symbolic imports, not an array
of the original executable machine code.

The scoped source-only native builder inherits the previously
reviewed 39-source CRT containing full stat556/4 DATA, fgets,
gets, fstat, both qsort bosses, the exception/RTTI xx,
original numeric scanner, path search and FILE I/O. It
assembles open at original member267 twice and uses genuine
TLIB/TLINK to reproduce the fixed **entire 67,372-byte
Japanese decoded MAINL EXE and original MAP bit-for-bit**,
with all **677 original MZ relocations**. **40 source
modules supply 22,170 exact original CODE bytes** while the
other **853 of893 original library member program records**
stay byte-identical.

The preceding fopen original BCC FIXUPP writer-order
difference and fclose one near TARGET-frame difference
remain open; source-only normal link exactness does not mean
all 40 OMF records are literal-original. This new open
member, however, is exact in complete CODE, PUBDEF/EXTDEF,
segment geometry and all ordered native OMF fields.
The accepted28-provider CRT, formally published211-owner
MAINL ledger, retained cold pair and Japanese target
candidate-local-attested identity remain unchanged.
No full cold, DIET or ancestor runtime replay occurred;
no accepted byte credit is claimed.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_open_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_open_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_open_work

Two complete source OBJ/LIB/EXE/MAP pairs and actual original
native phase logs are retained under .analysis/work/open-*,
along with mainl-open-native-{build,review}.json bound to the
current original source and native input targets.
