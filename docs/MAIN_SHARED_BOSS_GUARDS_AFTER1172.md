# Shared BOSS: natural launch and attack-selection early exits

The shared BOSS launch controller now returns immediately when no launch
request is active. Its register-based `REP MOVSW` template copy and the
order of both player-side state updates remain unchanged. The attack
selector returns during the waiting period before drawing a random pattern;
all rejected patterns still consume their original RNG words. The
explosion renderer uses natural zero-mode truthiness.

The complete original `ba_sring` and `ba_srest` owners passed two native
TC4/TLINK rounds at `af1172f`: 949 CODE bytes, 106 ordered native fields,
eight PUBLICs and the full Japanese MAIN image and relocations.

Two compiler-specific counterexamples were isolated. Using `pid_current`
truthiness in the register-based template copy changed the original
code, as did reversing the pattern-count comparison to put the count on
the left (`af1172g`). Both are left in their native-exact forms.
