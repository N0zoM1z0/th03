# Unbuilt after555 research — handoff only

The user stopped reconstruction for handoff maintenance. **No after555 builder,
native output, accepted owner or progress update was produced.** The last
validated source checkpoint is `e7697e1` / after554. Fifteen draft input files
were copied byte-for-byte, SHA-256 checked and removed from the product tree.

Private archive: `.analysis/handoff/after555-unbuilt/`.
Manifest: `manifest.json`, SHA-256
`4f606b05eeb89e19c8e7d211a4fc6e666a94b46f3379a7891bf542cf0a5ef596`.
The archive contains the original relative paths, byte counts and file hashes.
It is plain files, not a compressed/repacked native-evidence archive.

## Established observations

The current ownership-gap audit leaves1864 DATA bytes inside the contextual
`obj/th03/mainl.obj`, plus one registration trailing byte. This is not all
authored game data. The root object has9 segments: CODE10944, DATA2036,
BSS5108 and six empty CODE contributions. Its complete literal field stream
has392 entries, including two local near-pointer DATA fields at offsets0/2
with DGROUP frame1, target segment2 and addends632/639.

The first778 DATA bytes contain stage/shot state, character titles/names,
script names and resource filenames. Existing consumers prove `SHOT_FN[12]`;
its additional zero bytes belong to that declared buffer. Mutable stage
pointers and text scratch buffers must remain mutable.

The source comments for A. Koizuka's public-domain master.lib tables specify
`atan(n/256)*128/pi` for256 bytes and `sin(2*pi*n/256)*256` for320 signed words.
Nearest-integer evaluation matched every existing native table element in a
read-only comparison. Cosine aliases sine storage at+128 bytes (64 angles).
The archived generator reads no target, object or reference data. It has
**not** been used in a native product build.

Actual native DATA write coverage has holes at offsets0748–0767 (the32-byte
`bfnt_header <>` reservation),0782–0783 (`_cdg_noalpha`) and07F3 (final alignment).
The header and alpha state are file-backed DATA reservations, not initialized
bytes or BSS. Do not report them as initialized DATA.

## Draft, not accepted accounting

The draft config hypothesizes16 disjoint source extents totaling1859 bytes:
900 authored and959 supplier/library bytes. Of these,1825 are initialized and
34 are file-backed reserved DATA. Five unresolved padding positions
045D/04A3/0737/076F/07F3 remain excluded. These figures are investigation notes,
not source-exact progress, and need independent review before publication.

A prospective native stage would assemble the root carrier with bounded
maintained DATA includes, keeping the frozen CODE/BSS context unchanged.
It must retain actual after554 text-bank objects, after553 picture C object,
after552 root C++ object and after548 source C0/library. Compare the complete
OBJ field stream, initialized write map/holes, all PUBLIC definitions/layout,
the entire original EXE and all677 ordered MZ relocations. Never patch an
object or fill unexplained bytes to force equality. New source needs two
native output rounds; unchanged cold/runtime chains need no replay.

Restore a draft only after verifying every archive hash and checking that the
destination has no existing user changes. Fix hypotheses from actual native
evidence; do not treat the draft config as an acceptance oracle.
