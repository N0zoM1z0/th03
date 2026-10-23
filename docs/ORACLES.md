# Exact acceptance

`config/oracles.toml` defines required gates. A compiler success or matching
instruction shape alone does not establish exact reconstruction.

Require target/tool identity, complete ownership and ABI, two independent cold
source builds, valid OMF, correct MAP/layout and literal ordered relocations,
complete raw byte equality, affected behavior and aggregate regression checks.
Keep ledger scope honest: reviewed extents are not a whole-game denominator.
Never manufacture equality with target-byte arrays, padding or object patches.

Historical validation outputs were removed at the owner's request. Ledger rows
record past observations; scripts referring to discarded runs need a fresh
source build. Missing old receipts must not be treated as a new passing result.
