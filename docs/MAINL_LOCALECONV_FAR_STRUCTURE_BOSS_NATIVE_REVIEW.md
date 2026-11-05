# Original Borland localeconv FAR structure and monetary flags — after466

Original Japanese CL.LIB member lconv (index **242**) is now
recovered in natural [8086 source](../src/mainl/crt/lconv.asm).
The FAR __llocaleconv implementation reads the live __pLocale
object, sets up all ten original far strings in the 48-byte
__localeconvention structure (including the source offsets
+218h/+21Ah/+224h/+1CCh/+1D1h/+1D6h/+1D8h/+1DDh/+1E2h/+1E7h),
and copies all eight monetary and formatting fields at
locale offsets +1ECh..+1F3h to output offsets +40..+47.
It returns the original segment:offset of the structure.

Every one of the **212 CODE bytes** matches the original, as do
the complete public name, exact two ordered imported globals,
_TEXT/_DATA/_BSS segments and DATA-first GROUP. All **41 logical
OMF FIXUPPs** match original sites, lengths, frames, targets
and addends (including the true byte destinations from 40 to 47).
TASM differs from Borland in its original literal FIXUPP
packet order, and raw original OBJ-program identity is not
claimed. The source uses meaningful symbolic FAR locale field
assignments, not a byte fixture or a post-processing patch.

After466 independently verifies the after465 673-source parent
and produces two fresh native TASM/TLIB/TLINK rounds with raw
OBJ/LIB/EXE/MAP outputs, original source hashes and logs retained.
Both complete decoded Japanese MAINL EXE and MAP exactly match
the target, including 67,372 EXE bytes and 677 ordered MZ
relocations. Working CRT **674/893** original source-linked
members, **180,860 CODE bytes**, with 219 contextual vendor members
remaining. No full cold replay or new Factory source credit.

Focused reviewer: scripts/review_th03_mainl_after466_work.py
(mode localeconv-far-string-structure-boss).
Tests: tests.test_mainl_after466_work.
