# Reconstruction workflow

1. Inspect Git and `docs/RE_HANDOFF.md`; run `python3 scripts/preflight.py`.
2. Select a bounded source/ownership question. Before using database observations,
   run `python3 scripts/ghidra.py ARTIFACT check`.
3. Recover natural source and compile/link with the pinned native tools.
   Preserve 16-bit widths, near/far/Pascal ABI, layout and link order.
4. For exact acceptance, check complete raw bytes, literal ordered relocations,
   ownership, ABI/MAP/layout, affected behavior and two independent cold builds.
   Required checks are in `config/oracles.toml`; compiler success alone is insufficient.
   Use `scripts/review_th03_op_vs_work.py` for the SDK-guarded OP cold pair,
   cfg, dispatch, attract, sound, initializer/helper, renderer and VS caller reviews. It
   invokes the renderer/helper/sound/attract/dispatch/cfg chain once. Renderer switch-table
   bytes remain separate from instruction execution coverage. Its `--current-cold` mode revalidates a
   complete existing source/SDK/recipe/output-bound pair and runs all new helper
   gates; use it when product sources and native recipes have not changed.
   The VS model executes its real owned helpers, while character-selection
   procedures remain explicit unowned interfaces. The real title-box dependency
   receives no additional ownership credit. OP and MAINL sound scopes use independently checked native layouts
   with a shared execution core; refresh both reports after core changes.
   Preserve separate ordinary-entry and loop-continuation witness counts; the
   supplied SI continuation states do not prove elapsed frames. After rebuilding
   OP or MAINL, run `scripts/review_th03_shared_input_work.py`
   before republishing their source scopes. Its complete input models bind both
   current cold reports; status only replays short ABI cases. If shared acceptance
   helpers change, refresh all three product publications before regenerating progress.
   Use `scripts/review_th03_mainl_root_helpers_work.py` for one complete MAINL cold pair,
   six sound/timing reviews and five root helper reviews, then refresh shared input and publish.
   Its `--current-cold` mode revalidates the entire source/SDK/output graph before
   replaying all sound gates. Counter-update fixtures do not prove elapsed time
   or physical IRQ delivery. Adjacent explicit codestring padding remains open.
   Root helper contracts check every physical stack byte, GRCG port width/order/IF,
   both complete WORD seed lanes and all BYTE character pairs. Keep private
   STR_IEQ's near caller proof and its 9F00 equality result; three adjacent NOPs
   remain separate from function ownership and instruction coverage. Historical
   145-owner product receipts cannot accept the refined 149-extent inventory.
   Use `scripts/review_th03_zun_directory_work.py` for the complete ZUN cold pair,
   formatter, graphics, lifecycle, header/DATA, wrapper and directory reviews. It invokes the wrapper/DATA/lifecycle/graphics/formatter
   chain once. All six support `--current-cold` to revalidate existing source/output-bound
   prerequisites and rerun their own full gates without rebuilding.
   Publish ZUN scopes after this review. DATA consumers must read the original
   defaults/messages/tables from the initialized image; mutable argument inputs
   must be explicit. Keep static DATA-byte mutations separate from executed
   instruction mutations. Header/table callback checks stop at the selected
   entry, whose behavior is covered by its existing procedure scope. The two
   reserved DATA runs remain excluded. Treat CFG-proved unreachable CODE
   separately from executed instruction coverage. DOS 4C/31 termination also
   bounds lifecycle reachability; preserve the fifteen following bytes without
   counting them as executed. Real maintained nested helpers must execute.
   Wrapper coordinates belong to the outer decoded COM, not a child payload.
   Check all registers, defined flags, ordered stores and complete memory;
   preserve the retained count WORD and stop before payload execution. The
   directory's 324 metadata bytes receive separate DATA-TU credit. Check all
   seven actual linked-length definitions in both cold rounds, complete raw
   OBJ/COM/MAP outputs, bounded LIDATA expansion and both capacity controls.
   Native directory composition lives in `lib/zun_directory_source.py`; the
   shared `lib/zun.py` remains a frozen MAIN scheduling input. Keep its pin.
   Unused format slots have no instruction-execution credit. Direct transfer
   entry cases require DF=0. DOS AL replies are explicit bounded policies;
   do not assume that AH-only termination clears the exit status.
   `scripts/probe_th03_sound_nop_layout.py` is a non-accepting diagnosis over
   both current pairs. It recompiles selected sound copies and links against
   the unchanged remaining objects in a disposable DOS workspace. Generated
   assembly BYTE/WORD annotations are explicit controls, with zero source,
   authored-byte or whole-product credit even when header/relocation equality
   returns. Do not use their near matches as an exactness gate.
5. Record useful findings in the ledgers/current handoff, run focused checks,
   `python3 scripts/ci.py` and `git diff --check`, then commit.

Use `.venv/bin/python` for checks. Clear DISPLAY/WAYLAND_DISPLAY and serialize
Borland/Wine writers. Keep heavy work on one CPU at nice10. Ghidra heap limits
can be passed through `_JAVA_OPTIONS="-Xmx768m -XX:ActiveProcessorCount=1"`.

Keep one useful working tree. Delete obsolete experiments, duplicate builds,
logs and caches after use. Old validation outputs are not retention requirements;
future exact claims require fresh verification. Do not change target bytes,
pad code or invent ABI declarations to obtain equality.
Installed tools stay pinned; download archives and installation media can be
deleted after installation. Keep current findings in source, ledgers and the
handoff, without requiring old validation directories to remain on disk.
