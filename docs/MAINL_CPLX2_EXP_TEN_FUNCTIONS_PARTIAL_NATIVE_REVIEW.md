# cplx2 tenth complete FAR exp(complex) body — original bytes and OMF

Japanese Borland CL.LIB cplx2 (slot 209) is a 5,598-byte CODE
member with 22 FAR math and stream routines. The
[maintained partial source](../src/mainl/crt/cplx2_ten_functions_partial.asm)
now reconstructs **ten entire FAR functions**: three division
operators, acos, arg, asin, atan, cos, cosh and exp.

The new **exp(complex)** body at original CODE+2358..2563 is
**206 CODE bytes exactly matching** the Japanese original.
It performs the true FAR _exp of the complex real part,
FAR _sin and _cos of the imaginary part, multiplies both
by the exponential result using native x87 FPU operations,
and writes the original 16-byte complex result into the
hidden FAR destination or one allocated through the genuine
Borland FAR new helper. All stack/FPU ABI and original
return register behavior are maintained without embedded
target-opcode fixtures or post-assembly patches.

The first ten complete routines occupy original CODE+0..2563:
**2,564 original bytes**. TASM emits **2,562 CODE bytes**,
owing exclusively to the same two explicitly disclosed
intra-segment acos call differences: original CODE+799
and +984 use five-byte direct FAR CALL, where native
TASM emits four-byte PUSH CS and near CALL. Excluding
those two local call sequences, **2,554 aligned native
CODE bytes are original-equal**, including the new exp body.

There are **405 original CODE FIXUPPs** in this prefix;
all **403 emitted TASM fields** agree in logical site
(after shifts), target symbol name, location kind, size
and addend. Two original local CODE FAR-call fixups remain
absent, and **353 original Borland location-frame method 4**
FPU references compile as method 5 with TASM EMUL. These
are openly retained original/compiled serialization
differences, not an assertion of complete original OMF
or raw Borland OBJ identity.

The [scoped checker](../scripts/probe_th03_cplx2_exp_partial.py)
uses two independent native TASM rounds and cross-checks
all original CODE and symbolic fixups, plus the nonvolatile
OMF records. Focused tests:
tests.test_cplx2_exp_partial_native.

**Still unfinished:** 3,034 original CODE bytes, 12 later
FAR functions, full DATA and INITDATA, original location-frame
serialization and two local direct-FAR-call encodings.
Therefore cplx2 is **not a complete source-linked CRT member**
and contributes zero formal Factory/canonical credit.
No full MAINL native link or cold replay is claimed for
this deliberately partial large-boss source.
