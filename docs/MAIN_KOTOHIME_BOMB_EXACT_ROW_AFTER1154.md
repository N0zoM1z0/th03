# Kotohime Bomb: native explosion row and signed loop carrier

The original Kotohime Bomb row now uses a natural bounded `for`: the signed
X position advances by 96 pixels and the separate signed index advances
after each explosion call. Although no later source statement reads the
index, it is essential to the original instruction stream and cannot be
removed. Its lifetime may be narrowed to the active row block; both
player-side hardware checks accept natural byte truthiness.

Original Turbo C++/TLINK `af1154d` reproduces all 528 CODE bytes, 50
ordered native fields, and the complete Japanese MAIN image/relocations
in two rounds. The fade path's uninitialized color byte and its historical
machine behavior remain unchanged. A separate `af1154b` comparison also
confirmed that the byte shake mask cannot be freely rewritten.
