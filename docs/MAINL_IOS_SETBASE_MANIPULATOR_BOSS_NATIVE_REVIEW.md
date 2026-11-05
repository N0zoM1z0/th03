# Complete Borland ios setbase manipulator and FAR setter boss — after476

The original Japanese Borland CL.LIB mnsbase member (index **790**) is
recovered as real [8086 source](../src/mainl/crt/mnsbase.asm).
It comprises an actual private FAR ios::basefield setter at CODE+0
and public FAR @setbase$qi at CODE+110. The former maps the original
base-16, base-10 and base-8 manipulator integers onto 40h, 10h
and 20h flags, calls the real @ios@setf$qll with the original
@ios@basefield mask, and returns the native FAR ios pointer.
The latter conditionally allocates an original six-byte C++ object,
installs the genuine private FAR setter pointer as both a segment
and offset relocation, stores the requested base integer, and
returns the original FAR manipulator result.

All **205 original CODE bytes** and the genuine symbol/segment/GROUP
layout are original-equal, including the private function's original
0..109 span, one public at +110 and the true ordered imports.
All **six logical OMF FIXUPPs** match site, target, frame, width
and addend: CODE+72/+76 read the actual global basefield mask;
+91 calls ios::setf, +151 invokes far new, and +173/+178 contain
symbolic CODE segment/offset pointers to the original private
setter. The Borland/TASM literal packet chronology differs,
and raw original OMF module identity is not claimed. No
target executable-byte fixtures, filler or post-OBJ rewrites.

After476 validates the unchanged after475 source-bound 683-member
parent and produces two fresh native TASM/TLIB/TLINK rounds,
preserving all OBJ/LIB/EXE/MAP artifacts, logs, source/driver
hashes and original metadata. Both full decoded Japanese MAINL
EXE/MAP are original-equal (67,372 EXE bytes, 677 ordered MZ
relocations). Working CRT **684/893** source-linked original
members, **182,684 original-equal CODE bytes**, 209 contextual
vendor members. No full cold replay or new formal Factory
acceptance is implied.

Focused review: scripts/review_th03_mainl_after476_work.py
(mode cxx-ios-setbase-manipulator-boss);
tests: tests.test_mainl_after476_work.
