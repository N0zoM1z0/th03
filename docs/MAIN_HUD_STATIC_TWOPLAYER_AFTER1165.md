# Static HUD: native two-player dispatch and register lifetimes

The full `hud_stat` object now renders both players' half hearts, Bomb
slots, round wins and Gauge level in a natural bounded `for` loop. Each
player's four calls remains in the exact original order. The Gauge level
selector also uses natural PID truthiness, without changing the two-color
pixel/glyph placement or the Boss-level saturation rule.

The original TC4/TLINK stage `af1165h` reproduces all 539 CODE bytes,
18 ordered native fields, seven PUBLICs and the Japanese MAIN image plus
relocations in two independent rounds.

The original signed loop-local scopes remain significant. Trials
`af1165c/d/g` showed that declaring the Bomb, story-lives or halfheart
indices/counts later changes native CODE even where the C++ iteration
results match. Keep their original lifetime until a better codegen hypothesis
has been checked.
