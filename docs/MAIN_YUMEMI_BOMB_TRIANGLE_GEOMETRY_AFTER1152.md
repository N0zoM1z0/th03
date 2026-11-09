# Yumemi Bomb: native two-triangle geometry and player-side guard

The complete original `bomb~cxk` unit now names the first and second
triangle radii, three-vertex indexing, 200-line screen origin, and separate
radius decay. The renderer retains the original two real three-vertex GRCG
passes, six independent polar samples and original half-height division.
Its player-0 clip selection uses natural byte truthiness.

Original TC4/TLINK stage `af1152f` matches all 698 CODE bytes, 53 ordered
native fields and the Japanese MAIN image/relocations in both rounds.
Negative trials `af1152a/e` narrowed the shared signed triangle index,
changing CODE; `af1152d` showed that simplifying the explicitly widened
unsigned eight-frame shake predicate also changes TC4 output. Keep those
source forms even where the numeric results appear equivalent.
