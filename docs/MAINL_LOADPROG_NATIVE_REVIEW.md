# MAINL program resolution and load preparation

`src/mainl/crt/loadprog.asm` recovers the complete member: 871 CODE +40 DATA
bytes, with three procedures. These are library bytes, not authored game code.
Previous 183 owners and nested scopes remain unchanged.

## Source behavior and ABI

The private 132-byte far cdecl separator scan skips DBCS trail bytes, returns a
far pointer to an ordinary matching delimiter, and returns null for no match
or an unmatched final lead byte. Its original 16-bit offset increments remain.
The private 137-byte far cdecl probe keeps its unchecked 80-byte candidate buffer,
appends the requested suffix and either searches PATH or directly checks access.

The 602-byte near cdecl __LoadProg coordinator suppresses PATH search for drive
or separator-qualified names. Explicit suffixes are checked directly; suffixless
names probe COM, EXE, BAT in that order. BAT requires COMSPEC and the /c path.
It retains the original 156-byte frame, containing a 128-byte result path and
28 bytes of pointers, flags and results. Named ENOENT/ENOMEM/E2BIG constants come
from the actual preserved CRT errno include.

Real near DOSCMD/DOSENV providers prepare command and environment allocations.
The 128-byte command threshold, environment fallback, original deferred argument
cleanup and error/free paths are unchanged. A real far buffer-cleanup callback
runs before the near executor callback. The latter takes three far pointers,
exactly the 12-byte near callback ABI of the recovered overlay executor. Original
unchecked pointers, path copies and indirect calls gain no defensive fixes.

## Exact native production and composition

Two actual TASM assemblies, normal TLIB library builds and TLINK links reproduce
complete raw OBJ/LIB/EXE/MAP vectors. The whole EXE equals the pinned Japanese
decoded target; the whole MAP equals the retained MAP byte for byte. New loadprog,
reused natural exec/farheap objects and six retained source providers now coexist
as nine source CRT members in the same normal library. All 893 member positions
and all 890 other current member payloads are unchanged. Thirty-six project
objects are reused. Neither older source pair is rebuilt.

The complete initialized CODE/DATA payload equals the original compiler member.
All 32 native fields resolve independently, including 14 genuine external far
calls naturally relaxed by actual TLINK. The old compiler and TASM emit these
fields in different orders. Both literal streams are retained; field geometry,
identity and addends are checked by site without reordering either stream or
sorting MZ relocations. Only two explicit equivalent frame changes on the near
constructors are allowed. Complete literal scoped MZ vectors are empty.

The near callback reads its supplied code offset; the far cleanup callback reads
a pointer from DGROUP. Neither operand is a segment immediate. Private far helper
calls keep their natural same-CODE forms. All full bodies, return conventions,
local branches and callback boundaries are checked against actual native output.

## Group layout and real DATA

Native BYTE CODE, WORD DATA/empty BSS, the exact original DATA/BSS group member
order, the public entry and both MAP tables are checked. A trial reversed group
order added an empty BSS line. Correcting the source group order made that line
disappear naturally; no MAP row is masked. Explicit DGROUP-qualified string
offsets retain the original group frames and actual DS addressing.

All 40 DATA bytes are semantic strings: PATH, slash/backslash separators, an
empty suffix, two distinct BAT suffix instances, COM/EXE suffixes, COMSPEC and
/c. Their NUL terminators and duplicate BAT instances are genuine source data.
No filler, target-byte arrays, object edits or BSS file-byte credit is used.

All 938 retained cold outputs, source, recipe and tools remain validated and
unchanged. Only this source and affected combined library/links were rebuilt;
there was no full cold, DIET or ancestor runtime replay. The full cold recipe
still replaces six CRT members; this selected recipe composes the three newer
providers. Whole-product source ownership and physical DOS behavior remain open.

Actual private inputs in `.analysis/work/`: `mainl-loadprog-build.json`,
`mainl-loadprog-native.json`, `loadprog-source.asm`, `loadprog-errno.inc`,
`loadprog-library.rsp`, `loadprog-link.lnk`, both
`loadprog-roundN.obj/.lib/.exe/.map` vectors, and the retained farheap/exec pairs.
