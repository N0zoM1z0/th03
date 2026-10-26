# MAINL score-data: complete existing source ownership

2026-10-26; baseline `175c3ca`, no new implementation or native rebuild.
The bounded `review_th03_mainl_scoredat_work.py --current-cold` validates the
complete unchanged two-round native graph, then independently resolves this
producer. It writes its report atomically only after successful observation.
No new runtime harness or default ancestor replay chain is introduced.

## Native identity and ownership

Maintained `src/mainl/scoredat.cpp` is included by `th03/scoredat.cpp`.
Its actual first-use identity is GAME3 / BINARY'O' / first_binary'op', not'L'.
This is intentional shared build ordering. The header's O/L difference affects
only the unused load declaration; recreate's encode/save call remains near
Pascal. Do not force an L-mode recompilation to match the output's product name.
TC86 Borland C++4.02 object `obj/th03/scoredat.obj` SHA256:
`33aaa6f6f9a46fe950a183ae0b9dd6e8469a4e7fb5974094f1eb65697c17dfc0`.

The complete producer has one229-byte LEDATA, zero initialized DATA and BSS.
Three native publics at offsets0/60/187 coincide with complete nearRET0 bodies:

| CS start | Procedure | Bytes | Instructions |
| --- | --- | ---: | ---: |
|095F:17B9|scoredat_decode|60|25|
|095F:17F5|scoredat_recreate|127|51|
|095F:1874|scoredat_sum_invalid|42|22|

All15 fields are resolved in native order, not masked: fourteen C4/16 DGROUP2
external offsets address `_hi` at0E3F:21EE with literal addends, and one84/16
self-relative GROUP_01 external at object172 calls095F:1900. The local decode
call needs no external relocation. All229 resolved bytes equal target/candidate;
both scoped MZ relocation vectors are literally empty. Both MAP public tables,
complete allocation, group identities, three publics/two externals and complete
record inventory are independently checked. No padding or byte patches.

The actual compiler dependency comments include stddef.h, _defs.h and _null.h.
The complete installed SDK inventory and all938 repeated outputs remain bound
by the existing cold-source audit; no substitute header or host compiler is used.
All three bodies are fully decoded with branch boundaries and near call closure.
The adjacent registration bodies are checked as context without recounting them.
External206-byte `_hi`, encode/save body, music68 and pointerDATA40 receive no
new credit in this slice. Prior81 owner observations remain identical.

## Preserved semantics

Decode operates forwards over204 encrypted bytes including the checksum. Each
iteration uses the next still-encrypted byte, rotate-right3 and key2, then adds
key1 with BYTE wrap. The last byte uses key1+key2; key bytes204/205 remain plaintext.
No key validation or input sanitization is introduced.

Recreate fills ten reversed-name rows with period glyphs, score glyphs with zero,
playchar with none and stage with1. It sets the first default score's digit4 to1
and later rows' digit3 from9 down to1. It leaves the unknown byte untouched and
sets cleared18 before encoding each of four ranks, then decodes again. The
called MAINL encoder may change cleared using resident state; the local initial
assignment is not a promise that every saved rank remains uncleared. Initial key
bytes are not written by the local initializer; the external encoder owns its
key generation and file writes. No file-success or physical runtime claim.

Checksum validation sums all204 score bytes into uint16 and compares with the
stored WORD. Its bool result is in AL only; AH is not normalized or promised.
All functions are near noargs, with RET0. These behavior observations come from
maintained source and complete instructions, not a newly added runtime suite.

## Current acceptance

The new slice adds three owners/229 CODE, reaching84 extents/89 procedures and
12668 CODE+224 DATA. The live tracked namespace becomes180 rows. Frozen145-owner
eligibility and mock150 numerators remain unchanged. Existing tests only receive
necessary counter/fixture updates. OP/ZUN publications are refreshed because
status.py is shared, not because their source/native outputs changed.

Old current reports are preserved under `.analysis/work/mainl-scoredat-preserved`.
Current cold SHA remains
`746a2bc55f27efd72aac4fcba724baa2fec8da2f2f8b48de485ce266ffff67ef`.
Prior81-owner digest remains
`d739ff033f871dec669cef8a353a2e7bff549582bb9dc169be0e01ec1697fe95`.
Whole-product ownership, Factory registry acceptance and whole-game percentage
remain open. Final focused/fullCI terminal receipts are reported separately;
this document is not edited after those final gates.
