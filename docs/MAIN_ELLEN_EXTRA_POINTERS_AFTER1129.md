# Ellen Extra Attack: pointer progression and register-lifetime limits

The complete six-function `ex_ellen` source now advances all original near
slot/history/render pointers with natural prefix `++`, and scopes all three
first-free / paired-slot initializer indices to their `for` headers. The
12-slot update keeps the original active history shift, seven-sample arrival,
clip `continue`, and per-frame state transitions. Its collision stripe size
and activation sound are named constants.

Original TC4/TLINK `af1129e` matched all 1,129 CODE bytes, 79 native ordered
fields, six PUBLICs, and the complete Japanese MAIN image/relocations in two
independent rounds. Trials `af1129c` and `af1129d` narrowed the update's
signed index and history index respectively; `af1129f` narrowed renderer
coordinates/frame. All three changed native CODE and were reverted. The
larger local scopes are currently necessary for original compiler output.
