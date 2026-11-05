# Original exception-aware setjmp / longjmp runtime boss — after458

The original Japanese Borland CL.LIB member setjmp (slot **365**)
is now recovered in maintained [8086 ASM](../src/mainl/crt/setjmp.asm).
It contains two complete FAR entrypoints, _setjmp at CODE+0 and
_longjmp at +71. This is the real low-level 16-bit context restoration
runtime, not a conventional higher-level exception replacement.

The source saves the actual SS:SP, BP, IP:CS, FLAGS, DI, ES, SI, DS and
Borland exception-chain state to the caller's saved jump buffer.
The inverse longjmp rebinds SS:SP with the original interrupt-safe
flags transition, checks the current exception-chain head and invokes
the real __Global_unwind and __Local_unwind as required before
restoring saved register/segment state and issuing the original IRET.
The entrypoint/caller FAR ABI, 16-bit widths and exact saved-image
word ordering are retained. An original final compiler epilogue
appears after the IRET and remains expressed as a natural sequence.

All **214 original CODE bytes** and **four literal ordered original
OMF FIXUPPs** match, including CODE+55/+157 ->
__CurrExcContext, CODE+134 -> __Global_unwind and CODE+184
-> __Local_unwind. The actual PUBLIC offsets, original three
ordered import names, _TEXT segment and BSS-before-DATA GROUP
08ff03ff02 also match; DATA and BSS are empty. A copied new builder
descriptor initially expected _TEXTA; this was corrected to the
actual source/original _TEXT before native validation.

After458 inherits and checks the original after457 665-source
carrier and executes two fresh real TASM/TLIB/TLINK producer rounds.
Both complete Japanese decoded MAINL EXE and MAP are original-equal
(67,372-byte EXE, 677 ordered DOS MZ relocations). Raw OBJ/LIB/
EXE/MAP output pairs, logs and source hashes are retained.
The working CRT now contains **666/893 source-linked original
members** and **178,811 original-equal CODE bytes**, with 227
unchanged vendor members. This is scoped working source, not
independent full raw Borland OMF program identity, a full cold
replay or Factory accepted-source credit.

Focused review: scripts/review_th03_mainl_after458_work.py
(mode exception-aware-setjmp-longjmp-boss).
Tests: tests.test_mainl_after458_work.
