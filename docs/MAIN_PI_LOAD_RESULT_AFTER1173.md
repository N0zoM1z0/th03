# PI resource loader: a real 16-bit return local

The complete far-Pascal `pi_load` owner frees the requested image slot
before loading the new packed PI resource. The 16-bit `load_result` local is
not redundant source scaffolding: a direct `return graph_pi_load_pack(...)`
changed the original TC4 CODE (`af1173a`). Declaring the same local
separately (`af1173b`) or naming its purpose (`af1173c`) retains the native
instruction stream and exact order of the two far calls.

`af1173c` matches the entire original 70-byte CODE owner, six ordered
native fields, the PUBLIC and full Japanese MAIN image/relocations in two
independent original TC4/TLINK rounds.
