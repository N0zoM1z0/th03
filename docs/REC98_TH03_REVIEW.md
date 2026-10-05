# ReC98 TH03 intake review

The review scope is frozen at ReC98 revision
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`. The complete intake queue is
`config/rec98_th03_inventory.csv`; scoped review decisions are in
`config/rec98_th03_reviews.csv`. Regenerate or check the queue with:

```sh
python3 scripts/inventory_rec98_th03.py
python3 scripts/inventory_rec98_th03.py --check
```

The queue contains every tracked `th03/` file and root TH03 assembly/include,
every direct OP/MAIN/MAINL translation unit declared in the frozen Tupfile,
the named ZUN source subgraphs, and recursively referenced source includes.
Conditional includes are traversed conservatively, so cross-game branches
remain candidates until their TH03 relevance is reviewed. Unlinked TH03 files
remain visible as `unassigned`. Asset rows contain only names and hashes;
game assets and proprietary tools must never be imported. Unresolved includes
identify generated inputs or other dependency gaps requiring review.

This queue is not a compiler dependency graph or an acceptance ledger. A row
with `reviewed_code_artifacts` records only the local CODE extent review for
that artifact, backed by `config/units.csv` and the maintained replay manifest.
It does not close other artifacts, headers, initialized data, BSS layouts,
resources, packing, startup, scaffold assembly, or complete product ownership.
`boundary_review_artifacts` also records candidate boundary reviews; it grants
no exact credit. The enemy owner is a complete maintained candidate whose
ordered relocation gate remains unresolved, as documented in
`docs/reconstruction/MAIN_ENEMY_REVIEW.md`.
All remaining file/artifact review is open. Upstream exactness is never
inherited. Compatibility forwarders retain explicitly declared dependencies
on the frozen scaffold until the declarations can be localized and attested.

The existing thirteen MAIN source owners were rechecked in two cold builds
by `sol-rec98-baseline-20261005`: all forty functions and fourteen extents
passed the configured local gates. The baseline remains a bounded replay,
not a complete maintained game build.

Current MAIN acceptance contains twenty-five maintained source owners / twenty-nine
CODE extents / seventy-four functions / 9805 owned bytes. Forty-nine intake paths
have scoped CODE decisions, including the frozen wrappers and implementations
for hitbox, combo, gauge, movement, ordinary shots, player state, resident pointer,
extra-attack wrapper, hit circles, static HUD, playfield and sprite16 wrappers. Header/dependency and
other-artifact review remains separate.
