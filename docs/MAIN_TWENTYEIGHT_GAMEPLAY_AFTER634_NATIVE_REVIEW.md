# TH03 MAIN current 28-owner native source integration: after634

This retained checkpoint **recompiled** all 28 selected current physical
gameplay and BOSS C++ translation units, after actual Mima, Ellen,
Reimu and Marisa attack-source recovery. It did not merely read the
earlier after629 receipt. Each compiler wrapper explicitly references
the per-round changed source, and OMF COMENT records must confirm the
real consumed source and both maintained 32-byte entity/template
headers where applicable.

The newly updated major BOSS code includes:

- Mima's genuinely native-exact +7/-7 ring direction ternary,
  character-specific 18-mode dispatch, ring timings and **natural
  unsigned % 2 / % 4 frame cadence** in spread, orbit and random
  bomb volleys.
- Ellen's 18-mode dispatch and distinct warning, spread and two
  radial Extra Attack burst phase boundaries, preserving the
  original goto and signed nine-strip renderer wrap.
- Reimu's distinct pre-switch intro/pattern-selection behavior,
  18 shared-mode mappings and four independent original attack
  phase timelines, preserving original eight-bit sign expression.
- Marisa's wide/narrow columns with distinct end frames, explicit
  18-mode scheduling and genuinely original-equal natural **% 4**
  and **% 32** firing cadence.

Unsupported semantic rewrites were tested and **rejected** rather
than passing via stale source: inverted Ellen spread branches
(`af630a`), compressed Ellen strip index wrap (`af630d`),
unary-negated Reimu angle (`af631a`). The preserved source
is the original native code-producing variant.

## Full native link and ownership scope

| Family | Original physical TUs | CODE bytes | Literal ordered fields | PUBLICs |
| --- | ---: | ---: | ---: | ---: |
| Nine character BOSS controllers | 9 | 17,451 | 2,434 | 85 |
| Shared BOSS ring and seven-function controller | 2 | 949 | 106 | 8 |
| Ten Extra Attack / shared-flight TUs | 10 | 8,781 | 563 | 52 |
| Bullet, Fireball, Explosion, four Enemy producers | 7 | 8,195 | 582 | 50 |
| **Total** | **28** | **35,376** | **3,685** | **195** |

The two fresh original Turbo C++ 4.02/TLINK rounds recompiled
**only the 28 affected complete TUs**, reusing the other 71
original project objects, startup and CRT libraries in the
source-backed 99-object normal MAIN link. They match all original
CODE/data initializer payloads, literal ordered FIXUPPs, PUBLIC
offsets, segments/BSS and path-normalized entire MAPs. Both
ordinary MAIN EXEs equal the frozen after596 native parent;
the loaded Japanese program image and its 1,553 ordered MZ
relocations are identical. The independent standard DOS MZ
serialization reproduces all 130,882 Japanese MAIN.EXE bytes.

Command (one scoped build, two original native rounds):

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af634a \
      --units ba_chiyu,ba_kana,ba_koto,ba_ellen,ba_rikak,ba_yumem,ba_mima,ba_reimu,ba_maris,ba_sring,ba_srest,ex_yume,ex_mima,ex_rika,ex_rfly,ex_reup,ex_ellen,ex_koto,ex_chyu,ex_maris,ex_kana,e_fireb,e_expl,bullet,eforna,efornb,eupda,eupdb
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af634a

The source-bound native proof is retained at
`.analysis/work/exatt-layout-af634a/report.json`,
SHA-256 `db6cc2af112f3bdd1ed45e85709d4d613250e80ee83c10b7c76234abaf6fbdb4`.
Both full raw object/link/EXE/MAP/MZ output vectors, source
overlays, linker responses and original compiler/log evidence
remain in the native worktree. No full cold replay, object-patching,
historical receipt rewriting or target-copying was used.

This is verification of edited natural C++ source and already
owned native code. It does **not** grant new canonical packed-game
Factory byte credit, prove historic vendor raw OMF packet identity,
establish all-game code ownership, or certify physical PC-98
runtime behavior.
