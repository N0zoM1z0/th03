# Eight original Japanese MBCS, far-string, BGI and C++ leaves — after411

The original `CL.LIB` members `MBCLEN`, `FMBCLEN`, `MBSNINC`, `FMBSNINC`,
`fstrset`, `fnsplit`, `gregistr` and `srbstr` were checked *against the
actual 579-source after410 carrier* and were not already source-linked.
Their complete original maintained 16-bit ASM was preserved from the
existing working tree and integrated into the native proof chain. In all,
**335 CODE bytes** are reproduced without original executable byte arrays.

These are genuine ABI programs: Japanese near/far MBCS byte-length tests
using the original `__mbctype` flags; far-pointer MBCS advancement through
the real bounded byte counters; far string filling via `__fstrlen` and
`__fsetmem`; the full far `_fnsplit` argument forwarding; separate BGI
far driver and font registration; and the `strstreambuf::str()` C++
method with its original freeze call and far buffer result. All original
public names, imported dependencies, CODE/DATA/BSS segments, group membership
and original logical OMF relocation fields (including all frame/target
methods) are verified per member.

**Six of the eight** members reproduce literal *ordered* original Borland
FIXUPPs as well. For `fstrset` and `gregistr`, the full original logical
relocation population matches, while TASM emits a different FIXUPP record
chronology. Neither an original raw library-member program match nor any
new Factory accepted-source/packed-file credit is asserted.

`scripts/build_th03_mainl_after411_work.py eight-mbcs-string-bgi-leaves`
reuses the unchanged after410 native receipt, then performs two independent
actual TASM/TLIB/TLINK rounds, retaining raw OBJ/LIB/EXE/MAP and logs.
Both complete decoded Japanese MAINL EXE/MAP equal their originals byte
for byte (67,372-byte EXE with 677 ordered MZ relocations). The maintained
working CRT reaches **587/893** source-linked members, **165,913 original-
equal CODE bytes**, with **306** remaining unchanged vendor-context members.
No full cold replay was performed.

Focused verification:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after411_work.py eight-mbcs-string-bgi-leaves
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after411_work -v
```
