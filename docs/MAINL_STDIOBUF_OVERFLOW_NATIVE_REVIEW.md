# MAINL Borland `stdiobuf::overflow`: original member source recovery

The Japanese MAINL CRT's original selected `CL.LIB` member 827,
`sdboflow`, was examined as an **entire** native OMF object, not as a
function snippet or a synthetic linked-output patch. It defines precisely
342 CODE bytes in `_TEXTA`, zero DATA/BSS, one far public
`@stdiobuf@overflow$qi`, and three far externs:
`@streambuf@setp$qnct1`, `@streambuf@setg$qnct1t1`, `__fputc`.
The literal `DGROUP` is `08ff02ff03`, independently checked against
the original object.

The recovered `src/mainl/crt/sdboflow.asm` uses symbolic 8086 instructions
and control-flow labels. The body includes FILE error handling, pending
put-area flush via buffered/direct `__fputc`, conditional insertion of the
new character, restoration of get/put area boundaries, and a final FILE error
check. Original signed buffer count tests, far pointers, caller cleanup and
unchecked pointer assumptions are left intact.

## Narrow native verification

`scripts/build_th03_mainl_after319_work.py stdiobuf-overflow` uses an
unchanged 319-source parent receipt chain and rebuilds only this new member
with native TASM/TLIB/TLINK; it **does not cold-rebuild** the historical
parent product. Two independent actual native output rounds contain:

- All 342 original CODE bytes equal, with the same segment, public, extern,
  and DGROUP definitions; no DATA/BSS contribution.
- Four original 32-bit far fixup sites at CODE offsets 142, 214, 273, 307;
  their targets, frames and addends match site-for-site.
- 320 original-source CRT member replacements out of 893; 573 unchanged
  vendor members; entire decoded Japanese MAINL EXE and MAP byte-equal in
  both rounds, including all 677 *ordered* MZ relocation entries.

The original **literal OMF FIXUPP record order differs** (original writes
sites in descending order; TASM writes ascending); it is not claimed equal.
Link equality does not prove original Borland object-record serialization or
automatically add Factory-accepted source ownership. The review and focused
tests read original member bytes and both raw retained rounds:
`review_th03_mainl_after319_work.py` and
`tests.test_mainl_after319_work`.
