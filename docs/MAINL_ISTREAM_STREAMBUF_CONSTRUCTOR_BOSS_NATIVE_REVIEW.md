# Complete original `istream(streambuf*)` constructor and RTTI — after423

The original Japanese Borland CRT member `istctr2` (index 752) was
contextual in the 616-source after422 carrier. Its entire far C++
constructor is now maintained as natural 16-bit ASM in
`src/mainl/crt/istctr2.asm`. Unlike the related `ostream` constructor,
this allocates **46 bytes**, locates the `ios` base at offset **+6**,
initializes the actual input streambuf interface, sets the extra input
state word at object+4, and uses a **six-byte `this` adjustment** for
its local far destructor thunk at CODE+143. The source also constructs
complete typed Borland `istream` RTTI at CODE+155, inherited `ios` RTTI
at +221, a genuine far destructor symbol and the original 20-byte DATA
vtable/adjustor pointer records.

Native TASM reproduces **275/275 CODE bytes, 20/20 initialized DATA
bytes**, original `_TEXTA`/`_DATA`/`_BSS` sizes, DATA-first group,
public/import symbols and **all 13 complete logical OMF FIXUPP fields**.
The original 13 Borland records and TASM records occur in different
literal chronology; this does not establish byte-identical original
member program serialization. No target machine-code arrays or object
patches were used.

`scripts/build_th03_mainl_after423_work.py` inherits the unchanged after422
source-bound native receipt and performs two fresh TASM/TLIB/TLINK rounds.
Both complete Japanese decoded MAINL EXE and MAP are byte-for-byte equal
(67,372-byte EXE, 677 ordered DOS MZ relocations). Working CRT rises to
**617/893** source members, **169,781 original-equal CODE bytes**, and
**276** unchanged contextual vendor members. This is scoped native equality,
not full cold replay or Factory accepted-source credit.

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after423_work.py istream-streambuf-constructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after423_work -v
```
