# MAINL registration pointer-array ownership checkpoint

This checkpoint preserves a genuine semantic C++ pointer-array producer, a source-only DATA ownership composer and retained native evidence. It changes neither the default graph nor source/exact counts.

## Evidence and limits

MRD02 compiled the genuine registration/music code plus REGIST_PLAYCHARS array. The array retained the original ten logical entries and used symbolic external string names. TC4 emitted the 2,788-byte CODE body and 40-byte DATA array, with all 61 CODE and ten DATA relocations matching their scoped target sequences. The literal mixed 71-entry OMF stream also matched, without sorting. Pointer values were unresolved at this compiler-only stage.

MRD03 freshly compiled and assembled root/tail successfully, but TLINK rejected duplicate absolute _address_0. The copied tail header had inherited BINARY='E', making ReC98.inc export the root-owned singleton twice. The failed receipt remains at .analysis/mainl-regdata-link-output-20261021-v01 and is not relabeled. A bounded traversal of all 22 header/include files identified this as their only BINARY use.

The source-only v02 successor removes only that tail BINARY definition. Root, CPP and response are byte-identical to v01. MRD04 then freshly compiled, assembled root, assembled tail and linked, with all four phases exiting zero and certain cleanup. The report at .analysis/mainl-regdata-link-output-20261021-v02/linked-verification.json verifies the complete program against both target and MRL01, every prior public address, header fields, all 677 relocation members, the mixed 71 literal pairs and six snow pairs. Global target-order differences are 460, down from 461; 348 positions changed relative to MRL01.

MRD04 EXE SHA256: aebb25bf414624ce32295428eae6b306800ed8ebabfd5ce5e024fe2a60950f98.
MRD04 root OBJ SHA256: 6e47509b3899003e27d96c5db2b5a5e7cdab7013243cc591a35dd27e16d639e4.
MRD04 MAP SHA256: 6581d6b5ebf0b1723383950e6a8d5aef5e1dce5b8875844a112ee01a93b1e732.

The nested legacy tail_shape.pass_shape field is false because that shared inspector tests root-specific segments. The actual tail acceptance gate checks.tail_data_shape is true and requires an empty CODE segment and exactly 888 DATA bytes. Preserve this distinction; do not claim that every nested boolean is true.

## Maintained source contract

src/mainl/hiscore/regdata.cpp preserves the registration/music body and defines the ten-pointer array in original logical order. All string bytes remain in the existing ASM owner. The compiler naturally emits its DATA fixups in reverse address order. No binary or relocation table is rewritten.

scripts/lib/mainl_regdata_backend.py exposes pure generate(root,response,cpp). It accepts only identity-pinned textual sources. The original 3,094-byte root DATA becomes three same-name, word-aligned PUBLIC _DATA contributions: root prefix 2,166 bytes at E480, compiler array 40 bytes at ECF6, and source ASM tail 888 bytes at ED1E. Startup DATA remains before these; every intervening direct project DATA contribution is empty; CRT DATA still begins at F096. Source labels provide typed cross-object interfaces, and ten semantic string aliases add no storage. The tail preserves all original strings, constants, pointer definitions and retained includes. The root alone owns _address_0.

No full cold build, second source-to-product repeat, new runtime run, canonical DIET packing, historical original-TU identity, global relocation equality, default graph promotion or exact acceptance is claimed. The tail's remaining 24 pointer relocations and other root producer grouping remain unresolved.
