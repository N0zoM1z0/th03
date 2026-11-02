# Full Borland DOS putc subsystem: 974 CODE, 1 DATA, 1 BSS and 46-source link

The original Japanese DOS Borland CRT putc module (member271) is now
maintained as complete 8086 source in src/mainl/crt/putc.asm.
It contains four genuine original public routines:

| Routine | CODE offset | Native source bytes |
| --- | ---: | ---: |
| far __fputc | 0 | 32 |
| far _fputc | 32 | 395 |
| far _fputchar | 427 | 24 |
| near __FPUTN | 451 | 523 |
| **Total** | | **974** |

The complete native source preserves the original FILE count/
cursor/limit fields, buffered and direct-output modes, stdout
stream table lookup, DOS text CR/LF conversion and flush rules,
device status flags, partial write handling and multi-byte
buffer copying using the genuine far _fflush, ___write,
_lseek, __rtl_write and _memcpy services. No byte-array
substitution, synthetic executable padding or altered DOS
error semantics are introduced. Its one actual initialized
DATA byte is a carriage return (0Dh);its one original BSS
byte stores the transient output character.

Native TASM5 reproduces **all 974 original CODE bytes**,
the original DATA byte and **all 29 literal ordered OMF
FIXUPPs**. The four PUBLIC offsets, seven imported
names/indices, CODE974/DATA1/BSS1 ownership and literal
DATA-before-BSS GRPDEF 08ff02ff03 all agree.
The 29 fields retain their actual descending original
record order. They include GROUP-framed BSS byte/real DATA
references, __openfd+1 and __streams+20, genuine
TARGET-framed far external calls, and the original internal
far CALL to _fputc at CODE+21.

The internal CALL was a significant original codegen trap:
under TASM ASSUME CS:_TEXT, even explicit CALL FAR PTR
_fputc was optimized into **PUSH CS + near CALL**,
shortening the generated body by one byte and suppressing
the original OMF far-field record. An explicit DGROUP
qualification restored all original CODE bytes but made
the far field GROUP-framed (method1) rather than the
original TARGET frame (method5). Real TASM trials showed
the source-only solution: a zero-byte
ASSUME CS:NOTHING at this specific call followed by
CALL FAR PTR _fputc. This preserves the actual 5-byte
far CALL and original TARGET-frame internal segment1
relocation, without inserting instructions or patching
an OBJ. Different equivalent source forms were compiled
and reviewed; the correct declaration/ASSUME is retained
and independently checked by the reviewer.

The 974-byte source member was assembled twice at original
index271 alongside the **45 previously reconstructed CRT
source members**, including complete xx, both large qsort
algorithms, numeric scanner, DOS stream input, directory
subsystem, stat/open/file metadata and string functions.
The other **847 original CRT member program records** remain
byte-identical. Both actual native TASM/TLIB/TLINK rounds
reproduce the **entire 67,372-byte decoded Japanese MAINL
EXE and original MAP bit-for-bit**, preserving all **677
original MZ relocations**. The simultaneous 46-source
working CODE extent is now **23,777 exact original bytes**,
plus the original putc DATA and BSS owners.

The previous fopen literal FIXUPP-order discrepancy and
fclose near __MKNAME frame discrepancy are still OPEN in
those separate predecessor members. The complete product
link is exact, but it is not a claim that all 46 objects
match original OMF metadata. The putc OBJ itself does have
complete original ordered FIXUPP equality. The accepted
28-provider CRT, formal 211-owner MAINL ledger, fixed
candidate-local-attested Japanese targets and retained
cold pair remain untouched. No newly credited accepted
bytes or full cold/DIET replay are claimed.

Affected-only native reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_putc_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_putc_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_putc_work

Real native repeated OBJ/LIB/EXE/MAP vectors, all compiler
phase logs, source and target hashes and full source-bound
receipts are retained under .analysis/work/putc-*
and mainl-putc-native-{build,review}.json.
