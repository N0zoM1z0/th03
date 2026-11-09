# Hitbox and HitCircle: native early exits and live-slot loops

The original hitbox hit test now separately returns on a negative screen-Y
origin or a completed defeat banner, before touching the shotpair, explosion
or Chargeshot callback state. The thirteen-slot HitCircle animation and
12-slot enemy-circle sprite renderer use natural `continue` paths for unused
slots. All active record updates, color selection, near pointer advances,
and the separate player-circle render still execute in their original order.

Original TC4/TLINK stages `af1194a` (hitbox), `af1194b` (HitCircle update),
and final `af1194c` (HitCircle renderer) each matched the complete two-owner
scope: **711 CODE bytes**, 63 literal ordered fields, five PUBLICs and the
Japanese MAIN image/ordered MZ relocations in two independent rounds.
