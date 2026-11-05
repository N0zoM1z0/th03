# MAINL `stdiobuf(FILE*)` constructor: full C++ metadata boss

Recover the **complete original** Borland CL.LIB member `sdbctr` (member
825) rather than just a constructor entry point. The original Japanese
OMF object contains 345 CODE bytes (`_TEXTA`), 52 initialized DATA bytes,
zero BSS and 23 logical relocation fields. Its one far public is
`@stdiobuf@$bctr$qn4FILE`; there are 19 original far C++ imports.

The natural source `src/mainl/crt/sdbctr.asm` includes:
- Heap allocation on null `this`, construction of the streambuf base,
  assignment of the caller's far `FILE*`, the 516-byte backing allocation,
  and far `setb` / `setp` / `setg` calls with original register/stack
  conventions and unchecked allocation paths.
- The two **typed** `stdiobuf` and `streambuf` Borland RTTI descriptors
  residing in CODE after `retf`; the class-name strings, descriptor words,
  far destructor pointers and linked base-class reference are source
  declarations, not raw machine CODE arrays.
- The actual **52-byte initialized DATA vtable**, with its far RTTI pointer,
  two preamble words, and eleven far virtual method slots.

An initial trial produced 344 CODE bytes because it omitted the *second*
zero after the `stdiobuf` null-terminated name. The original OBJ proves
both bytes at CODE+263..264; preserving that Borland RTTI field-alignment
byte restored the complete 345-byte native member and the internal
relocation addend at CODE+265 to original class CODE+285. This corrects a
source-layout error, not an object patch or a forged filler region.

## Native evidence boundary

`scripts/build_th03_mainl_after321_work.py stdiobuf-constructor` consumes
the source/receipt-bound 321-member parent and rebuilds only this member,
with normal TASM/TLIB/TLINK. It checks raw outputs in **two independent
rounds**, preserving the entire original Japanese decoded MAINL EXE/MAP
and all 677 ordered DOS MZ relocation entries. The library now has **322
complete original-source CRT members** with 571 contextual vendor members
and **105,871 original-equal CRT CODE bytes**.

Both original and assembled member have the same CODE and DATA bytes,
SEGDEF/PUBDEF/EXTDEF/GROUP identities and 23 site/target/frame-equivalent
fixups (eleven in CODE and twelve in DATA). The literal OMF **FIXUPP
record order is still not equal**, so this is *not* byte-identical
Borland-object serialization or a formal packed-unit/Factory acceptance.
`review_th03_mainl_after321_work.py` and
`tests.test_mainl_after321_work` enforce the precise scoped claim.
