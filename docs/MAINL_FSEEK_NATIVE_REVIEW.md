# Real DOS fseek/ftell: complete 492-byte semantic source

The maintained native 8086 source src/mainl/crt/fseek.asm and original
stdio_layout.inc recover the actual selected Borland CRT fseek member232.
It comprises a private near Pascal text-buffer adjustment helper
(137 CODE bytes, RET 4), public far _fseek at137 (130 bytes), and
public far _ftell at267 (225 bytes). Original FILE fields, LF text
translation, buffer adjustment, _fflush, _lseek and __openfd handling
are preserved as actual symbolic 16-bit instructions.

Actual native TASM generates all 492 original CODE bytes, the original
DATA0/BSS0, public offsets137/267, import order _fflush/_lseek/__openfd
and exact DATA-before-BSS GRPDEF. Crucially its **six original OMF
FIXUPPs are in the genuine selected 893-member CRT's literal order:
342,149,239,293,365,409**. The field at342 targets the original
group-framed __openfd+1 byte;the other five are TARGET-framed far
_fflush/_lseek calls.

A distinct standalone original vendor/fseek.obj has the same 492 CODE
bytes and six logical relocation sites/targets but a different OMF
record order **409,365,342,293,239,149**. This genuine difference
must not be hidden: earlier attempts to match the standalone
object with reversed source blocks would regress compatibility with
the real original CRT member. The maintained readable source with
FILE macros reproduces the *selected actual library member*, which
the current reviewer checks alongside the standalone vendor variant.

Rebuilding the original 893-member CRT with this source and all 30
previously verified source modules leaves the other **862 original
library member program records** untouched. Two real TASM/TLIB/TLINK
rounds reproduce the complete original **67,372-byte Japanese decoded
MAINL EXE and native MAP byte-for-byte**, with all **677 MZ
relocations**. The cumulative exact native source CODE extent is
**19,832 bytes across31 modules**.

The original accepted28-provider library, frozen211-owner MAINL
publication and candidate-local-attested fixed Japanese target
remain unchanged; source-only normal-link exactness does not grant
formal accepted byte credit. No full cold or DIET replay was run.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_fseek_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_fseek_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_fseek_work

Both complete source native OBJ/LIB/EXE/MAP rounds and actual
writer logs are retained in .analysis/work/fseek-full-* and
mainl-fseek-native-{build,review}.json.
