# Six original Japanese MBCS near/far string-span and bounded comparison APIs

The complete original Japanese CL.LIB members for multibyte `strspn` /
`strcspn` and `strncmp` functionality now have real symbolic 8086 source,
including the original near/far calling conventions and DBCS lead/trail
scanning. These are not empty wrappers or byte arrays copied from the
pinned object; every complete loop, count and comparison path is present.

| Original CRT member | CODE | Native far public |
| --- | ---: | --- |
| `MBSCSPN` (604) | 194 | `__mbscspn` |
| `FMBSCSPN` (660) | 194 | `__fmbscspn` |
| `MBSSPN` (630) | 194 | `__mbsspn` |
| `FMBSSPN` (686) | 194 | `__fmbsspn` |
| `MBSNCMP` (620) | 180 | `__mbsncmp` |
| `FMBSNCMP` (676) | 180 | `__fmbsncmp` |

All **1,136 original CODE bytes** and **12 literal ordered original OMF
FIXUPPs** match the actual pinned Japanese library, including group frame1,
`__mbctype+1` target and addend. Span functions use original relocation
sites `[145,49]`, while the bounded comparators use `[99,34]`, each in
original descending Borland FIXUPP order. All complete original public
names, exact entry offsets, `_TEXT`/DATA/BSS segment sizes, group
`08ff02ff03` and zero initialized DATA/BSS match. The source emits genuine
original 8086 instruction blocks at original offsets using symbolic `ORG`,
not machine CODE byte arrays or patched OBJ/EXE records. The complete
Borland original OMF record serialization still differs from TASM in
ancillary metadata, and full member OBJ equality is **not** claimed.

`scripts/build_th03_mainl_after372_work.py japanese-mbcs-span-and-length`
consumes the complete **452-source** original CRT parent, assembles only
these six changed members and reconstructs all **893 original CL.LIB slots**
and the decoded Japanese MAINL link with native TASM/TLIB/TLINK in **two
independent rounds**. Both reproduce the original **67,372-byte EXE and
full MAP byte-for-byte**, including all **677 ordered DOS MZ relocations**.
The live working CRT reaches **458 complete source-backed members**, **435
unchanged original contextual library programs** and **145,085 source-built
original-equal CODE bytes**, an increase of **1,136**. Source/parent/driver
SHA receipts, whole raw OBJ/LIB/EXE/MAP pairs and writer logs remain under
`.analysis/work/after372-*`, with independent checks at
`scripts/review_th03_mainl_after372_work.py` and
`tests/test_mainl_after372_work.py`.

This is scoped working-source evidence, not formal Factory acceptance or
canonical packed-unit source ownership. No full cold replay was executed.
