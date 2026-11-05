# Actual large cplx2 boss reconstruction, first three complete FAR division functions

The original Japanese Borland CL.LIB **cplx2** member (index 209) is
the major **5,598-CODE-byte, 22-public C++ complex math boss**.
This work reconstructs its first **three entire FAR complex division
functions** as meaningful native 8086/x87 source at
[src/mainl/crt/cplx2_divisions_partial.asm](../src/mainl/crt/cplx2_divisions_partial.asm):

- CODE+0 through +165: complex::operator/=, 166 source-equal bytes.
  Normalizes a complex divisor using original norm(), conjugate
  multiplication and 80-bit x87 extended temporaries.
- CODE+166 through +404: complex/complex division returning a
  hidden FAR output object, 239 source-equal bytes. It uses
  actual Borland complex multiplication, normalization and
  conditional 16-byte FAR result allocation.
- CODE+405 through +691: double/complex scalar division, 287
  source-equal bytes, with correctly preserved real/imaginary x87
  operations, the original FAR output ABI and conditional allocation.

**692 original CODE bytes are completely byte-identical** when
independently assembled with original TASM 5 using the genuine
EMUL directive. No target-machine-byte arrays, binary patches
or filler CODE were used. The complete original *prefix* has
**97 FIXUPP sites**; all source-emitted sites, kinds, widths,
target symbol identities and addends compare exactly with the
true Japanese CL.LIB member. This includes original calls to
norm(), complex::operator*=, complex operator*, the FAR
allocation function and all real FIDRQQ/FIWRQQ/FIERQQ x87
emulation references. The public ABI offsets +0/+166/+405
also match exactly.

**The original OMF framing is not fully matched.** Exactly
**90 of these 97** original FIXUPPs use Borland frame method
4 (frame of the location), whereas TASM EMUL emits frame
method 5 for them. Both the literal original field values
and native generated field values are retained and compared,
with no normalization pretending that these are byte-identical
OMF fields. The other seven original method-5 fixups remain
method-5 in the source OBJ. Resolving the location-frame
difference is further work before complete original member
source parity can be claimed.

The focused script
[scripts/probe_th03_cplx2_divisions_partial.py](../scripts/probe_th03_cplx2_divisions_partial.py)
builds this actual source twice with native TASM under the normal
serialized writer lock. It validates every CODE byte and
reidentifies targets by the original and generated EXTDEF
names, independently of reordered external indices.
Every emitted relocation is checked against the original,
and all nonvolatile OMF records are identical between runs.
TASM automatically writes a COMENT 40E9 build-time stamp:
one clock byte legitimately differs between two raw OBJs.
That discrepancy is explicitly detected and reported, not
hidden by claiming equal raw OBJ hashes.

**This is partial large-boss progress, not a full CRT member.**
The remaining 4,906 CODE bytes, 19 later public functions,
the whole original 63-byte DATA segment (including 16 implicit
sites), six-byte INITDATA, 763 further FIXUPPs and final
library/EXE integration are NOT recovered in this scope.
Accordingly the working CRT source-member count remains
**680/893** (after472), *not* 681/893; no new Factory/canonical
source credit is claimed and no full cold replay was run.

Reproduce with narrowly scoped commands:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_cplx2_divisions_partial.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_cplx2_divisions_partial_native -v

This addresses a major previously unimplemented native boss
rather than only selecting short original library leaves.
