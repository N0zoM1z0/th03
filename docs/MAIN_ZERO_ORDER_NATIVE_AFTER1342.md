# Source-bound MAIN segment order carriers: zero code, exact physical alignment

The original `bo_shim.obj` and `ex_ord.obj` have no initialized CODE/DATA,
FIXUPP fields or PUBLICs. Their purpose is to establish **30 ordered empty
CODE segment definitions** (19 and 11 respectively) before separately
compiled BOSS, Bullet, Extra Attack and enemy producers enter TLINK.
The real maintained sources already exist at `src/main/boss/order.asm`
and `src/main/player/exatt_order.asm`.

The initial `af1342a` source trial assembled both with genuine TASM and
relinked the complete original Japanese MAIN in two independent rounds.
All segment name/class/size fields and the normal EXE and MAP matched.
A negative `af1342b` trial changed the `SHARED` declaration from `word`
to `byte` alignment. The generic scope comparison incorrectly accepted
it because that helper did not retain **raw OMF ACBP alignment** in its
semantic SEGDEF summary. This was a real verification blind spot, not a
successful source experiment.

The narrow strict verifier extension now compares the **complete ordered
OMF LNAMES / SEGDEF / SEGDEF32 / GRPDEF data records**, byte-for-byte,
against the original physical owners, including alignment byte `0x48`
versus the incorrect `0x28`. It fails the negative `af1342b` source,
while exact `af1342c` compiles both original owners in two fresh TASM
rounds, reproduces both entire unchanged 99-object normal MAIN links,
full normalized MAP and ordered MZ relocations and pins the raw OMF
segment-layout hashes in the per-round report. The new stronger comparison
is opt-in for these original zero-byte segment scaffolds; historical
proofs of unrelated owners remain source-bound and unmodified.

This adds two **physical native source scopes**, not new functions,
initialized bytes, CODE percentage or Factory packed-file acceptance.
No cold replay and no manual target-byte repairs were performed.

Current read-only original-source verification:

```
PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_zero_order_carriers.py --stage af1342c --check
```
