# Original OP IRAND: maintained symbolic assembler source

`src/op/libs/random.asm` reconstructs the original 42-byte far `IRAND` at
OP decoded CODE `0000:1D12`. This is the original master.lib 8086 random
routine: multiply the persistent 32-bit seed by `0x015A4E35`, add one, store
both seed words and return the upper fifteen bits in AX. The original seed
DATA remains in the adjacent library data owner. The register, carry and
far-return behavior remains the native assembly, not a C++ approximation.

The original OP assembler includes master.lib's `random.asm`. The scoped
`probe_th03_op_irand_source.py` overlays only that include with the maintained
symbolic body in an isolated copy of the original physical `th03_op.asm`.
Everything else in the existing OP cold-source graph stays unchanged so that
its accepted source scopes do not become stale.

Two original TASM 5.0/TLINK 6.10 native rounds at `af1308d` reproduced the
**entire** original OP assembler owner: 11,323 initialized CODE/DATA bytes,
367 ordered native fixup fields, 273 PUBLIC offsets and three physical
segments. The actual OMF dependency path points to the staged maintained
`random.asm` in each round. Both newly linked complete OP executable images
were byte-for-byte equal to the existing original decoded Japanese OP image;
ordered MZ relocations, and complete MAP after normalizing the expected module
filename, were equal as well. A separate native negative trial `af1308e`
changed `AND AH,7Fh` to `AND AH,3Fh`; the complete original object
comparison correctly rejected the altered initialized CODE. This is a source-bound original native result,
not merely matching the isolated 42 instruction bytes.

Reproduce *only this physical owner*, using a previously unused DOS-safe ID:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/probe_th03_op_irand_source.py --stage afNEWa
```

The `afNEWa` placeholder must be replaced by actual digits and a letter.
The retained source-bound receipt is
`.analysis/work/op-irand-source-af1308d/report.json`. The existing OP source
cold-build graph and its independently published scopes are unchanged;
canonical packed-file unit credit and whole-product source ownership are
still separate unresolved gates.
