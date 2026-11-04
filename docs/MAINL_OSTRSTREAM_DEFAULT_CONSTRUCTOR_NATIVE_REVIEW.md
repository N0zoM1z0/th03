# Original Japanese CRT `ostrstream` default constructor (`osrctr2`)

Actual selected Borland CRT member **801** (`osrctr2`) has a complete
**616-byte `_TEXTA` CODE** section, **28-byte initialized DATA**, zero
BSS, one far public `@ostrstream@$bctr$qv` at CODE+0 and 11 ordered
original imports. It is distinct from the already sourced `osrctr1`
member: the `ostrstream` default constructor owns a different entrypoint,
base constructor sequence and original exception/unwind table.

`src/mainl/crt/osrctr2.asm` reconstructs the full far constructor as
native 8086 instructions: `ios` and `strstreambase` construction, ostream
binding, original far streambuf ownership and native destructor counts.
After the executable body ends at CODE+176, **two actual executable
12-byte far destructor-adjustor thunks** preserve the original `EA` far
jumps. Remaining CODE is authentic typed Borland RTTI for `ostrstream`,
`ios`, `ostream`, `strstreambase`, `strstreambuf` and `streambuf`, including
readable class names, true relocatable `dw`/`dd` pointer descriptors, and
original 28-byte DATA exception fields. No copied executable machine-CODE
arrays, padding or native OBJ patches are used.

Independent TASM `/m /mx /kh32768 /t` reproduces **616/616 CODE bytes**,
**28/28 DATA**, full segment/public/import ABI, and all **27 OMF fixups**
at their original segment/site/type/target/addend/frame. BCC and TASM
serialize these in different **record order**; complete original OBJ
byte identity is not claimed.

`build_th03_mainl_after258_work.py ostrstream-constructor` adds this selected
member to the source-bound 258-source Japanese CRT. **Two independent normal
TASM/TLIB/TLINK rounds** reproduce the complete original **67,372-byte
decoded Japanese MAINL EXE and MAP byte-for-byte**, preserving **677 ordered
MZ relocations** and **634 untouched original vendor CRT member records**.
The working CRT reaches **259 members / 96,681 original-equal CODE bytes**.
This does not grant formal accepted-ledger credit; no full cold replay ran.

Proof: `review_th03_mainl_after258_work.py ostrstream-constructor`,
`tests.test_mainl_after258_work`, raw native output pairs and writer logs
under `.analysis/work/after258-*`.
