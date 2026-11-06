# Large isteldbl native parser: sign and integer digit acquisition, first 460 bytes

Japanese CL.LIB isteldbl (original slot 765) is a **1,947-byte CODE
large Boss** implementing the ten-byte long-double stream parser
used by the separately recovered float/double extraction wrappers.
It has a single original FAR public, 14 bytes of DATA and a
complex control flow across streambuf, ios state and x87 arithmetic.
The [maintained original 8086/x87 partial source](../src/mainl/crt/isteldbl_integer_prefix_partial.asm)
now reconstructs the **first 460 consecutive CODE bytes**.
This is meaningful source, not an assembly opcode-array dump:
it calls the original istream ipfx helper, fetches/refills the
real streambuf (including original FAR virtual call and snextc),
detects sign and EOF, calls ios setstate on EOF, initializes the
ten-byte FAR numeric destination with genuine x87 fldz/fstp,
classifies digits using the actual __ctype table, and loops
over integer digits using x87 multiply-by-10, fild and faddp.

**Bounded exactness:** 458/460 native bytes are original-equal.
The only two excluded original bytes are CODE+30/+31, the
relative displacement of the initial near jump from CODE+29
to the as-yet-unrecovered EOF/exit block at CODE+0x78F.
The partial source deliberately uses a genuinely unresolved
near symbol parser_eof, so TASM emits a symbolic near relocation
and zeros those two bytes. It does not invent the rest of the
function body, manufacture the original relative displacement,
insert padding, or patch an OBJ. The native 460-byte code
segment ends exactly at original CODE+0x1CC, where the remaining
fraction/exponent parsing must be reconstructed. An external
source cannot yet be linked as a complete member.

All **16 original OMF symbolic references** in this prefix
match TASM sites, imports or DATA segment target identities,
kinds, widths and addends. The one additional TASM near
relocation at CODE+30 is only for the deliberately unresolved
parser_eof target; it does not occur in the full Borland
member. Nine original x87 frame-method-4 references compile
as method 5. The original four DATA bytes at +0..3 (typed
10.0f) are exact; the other ten original DATA bytes and all
original CODE+460..1946 remain open.

The [independent scoped verifier](../scripts/probe_th03_isteldbl_integer_prefix_partial.py)
assembles the maintained source **twice with real TASM** under
the Borland writer lock, verifies all 458 original-equal CODE
bytes and the two explicitly excluded operands, all 16
original symbolic relocations, first four DATA bytes and
nonvolatile native OMF stability. Targeted test:
tests.test_isteldbl_integer_prefix_partial_native.

**Not yet a complete member:** The outstanding 1,487 CODE bytes
include fractional digit handling, exponent parsing, long-double
normalization, error paths and return. This partial large-Boss
scope earns **zero** complete CRT source-linked or formal Factory
accepted units. No full MAINL link or cold replay is claimed.
