# TH03 MAIN full enemy collision/chain/update source-native after739

The maintained shared `src/main/enemy/enemy.cpp` is partitioned into four
original physical TC4 source objects. The `eupdb` unit contains four
complete original functions: the substantial ~848-byte `enemy_hittest`
chain/collision controller, enemies_hittest(), enemies_render() and
individual enemies_update(). This changed-source trial rebuilt the
**complete original 1,160-byte physical eupdb object**, not just an
isolated short collision leaf.

Natural C++ source improvements now describe the original fireball/Extra
Attack chain thresholds explicitly: `hits <= 2` charges the chain,
`hits <= 9 - chain_slot` fires a transferred pellet, and
`hits <= 14 - 2 * chain_slot` handles the later charge band. The original
round-speed mapping remains a four-band division, with named compile-time
thresholds and **unchanged operation order**. The two render/update loops
and descending hit scan use natural prefix `++i`/`--i` for their signed
local counters while keeping the original *pointer* `p++`, `p--` and
`efe_p.enemy++` memory traversal order. The renderer uses natural
`if(!p->pid)` for the original two-playfield clip routing.

### Direct original compiler negative experiments

`af739a` used additional apparently natural Boolean expressions for the
original `hitbox_hittest` AL result, enemy HP and hit-count parity. It
compiled but expanded the original physical source by **three CODE
bytes**, moving later public addresses and branch displacement fields.
`af739b` independently restored the AL comparison and `af739c` restored
the original byte-HP comparison. Neither eliminated the difference.
The remaining change `if(!(hits & 1))` was the cause: TC4 generated a
longer register load/test instead of the original direct memory test.
Restoring `if((hits & 1) == 0)` in `af739d` produced a completely exact
native compile while retaining all other natural source changes.

The original explicit near-call ABI for hitbox and transfer pellet, chain
slot wrap, fireball charging, potentially surprising HP=0 behavior,
original two-dimensional hitbox setup and score order remain unchanged.
No game bug was "fixed", original assembly memory access removed, or
bounds checks invented.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af739d --units eupdb
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af739d

Both genuine original Turbo C++ 4.02/normal full TLINK rounds reproduce
**every original 1,160 CODE byte, all 103 literal ordered OMF FIXUPP
fields, all 4 PUBLIC offsets, complete segment declarations and
source dependencies**. Both full normal MAIN EXE/MAP, Japanese
124,642-byte loaded program, all 1,553 ordered MZ relocations and
independently serialized original Japanese 130,882-byte MAIN.EXE match.
Only `eupdb` was rebuilt; 98 other project objects and original CRT
were reused. No cold replay or binary patch.

Current native source-bound receipt:
`.analysis/work/exatt-layout-af739d/report.json`, SHA-256
`8d3e0797fb3276d34874eb5bed11de76e4bef37d27a53923cd8518edb25a9c75`.
Both actual compiler/linker rounds, OMF object, original MAP, source
snapshots, complete responses and negative writer stages are retained.
This is current maintainable original-source recovery, **not** additional
canonical Factory packed-file accepted bytes, historical vendor raw
OMF identity, or proof of full project source ownership.
