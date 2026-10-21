# MAINL DIET packing diagnostics

This is a packing calibration and source-product diagnostic, not an ownership or
exactness promotion. MAINL remains 145/145 source units, 28,381 source bytes,
and zero formal exact units.

## Actual native observations

The pinned DIET 1.45f default command, `DIET.EXE MAINL.EXE`, was run on two
fresh private copies per experiment. Both experiments also ran the vendor
selfcheck and restored separate copies of both packed outputs with `-RA`.
The original inputs and packed outputs were preserved. Each phase was headless,
one CPU, nice >=10, with a 90-second native limit and 15-second owned cleanup.
All ten phases completed with certain cleanup and released their writer locks.
Selfcheck returned 0; each single-file compression/restoration returned 1 with
`Success!`. Exit 1 is this observed tool convention, not a waived build error.

- Target-fed positive control: decoded input 67,372 bytes,
  SHA256 `92600c8858bb407516cac6a9d77538ebdf0c33522c4f6bd9194d569eb927134a`.
  Both compressed outputs equal the canonical stored target, all 37,975 bytes,
  SHA256 `5b613023b4ae021794ff778871a732e7af0d0457ccdb3613e3458f2a609e466c`.
  Both restoration outputs equal the complete decoded input.
- Source-fed experiment: actual repeated CRT-integrated MCO02 executable,
  67,372 bytes, SHA256
  `6d159b90fffe0d0ac00d587429204fa616228abc7244ee4c4e184449a2fdde63`.
  Both compressed outputs are 38,048 bytes, SHA256
  `c87a7ace64a9a6c3356921df2eeee41f645d2f850a46e651f9bc60df840a5567`.
  They differ from the canonical packed target at 2,259 raw byte positions,
  including the 73-byte length difference. Both restore exactly to the source
  input, not to the target-derived decoded image.

The source input differs from the target-derived decoded executable at 1,377
raw file byte positions. Its program image differs only at linear 60,473
(DATA 0E3F:0849, target 90h versus source 00h). Relocation membership is equal,
but 461 ordered relocation entries differ. The exact restoration of the source
input proves this DIET route does not canonicalize away that relocation order.
The packed differences cannot be attributed exclusively to the DATA byte.

## Meaning and remaining gates

The available default packer can reproduce the historical packed envelope when
fed the corresponding decoded target. No alternative compression flags or
output patches are justified by these observations. The next natural producer
questions are the genuine EVEN fill and original relocation ordering.

The positive control is target-fed and cannot count as authored reconstruction.
The source-fed input is a proved composed source product with retained cold-built
context; this packing experiment is not a new whole-project cold build.
Restoration uses separate invocations of the same vendor tool, not an independent
DIET decoder. Canonical packed mapping, producer/layout gates, and the complete
acceptance criteria remain unchanged. No target, object, executable or packed
output was patched, and no source/exact totals change.

## Replay

`config/mainl_diet_packing/proof.json` pins both native manifests, launch scripts,
actual phase receipts/logs/registry snapshots, source/tool inputs, raw products,
and the source-product provenance. Run:

    .venv/bin/python3 -B scripts/replay_th03_mainl_diet_packing.py

The replay verifies 175 pinned files, actual five-phase chains for both roles,
semantic exit conventions, complete raw compression comparisons and roundtrips.
It does not invoke native tools or grant acceptance credit. Detailed packed-byte
differences remain in the pinned ignored native receipt rather than copied into
maintained product source.
