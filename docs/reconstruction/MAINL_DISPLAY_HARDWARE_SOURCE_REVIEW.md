# MAINL display/hardware source ownership

## Source checkpoint, not acceptance

Twenty complete symbolic include providers cover sixteen existing decoded units /
2,116 bytes. The current MIA02 root consumes each old provider once; the composer
replaces only that include path with maintained TH03 product source. Expanded
statements, macro definitions, aliases, conditionals and alignment are unchanged.
Current source progress remains 84/145 units and 23,150 bytes; exact remains 0
until separate native consumption, runtime and intake proof is reviewed.

## ABI and behavioral contracts

- Palette preserves signed fade speed, clamped tone, partial RGB reads, explicit
  ports and the mutable CS LCD XOR immediate.
- VSYNC preserves saved CS interrupt vectors, real IRET frames, IF-gated delivery,
  delay overflow and bounded waiting. DOS_SETVECT retains far address parameters
  and six-byte Pascal stack cleanup.
- EGC and graphics preserve register order, shared entries, signed clipping,
  stack CLI/STI sequences, caller DF, edge masks and zero-width wrapping.
- Gaiji preserves font ports, actual heap cycles, malformed BFNT/read handling,
  original failure cleanup and caller DF. Screen retains BIOS/VRAM context,
  plane order and allocation failure behavior.

## Proof plan and boundaries

First and repeat native root assemblies/links must consume these includes,
produce equal raw OBJ/EXE/MAP and prove all 2,116 scoped bytes against target.
The sole scoped relocation is VSYNC 0000:1FE5. Palette runtime proof may only be
retained via complete EXE identity plus actual model dependencies; VSYNC,
graphics, gaiji and screen require fresh serial target/candidate model phases.
Each model independently checks actual memory; cross-image comparison omits
only its existing top-level before/after memory digest fields.

Already-owned BFNT, DOS open, GDC and heap receive no second credit. Other
objects and hardware models remain explicit context. DATA EVEN 0E3F:0849
(target 90/current 00), global relocation ordering, cold aggregate ownership
and canonical packed equality remain open. No literal byte repair, output
normalization, new denominator or whole-product exactness is claimed.
