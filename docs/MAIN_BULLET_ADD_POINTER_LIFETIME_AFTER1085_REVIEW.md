# TH03 MAIN Bullet add: allocator pointer initialized at first use (af1085x)

The 562-byte far `bullets_add()` allocates a free bullet slot, initializes its
state and trail ring, and then dispatches either transfer-pellet creation or
the 819-byte group-velocity engine. The original first-free-slot loop is
compiler-sensitive: a natural `while` rewrite changed CODE in af899c, so its
`for` / `continue` / `break` structure and original signed index remain.

## Accepted source lifetime

The near pointer to the first bullet record is now initialized at its first
use rather than declared uninitialized and assigned immediately before the
bullet-type switch:

```cpp
void bullets_add(void)
{
    int trail_i;
    int bullet_i;
    int group_i = 0;
    // transfer coordinate and speed scratch declarations
    // ...
    if (outside_playfield) {
        return;
    }

    bullet_t near *p = bullets;
    switch(bullet_template.type) {
        // ...
    }
}
```

This preserves the early return before pointer initialization, the exact
first pointer value, and the later postfix near-pointer increment in the
allocator's comma expression. The original object compiler accepts this
natural C++ lifetime without changing its emitted bytes.

## Complete original-owner verification

Stage `af1085w` rebuilt the complete Bullet physical owner in two independent
original Turbo C++ 4.02 rounds. All 2,685 CODE bytes, 196 ordered native fields
and 20 PUBLIC offsets match. The original 9,500-byte BSS extent is preserved,
and both normal Japanese MAIN links reproduce the original loaded image and
ordered MZ relocations. The source overlay checked the maintained `bullet.cpp`
producer.

Report: `.analysis/work/exatt-layout-af1085w/report.json`

SHA-256: `340af6d938b01be5342a8fc0aace3cb044fad6ab2da02fb213ffe33baaa9bc6a`

Current `bullet.cpp` SHA-256:
`87c48268237fb4e75677bd3ce4e47b02a7762fb7f5f356022c09966304dba6c6`

## Eight-owner integration

Stage `af1085x` rebuilt the current Bullet owner together with
`ba_koto`, `ba_reimu`, `ba_yumem`, `ba_chiyu`, `ex_rfly`, `ex_reup` and
`hitcirc` in two independent original TC4 rounds: 13,158 CODE bytes, 1,555
ordered native fields and 75 PUBLIC offsets match. Both normal Japanese MAIN
links reproduce the original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1085x/report.json`

SHA-256: `8e5883fb880311c5d785ccc16243c496309387ce5b81b6f1aef5eae2bdc249b7`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.
