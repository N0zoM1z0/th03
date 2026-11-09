# Yumemi Chargeshot: shared target search and sprite lifecycle source

The original `cs_yume` gameplay owner contains shared `ellen_target_set`,
charged projectile movement/collision, the sixteen-sprite polar renderer
and the eight-case Gauge switch. The target-selection scan can advance its
near Enemy pointer with `++p`; the active renderer's frame and sprite offset
can initialize at first use. Neither changes the precedence of BOSS targets,
formation filtering, Blooming transitions or the Gauge switch table.

The final `af1143h` real TC4/TLINK stage matches all 1,645 CODE bytes,
133 ordered native fields and the complete Japanese MAIN image and
relocations in two independent rounds. Independent experiments that moved
the sixteen-sprite ring's signed index into a `for` header (`af1143c/d`)
or narrowed its frame local (`af1143f/g`) changed original CODE and were
reverted. This loop retains its separately ordered byte-angle update.
