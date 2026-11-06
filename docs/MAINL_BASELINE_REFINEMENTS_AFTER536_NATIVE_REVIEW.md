# MAINL baseline PUBLIC and GROUP refinements after536

This stage improves two existing owners; **new source members and new CODE
credit are both zero**. The compiler-library union remains 893 source-bound
slots / 209,272 original-equal CODE bytes. The affected existing owners contain
178 CODE and 91 DATA bytes. The frozen cold sources and receipts are unchanged.

`src/mainl/crt/h_padd_link.asm` retains the original huge-pointer addition and
subtraction instructions and six near/far exports. The pinned compatible
JWasm emitter now preserves the original **ordered PUBLIC symbol payload**:
`F_PADD@, N_PADD@, F_PSUB@, N_PSUB@, PSUB@, PADD@`. Its SHA-256 is
`31883da383c3889f19d039fe47f0fce0619b21ae90fd7fee9f33b79ddce1070e`.
All 96 original CODE bytes, segment attributes and GROUP agree; there are no
relocation fields. PUBDEF record packing and SEGDEF LNAMES indices differ,
so original OMF-record/program identity is not claimed.

`src/mainl/crt/ioerror_link.asm` preserves the original 82 CODE / 91 DATA bytes
and both near callee-pop helpers. Reversing TASM's GROUP operands produces
the original literal BSS/DATA group enumeration. All five complete relocation
fields remain equal at their sites. Their original order `22,28,45,39,51`
still differs from the emitted `22,28,39,45,51`; the full literal streams and
PUBLIC-order difference remain recorded. No ordered FIXUPP equality is claimed.
The unchanged `crt_errno.inc` and `dos_error_map.inc` are source-bound.

Two fresh assembly/TLIB/TLINK rounds adopt these objects in their original
slots 72 and 79. All **891 other member programs and all 893 member positions**
are unchanged. Each round reuses the source-generated C0 from after535 and the
unchanged game objects, without cold replay. Both whole raw two-OBJ/LIB/EXE/MAP
vectors repeat. The complete 67,372-byte Japanese EXE, including the original
677 ordered MZ relocations, remains byte-exact.

The native MAP is deliberately **not** claimed byte-identical to the historical
80,893-byte retained MAP. The complete new 80,967-byte MAP differs only by:

1. `F_PADD@` and `PADD@` exchanging display order at the **same** address
   `0000:3182`, with identical idle flags. This follows the original compiler
   PUBLIC chronology. It is the same bounded tie seen in the after529 probe.
2. The corrected `ioerror` GROUP exposing its real **zero-length** `_BSS`
   owner at the existing address `0E3F:286A`, between `getvect` and `isatty`.

The comparator checks exactly that literal alias exchange and exactly that
literal zero-extent row; every other MAP byte, address, size and flag must
agree. It does not broadly sort/normalize the MAP or rewrite either artifact.
The historical MAP remains intact. The previous after529 candidate was left
separate because of the alias tie; after536 explicitly reviews that tie and
closes the PUBLIC-order question rather than calling it a changed code layout.
This creates no duplicate source credit.

Producer: `scripts/build_th03_mainl_after536_work.py`.
Independent reviewer: `scripts/review_th03_mainl_after536_work.py`.
Emitter scope: `config/th03_mainl_baseline_refinements.toml`, with the unchanged
pinned JWasm tool attestation. This is not an original-assembler identity claim.

Root: `.analysis/work/mainl-after536-baseline-refinements-build.json`.
SHA-256: `c2b2853f4bddda4a73e2e01c8a78fe407c6a32e35b0f41ed8a6217f306de831d`.
New MAP SHA-256:
`ece28f0b816a0b519b1628aade5dc01069a6c0852aa99d37cb671f12c78b6a14`.
Both raw vectors and native logs use **af536f-baseline-refinements-** paths.
`probe/af536f` retains all actual sources, includes, source objects, extracted
library inputs, immutable recipe/profile and both library/link responses.

The first native round already matched the EXE, but the original MAP comparator
omitted the zero-BSS row and correctly stopped. Its complete raw outputs, logs,
inputs and incomplete receipt remain, with **21 SHA-inventoried snapshots** at
`.analysis/work/probe/baseline-zero-BSS-map-correction/manifest.json` and original
`probe/af536e`. Earlier bounded `af536a` C compilation produced 101 rather than
82 CODE bytes and was not adopted; alias/two-pass probes `af536b`/`af536c` did
not repair FIXUPP order. `af536d` checked the compatible PUBLIC emitter. All
those sources, objects and logs remain. No output cleanup was performed.

Independent native review, progress/tracking and whitespace checks pass.
No runtime matrix, ancestor runtime review, full CI or native cold rebuild was
run. Formal canonical Factory acceptance remains **0/250**; remaining literal
OMF gaps, including after535 startup ordering, are still explicit.
