# CFG resident loader: native uninitialized scratch and direct return

The original `cfg_lres` owner loads the resident configuration into a true
stack-allocated `cfg_t` scratch, here named `resident_cfg`, and directly
returns the resident segment pointer supplied by the CFG loader. The
scratch must not be zero-initialized: that would add non-original stores.
Likewise a named result pointer changes the native TC4 register and stack
layout; only the source-level scratch identifier is changed.

The two original TC4/TLINK rounds of `af1182a` matched all 49 CODE bytes,
six ordered native fields, one PUBLIC and the complete Japanese MAIN image
and relocation order. The resident `CFG_FN` external symbol remains the
original one, with the historical macro undefined before declaration.
