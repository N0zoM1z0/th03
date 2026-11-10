# Chiyuri BOSS: exact ring, fan and intro control

The complete `ba_chiyu` controller now positively gates its high-level
four-group pellet ring, rather than returning from the common 32-shot
pattern. Horizontal and vertical fan passes express the signed 16-bit
position/angle products as index times step, with the division preceding
subpixel scaling and eight-bit angle truncation. Only the exact vertical
release frame performs the two vertical speed passes. The intro flicker,
render mode and byte palette counters use explicit original state gates.

One important compiler finding corrects older contextual advice:
`af1329g` recompiled the *current* source after changing both rising fan
speed expressions to `+=`. This **passed the full native object and normal
MAIN link**, contrary to trials `af922h`/`af1033q` under earlier source
forms. `af1329j` additionally proved both falling passes' `-=`, and
`af1329k` proved the ring sprite-angle `+=`. These source expressions are
now retained and documented as source-context-specific, not a blanket rule
for byte-valued arithmetic in other owners.

Final original TC4/TLINK stage `af1329l` reconstructed the entire **2,654
CODE bytes, 381 literal ordered fixup fields and 11 PUBLICs** in two
independent rounds. Joint stage `af1329m` additionally recompiled the
Bullet engine and both shared BOSS owners: **6,288 CODE bytes, 683 ordered
native fields and 39 PUBLICs** matched complete Japanese MAIN images,
MAP and ordered MZ relocations in both links. No cold replay was run.

Read-only native source check:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1329l af1329m
```
