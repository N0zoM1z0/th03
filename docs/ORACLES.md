# Exact reconstruction Oracles

`config/oracles.toml` defines the executable acceptance policy. A successful
build, analyzer query, reference-source read or Git commit does not establish
exact reconstruction on its own.

For a reviewed artifact or owned extent, every required gate must pass:

1. Original target identity and MZ format integrity.
2. Complete boundary and byte ownership, including exits and shared tails.
3. Pinned compiler/tool identity and recorded executable tool replay.
4. Valid Intel OMF output with the expected producer.
5. Two independent cold source materializations with a deterministic declared
   output/object vector.
6. Correct MAP placement, segment/group/alignment and ordered MZ relocation
   sites and original word values.
7. Zero byte differences over the complete accepted extent.
8. Consistent ledgers, source presence, extent scoping and nonoverlapping owners.
9. Cold aggregate replay covering every affected accepted owner.

`python3 scripts/replay_th03_main_exact_units.py` implements the maintained
MAIN owner replay. `--unit` selects the requested owner for routing; both
maintained owners are always rebuilt and checked together so focused work
cannot omit the accepted aggregate. The full product graph is still open and
uses a pinned, freshly compiled ReC98 scaffold for unmaintained link inputs.
Only reviewed maintained owners receive local exact credit.

The declared object roots and counts live in `config/th03_main_exact_units.toml`.
Timestamp normalization applies only to identified OMF source metadata; it
never changes LEDATA, relocation words or generated code. All non-game object
differences are retained diagnostically. The older imported calibration hashes
remain unchanged and are separate from this owned-extent source replay.

Portable negative controls in `tests/test_main_exact_oracle.py` reject a changed
last byte, a changed relocation word, reordered or duplicated relocation sites,
a split relocation word, invalid MZ structure and out-of-bounds ownership.
Private DOS probes exercise the actual maintained objects with explicit hardware
test doubles. Headless Ghidra supplies target analysis, with independent full
MZ/database attestation before its output is interpreted.

See [MAIN_INPUT_MATH_EXACT.md](MAIN_INPUT_MATH_EXACT.md) for the first reviewed
ownership and ABI evidence. Local exact ledgers are imported claims in the
shared Factory. Only a registered native receipt driver and policy-accepted
fresh receipt could publish Factory Truth Kernel acceptance; repository-shell
Oracle execution does not do that automatically.
