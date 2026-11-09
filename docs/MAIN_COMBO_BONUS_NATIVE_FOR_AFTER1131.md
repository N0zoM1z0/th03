# Combo bonus display: shared native for-loop progression

The complete Combo bonus/HUD dispatcher now uses a natural `for` header to
advance both the player index and the near combo pointer, including the
inactive-combo `continue`. The time decrement, digit rendering, flashing,
score payout and two-player layout preserve their original order.

Original TC4/TLINK `af1131a` matched both `p_combo` and `p_cmbhl` physical
objects: 978 CODE bytes, 57 ordered native fields and the Japanese MAIN
image/relocations across two independent rounds. `af1131b` additionally
moved the signed player index declaration into the `for` header; that changed
original `p_combo` CODE, so its earlier declaration remains.
