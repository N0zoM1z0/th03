# TH03 MAIN — both background chains, natural particle traversal (af1115b)

Both original Chain 1 and Chain 2 physical Turbo C++ 4.02 translation units
have been rebuilt together, including their acceleration/periodic rendering
controllers and the shared phase include. The complete 80-slot velocity reset,
48-slot Chain 1 random initializer, and 50-slot Chain 2 initializer now use
natural C++ `for` headers that advance the signed counter and near particle
pointer after all vector/RNG/sprite stores. The original Chain 2 first-40
sprite selection remains a real conditional, not a ternary. Chain 1's reset
shares a named 64-angle constant with its 48-slot initializer; Chain 2's
separately randomized horizontal/vertical subpixel extents are named without
changing either original modulo or call order.

`af1115a` independently checked the complete natural C++ loops, and
`af1115b` checked their named angle and random extents. Each stage passed two
real original TC4/normal MAIN TLINK rounds for **both** physical owners,
including all 1,245 original initialized CODE bytes, 86 ordered original
native fields, nine PUBLICs, the complete Japanese MAIN loaded image and all
1,553 MZ relocations. The final source-linked report is
`.analysis/work/exatt-layout-af1115b/report.json`.

The low-level DS:DI register contracts and the periodic phase branch labels
remain explicit assembly: they have not been replaced by unverified C++.
The original uninitialized `changed` byte in both phase controllers remains
untouched. This is current local native evidence, not canonical Factory
packed-unit credit or whole-product acceptance.
