# Current entry points

Run these from the repository root with `.venv/bin/python scripts/SCRIPT`.

| Script | Purpose |
| --- | --- |
| `preflight.py` | Check the environment, pinned targets and tracking before work. |
| `replay_th03_main_native.py` | Rebuild two independent MAIN source trees, compare all native outputs and review accepted owners. This is the current MAIN replay entry point. |
| `build_th03_main_work.py --build --cold --runtime` | Run one fresh MAIN source build, with entry/lose runtime checks. |
| `review_th03_main_native_units.py` | Review all configured extents and native-owner gates against the current cold pair. |
| `probe_th03_main_producers.py` | Replay unresolved renderer, state/shot grouping and alignment controls. Diagnostic only; temporary native products are removed. |
| `ci.py` | Run tests, tracking/progress checks and available local tool/database checks. |
| `build_th03_op_work.py` | Build all 30 OP objects twice from current source, compare raw OBJ/EXE/MAP and the complete decoded target, repeat canonical DIET packing and run exit/plane ownership/ABI models. `--review` revalidates current source/output/recipe bindings, repeats packing and reruns scoped checks. Reference source and vendor libraries remain unowned context. |
| `publish_th03_op_work_scopes.py` | Independently replay the current cold bindings, OMF/MAP ownership, instruction contracts and eleven required gates for the three decoded exit/plane functions (133 bytes). Publish source acceptance separately from canonical packed-file unit credit and whole-product ownership. No old private verification trees are inputs. |
| `build_th03_mainl_work.py` | Build all 36 MAINL project objects and six CRT providers twice, use normal TLIB extraction/rebuild to preserve the 893-member library order, compare all 938 raw outputs and complete decoded/stored targets, then execute the four lifecycle owner/ABI models. Bind the three consumed SDK headers to the pinned installation before and after native builds. Reference source and 887 vendor members remain unowned context. |
| `publish_th03_mainl_work_scopes.py` | Independently revalidate the complete current 938-output cold graph, library membership, consumed source/SDK headers, four complete native owners, nineteen literal relocations and eleven scoped gates. Publish four decoded lifecycle source functions / 210 bytes; canonical packed-file unit credit and whole-product source ownership remain separate. |
| `bootstrap_jwasm.py` | Build the bounded ZUN compatible OMF emitter from the pinned public source commit; `--check` checks source/archive/executable identity and the observed version/help exit status. This does not identify the original assembler. |
| `build_th03_zun_driver_work.py` | Build the complete maintained -4 driver twice through pinned JWasm plus the normal TLINK, check all 56 public addresses and tiny layout, compare the entire decoded payload, and reject the actual ten-byte TASM control. Outer launcher/storage and formal acceptance remain separate. |
| `build_th03_zun_work.py` | Build the wrapper and -2/-3/-4/-5 twice, compose actual outputs with explicit unowned -1, compare all 23 raw outputs and complete decoded/stored targets. Run wrapper/transfer, 5,111-case/image logo and 3,548-case/image resident contracts; reject 34 actual guest mutations. Bind consumed tiny runtime/startup copies and the resident SDK before/after execution. Unowned context and whole-product acceptance remain separate. |
| `publish_th03_zun_work_scopes.py` | Revalidate the current cold recipe, every output, complete -3/-5 CODE/DATA/BSS and all twelve owned entries. Bind both full runtime witnesses and execute thirty short ABI cases, without repeating full models in each status view. Publish twelve decoded functions / 1,621 bytes separately from canonical packed-file unit credit. |
| `ghidra.py ARTIFACT check` | Re-attest the headless database before using its observations. |
| `attest_toolchain.py` | Check installed native tools and repeat execution probes; temporary probe trees are removed automatically. |
| `verify_targets.py` | Check canonical target hashes. |
| `status.py`, `progress.py` | Read ledger-derived progress; `progress.py --check` checks generated progress documents. |

Heavy tools run headless, on one available CPU at nice10. Keep one Borland/Wine
writer at a time. Current MAIN outputs use
`.analysis/toolchain/wineprefix/drive_c/TH03WORK`; reports use `.analysis/work`.

Historical replay helpers may refer to deleted private runs. Those outputs were
intentionally discarded; use fresh source builds for new exact verification.
Keep useful source, contracts and replay scripts; old generated verification
trees, logs and caches can be deleted. The installed Wine prefix and tools are
reused by subsequent agents. See [the handoff](../docs/RE_HANDOFF.md) for the next
reconstruction question and [the full README](../README.md) for installation.
