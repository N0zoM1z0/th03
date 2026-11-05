# Original three integer/radix string conversion APIs — after486

Japanese Borland CL.LIB ltoa1 (original slot **253**) is now recovered
as [maintained 8086 source](../src/mainl/crt/ltoa1.asm).
It contains three complete FAR entrypoints: _itoa at CODE+0,
_ultoa at CODE+47 and _ltoa at CODE+80, all forwarding the
original 16-bit Borland argument/return ABI to the real near
__LONGTOA helper. The signedness flag differs for decimal
radix 10 versus the other radices, including the original
CWD sign extension of 16-bit _itoa and 32-bit _ltoa input.
The character base 'a', native FAR string pointers and both
16-bit halves of long values are retained in the original
callee argument order.

All **124 original CODE bytes**, zero DATA/BSS, three
original public offsets, the one ordered __LONGTOA import,
and original three-segment/GROUP layout match.
The complete logical OMF site/type/width/target/addend
fields also match at CODE+41/+74/+118. Each original
Borland imported NEAR call has TARGET-frame method 5,
whereas TASM outputs the equivalent CODE segment frame
method 0. These **three specific sites and import 1**
are the only permitted differences in the scoped builder,
and every other original field is individually asserted
by the reviewer and test. Literal Borland FIXUPP equality
and complete raw original OBJ identity are not claimed.
There are no target executable-byte arrays or object patches.

After486 validates its unchanged after485 693-source carrier
then performs two fresh TASM/TLIB/TLINK native rounds,
preserving both raw OBJ/LIB/EXE/MAP pairs, writer logs,
source hashes and the original parent receipt.
Both complete Japanese decoded MAINL EXE/MAP match
their targets byte-for-byte (67,372 EXE bytes and
677 ordered MZ relocations). Working CRT now has
**694/893** original source-linked members,
**184,344 CODE bytes**, 199 contextual vendor members.
No full cold replay or formal Factory source credit.

Focused reviewer: scripts/review_th03_mainl_after486_work.py
(mode integer-radix-string-three-entrypoints).
Tests: tests.test_mainl_after486_work.
