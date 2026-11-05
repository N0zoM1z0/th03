# Original strstreambuf dynamic doallocate paths — after446

Japanese Borland CL.LIB member srbdalc (index **840**) is now complete
in maintained [8086 source](../src/mainl/crt/srbdalc.asm). The virtual
strstreambuf::doallocate function obtains a dynamic allocation size
or the original default 16; it honors the installed far allocator
callback by passing a sign-extended count, and otherwise invokes the
original new-array allocation. After allocation, it clears the
requested-size field, registers the far range with streambuf::setb
and writes the initial NUL, returning exactly the original success
or failure result. The unchecked 16-bit offset addition and callback
ABI are preserved rather than replaced by defensive behavior.

All original **141 CODE bytes** and the exact public/import and
segment/GROUP layouts agree; there is no DATA. Both original logical
OMF FIXUPPs match: new-array at CODE+61 and setb at CODE+118.
Their literal packet order differs between Borland and TASM; full
original vendor OMF record equality is not claimed.

After446 independently verifies the previous after445 653-source
carrier and produces two fresh native TASM/TLIB/TLINK rounds, with
all native writer logs, source hashes and complete OBJ/LIB/EXE/MAP
pairs retained. Both full decoded Japanese MAINL EXE and MAP equal
their original targets, preserving the 67,372-byte EXE and 677 ordered
DOS MZ relocations. Working CRT **654/893** members,
**176,156 original-equal source CODE bytes**, 239 contextual vendor
members. This is working source evidence, not formal Factory
accepted-source credit or a full cold replay.

Review: scripts/review_th03_mainl_after446_work.py
(mode strstreambuf-dynamic-doallocate);
tests: tests.test_mainl_after446_work.
