# TH03 DIET storage and decoded namespaces

The canonical Japanese targets stay at the ignored paths pinned by
`config/targets.toml`. This review does not replace them with decoded or patched
images. Stored Ghidra databases were re-attested with `scripts/ghidra.py` before
observations. Their loaded bytes are the stored images, not the decoded game
functions. Independent pristine-dump provenance remains unknown.

## Observed storage and restoration

OP, MAINL and ZUN each have a 32-byte stored MZ header, zero stored relocations,
CS:IP 0000:0000, and the four-byte `diet` marker at file offset 001C. Their
stored entry saves registers/flags, copies the extraction code and returns far
into that code. Those instructions belong to the storage layer. Decoded CODE
addresses and relocation entries cannot be substituted into that database.

| Artifact | Stored bytes / format | Restored bytes / format | Restored header | Restored MZ relocations |
| --- | --- | --- | ---: | ---: |
| OP.EXE | 36041 / MZ | 63866 / MZ | 4096 | 607 |
| MAINL.EXE | 37975 / MZ | 67372 / MZ | 4096 | 677 |
| ZUN.COM | 16242 / MZ | 22812 / flat COM | none | none |

The decoded SHA-256 values are:

- OP: `efd858aef69a240af3a27c747a5beae150f55f0b41b8afdd1eda1760a759ecc0`
- MAINL: `92600c8858bb407516cac6a9d77538ebdf0c33522c4f6bd9194d569eb927134a`
- ZUN: `83b034a59fabfd0c4dd48e44a4be5287ac1ea6ea0c0e9677311071113eff9e26`

MAIN is already an unpacked MZ target and is not passed to this decoder.
MAINL remains TH03's ending product. ZUN has a stored MZ envelope even though
its restored launcher is a real COM file; its decoded entry is PSP:0100.
The latter is the standard COM load convention, not a discovered function ABI.

## Tool observations and recipe

The existing private DIET executable is 26370 bytes, SHA-256
`a3fabbb9e4209ca6654c34f1d0945868732422dff6fe0a7fe0f5bcd2d48d2803`.
Its console banner identifies version 1.45f; `-!` reports its original-file
selfcheck and exits zero. The bundled `DIET145F.DOC` documents `-RA` restoration
of executable SFX files. For these single-file restorations, the observed exit
code is 1 with a `Success!` message. A return code alone never establishes
success: the replay also checks each complete decoded SHA-256, size and format.

`config/th03_diet.toml` pins this diagnostic tool and output identities.
`scripts/review_th03_diet.py` first attests the console runner/toolchain, then
runs only on fresh private copies in a new 8.3 directory inside the game-local
Wine prefix. It freezes configuration/script inputs, checks tool identity and
selfcheck, verifies the full restored images, and rechecks every original target
and tool/config input afterward. Outputs and receipts live under ignored
`.analysis/th03-diet/`. It does not load DIET as a TSR, launch the game, alter
an original target, or promote an automatic function.

```sh
python3 scripts/review_th03_diet.py --run-id NEW_UNIQUE_ID
# Optional bounded selection:
python3 scripts/review_th03_diet.py --run-id ANOTHER_NEW_ID --artifact th03-op
```

Runs `sol-diet-restoration-20261006-a` and `sol-diet-restoration-20261006-b`
restored all three inputs in independent workspaces and produced identical
complete decoded bytes. Both record unchanged canonical targets. The second
also freezes the final script/config inputs. An earlier disposable probe
incorrectly assumed every successful DOS tool must return zero; the tool had
already restored OP correctly. The replay now records the observed convention
and independently validates every output, rather than rerunning on a changed
canonical file or accepting a status message by itself.

## Upstream binding and acceptance limits

At frozen ReC98 revision `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th03_op.asm` records input MD5 `661f4f8ffaf1f3274f503d154133def0` and
`th03_mainl.asm` records `ce44aa7a114237c6b3cd67eea9c0225a`. The full restored
OP and MAINL files have those respective MD5 values; the stronger decoded
SHA-256 values are independently recorded above. The replay reads the original
frozen Git objects and checks the quoted input hashes. This binds the generated
scaffolds to the restored target images. It grants neither authored progress
for disassembly nor an independent exactness Oracle. The restored ZUN MD5 is
`61b9be6641b0a0146e1a02ac1f863fad`; no generated-root input-MD5 binding is claimed
for its source-generated launcher/component pipeline.

The configured source/link scaffold builds unpacked products, so a comparison
against a compressed canonical file mixes distinct namespaces. The products from the maintained MAIN aggregate's frozen scaffold also fail
complete raw equality against the decoded images: OP has a different file/header size, MAINL has raw differences, and
flat ZUN differs by ten bytes. These compiler/linker observations are separate
from the restoration facts and cannot be promoted as whole-product builds.
The replayable comparison receipt is
`.analysis/sol-diet-reference-comparison-20261006.json`.

Next review must use full decoded function boundaries, source owners,
near/far/tiny/large ABIs, DGROUP/data layouts and original decoded relocation
order, with explicit lineage back to the immutable stored targets. The
repository's current exact policy still requires file-backed owned extents in
the canonical artifact. No decoded function is marked exact or assigned a
fabricated stored-file offset by this review. Original packing/stub ownership
and storage-to-source acceptance remain open. Runtime extraction has not been
independently executed or compared; the current observation is vendor-tool
restoration with full byte/format guards, not gameplay runtime equivalence.
