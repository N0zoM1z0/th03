# Player effects: original pool updates and rendering for-loops

The complete `effects` physical owner now advances the signed entity index
and near effect pointer together in the headers of both lifetime update and
render passes. Expiration, radius adjustment, playfield clipping, circular
blitting and quad rotation retain their original source/call order.

Original TC4/TLINK `af1133a` matched 628 CODE bytes, 33 ordered native fields,
five PUBLICs and the full Japanese MAIN image/relocations in two independent
rounds. Two independent quad-vertex loop experiments, `af1133b` and `af1133c`,
changed original CODE even when angle mutation stayed in the body. The signed
vertex loop and byte-angle update therefore retain their original structure.
