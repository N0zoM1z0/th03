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

## Near filename storage and direct segment return (2026-11-11)

The 49-byte CFG resident loader now explicitly declares the filename
as a `near` array and passes `&CFG_FN[0]` to the existing loader.
The original `CFG_FN` EXTDEF and two-byte near address remain unchanged;
the `cfg_t` scratch is still genuinely allocated on the stack and is
**not initialized**. The return stays the original `resident_t __seg*`
value directly from the call, without a local pointer that would alter
the old TC4 register allocation.

Native stage `af1367r` proved address-of-first-byte equivalence;
`af1367s` also proved explicit near storage. Current `af1367t`
recompiles all **49 CODE bytes, six ordered native fields and one
PUBLIC** in two exact TC4 rounds and normal Japanese MAIN links.
The joint `af1367u` recompiles this leaf with MAIN entry, initializer,
DOS executable handoff and PI loader: **3,310 CODE bytes, 463 native
fields and 12 PUBLICs**, with both normal MAIN links and ordered MZ
relocations exact. No cold replay or target-byte adjustment was used.

Owner proof: `.analysis/work/exatt-layout-af1367t/report.json`, SHA-256
`512ae5009e9393176f760dd88b9b5e7831553f1f9d94677357a4da97c95dfd4a`.
Joint proof: `.analysis/work/exatt-layout-af1367u/report.json`, SHA-256
`574f18dea2d04da55edf5b799b667e5391be44824f95cae2b075e13fb832d957`.
