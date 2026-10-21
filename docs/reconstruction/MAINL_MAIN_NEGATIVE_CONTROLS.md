# MAINL main compiler controls: preserved negative evidence

Baseline: bb187e206e094ef83b781bc638ea8e5022a60e8d. No source promotion, count change, SVG change, default backend change, runtime acceptance or exactness credit.

- MRC06 (earlier background evidence): main-only documented -O- -y moved the shared execl call earlier, but produced 2462 bytes instead of2458; strict byte and ordered111 gates failed.
- MRA01: whole symbolic main rejected three PUSH LARGE0 spellings (undefined large). No object.
- MPL01: isolated PUSH0L rejected undefined L. No object.
- MPD01: isolated PUSH DWORD PTR0 rejected invalid opcode/operands. No object or width proof.
- MHC01: hybrid cleanup ASM and complete C++ execl calls produced67 bytes, earlier execl25, but two extra compiler epilogues and JMP63→25. Strict63-byte contract failed.
- MHR01: replacing manual LEAVE/RETF with genuine C++ return restored63 bytes but moved execl back to53 with JMP25→53. Strict earlier-anchor contract failed.
- MTR01: three semantic ASM conditional transfers produced2456 bytes,344 non-fixup differences; the1930-byte prefix and all11 public offsets remained stable. Critically, the entry JZ encoded7401 and branches to main+12 at the PUSH immediate opcode after skipping PUSH DS, not the intended final return at main+524. Compiler exit success did not establish semantic validity. This candidate must never be integrated or executed.

All namespaces and failures are preserved. No automated retry or shape sweep is authorized by this record. The current maintained DATA backend remains unchanged: full decoded linked program equality,677 relocation membership,102 ordered differences, suffix149..676 exact. Formal exact credit remains zero.

The companion replay hashes only relevant sources, actual manifests/completion/logs/reports/objects, checks negative outcomes, and decodes the critical short branch from OMF data. It does not run a compiler, linker or diagnostic function. Ignored evidence must be present to replay; absent evidence fails closed.
