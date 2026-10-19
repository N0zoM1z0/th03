# MAIN gameplay bounded CODE acceptance

The metadata records 78 reviewed extents / 371 complete functions / 59,624 owned CODE bytes, including the new 6,502-byte / 37-function Marisa, Reimu/shared and Mima owners. This is the reviewed CODE subset, not a whole-game percentage or Factory acceptance. Final installation CI is a separate checkpoint.

## Verified results

Fresh default run `gpt-dots-gameplay-promoted-default-cold-v01` passed both cold rounds. Receipt observation: 2026-10-19T10:03:44.865690Z. Original byte, MAP, literal ordered relocation, OMF and configured determinism gates remain unchanged. Supervisor exited zero after one invocation; guards were unchanged, claim released and cleanup clear.

- Receipt: `.analysis/th03-main-exact/gpt-dots-gameplay-promoted-default-cold-v01/receipt.json`, SHA-256 `846886cd5775bd9dbc3b797069e8da2227d5966592c3b895b93a28c211eaf078`.
- Completion: `.analysis/th03-main-serial/runs/gpt-dots-gameplay-promoted-default-cold-v01/completion-evidence.json`, SHA-256 `013f062c048085926f583ebe0a7043fb0ace30f38cb0d04eeb1266dd77874a68`.
- Strict comparison: `.analysis/gpt-dots-gameplay-acceptance-v01/postrun-verifier-v03/fresh-default-comparison-v01.json`, SHA-256 `f5c25b33f04fb83d5a94c38e1e4fb8e4c8342c424d70ae86b7d3fc2ce7cc2c26`.

Strict v03 comparison checked all four fresh-versus-historical round pairs: complete MAIN file/program image, literal relocation order, allocation/stack header and overlay, 43 ordered MAP inventories and 254 DATA/BSS/STACK rows including zero-size rows and duplicate publics. All 20 declared products match. All 31 executable outputs also match as additional evidence; the 11 auxiliaries derive from the pinned reference build graph, not the original receipt's 20-product vector.

Marisa adds 1,958 bytes / 10 functions; Reimu/shared 2,373 / 14; Mima charge 1,338 / 10 and bomb 833 / 3. Both Mima ledger rows retain the logical primary-source contract; physical producers remain separately declared.

## Limitations retained

Existing carrier DATA/BSS addresses and allocations are preserved, without new historical physical ownership. Behavior evidence covers the existing DOS input/math probe only. Nine non-game Research object metadata drifts remain: all-object equality is false; game objects and products are deterministic. The reference-owned HITBOX tail receives no additional authored credit. Provenance remains candidate-local-attested. Whole-game closure, other artifacts and Factory acceptance remain open. Experimental stage/round and round-loop blockers are unchanged and excluded.

The v01 supplemental design was rejected before execution for historical scope assumptions. The failed v02 report remains preserved: its inventory assumption incorrectly excluded 11 auxiliary executables. v03 retains every original gate and adds the full 31-output comparison. No outputs were removed or changed to make it pass.

## Metadata and validation provenance

Binary source, manifests, compiler inputs, scheduling and comparison controls are unchanged after the native proof. Only ledger states/evidence, function metadata, documentation and progress change afterward. Retain complete proof trees and frozen source/guard snapshots. Do not silently rebind the historical proof to later metadata.

Snapshot A validates the actual fresh evidence and proposed exact states with the inherited historical global-ledger link. A new global-ledger row explicitly references A's real inventory/log. Snapshot B substitutes that link and receives an independent validation. The two snapshots and logs are retained under `.analysis/gpt-dots-gameplay-acceptance-v01/final-metadata-v01/`; neither is claimed to validate later changes. Final installation CI remains a distinct result. The original 19 dirty files and original untracked test are untouched. Mode checks cover before/after supplemental verification; comprehensive replay-time mode pins were not available.

## Reproduction

The reviewed verifier is `.analysis/gpt-dots-gameplay-acceptance-v01/postrun-verifier-v03/verify.py`, SHA-256 `bcd47fa7bb0c0ec77d4a09a715baaaf550321bdd87fbd5301344cd01e6927123`; 21 tests passed. The recorded CLI is:

    PYTHONDONTWRITEBYTECODE=1 python3 .analysis/gpt-dots-gameplay-acceptance-v01/postrun-verifier-v03/verify.py --report .analysis/gpt-dots-gameplay-acceptance-v01/postrun-verifier-v03/fresh-default-comparison-v01.json

That report exists and must not be overwritten. The verifier is intentionally bound to the pre-finalization live inventory and will reject later metadata drift. A new current proof needs a new reviewed plan/run ID and its own retained evidence; do not weaken the existing guards.
