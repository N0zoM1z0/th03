# Original large cplx2: twelfth complete FAR log10(complex) function

Japanese Borland CL.LIB cplx2 is a 5,598-CODE-byte, 22-public
complex math boss. The [maintained native 8086/x87 partial source](../src/mainl/crt/cplx2_twelve_functions_partial.asm)
now implements twelve complete original FAR bodies: three division
operators, acos, arg, asin, atan, cos, cosh, exp, log and log10.

The new log10(complex) at original CODE+2708..2867 is **160
byte-identical CODE bytes**. It calls the authentic local log(complex)
through PUSH CS plus the native near call, then multiplies both
result components by a typed double conversion constant and constructs
a FAR 16-byte return value with original optional heap allocation.
Its original DATA+28..35 contains 1/log(10) represented as the exact
IEEE double 0x3fdbcb7b1526e50e. A short decimal literal initially
compiled one binary unit too low in TASM; defining a full-precision
natural decimal value 0.434294481903251816667932416748954 yields
exact original DATA bytes, without copying a target-byte array.
All 20 actual original initialized DATA bytes at +16..35 match;
the 16 preceding DATA bytes remain truly unmaterialized.

The original twelve-function CODE prefix is 2,868 bytes and native
TASM emits 2,866. Only the two pre-existing acos local FAR calls
at original CODE+799 and +984 are one byte shorter as
PUSH CS plus near CALL than the original direct FAR CALL.
All other 2,858 native CODE bytes match. Of 435 original
prefix FIXUPPs, 433 TASM-emitted fields match site after
these shifts, target symbol names, widths and addends.
The two original local FAR-call fixups remain unrepresented
and 377 original Borland FPU location-frame method-4
references compile with TASM method 5. These differences
are recorded, not silently normalized or accepted as raw OBJ equality.

The [scoped source verifier](../scripts/probe_th03_cplx2_log10_partial.py)
runs two genuine TASM rounds under the writer lock, independently
compares the original CODE, typed DATA and symbolic relocation
sites/targets, and verifies stable nonvolatile OMF record data.
Focused test: tests.test_cplx2_log10_partial_native.

This is **partial large-Boss source**, not a complete CRT library
member. Another 2,730 CODE bytes and ten FAR procedures remain,
along with the complete original DATA/INITDATA records and exact
original frame-4 metadata. It does not add any full source-linked
CRT member or Factory accepted-source credit, and is not a full
MAINL native link. No full cold replay was run.
