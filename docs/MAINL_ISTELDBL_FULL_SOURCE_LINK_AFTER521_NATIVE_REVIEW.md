# Complete isteldbl long-double parser — after521

Original Japanese Borland CL.LIB member **765, isteldbl**, is now maintained
in [isteldbl.asm](../src/mainl/crt/isteldbl.asm): **1,947 complete CODE bytes,
14 initialized DATA bytes, zero BSS**, and the original far
`istream::operator>>(long double&)` public entry.

This completes the historical 754-byte fractional prefix. Its unresolved
initial near jump now reaches the real return epilogue at CODE+0x78F.
The recovered tail implements optional signed exponent parsing with actual
streambuf refill, 32-bit exponent accumulation capped at 49,320, combined
exponent clamping to +/-493,200, x87 exponentiation by squaring with overflow
checks, range saturation, ERANGE, mantissa sign, and fail/eof stream flags.
Original unchecked input and ABI behavior are preserved.

The original DATA consists of typed 10.0f and an 80-bit scale near 10^2466.
TASM's decimal conversion of `1e2466` is 11 ULP below Borland's stored scalar;
the source therefore uses a single typed hexadecimal real literal for that
extended value. It contains no target instruction arrays, padding, or object
patches. All original CODE and DATA bytes match without exclusions.

All **112 logical OMF fields** match their original sites, kinds, symbols,
segments, widths and addends. **85 original x87 references use Borland frame
method 4 where TASM emits method 5**. Original threaded FIXUPP enumeration also
differs from TASM order. Complete literal raw FIXUPP equality and original OBJ
program-record identity remain explicitly **false**; the member's byte and
symbolic-field proof does not hide these differences.

The [incremental native producer](../scripts/build_th03_mainl_after521_work.py)
extends the unchanged after520 source-bound pair. Native TLIB extracts the
893 inherited members; only the new parser is assembled, and TLIB/TLINK
rebuild the library/link in two rounds. Each round preserves all 728 earlier
source members and 164 remaining vendor members. Both rounds reproduce the
**entire 67,372-byte Japanese decoded MAINL EXE and original MAP**, including
all **677 literal ordered MZ relocations**. OBJ/LIB/EXE/MAP rounds are identical
to each other and retained with all writer logs.

The [independent reviewer](../scripts/review_th03_mainl_after521_work.py) binds
source/recipe hashes, the parent receipt, complete member contents, logical
fields, native writer logs, library membership, and both full EXE/MAP vectors.
It recomputes the raw FIXUPP inequality rather than granting original OBJ
identity. No new emulator specification or full cold replay is needed for
this complete native-byte/codegen question.

Current working-source CRT: **729/893 complete members, 196,239 original-equal
CODE bytes**. This adds one complete member and 1,947 CODE bytes; the old
unlinked partials had never earned member credit. Formal Factory canonical
packed-file acceptance remains **0/250**; whole-game completion is unknown.

Receipt: `.analysis/work/mainl-after521-istream-long-double-parser-build.json`

SHA-256: `80c78e22d99044c9087fc40ccd9094a5f3eb5cc15a9854736e0c1e03281ab33c`.

After521 native outputs and scratch are retained. The applied after520 cleanup
guard now fails closed; no native evidence deletion was performed.
