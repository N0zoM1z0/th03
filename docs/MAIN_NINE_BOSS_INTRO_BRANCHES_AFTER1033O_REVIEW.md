# TH03 MAIN nine-BOSS INTRO completion branches after1033o

The nine character-specific BOSS update controllers now all express their
INTRO completion as a positive equality path. The forms differ where the
original controller has additional work around the completion frame:

- Chiyuri's INTRO uses its existing three-way completion/cross-effect/default
  chain.
- Kotohime and Mima already had positive completion branches with explicit
  early returns.
- Marisa, Reimu, Ellen, Kana and Rikako now use a positive equality branch
  with `else return` before their existing switch exit.
- Yumemi performs its two original INTRO sound-frame checks first, then uses
  the positive completion branch with `else return`.

These refinements preserve each frame comparison, reset, SELECT assignment,
sound operation and switch/fallthrough behavior. They were each rebuilt as
the complete affected physical owner in two independent original TC4 4.02
rounds at af1033g/i/j/k/m/n.

All nine update controllers retain their positive launched-player scopes.
The simultaneous integration at af1033o rebuilt all nine complete physical
owners in two original TC4 rounds:

- 17,451 CODE bytes
- 2,434 ordered native fields
- 85 PUBLIC offsets
- complete original Japanese MAIN loaded image and ordered MZ relocations

Protected report: `.analysis/work/exatt-layout-af1033o/report.json`

SHA-256: `4f0c3c334ab083a8f81b90b08106c56183a151dc158a3a1febb4ba074f350e54`
