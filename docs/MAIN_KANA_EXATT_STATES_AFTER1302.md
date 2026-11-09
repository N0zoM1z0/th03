# Kana Extra Attack: eight-slot allocation and renderer control

The full Kana Extra Attack owner now handles both single-entity rendering
branches through natural early returns. Its eight-slot sprite pass and
special allocator skip inactive or occupied records with explicit
`continue` statements, maintaining their original index/near-pointer
advances. Both the sprite frame and the update's opponent PID are
initialized at their actual first use. The eight-slot active movement,
acceleration, clipping and timed bullet dispatch are unchanged.

Original TC4/TLINK stages `af1302a`–`af1302d` and final `af1302f` reproduce
all 663 CODE bytes, 44 ordered native fields, five PUBLICs, and the complete
Japanese MAIN loaded image/ordered relocations in two rounds. One isolated
trial `af1302e` replaced `(1 - pid_current) == 0` with `pid_current` in the
render clipping selector; the original CODE changed, so the explicit
subtraction remains.
