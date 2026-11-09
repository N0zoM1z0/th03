# Reimu BOSS: native spread and orbit-renderer exits

The complete Reimu BOSS `ba_reimu` now uses explicit early returns in both
staged spread-attack windows. On frames without the shared 16-frame firing
trigger, the narrow and five-direction phases exit before touching the
projectile template; their normal firing and later BOSS-selection effects
remain in original order. The main sprite renderer also returns before
orbit-cel setup when no orbit effect is active, preserving the distinct
signed-index orbit-sprite pass and its byte-valued animation masks.

Original TC4/TLINK stages `af1175c` (render mode), `af1175d` (narrow spread),
`af1175e` (medium spread), and final `af1175f` all reproduced the complete
2,020 CODE bytes, 270 ordered native fields, nine PUBLIC offsets, and normal
Japanese MAIN loaded image and MZ relocations in two independent rounds.

An isolated `af1175a` trial instead inverted the orbit-attack final-release
guard. Despite equivalent phase values, TC4 generated different CODE; that
state machine keeps its original release-frame branch.
