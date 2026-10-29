# OP shared CDG and text native source review

2026-10-29: two complete TC4 producers now have current OP CODE ownership:
CDG593 plus text613, six procedures/1206 CODE bytes/41 native fields/27 literal
ordered MZ relocations. Both producers have zero private DATA/BSS. These two
existing OP extents are accepted separately; MAINL ownership is unchanged.

| Procedure | OP CS-relative offset | CODE | Native return cleanup |
| --- | --- | --- | --- |
| CDG single | 05DA | 138 | Far Pascal8 |
| CDG single without alpha | 0664 | 134 | Far Pascal8 |
| CDG all | 06EA | 230 | Far Pascal6 |
| CDG all without alpha | 07D0 | 28 | Far Pascal6 |
| CDG free | 07EC | 63 | Far Pascal2 |
| graph_putsa_fx | 082B | 613 | Far Pascal10 |

## Actual OP source and native bindings

The two native wrappers literally include `src/shared/formats/cdg_load.cpp`
and `src/shared/graphics/text.cpp`. The latter consumes the complete bounded
`text_glyph.inl`. Every native source/header dependency is bound to the current
source graph and staged file. The five consumed TC4 headers (`mbctype.h`,
`ctype.h`, `_defs.h`, `mbstring.h`, `_null.h`) are also compared against the
pinned installation, whose full toolchain surface is checked with the cold pair.

The native CODE segment is BYTE-aligned SHARED, outside an OMF group; the sole
group is DGROUP over the empty DATA/BSS segments. Complete allocations, publics
and both OP MAP public tables are checked. CDG's35 native fields and text's six
native fields are resolved from the actual OP MAP, then the entire resulting
CODE and literal ordered MZ streams are compared with the Japanese target and
current candidate. No native object or executable is patched.

The unchanged MAINL layout modules supply shared producer-shape metadata:
literal field streams, procedure boundaries and text dependency identities.
They supply no OP linked addresses. CDG's existing native shape parser also
checks the earlier-defined all-loader's compiler bridge; its MAINL comparison
image is discarded. The OP verifier begins again with its own raw native CODE
and resolves every field independently. Actual OP and MAINL objects differ;
neither equal object hashes nor MAINL acceptance are assumed.

## Real far-call bridges

Four source calls to the forward-defined `cdg_free` are emitted as genuine
same-segment far CALL fields. Normal TLINK emits NOP/PUSH CS/CALL near, keeping
the CS word required by the far return and producing no MZ segment entry for
these calls. The target `CDG_FREE` public and every displacement are checked
against the OP MAP. The comparison-buffer transformation never edits an object.

The backward call from the noalpha wrapper to the earlier all-loader is already
PUSH CS/CALL near in TC4 output, without a fixup or separator NOP. Keep the
distinction between this compiler bridge and the four linker bridges. The
other24 CDG far CALL fields retain their complete ordered MZ entries.

## Original CDG behavior

CDG slots are16-byte records in external storage. Single-image loads free the
slot first, read the header, seek to the requested image and allocate/read the
planes. The image-size multiplication by5 wraps to16 bits before widening;
the index multiplication and seek retain their32-bit behavior. Color allocation
and read sizes also retain the original16-bit multiplication by4.

The all-loader frees subsequent slots using the first header's BYTE image
count, copies its geometry/count into each slot, and sets the plane layout
before loading. Its shared noalpha flag selects either alpha allocation or a
skip with a null alpha segment. The wrapper sets the flag, calls the loader
and clears it. Free visits both segment handles, frees nonzero handles and
clears each one. Preserve this sequence, unchecked files/allocations/indexes
and shared flag behavior. The external flag/slot storage is not owned by these
CODE extents.

## Original text behavior

The613-byte function fully decodes to226 instructions through RETF10. Its
50-byte native stack frame includes the16-row WORD glyph buffer. Color occupies
the low four effect bits; weight uses bits4..5 and spacing bits6..8. It enables
GRCG RMW and CG ROM dot access, then classifies each byte with the actual CRT
tables, including the native plus-one table offsets.

Lead bytes call the far cdecl Shift-JIS converter, with explicit caller cleanup.
Kana and printable single-byte characters use the original alternate JIS rows;
other bytes become the original space codepoint. Invalid converted codepoints
still reach the ports. No new validation is inserted. Halfwidth glyph rows
occupy the high byte of a WORD. Fullwidth rows combine both ROM halves.

Weight operates in16 bits, retaining the original loss of new dots beyond the
left edge. Aligned rows write two VRAM bytes; shifted rows write three and
advance by80 bytes. Signed coordinates, right-edge checks, lack of vertical
clipping and the original string advancement remain. The final CG ROM mode and
GRCG-off calls are preserved. Three external far calls yield three ordered MZ
entries. CRT tables/conversion and GRCG services remain contextual, with no new
library or physical-font/device credit.

## Checks

```sh
PYTHONPATH=scripts .venv/bin/python -m lib.op_shared_native
.venv/bin/python -m unittest tests.test_op_shared_native tests.test_op_work_acceptance
.venv/bin/python scripts/publish_th03_op_work_scopes.py
```

Use one CPU, nice10 and empty displays. The unchanged native cold pair is
revalidated, without compiling/linking again. Focused checks reject identical
incorrect classifier fields, identical corrupted linker bridges and reordered
MZ entries. No new runtime matrix is required for these native source scopes.
