# TH03 MAIN — Kana BOSS staged barrage and rotating state machine (af1117f)

The complete original `ba_kana` Turbo C++ 4.02 physical owner includes all
attack families, the major update/collision controller and intro/main sprite
renderers. The staged-ring controller now uses independent natural `if`
branches after its early warning and firing returns, instead of retaining
an unnecessary `else if` cascade. The sixteen-projectile middle salvo now
has a tightly scoped `register int i` in its real `for` header and natural
prefix progression after the original projectile and speed updates.

The main BOSS frame uses natural unsigned-word prefix increment; the
four-frame rotating ring and variable cloud interval use natural unsigned
word remainder tests. The template's second-player condition explicitly
compares with zero, and the main sprite renderer uses natural hit-flag
truthiness. The rotating attack's identical return destinations are
expressed by one return after the signed-byte angular update; the original
mutable byte's compound update remains unchanged.

Real native source experiments `af1117a` (staged branches), `af1117b`
(frame/parity/template), `af1117c` (renderer and salvo progression),
`af1117d` (loop lifetime), `af1117e` (rotating phase exit) and final
`af1117f` (truthy remainder guards) each passed two independent original
TC4 and complete normal MAIN TLINK rounds. All 1,874 original CODE bytes,
274 native ordered fields, nine PUBLIC offsets, the complete Japanese MAIN
loaded image and all 1,553 ordered MZ relocations matched. Final bound
native evidence: `.analysis/work/exatt-layout-af1117f/report.json`.

A fresh `af1117g` counterexample tried replacing the original inline
`SUB AL,10h` in Kana's cloud angle with C++ pseudo-register `_AL -= 0x10`.
Despite preserving the AL carrier and value, TC4 changed CODE. It was
rejected and original instructions retained. This scope does not establish
new canonical Factory packed-game credit.
