# Original tied istream(streambuf*,ostream*) constructor and typed RTTI — after427

Japanese Borland `CL.LIB` member **istctr3** (index 753) is recovered in
natural 16-bit ASM at `src/mainl/crt/istctr3.asm`. The complete far
`@istream@$bctr$qn9streambufin7ostream` constructor allocates an original
46-byte object if needed, constructs its `ios` base at `this+6`, installs
its actual DATA vtable and initializes the given stream buffer. Unlike
`istream(streambuf*)`, this overload also invokes the real `ios::skip`
and `ios::tie(ostream*)` imports and performs the original **22-byte**
combined argument cleanup. It then increments the true 32-bit destructor
reference count.

All **305 CODE bytes and 20 initialized DATA bytes**, including the
local CODE+173 FAR destructor this-adjustment thunk, `istream` RTTI at
+185, inherited `ios` RTTI at +251, the original public, eight ordered
imports, segment layout and DATA-first GROUP, match the live original.
The **15 logical OMF FIXUPP fields** all match site, width, frame, target
and addend. The additional imported `ios::skip` and `ios::tie` targets
at CODE+120 and +138 are independently checked; literal Borland-vs-TASM
FIXUPP chronology and raw member-program serialization remain distinct.
No target machine-code bytes were stuffed into executable source or patched
into object files.

The after427 source-bound producer inherits and validates the unchanged
after426 parent, then performs two actual fresh TASM/TLIB/TLINK rounds.
Both decoded Japanese MAINL EXE/MAP are byte-for-byte original-equal
(67,372-byte MZ and 677 ordered relocations), with full writer logs and
native OBJ/LIB/EXE/MAP retained. Working-source CRT becomes **623/893**
members, **170,978 original-equal CODE bytes**, with **270** unchanged
contextual vendor members. Full cold replay and Factory source acceptance
were not invoked or claimed.

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after427_work.py istream-tied-stream-constructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after427_work -v
```
