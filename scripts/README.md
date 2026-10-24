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
| `publish_th03_op_work_scopes.py` | Independently replay the current cold bindings, OMF/MAP ownership, instruction contracts and eleven required gates for twelve decoded lifecycle/input functions (500 bytes), including seventeen literal relocations. Publish source acceptance separately from canonical packed-file unit credit and whole-product ownership. No old private verification trees are inputs. |
| `build_th03_mainl_work.py` | Build all 36 MAINL project objects and six CRT providers twice, use normal TLIB extraction/rebuild to preserve the 893-member library order, compare all 938 raw outputs and complete decoded/stored targets, then execute the four lifecycle owner/ABI models. Bind the three consumed SDK headers to the pinned installation before and after native builds. Reference source and 887 vendor members remain unowned context. |
| `publish_th03_mainl_work_scopes.py` | Independently revalidate the complete current 938-output cold graph, library membership, consumed source/SDK headers, thirteen complete function owners, twenty-five literal relocations and eleven scoped gates. Publish thirteen decoded source functions / 577 bytes; canonical packed-file unit credit and whole-product source ownership remain separate. |
| `review_th03_shared_input_work.py` | After fresh OP/MAINL cold pairs, independently review their complete shared nine-function / 367-byte input producer. Resolve all 58 native fields and ten ordinary TLINK call relaxations, bind six literal ordered relocations per product, and execute 2,218 guest cases per image with nineteen mutation controls. Status rechecks bindings and twelve short cases per image; keyboard/joystick/timing bodies remain interfaces. |
| `bootstrap_jwasm.py` | Build the bounded ZUN compatible OMF emitter from the pinned public source commit; `--check` checks source/archive/executable identity and the observed version/help exit status. This does not identify the original assembler. |
| `build_th03_zun_driver_work.py` | Build the complete maintained -4 driver twice through pinned JWasm plus the normal TLINK, check all 56 public addresses and tiny layout, compare the entire decoded payload, and reject the actual ten-byte TASM control. Outer launcher/storage and formal acceptance remain separate. |
| `build_th03_zun_work.py` | Build wrapper and -2/-3/-4/-5 twice; repeat 23 raw outputs and complete decoded/stored targets. Execute five full models and reject 80 guest mutants; nine command procedures / 361 CODE bytes run 6,678 cases per image. Driver has nine natural CODE contributions, 71 linker bytes, native EVEN and 206 real fixups; sixteen scalar and thirty command fixups bind twenty-five library owners. Native WORD/no-EVEN source controls reject equality without changing procedure includes. Bind runtime/startup and SDK copies. Driver remainder/12 reserved DATA bytes and whole-product acceptance stay open. |
| `publish_th03_zun_work_scopes.py` | Revalidate current cold recipe, every output and complete scoped -2/-3/-4/-5 ownership. Bind five full runtime witnesses and execute 104 short ABI cases. Publish 38 decoded extents / 46 procedures / 3,017 CODE bytes. Keep 789 library CODE bytes and init's original-ASM 607 CODE + 783 DATA separate from 1,621 authored bytes; canonical packed-file unit credit stays unchanged. |
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
