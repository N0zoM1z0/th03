# Chiyuri BOSS: native trail ring and dual fan release control

Two full attack controllers now use an explicit release-frame guard. The
48-projectile trailing ring returns until its exact release tick, after
recording the periodic eight-frame bomb warning. The dual fan controller
returns after its separate horizontal release or before its vertical release;
its four positive/negative speed passes preserve the native signed quotient,
byte angle reflection, per-projectile call order and speed changes.

Original TC4/TLINK stages `af1190a` (trail), `af1190b` (vertical guard),
`af1190c` (fan scope) and final `af1190d` (flat natural source) each matched
the complete 2,654 CODE bytes, 381 ordered native fields, eleven PUBLICs and
Japanese MAIN image/relocations in two independently compiled rounds.
