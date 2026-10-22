# ZUN -3 logo root: two independent cold builds

Two source-only initial carriers independently compiled and context-linked the
maintained logo root. ZS0101 and ZS0102 have identical raw OBJ, COM and MAP,
without output normalization, timestamp rewriting, copied project objects or
patched outputs. The scope remains ten maintained procedures / 1,299 CODE
bytes; DATA15 and BSS293 are separate layout evidence. ZUN stays at 15/18
source-present units and 1,855 scoped CODE bytes, with exact zero.

## Actual production and comparison

The original ZS0101 compile/link completed on 2026-10-21 at 22:33:23 UTC.
Its original `config/zunsoft_root/proof.json`, native receipts and runtime
receipt remain unchanged and still describe one build and 2,600 model calls.

The parent ran the new ZS0102 compile/link on 2026-10-22 at 00:50:02–00:50:13 UTC
(Factory command `5a57f36814e2470398b1d2d0c4f0b4f2`). Both phases exited zero;
exact-owned process inventories and registry policy passed, and the shared lock
was released. The parent verification at 00:51:13–00:51:19 UTC
(command `1d333ff3358e4b31b97530178488bb69`) passed all fourteen structural gates
and the raw comparison below.

- OBJ: 4,133 bytes, SHA-256
  `845de18164def1d384eadc59be287a22ca47b99a6d4d989c0dfa407c094a08a5`.
- COM: 10,096 bytes, SHA-256
  `beeb86dc055c585a32f4500c9eabb2e6cb1e0537bcdbc5f3763ebefa4308e297`.
- MAP: 28,657 bytes, SHA-256
  `882ac7e3fba775f9225aa55adc276e17604620fa2e7608ae7cc18aa9081bc3ed`.

These are complete raw-file comparisons, including OMF dependencies and MAP
text, not normalized equality. The COM also equals the attested decoded -3
payload. This diagnostic equality does not claim ownership of its vendor code.

## Independent inputs and bounded execution

Each initial carrier contains exactly 21 declared inputs: the maintained root,
five compatibility forwarders, the original translation-unit wrapper, twelve
reference headers, the link response and vendor masters.lib. No project OBJ or
COM is copied. C0T, EMU, MATHS and CT remain explicit toolchain context.

Source bytes, modes and recorded source timestamps match across both actual
carriers. All original fixed tool timestamps remain unchanged. The first build
already used fixed source timestamps; this repeat preserves those actual
recorded values rather than inventing an earlier historical timestamp.

The compiler vector remains `-O -b- -3 -Z -d -DGAME=1 -mt`, with source pragma
`-2 -d-` and signed default char. GAME=1 selects the original tiny logo producer;
it is not the separate GAME=3 resident build. Tiny link order remains C0T,
fresh root OBJ, masters, emu, maths and ct.

Both executions are headless with empty DISPLAY/WAYLAND_DISPLAY, one CPU and
nice at least 10. The reused guarded runner retains the shared writer lock,
poison checks, 90-second native phase, 15-second owned cleanup, registry policy
and exact-owned cleanup. The repeat only adds continuous input/tool timestamp
guards. Every old record is preserved in place.

## Runtime and ownership limits

The retained model is still one target plus ZS0101, each with 1,300 calls,
2,600 total. No model was run for ZS0102. Its connection to the modeled candidate
is complete raw COM identity, not another 1,300-call observation.

Vendor startup, master.lib, CRT helpers, assets and graphics/BFNT interfaces
remain unowned context. Actual PC-98 device/runtime behavior, complete payload
ownership, launcher integration, DIET packaging and full acceptance remain open.
Two cold builds do not grant formal exact credit.

## Maintained replay and retention

```sh
python3 -m unittest discover -s tests -p 'test_zunsoft*' -v
.venv/bin/python3 scripts/replay_th03_zunsoft_root.py
.venv/bin/python3 scripts/replay_th03_zunsoft_repeat.py
```

The separate compact proof is `config/zunsoft_repeat/proof.json`. It composes
the unchanged original guarded replay, a pinned raw-repeat verifier, and the
retained second structural report. It rechecks actual source/helper closure,
source-to-both-carriers bindings, four process/registry phases and all raw files.
It does not require unrelated tracked files from historical source snapshots
to remain unchanged. No native tools or runtime matrices execute in replay.

The detailed ignored inventory is
`.analysis/zunsoft-repeat-maintained-proposal-20261022-v01/inventory.json`.
Its checked repository-relative `inputs` dictionary retains every concrete
proof dependency through cleanup, including dependencies whose older reports
used absolute paths. It is not duplicated into tracked configuration.

Native proposal: `.analysis/zunsoft-repeat-proposal-20261022-v01/manifest.json`
(SHA-256 `e1805fa1c8ba50b30f97410b871201120657886fc3952ad46beb77926696b559`).
Actual reports:
`.analysis/zunsoft-repeat-output-20261022-v01/structural-verification.json` and
`.analysis/zunsoft-repeat-output-20261022-v01/raw-repeat-verification.json`.
