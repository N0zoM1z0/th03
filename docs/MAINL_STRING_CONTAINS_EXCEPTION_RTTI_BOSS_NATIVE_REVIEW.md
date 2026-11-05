# Original string::contains C++ exception scope and typed string RTTI — after487

Japanese Borland CL.LIB member contain (index **397**) is
fully recovered in [maintained 8086 source](../src/mainl/crt/contain.asm).
This is not a simple leaf call: the 200-byte _TEXT segment
contains its real 32-byte Borland C++ exception/unwind frame
at CODE+0..31, the complete FAR @string@contains$xqnxc
public at CODE+32..141 and the typed string class RTTI
at CODE+142..199. It constructs a temporary string from
the actual FAR char pointer, calls the original
string::find(const string&, unsigned), converts -1 into
the native bool result, destructs the temporary with
the real FAR string destructor and unwinds the exception
scope through the original Init/ExitExceptBlocks routines.

All **200 CODE bytes** (including actual typed exception metadata
and string RTTI) are byte-for-byte original-equal. The
source emits the original CODE+4 pointer to the CODE+142
string type descriptor, CODE+18 unwind pointer to CODE+0,
the original CODE+30 frame offset and CODE+41/44 exception
context references, rather than storing a raw target CODE
blob. The class descriptor at CODE+172 has a real far
string destructor reference. All **11 logical OMF FIXUPPs**
match the original at precise segment/site/frame/target/addend,
including the genuine far constructor, find, destructor and
exception frame calls. The import list and public ABI are exact;
the original TASM/Borland literal FIXUPP packet chronology
still differs, so full original raw OBJ identity is not claimed.

An initial disassembly hypothesis set the local exception
state at [BP-22h] instead of the authentic [BP-16h].
CODE byte comparison found the one-byte wrong displacement
at CODE+53, and the source expression was corrected before
any native integration. No target-byte arrays, dummy padding
or OBJ mutations were introduced.

After487 checks the entire inherited after486 **694-source**
carrier before two fresh TASM/TLIB/TLINK native rounds.
Both complete decoded Japanese MAINL EXE and MAP are
byte-for-byte original-equal (67,372 EXE bytes, 677 ordered
MZ relocations). Raw OBJ/LIB/EXE/MAP vectors, writer logs,
source hashes and the original parent receipt are retained.
Working CRT: **695/893** original source-linked members,
**184,544 CODE bytes**, 198 contextual vendor members.
This is bounded working-source evidence, not a full cold
replay or new Factory accepted-source credit.

Focused reviewer: scripts/review_th03_mainl_after487_work.py
(mode string-contains-exception-rtti-boss).
Tests: tests.test_mainl_after487_work.
