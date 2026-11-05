# Original DOS Ctrl-Z trim/append and private seek/read helpers — after481

The original Japanese Borland CRT member zapctlz (slot **153**) is
now maintained as [natural 8086 source](../src/mainl/crt/zapctlz.asm).
Its 189-byte original CODE contains four complete functions:
two private DOS file helpers at CODE+0 (seek to EOF minus one)
and CODE+24 (read a single byte), and the public near
__TRIMCTLZ at CODE+64 and __APPENDCTLZ at CODE+136.

The actual code uses DOS INT 21h 4202h/3Fh/40h paths to test and
remove or append the text-mode Ctrl-Z (1Ah) sentinel, restores the
original saved DOS file position and invokes the real FAR _lseek
with original word parameter order for a required final seek.
The tiny private helpers preserve their native near caller-pops-
two convention, SS buffer addressing, and exact 16-bit stack
layout. This is not substituted by host platform file I/O.

All **189 original CODE bytes**, zero DATA/BSS, both public
offsets, sole ordered FAR _lseek import and BSS-before-DATA
GROUP match. The native source reproduces its single **literal
ordered original OMF FIXUPP** at CODE+123, including FAR width,
target index and frame method. No executable target-byte
array, filler instructions or object mutation is used.

After481 verifies the entire unchanged after480 688-source
CRT parent, then performs two fresh native TASM/TLIB/TLINK
rounds, preserving all raw OBJ/LIB/EXE/MAP vector outputs,
writer logs and source hashes. Both full Japanese decoded
MAINL EXE and MAP are byte-for-byte original-equal:
67,372 EXE bytes and 677 ordered MZ relocations.
The working CRT advances to **689/893** source-linked
original members and **183,539 CODE bytes**, leaving
204 contextual vendor members. This is bounded working
source, not Factory accepted-source credit or full cold replay.

Focused reviewer: scripts/review_th03_mainl_after481_work.py
(mode dos-text-stream-ctrlz-helpers-boss);
tests: tests.test_mainl_after481_work.
