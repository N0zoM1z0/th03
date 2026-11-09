# Kotohime Chargeshot: natural collision guard and named geometry

The complete `cs_koto` physical owner now checks an inactive charged shot
with an early return, allowing its live 8-byte collision view to follow the
guard instead of being enclosed by an outer conditional. The real BX-based
near alias stays intact because it determines original target instructions.
Original render dimensions, collision margins and damage amount now have
semantic compile-time names, as do the Gauge RNG spawn range and bias.

Original TC4/TLINK `af1146d` matched all 690 CODE bytes, 79 ordered native
fields, nine PUBLICs, full Japanese MAIN image and MZ relocations across
two independent compiler rounds. The earlier `af1146b` test flattened the
Gauge spawn/expiration `if` / `else if`; TC4 produced different CODE, so
that branch relationship remains unchanged.
