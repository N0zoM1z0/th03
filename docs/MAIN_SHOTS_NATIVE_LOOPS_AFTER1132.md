# Player shotpairs: source-exact creation and rendering progression

The complete `shots` physical owner now advances near pointers and signed
indices with natural prefix updates across shotpair creation, movement and
sprite rendering. The left-edge adjustment while preparing shot pairs also
uses a `for` header, retaining the original left-coordinate increment before
the pair index. Animation frame and shot allocation order remain unchanged.

Original TC4/TLINK `af1132b` matched 449 CODE bytes, 17 ordered native
fields and the Japanese MAIN image/relocations in both compiler rounds. An
isolated `af1132c` trial scoped the shot-allocator index to the `for` header;
this changed original CODE, so the wider index declaration remains.
