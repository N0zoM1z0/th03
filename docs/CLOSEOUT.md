# TH03 reconstruction closeout

> **Historical snapshot (2026-10-06).** Reconstruction resumed on 2026-10-07; current counts and active instructions live in RE_HANDOFF.md and PROGRESS.md.

Work stopped at the owner's request on 2026-10-06. At that checkpoint no
additional reconstruction was queued. The repository retained its partial source and evidence;
the 505-file intake and the whole maintained game build are unfinished.

The current [handoff](RE_HANDOFF.md), [progress](PROGRESS.md) and
[review index](REC98_TH03_REVIEW.md) supersede these counts. At closeout MAIN had
38 exact source owners / 43 CODE extents / 101 functions / 11628 owned bytes.
OP, MAINL and ZUN retain source-presence observations with exact0. Candidate
and modeled-runtime observations keep their existing qualifications.

## Scope of this closeout

Product code, compatibility headers, ownership manifests, target bytes and
Oracle-bearing reconstruction scripts retain their attested contents and paths.
Cleanup does not promote or revoke an exact claim. At closeout the README reported
those counts and stopped status; the handoff was condensed and directed historical
probe details to bounded notes and ledgers. The earlier input/math document is
explicitly labeled a historical checkpoint. Script and note indexes identify
current maintenance entry points.

Private cleanup follows the existing protected-state policy and additionally
keeps literal `.analysis/` references in tracked documents, scripts and ledgers.
Targets, tools, the game-local Wine prefix, runtime images, Ghidra state,
complete cold receipt trees, live proof dependencies and meaningful failure
transcripts remain. Age alone does not decide deletion.

Three superseded unaccepted diagnostic snapshots are selected separately:
prototype drawing, preliminary CRT and the initial shared-input review. They
have no tracked, ledger or live retained-JSON dependency. Old cleanup corpus
fingerprints record their former existence and remain historical; their hashes
are not rebased. Retirement records retain original hashes, sizes and reasons.

## Audit and replay

The MAIN aggregate at closeout had 152 recorded source/input guards: 149 matched.
Its `config/units.csv`, `config/evidence.csv` and `docs/PROGRESS.md` snapshots
already differed before closeout because subsequent work updated those records.
The baseline Git commit and cleanup-time hashes are recorded in
`.analysis/closeout/sol-closeout-20261006/main-aggregate-guard-audit.json`.
The old receipt is unchanged; no new cold MAIN aggregate was run to replace it.
At that checkpoint OP/MAINL source 733, diagnostic 723 and coverage 748 guards passed.

The cleanup tool records its frozen candidate list, reference corpus, retired
proofs and retained input states. Before deletion it checks both file contents
and file-set changes, including new proof dependencies. Historical missing or
stale guards are preserved as found, rather than repaired. Fourteen controls
exercise documentation preservation, cold receipt retention, candidate/reference
races, symlink boundaries, explicit retirement, escaped JSON dependencies and unsafe output rejection.

```sh
python3 scripts/closeout_cleanup.py --output .analysis/closeout/UNIQUE/receipt.json
python3 scripts/closeout_cleanup.py --output .analysis/closeout/ANOTHER/receipt.json --apply
```

`--retire-proof PATH` requires an explicit top-level unaccepted diagnostic and
rejects live references and source/exact acceptance. Finish every build/replay
before cleanup. Each audit needs a fresh receipt path. The final closeout
receipt and verification logs reside under
`.analysis/closeout/sol-closeout-20261006/`.

The first cleanup removed 32,409 files / 446,056,881 bytes (425.4 MiB), with 2,957
retained input states unchanged. All 206 product/compat/target-manifest/MAIN-owner
inputs match their before-cleanup hashes. Original cleanup tool/control-source
versions are snapshotted in the audit directory; its receipt remains unchanged
after strengthening escaped-reference checks. The final post-CI receipt uses
the strengthened tool. No full reconstruction build is claimed from this
maintenance pass.

## Final verification

Closeout CI: 607 tests / 50.517 seconds and all available private headless gates passed.
Log `.analysis/closeout/sol-closeout-20261006/ci-final.log`, SHA256
`9b1488f342b6561e268f406f131d81aeaf39d5c04226b84c48694db4ff5b0187`.
The fourteen focused controls pass, all local Markdown links resolve, target
verification passes, tracking/index/progress checks pass and whitespace is clean.
MAIN/OP/MAINL/ZUN ownership and exact counts remain unchanged.

Post-CI cleanup removed 191 regenerated cache files / 4,263,838 bytes, with 2,968
retained states unchanged. Receipt
`.analysis/closeout/sol-closeout-post-ci-20261007/receipt.json`, SHA256
`134488d54a9e74d11ab5bd0adc90b0c5b68e588b2ae72d5921323960376f336d`. Total closeout:
**32,600 files / 450,320,719 bytes (429.5 MiB)**. Final checks used Python `-B`
to keep caches absent. Closeout completed on 2026-10-07 (Asia/Singapore).
