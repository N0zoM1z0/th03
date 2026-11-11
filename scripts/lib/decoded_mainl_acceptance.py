"""Current decoded MAINL scopes from retained cold evidence and native refreshes."""

import contextlib
import csv
import io
import json
import subprocess
from pathlib import Path
import tomllib

from lib.borland_library import compare_members, library_members
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, read_verified_artifact
from lib.toolchain import attest_surface
from lib.mainl_lifecycle_layout import OWNERS, verify as layout
from lib.mainl_lifecycle_runtime import verify as runtime, negative_controls
from lib.op_work_acceptance import GATES, sha, digest, oracle_rows as shared_oracle_rows


from review_th03_shared_input_work import current_scope as input_scope
from lib.shared_input_layout import SOURCE as INPUT_SOURCE, WRAPPER as INPUT_WRAPPER
from lib.mainl_wait_layout import SOURCE as WAIT_SOURCE, WRAPPER as WAIT_WRAPPER
from review_th03_mainl_sound_work import current_scope as sound_scope
from review_th03_mainl_root_helpers_work import current_scope as root_helper_scope
from review_th03_mainl_pi_free_work import current_scope as pi_free_scope
from review_th03_mainl_pi_work import current_scope as pi_scope
from review_th03_mainl_cdg_work import current_scope as cdg_scope
from review_th03_mainl_cdg_draw_work import current_scope as cdg_draw_scope
from review_th03_mainl_ending_work import current_scope as ending_scope
from review_th03_mainl_staff_draw_work import current_scope as staff_draw_scope
from review_th03_mainl_snow_work import current_scope as snow_scope
from review_th03_mainl_dissolve_work import current_scope as dissolve_scope
from review_th03_mainl_staff_callers_work import current_scope as staff_callers_scope
from review_th03_mainl_staff_hold_work import current_scope as staff_hold_scope
from review_th03_mainl_staff_single_work import current_scope as staff_single_scope
from review_th03_mainl_staff_pair_work import current_scope as staff_pair_scope
from review_th03_mainl_staff_verdict_work import current_scope as staff_verdict_scope
from review_th03_mainl_staff_data_work import current_scope as staff_data_scope
from review_th03_mainl_staff_roll_work import current_scope as staff_roll_scope
from review_th03_mainl_cutscene_work import current_scope as cutscene_scope, INPUTS as CUTSCENE_INPUTS
from review_th03_mainl_registration_work import current_scope as registration_scope, INPUTS as REGISTRATION_INPUTS
from review_th03_mainl_scoredat_work import current_scope as scoredat_scope, INPUTS as SCOREDAT_INPUTS
from review_th03_mainl_root_orchestration_work import current_scope as root_orchestration_scope, INPUTS as ROOT_ORCHESTRATION_INPUTS
from review_th03_mainl_text_work import current_scope as text_scope, INPUTS as TEXT_INPUTS
from lib.decoded_mainl_root_orchestration_layout import transport as root_transport
from lib.decoded_mainl_pi_decoder_native import verify as pi_decoder_scope, review_library_origins
from lib.decoded_mainl_resources_native import verify as resources_scope, TABLE_UNIT, TABLE_SOURCE
from lib.decoded_mainl_file_native import verify as file_scope, DATA_UNIT as FILE_DATA_UNIT, SELECTED_SOURCE as FILE_STATE_SOURCE
from lib.decoded_mainl_bfnt_native import verify as bfnt_scope, DATA_UNIT as BFNT_DATA_UNIT, SELECTED_SOURCE as BFNT_SIGNATURE_SOURCE
from lib.decoded_mainl_archive_native import verify as archive_scope, DATA_UNIT as ARCHIVE_DATA_UNIT, SELECTED_SOURCE as ARCHIVE_STATE_SOURCE
from lib.decoded_mainl_graphics_native import verify as graphics_scope, DATA_SOURCES as GRAPHICS_DATA_SOURCES
from lib.decoded_mainl_display_native import verify as display_scope, DATA_SOURCES as DISPLAY_DATA_SOURCES
from lib.decoded_mainl_crt_native import verify as crt_scope, SOURCE_MAP as CRT_SOURCE_MAP
from lib.decoded_mainl_resident_native import verify as resident_scope, DATA_SOURCES as RESIDENT_DATA_SOURCES
from lib.decoded_mainl_farheap_native import verify as farheap_scope, UNIT as FARHEAP_UNIT, SOURCE as FARHEAP_SOURCE
from lib.decoded_mainl_exec_native import verify as exec_scope, UNIT as EXEC_UNIT, SOURCE as EXEC_SOURCE
from lib.decoded_mainl_loadprog_native import verify as loadprog_scope, UNITS as LOADPROG_UNITS, SOURCE as LOADPROG_SOURCE
from lib.decoded_mainl_dosconstruct_native import verify as dosconstruct_scope, SOURCE_MAP as DOSCONSTRUCT_SOURCE_MAP
from lib.decoded_mainl_path_native import verify as path_scope, SOURCE_MAP as PATH_SOURCE_MAP
from lib.decoded_mainl_stdio_native import verify as stdio_scope, SOURCE_MAP as STDIO_SOURCE_MAP
from lib.decoded_mainl_exception_native import verify as exception_scope, SOURCE_MAP as EXCEPTION_SOURCE_MAP
from lib.decoded_mainl_completion_native import verify as completion_scope
from lib.decoded_mainl_switch_native import verify as switch_scope
from lib.decoded_mainl_root_state_native import verify as root_state_scope, SOURCE_MAP as ROOT_STATE_SOURCE_MAP
from lib.decoded_mainl_picture_files_native import verify as picture_files_scope, SOURCE_MAP as PICTURE_FILES_SOURCE_MAP
from lib.decoded_mainl_text_banks_native import verify as text_banks_scope, SOURCE_MAP as TEXT_BANKS_SOURCE_MAP
from lib.decoded_mainl_registration_layout import SOURCE as REGISTRATION_SOURCE, WRAPPER as REGISTRATION_WRAPPER
from lib.decoded_mainl_ending_layout import SOURCE as ENDING_SOURCE, WRAPPER as ENDING_WRAPPER
from lib.decoded_mainl_root_helpers_layout import OBJECT as ROOT_OBJECT, WRAPPER as ROOT_WRAPPER


PUBLICATION = "config/mainl_work/scoped_acceptance.json"
BASELINE = "3e7e9dd87dd6899596c1c73295e3ee62d87e443c"
COMMAND = ".venv/bin/python scripts/publish_th03_mainl_work_scopes.py"
PROOF_INPUTS = ("scripts/lib/decoded_mainl_acceptance.py", "scripts/publish_th03_mainl_work_scopes.py",
                "scripts/lib/op_work_acceptance.py", "scripts/validate_tracking.py",
                "config/oracles.toml", "scripts/review_th03_shared_input_work.py",
                "scripts/lib/shared_input_layout.py", "scripts/lib/shared_input_runtime.py",
                "scripts/lib/mainl_wait_layout.py", "scripts/lib/mainl_wait_runtime.py",
                "scripts/review_th03_mainl_sound_work.py", "scripts/lib/decoded_mainl_sound_layout.py", "scripts/lib/decoded_mainl_sound_runtime.py",
                "scripts/lib/shared_sound_runtime.py", "scripts/lib/op_sound_layout.py",
                "scripts/review_th03_mainl_root_helpers_work.py", "scripts/lib/decoded_mainl_root_helpers_layout.py",
                "scripts/lib/decoded_mainl_root_helpers_runtime.py",
                "scripts/review_th03_mainl_pi_free_work.py", "scripts/lib/decoded_mainl_pi_free_layout.py",
                "scripts/lib/decoded_mainl_pi_free_runtime.py",
                "scripts/review_th03_mainl_pi_work.py", "scripts/lib/decoded_mainl_pi_layout.py",
                "scripts/lib/decoded_mainl_pi_runtime.py",
                "scripts/review_th03_mainl_cdg_work.py", "scripts/lib/decoded_mainl_cdg_layout.py",
                "scripts/lib/decoded_mainl_cdg_runtime.py",
                "scripts/review_th03_mainl_cdg_draw_work.py", "scripts/lib/decoded_mainl_cdg_draw_layout.py",
                "scripts/lib/decoded_mainl_cdg_draw_runtime.py",
                "scripts/review_th03_mainl_ending_work.py", "scripts/lib/decoded_mainl_ending_layout.py",
                "scripts/lib/decoded_mainl_ending_runtime.py",
                "scripts/review_th03_mainl_staff_draw_work.py", "scripts/lib/decoded_mainl_staff_draw_layout.py",
                "scripts/lib/decoded_mainl_staff_draw_runtime.py",
                "scripts/review_th03_mainl_snow_work.py", "scripts/lib/decoded_mainl_snow_layout.py",
                "scripts/lib/decoded_mainl_snow_runtime.py",
                "scripts/review_th03_mainl_dissolve_work.py", "scripts/lib/decoded_mainl_dissolve_layout.py",
                "scripts/lib/decoded_mainl_dissolve_runtime.py",
                "scripts/review_th03_mainl_staff_callers_work.py", "scripts/lib/decoded_mainl_staff_callers_layout.py",
                "scripts/lib/decoded_mainl_staff_callers_runtime.py",
                "scripts/review_th03_mainl_staff_hold_work.py", "scripts/lib/decoded_mainl_staff_hold_layout.py",
                "scripts/lib/decoded_mainl_staff_hold_runtime.py",
                "scripts/review_th03_mainl_staff_single_work.py", "scripts/lib/decoded_mainl_staff_single_layout.py",
                "scripts/lib/decoded_mainl_staff_single_runtime.py",
                "scripts/review_th03_mainl_staff_pair_work.py", "scripts/lib/decoded_mainl_staff_pair_layout.py",
                "scripts/lib/decoded_mainl_staff_pair_runtime.py",
                "scripts/review_th03_mainl_staff_verdict_work.py", "scripts/lib/decoded_mainl_staff_verdict_layout.py",
                "scripts/lib/decoded_mainl_staff_verdict_runtime.py",
                "scripts/review_th03_mainl_staff_data_work.py", "scripts/lib/decoded_mainl_staff_data_layout.py",
                "scripts/lib/decoded_mainl_staff_data_runtime.py",
                "scripts/review_th03_mainl_staff_roll_work.py", "scripts/lib/decoded_mainl_staff_roll_layout.py",
                "scripts/lib/decoded_mainl_staff_roll_services.py", "scripts/lib/decoded_mainl_staff_roll_machine.py",
                "scripts/lib/decoded_mainl_staff_roll_runtime.py", "scripts/lib/decoded_mainl_staff_roll_proofs.py")

PROOF_INPUTS = tuple(dict.fromkeys((*PROOF_INPUTS, *CUTSCENE_INPUTS, *REGISTRATION_INPUTS, *SCOREDAT_INPUTS, *ROOT_ORCHESTRATION_INPUTS, *TEXT_INPUTS,
    "scripts/build_th03_mainl_linked_current.py", "scripts/lib/decoded_mainl_linked_current.py",
    "scripts/build_th03_mainl_function_bodies.py",
    "scripts/build_th03_mainl_current.py", "scripts/stage_th03_mainl_fullcold.py",
    "scripts/lib/decoded_mainl_pi_decoder_native.py", "scripts/lib/op_asset_native.py", "scripts/lib/op_shared_native.py",
    "scripts/lib/decoded_mainl_resources_native.py", "scripts/build_th03_mainl_resources_work.py",
    "scripts/lib/decoded_mainl_file_native.py", "scripts/build_th03_mainl_file_work.py",
    "scripts/lib/decoded_mainl_bfnt_native.py", "scripts/build_th03_mainl_bfnt_work.py",
    "scripts/lib/decoded_mainl_archive_native.py", "scripts/build_th03_mainl_archive_work.py",
    "scripts/lib/decoded_mainl_graphics_native.py", "scripts/build_th03_mainl_graphics_work.py",
    "scripts/lib/decoded_mainl_display_native.py", "scripts/build_th03_mainl_display_work.py",
    "scripts/lib/decoded_mainl_crt_native.py",
    "scripts/lib/decoded_mainl_resident_native.py", "scripts/build_th03_mainl_resident_work.py",
    "scripts/lib/decoded_mainl_farheap_native.py", "scripts/build_th03_mainl_farheap_work.py",
    "scripts/lib/decoded_mainl_exec_native.py", "scripts/build_th03_mainl_exec_work.py",
    "scripts/lib/decoded_mainl_loadprog_native.py", "scripts/build_th03_mainl_loadprog_work.py",
    "scripts/lib/decoded_mainl_dosconstruct_native.py", "scripts/build_th03_mainl_dosconstruct_work.py",
    "scripts/lib/decoded_mainl_path_native.py", "scripts/build_th03_mainl_path_work.py",
    "scripts/lib/decoded_mainl_stdio_native.py", "scripts/build_th03_mainl_stdio_work.py",
    "scripts/lib/decoded_mainl_exception_native.py", "scripts/build_th03_mainl_exception_work.py",
    "config/mainl_work/exception_toolchain.toml", "scripts/lib/decoded_mainl_completion_native.py",
    "scripts/build_th03_mainl_after332_work.py", "scripts/build_th03_mainl_after493_work.py",
    "scripts/lib/decoded_mainl_switch_native.py", "config/mainl_work/switch_tables_after551.json",
    "scripts/lib/decoded_mainl_root_state_native.py", "scripts/build_th03_mainl_root_state_work.py",
    "scripts/review_th03_mainl_root_state_work.py", "config/mainl_work/root_state_after552.json",
    "scripts/lib/decoded_mainl_picture_files_native.py", "scripts/build_th03_mainl_picture_files_work.py",
    "scripts/review_th03_mainl_picture_files_work.py", "config/mainl_work/picture_files_after553.json",
    "src/mainl/root/picture_files.c",
    "scripts/lib/decoded_mainl_text_banks_native.py", "scripts/build_th03_mainl_text_banks_work.py",
    "scripts/review_th03_mainl_text_banks_work.py", "config/mainl_work/text_banks_after554.json",
    "src/mainl/data/registration.asm", "src/mainl/data/ending_text.asm", "src/mainl/hiscore/regi_codes.inc",
    "src/mainl/root/recovered/complete.cpp", "src/mainl/root/recovered/cfg_load.inl",
    "src/mainl/root/recovered/win.inl", "src/mainl/root/recovered/state.inl")))

def need(value, message):
    if not value:
        raise ValueError("current MAINL acceptance: " + message)


def proof_inputs(root):
    return {n: sha((root / n).read_bytes()) for n in PROOF_INPUTS}


def oracle_rows(proof, now, policy):
    rows = shared_oracle_rows(proof, now, policy, artifact="th03-mainl", publication_path=PUBLICATION,
                              prefix="ev-mainl-current-", command=COMMAND)
    if 'current_native_refresh' in proof['scope']:
        linked_units = {o['unit_id'] for o in proof['scope'].get('current_linked_native', {}).get('owners', [])}
        for unit_id, owner_rows in rows.items():
            for row in owner_rows.values():
                row['tool'] = ('two current 36-object MAINL builds, source xx and bounded natural function bodies'
                               if unit_id in linked_units else
                               'retained MAINL cold pair plus two current physical-owner builds and complete native links')
                row['command'] = COMMAND + ' --stage ' + proof['scope']['current_native_refresh']['stage']
    return rows


def audit(root, *, stage=None):
    import build_th03_mainl_work as build
    from build_th03_mainl_current import CURRENT_STAGE, SOURCES, source_graph, review as current_review
    from build_th03_op_work import compare_mz
    import validate_tracking as tracking
    root = Path(root)
    need(root.resolve() == build.ROOT, "live repository root")
    work = build.WORK
    raw_report = (build.OUT / "mainl-build.json").read_bytes()
    report = json.loads(raw_report)
    need(report["complete"] and report["raw_repeat_equal"] and report["retained_project_objects"] == 0,
         "complete source-only cold pair")
    if stage is None:
        installed = root / PUBLICATION
        published = json.loads(installed.read_bytes()) if installed.is_file() else {}
        stage = published.get('audit', {}).get('scope', {}).get('current_native_refresh', {}).get('stage', CURRENT_STAGE)
    refresh = current_review(stage)
    current_work = root / refresh['current_work']
    current_files = {n: (current_work / n).read_bytes()
                     for n in refresh['current_source_inventory_sha256']}
    need(report["vendor_header_sha256"] == build.vendor_header_inventory(), "consumed vendor header drift")
    files, graph, archive_sha = source_graph(False)
    need(report["source_sha256"] == {n: sha(b) for n, b in sorted(files.items())}
         and report["archive_sha256"] == archive_sha, "retained cold source graph drift")
    need(all((work / n).read_bytes() == b for n, b in files.items()), "retained cold source snapshot drift")
    need([r["round"] for r in report["rounds"]] == [1, 2], "two independent rounds")
    outputs = report["rounds"][0]["outputs"]
    need(len(outputs) == 938 and outputs == report["rounds"][1]["outputs"], "complete raw cold output vector")
    fresh = {r["output"] for r in graph} | {"owned/" + n + ".obj" for n in build.CRT}
    need(len(fresh) == 42, "36 project and six fresh CRT producers")
    for name, row in outputs.items():
        raw = (work / name).read_bytes()
        need(row == dict(bytes=len(raw), sha256=sha(raw)), "current output drift: " + name)
        if name in fresh:
            description = describe_omf(raw)
            need(description["valid"], "fresh native OMF integrity: " + name)
            build.verify_vendor_dependencies(description, report["vendor_header_sha256"])
    config = tomllib.loads((root / "config/toolchain.toml").read_text())
    surfaces = [attest_surface(root, s) for s in config["surfaces"] if not s.get("bootstrap_only")]
    need(report["toolchain_surfaces"] == surfaces and all(s["pass"] or not s["required"] for s in surfaces),
         "current toolchain identity")
    prefix = root / config["paths"]["wine_prefix"]
    need(sha((prefix / "drive_c/TC4/BIN/TLIB.EXE").read_bytes()) == report["tlib_sha256"] == build.TLIB_SHA,
         "normal TLIB identity")
    vendor = (prefix / "drive_c/TC4/LIB/CL.LIB").read_bytes()
    need(sha(vendor) == report["vendor_library_sha256"], "vendor library identity")
    original = library_members(vendor)
    need(len(original) == 893, "complete vendor member inventory")
    replacements = {n: (work / "owned" / (n + ".obj")).read_bytes() for n in build.CRT}
    library = compare_members(original, library_members((work / "crt.lib").read_bytes()), replacements)
    need(all(r["library"] == library for r in report["rounds"]), "normal library rebuild proof")
    expected_outputs = fresh | {"vendor/" + m.name + ".obj" for m in original} | {"crt.lib", "bin/th03/mainl.exe", "obj/th03/mainl.map"}
    need(set(outputs) == expected_outputs, "complete output ownership")
    labels = []
    for rnd in (1, 2):
        labels += [f"round{rnd}:crt:" + n for n in build.CRT]
        labels += [f"round{rnd}:extract-vendor", f"round{rnd}:build-crt-library"]
        labels += [f"round{rnd}:" + r["output"] for r in graph] + [f"round{rnd}:link"]
    labels += ["diet:selfcheck", "diet:restore-target", "diet:pack1", "diet:roundtrip1", "diet:pack2", "diet:roundtrip2"]
    need([p["label"] for p in report["native_phases"]] == labels and
         all(p["returncode"] == (1 if p["label"].startswith("diet:") and p["label"] != "diet:selfcheck" else 0)
             for p in report["native_phases"]), "complete serial native execution schedule")
    targets = tomllib.loads((root / "config/targets.toml").read_text())
    stored = read_verified_artifact(root, find_artifact(targets, "th03-mainl"))
    declaration, = [a for a in tomllib.loads((root / "config/th03_diet.toml").read_text())["artifacts"] if a["id"] == "th03-mainl"]
    decoded = (work / "bin/th03/mainl.target.exe").read_bytes()
    need(len(decoded) == declaration["decoded_size"] and sha(decoded) == declaration["decoded_sha256"], "decoded target identity")
    candidate_raw = (work / "bin/th03/mainl.exe").read_bytes()
    target, candidate = parse_mz(decoded), parse_mz(candidate_raw)
    need(target.valid and candidate.valid and decoded == candidate_raw, "complete decoded file/format equality")
    need(compare_mz(candidate_raw, decoded) == report["comparison"], "independent MZ comparison")
    need((work / "bin/th03/mainl.packed.exe").read_bytes() == stored, "canonical stored equality")
    packing = report["packing"]
    need(packing["options"] == ["-B"] and packing["raw_repeat_equal"] and packing["stored_equal"]
         and packing["same_tool_roundtrip"] and len(packing["rounds"]) == 2, "two pack/restore rounds")
    need(all(p["sha256"] == sha(stored) and p["bytes"] == len(stored) and p["stored_equal"] and p["roundtrip_equal"]
             for p in packing["rounds"]), "complete stored/decoded roundtrip proof")
    # Revalidate the entire unchanged native graph above, then retain complete
    # prior ownership/runtime observations. New native source review does not
    # rerun every historical ancestor's emulator matrices.
    previous_raw = subprocess.check_output(['git', 'show', BASELINE + ':' + PUBLICATION], cwd=root)
    previous = json.loads(previous_raw)
    need(previous['schema'] == 'mainl-current-source-acceptance-v1' and
         previous['state'] == 'repository-local-accepted', 'reviewed prior97 checkpoint')
    adapted = {'scripts/lib/decoded_mainl_acceptance.py', 'scripts/status.py',
               'scripts/publish_th03_mainl_work_scopes.py',
               'scripts/lib/decoded_mainl_farheap_native.py', 'scripts/lib/decoded_mainl_stdio_native.py',
               *SOURCES.values()}
    # status.py only presents this result. Its spelling is not a native or
    # verifier input; caller-inventory validation belongs in the status adapter.
    for name, expected_hash in previous['proof_inputs'].items():
        if name not in adapted:
            need(sha((root / name).read_bytes()) == expected_hash, 'unchanged prior verifier input: ' + name)
    prior = previous['audit']
    need(prior['cold_report_sha256'] == sha(raw_report) and prior['recipe_sha256'] == report['recipe_sha256'] and
         prior['vendor_header_sha256'] == report['vendor_header_sha256'] and prior['library'] == library and
         prior['source_inventory_sha256'] == digest(report['source_sha256']) and
         prior['decoded_sha256'] == sha(decoded) and prior['stored_sha256'] == sha(stored),
         'complete unchanged prior source/tool/output/library/packing graph')
    policy = tomllib.loads((root / 'config/oracles.toml').read_text())
    need(previous['owner_oracles'] == oracle_rows(prior, previous['observed_utc'], policy),
         'complete previous scoped gate evidence remains intact')
    scope = json.loads(json.dumps(prior['scope']))
    old_scope_digest = digest(scope)
    scope['current_native_refresh'] = {k: v for k, v in refresh.items()
                                       if k != 'current_source_inventory_sha256'}
    owners = scope['owners']
    need(len(owners) == 97 and sum(o['size'] for o in owners) == 16362 and
         sum(o.get('procedure_count', 1) for o in owners) == 102,
         'complete previously accepted owner cohort, without duplicate historical aggregates')
    decoder = pi_decoder_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in decoder['owners']}),
         'new complete library decoder does not duplicate previous ownership')
    owners.extend(decoder['owners'])
    scope['pi_decoder_native'] = decoder
    scope['library_origin_review'] = review_library_origins(root, files, owners)
    resources = resources_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in resources['owners']}), 'separate complete SUPER and generated table owners')
    owners.extend(resources['owners'])
    scope['resources_native'] = resources
    file_native = file_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in file_native['owners']}), 'separate complete file/DOS/hook/state owners')
    owners.extend(file_native['owners'])
    scope['file_native'] = file_native
    bfnt_native = bfnt_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in bfnt_native['owners']}), 'separate complete BFNT source/ABI/signature owners')
    owners.extend(bfnt_native['owners'])
    scope['bfnt_native'] = bfnt_native
    archive_native = archive_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in archive_native['owners']}), 'separate complete buffered/archive reader owners')
    owners.extend(archive_native['owners'])
    scope['archive_native'] = archive_native
    graphics_native = graphics_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in graphics_native['owners']}), 'separate complete graphics/heap/state owners')
    owners.extend(graphics_native['owners'])
    scope['graphics_native'] = graphics_native
    display_native = display_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in display_native['owners']}), 'separate complete palette/VSync/gaiji/state owners')
    owners.extend(display_native['owners'])
    scope['display_native'] = display_native
    crt_native = crt_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in crt_native['owners']}), 'separate complete CRT library source owners')
    owners.extend(crt_native['owners'])
    scope['crt_native'] = crt_native
    resident_native = resident_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in resident_native['owners']}), 'separate complete resident/math/text/joystick owners')
    owners.extend(resident_native['owners'])
    scope['resident_native'] = resident_native
    farheap_native = farheap_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in farheap_native['owners']}), 'separate complete far-heap source owner')
    owners.extend(farheap_native['owners'])
    scope['farheap_native'] = farheap_native
    exec_native = exec_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in exec_native['owners']}), 'separate complete DOS overlay source owner')
    owners.extend(exec_native['owners'])
    scope['exec_native'] = exec_native
    loadprog_native = loadprog_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in loadprog_native['owners']}), 'separate complete program-loader CODE/DATA owners')
    owners.extend(loadprog_native['owners'])
    scope['loadprog_native'] = loadprog_native
    dosconstruct_native = dosconstruct_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in dosconstruct_native['owners']}), 'separate complete DOS command/environment source owners')
    owners.extend(dosconstruct_native['owners'])
    scope['dosconstruct_native'] = dosconstruct_native
    path_native = path_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in path_native['owners']}), 'separate complete DOS path CODE/DATA/INIT owners')
    owners.extend(path_native['owners'])
    scope['path_native'] = path_native
    stdio_native = stdio_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in stdio_native['owners']}), 'separate complete buffered I/O CODE/DATA/INIT owners')
    owners.extend(stdio_native['owners'])
    scope['stdio_native'] = stdio_native
    exception_native = exception_scope(root, work, target, candidate, graph, files)
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in exception_native['owners']}), 'separate complete C++ CODE/inline-EH/DATA/INIT/EXIT owners')
    owners.extend(exception_native['owners'])
    scope['exception_native'] = exception_native
    completion_native = completion_scope(root, work, target, candidate, graph, files)
    occupied = {site for o in owners for site in range(o['start'], o['start'] + o['size'])}
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in completion_native['owners']}) and
         all(not (set(range(o['start'], o['start'] + o['size'])) & occupied)
             for o in completion_native['owners']), 'disjoint complete project procedures and pointer DATA')
    owners.extend(completion_native['owners'])
    scope['completion_native'] = completion_native
    switches = switch_scope(root, current_work, target, candidate, graph, current_files)
    occupied = {site for o in owners for site in range(o['start'], o['start'] + o['size'])}
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in switches['owners']}) and
         all(not (set(range(o['start'], o['start'] + o['size'])) & occupied)
             for o in switches['owners']), 'generated tables/alignment remain disjoint from every instruction owner')
    owners.extend(switches['owners'])
    scope['switch_tables_native'] = switches
    root_state = root_state_scope(root, work, target, candidate, graph, files)
    occupied = {site for o in owners for site in range(o['start'], o['start'] + o['size'])}
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in root_state['owners']}) and
         all(not (set(range(o['start'], o['start'] + o['size'])) & occupied)
             for o in root_state['owners']), 'complete initialized root pointers; no BSS or old instruction overlap')
    owners.extend(root_state['owners'])
    scope['root_state_native'] = root_state
    pictures = picture_files_scope(root, work, target, candidate, graph, files)
    occupied = {site for o in owners for site in range(o['start'], o['start'] + o['size'])}
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in pictures['owners']}) and
         all(not (set(range(o['start'], o['start'] + o['size'])) & occupied)
             for o in pictures['owners']), 'complete near filename table; no strings or old instruction overlap')
    owners.extend(pictures['owners'])
    scope['picture_files_native'] = pictures
    text_banks = text_banks_scope(root, work, target, candidate, graph, files)
    occupied = {site for o in owners for site in range(o['start'], o['start'] + o['size'])}
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in text_banks['owners']}) and
         all(not (set(range(o['start'], o['start'] + o['size'])) & occupied)
             for o in text_banks['owners']), 'complete maintained text/state banks; no table, instruction or linker-gap credit')
    owners.extend(text_banks['owners'])
    scope['text_banks_native'] = text_banks
    from lib.decoded_mainl_linked_current import verify as linked_scope
    linked = linked_scope(root)
    occupied = {site for o in owners for site in range(o['start'], o['start'] + o['size'])}
    need(not ({o['unit_id'] for o in owners} & {o['unit_id'] for o in linked['owners']}) and
         all(not (set(range(o['start'], o['start'] + o['size'])) & occupied)
             for o in linked['owners']), 'disjoint complete xx, functions and natural producer ownership')
    owners.extend(linked['owners'])
    scope['current_linked_native'] = linked
    linked_units = {o['unit_id'] for o in linked['owners']}
    with (root / "config/units.csv").open() as stream:
        units = {u["id"]: u for u in csv.DictReader(stream)}
    for o in owners:
        # Only these two physical producers changed. Their compiler-consumed
        # input snapshots and complete native objects are revalidated above;
        # all other owners retain the unchanged cold/selected native inputs.
        rebound = o['source'] in SOURCES.values()
        bound_work = current_work if rebound else work
        bound_files = current_files if rebound else files
        bound_inventory = refresh['current_source_inventory_sha256'] if rebound else report['source_sha256']
        u = units[o["unit_id"]]
        segment = o.get("segment", 0xC7E)
        need(u["artifact"] == "th03-mainl" and u["segment"].lower() == f"decoded:{segment:04x}"
             and int(u["offset"], 0) + segment*16 == o["start"] and int(u["size"], 0) == int(u["compare_size"], 0) == o["size"]
             and u["state"] == "source-present" and u["origin"] == o.get("origin", "authored") and u["boundary_state"] == "reviewed"
             and not u["file_offset"] and u["source"] == o["source"], "current decoded ownership ledger")
        if o['unit_id'] in linked_units:
            # The complete current linked build binds these actual fresh
            # objects, source snapshots and all original fields independently.
            continue
        if o['unit_id'] in TEXT_BANKS_SOURCE_MAP:
            name = 'registration' if o['unit_id'].endswith('registration-initialized-bank') else 'ending'
            need((o['source'], o['object']) == TEXT_BANKS_SOURCE_MAP[o['unit_id']] and
                 o['maintained_native_object'] == '.analysis/work/text-banks-after554-native-round1-' + name + '.bin',
                 'actual standalone maintained semantic ASM bank in both fresh normal links')
            row = dict(source=o['source'], wrapper=o['source'])
        elif o['unit_id'] in PICTURE_FILES_SOURCE_MAP:
            need((o['source'], o['object']) == PICTURE_FILES_SOURCE_MAP[o['unit_id']] and
                 o['maintained_native_object'] == '.analysis/work/picture-files-after553-round1-obj.bin',
                 'actual natural C near-pointer table in both fresh normal links')
            row = dict(source=o['source'], wrapper=o['source'])
        elif o['unit_id'] in ROOT_STATE_SOURCE_MAP:
            need((o['source'], o['object']) == ROOT_STATE_SOURCE_MAP[o['unit_id']] and
                 o['maintained_native_object'] == '.analysis/work/root-state-after552-round1-obj.bin',
                 'actual complete root TU in both fresh normal links')
            row = dict(source=o['source'], wrapper=o['source'])
        elif o['unit_id'] in EXCEPTION_SOURCE_MAP:
            name = Path(o['object']).stem
            need((o['source'],o['object']) == EXCEPTION_SOURCE_MAP[o['unit_id']] and
                 o['maintained_native_object'] == '.analysis/work/exception-native-round1-'+name+'.obj', 'actual complete optimizing C++ producer in combined normal library')
            row = dict(source=o['source'],wrapper=o['source'])
        elif o['unit_id'] in STDIO_SOURCE_MAP:
            name = Path(o['object']).stem
            need((o['source'],o['object']) == STDIO_SOURCE_MAP[o['unit_id']] and
                 o['maintained_native_object'] == '.analysis/work/stdio-round1-'+name+'.obj', 'actual fresh buffered I/O CODE/DATA/INIT producer in combined normal library')
            row = dict(source=o['source'],wrapper=o['source'])
        elif o['unit_id'] in PATH_SOURCE_MAP:
            name = Path(o['object']).stem
            need((o['source'],o['object']) == PATH_SOURCE_MAP[o['unit_id']] and
                 o['maintained_native_object'] == '.analysis/work/path-round1-'+name+'.obj', 'actual fresh path CODE/DATA/INIT producer in combined normal library')
            row = dict(source=o['source'],wrapper=o['source'])
        elif o['unit_id'] in DOSCONSTRUCT_SOURCE_MAP:
            name = o['unit_id'].removeprefix('th03-mainl-decoded-crt-')
            need((o['source'],o['object']) == DOSCONSTRUCT_SOURCE_MAP[o['unit_id']] and
                 o['maintained_native_object'] == '.analysis/work/dosconstruct-round1-'+name+'.obj', 'actual fresh near constructor producer in combined normal library')
            row = dict(source=o['source'],wrapper=o['source'])
        elif o['unit_id'] in LOADPROG_UNITS:
            need(o['source'] == LOADPROG_SOURCE and o['object'] == 'vendor/loadprog.obj' and o['maintained_native_object'] == '.analysis/work/loadprog-round1.obj',
                 'actual fresh program-loader CODE/DATA producer in the combined normal library')
            row = dict(source=o['source'],wrapper=o['source'])
        elif o['unit_id'] == EXEC_UNIT:
            need(o['source'] == EXEC_SOURCE and o['object'] == 'vendor/exec.obj' and o['maintained_native_object'] == '.analysis/work/exec-round1.obj',
                 'actual fresh DOS overlay source producer in the combined normal library')
            row = dict(source=o['source'],wrapper=o['source'])
        elif o['unit_id'] == FARHEAP_UNIT:
            need(o['source'] == FARHEAP_SOURCE and o['object'] == 'vendor/farheap.obj' and o['maintained_native_object'] == '.analysis/work/farheap-round1.obj',
                 'actual fresh far-heap producer replaces only the contextual normal library member')
            row = dict(source=o['source'],wrapper=o['source'])
        elif o['unit_id'] in CRT_SOURCE_MAP:
            need((o['source'],o['object']) == CRT_SOURCE_MAP[o['unit_id']], 'actual bounded CRT producer ownership')
            # CRT TUs enter through the normal library, outside the36 project-object graph.
            row = dict(source=o['source'],wrapper='owned/'+Path(o['source']).name)
        else:
            row, = [r for r in graph if r["output"] == o["object"]]
        if o["object"] == ROOT_OBJECT:
            need(row["wrapper"] == ROOT_WRAPPER and row["source"] == ROOT_WRAPPER
                 and row["game"] == 3 and row["binary"] == "L" and row["first_binary"] == "mainl"
                 and (o['unit_id'] in (TABLE_UNIT, FILE_DATA_UNIT, BFNT_DATA_UNIT, ARCHIVE_DATA_UNIT) or o['unit_id'] in GRAPHICS_DATA_SOURCES or o['unit_id'] in DISPLAY_DATA_SOURCES or o['unit_id'] in RESIDENT_DATA_SOURCES or ('include '+o["source"]).encode() in bound_files[ROOT_WRAPPER]), "actual maintained root include producer")
            if o['unit_id'] == TABLE_UNIT:
                need(o['source'] == TABLE_SOURCE and o['maintained_native_object'] == '.analysis/work/resources-round1.obj',
                     'actual separately rebuilt generated table producer; frozen cold wrapper remains contextual')
            elif o['unit_id'] == FILE_DATA_UNIT:
                need(o['source'] == FILE_STATE_SOURCE and o['maintained_native_object'] == '.analysis/work/file-round1.obj',
                     'actual separately rebuilt file state producer; frozen cold wrapper remains contextual')
            elif o['unit_id'] == BFNT_DATA_UNIT:
                need(o['source'] == BFNT_SIGNATURE_SOURCE and o['maintained_native_object'] == '.analysis/work/bfnt-round1.obj',
                     'actual separately rebuilt BFNT signature producer; frozen cold wrapper remains contextual')
            elif o['unit_id'] == ARCHIVE_DATA_UNIT:
                need(o['source'] == ARCHIVE_STATE_SOURCE and o['maintained_native_object'] == '.analysis/work/archive-mini-round1-state.obj',
                     'actual independent five-byte state producer; legacy root fill remains contextual')
            elif o['unit_id'] in RESIDENT_DATA_SOURCES:
                module = 'resident' if o['unit_id'].endswith('resident-signature') else 'joystick'
                need(o['source'] == RESIDENT_DATA_SOURCES[o['unit_id']] and o['maintained_native_object'] == '.analysis/work/resident-mini-round1-'+module+'.obj',
                     'actual independent resident/joystick state source producer')
            elif o['unit_id'] in DISPLAY_DATA_SOURCES:
                producer = '.analysis/work/display-mini-round1-context.obj' if o['unit_id'].endswith('vsync-initialized-data') else '.analysis/work/display-round1.obj'
                need(o['source'] == DISPLAY_DATA_SOURCES[o['unit_id']] and o['maintained_native_object'] == producer,
                     'actual maintained palette/VSync/gaiji state producer')
            elif o['unit_id'] in GRAPHICS_DATA_SOURCES:
                need(o['source'] == GRAPHICS_DATA_SOURCES[o['unit_id']] and o['maintained_native_object'] == '.analysis/work/graphics-round1.obj',
                     'actual maintained graphics/heap state or semantic generator producer')
        else:
            need(row["source"] == o["source"], "actual source producer ownership")
        if o["source"] == INPUT_SOURCE:
            need(row["wrapper"] == INPUT_WRAPPER and row["game"] == 3 and row["binary"] == "O"
                 and row["first_binary"] == "op", "input producer retains GAME3/O first-use slot")
        if o["source"] == WAIT_SOURCE:
            need(row["wrapper"] == WAIT_WRAPPER and row["game"] == 3 and row["binary"] == "L"
                 and row["first_binary"] == "mainl", "ending wait retains GAME3/L first-use slot")
        # Staff's native short filename is a literal copy of its maintained TU,
        # rather than an include wrapper. The ending layout independently binds
        # its exact wrapper/source relationship and full native owner fields.
        if o['unit_id'] in TEXT_BANKS_SOURCE_MAP:
            need(sha((root / o['source']).read_bytes()) == text_banks['source_sha256'][o['source']],
                 'maintained UTF-8 source and exact reversible CP932 text transport in both native rounds')
        elif o['unit_id'] in PICTURE_FILES_SOURCE_MAP:
            need(sha((root / o['source']).read_bytes()) == pictures['source_sha256'],
                 'actual natural C TU consumed by both native rounds')
        elif o['unit_id'] in ROOT_STATE_SOURCE_MAP:
            need(sha((root / o['source']).read_bytes()) == root_state['source_sha256'][o['source']],
                 'actual recovered root TU and bounded includes consumed by both native rounds')
        elif o['unit_id'] in EXCEPTION_SOURCE_MAP:
            need(sha((root / o['source']).read_bytes()) == exception_native['source_sha256'][o['source']], 'complete C++ TUs consumed by both fresh native rounds')
        elif o['unit_id'] in STDIO_SOURCE_MAP:
            need(sha((root / o['source']).read_bytes()) == stdio_native['source_sha256'][o['source']], 'complete buffered I/O TUs consumed by both fresh native rounds')
        elif o['unit_id'] in PATH_SOURCE_MAP:
            need(sha((root / o['source']).read_bytes()) == path_native['source_sha256'][o['source']], 'complete path TUs consumed by both fresh native rounds')
        elif o['unit_id'] in DOSCONSTRUCT_SOURCE_MAP:
            need(sha((root / o['source']).read_bytes()) == dosconstruct_native['source_sha256'][o['source']], 'complete constructor TUs consumed by both fresh native rounds')
        elif o['unit_id'] in LOADPROG_UNITS:
            need(sha((root / o['source']).read_bytes()) == loadprog_native['source_sha256'], 'complete loader TU consumed by both fresh native rounds')
        elif o['unit_id'] == EXEC_UNIT:
            need(sha((root / o['source']).read_bytes()) == exec_native['source_sha256'], 'complete overlay TU consumed by both fresh native rounds')
        elif o['unit_id'] == FARHEAP_UNIT:
            need(sha((root / o['source']).read_bytes()) == farheap_native['source_sha256'], 'complete maintained far-heap TU consumed by both fresh native rounds')
        elif o['unit_id'] in CRT_SOURCE_MAP:
            need(bound_files[row['wrapper']] == (root / o['source']).read_bytes(), 'literal maintained CRT TU source transport')
        elif o['unit_id'] in RESIDENT_DATA_SOURCES:
            need(o['source'] == RESIDENT_DATA_SOURCES[o['unit_id']], 'explicit actual resident/joystick DATA source')
        elif o['unit_id'] in DISPLAY_DATA_SOURCES:
            need(o['source'] == DISPLAY_DATA_SOURCES[o['unit_id']], 'explicit consumed palette/VSync/gaiji state source')
        elif o['unit_id'] in GRAPHICS_DATA_SOURCES:
            need(o['source'] == GRAPHICS_DATA_SOURCES[o['unit_id']], 'explicit consumed graphics/heap state source')
        elif o['unit_id'] in (TABLE_UNIT, FILE_DATA_UNIT, BFNT_DATA_UNIT, ARCHIVE_DATA_UNIT):
            # Each selected native scope binds its real wrapper and source,
            # entire native record stream and both target-equal link rounds.
            need(o['source'] == {TABLE_UNIT: TABLE_SOURCE, FILE_DATA_UNIT: FILE_STATE_SOURCE, BFNT_DATA_UNIT: BFNT_SIGNATURE_SOURCE, ARCHIVE_DATA_UNIT: ARCHIVE_STATE_SOURCE}[o['unit_id']], 'explicit selected source transport')
        elif o["source"] in ('src/mainl/root/complete_data.cpp', 'src/mainl/root/continue.cpp'):
            # The bounded native layout verifies the literal composer transform;
            # no generic source-equality bypass is introduced for other owners.
            need(bound_files[row['wrapper']].replace(b"\r\n", b"\n") == root_transport(o['source'], (root / o['source']).read_bytes()),
                 "declared root/continue source transport")
        else:
            transported = {ENDING_SOURCE: ENDING_WRAPPER, REGISTRATION_SOURCE: REGISTRATION_WRAPPER}.get(o["source"], o["source"])
            need(bound_files[transported].replace(b"\r\n", b"\n") == (root / o["source"]).read_bytes().replace(b"\r\n", b"\n"),
                 "maintained source and declared line-ending transport")
        if o['unit_id'] in EXCEPTION_SOURCE_MAP or o['unit_id'] in ROOT_STATE_SOURCE_MAP or o['unit_id'] in PICTURE_FILES_SOURCE_MAP or o['unit_id'] in TEXT_BANKS_SOURCE_MAP:
            # The selected optimizing pair binds its own actual source and all
            # consumed pinned SDK headers, rather than a contextual old TU.
            continue
        for name in describe_omf((bound_work / o["object"]).read_bytes())["dependency_paths"]:
            name = name.replace(chr(92), "/")
            if name.startswith("C:/TC4/INCLUDE/"):
                need(name in report["vendor_header_sha256"], "undeclared consumed vendor header")
            else:
                if o['unit_id'] in CRT_SOURCE_MAP:
                    name = 'owned/' + name  # Native CRT assembly runs in the actual owned/ cwd.
                need(name in bound_files and sha((bound_work / name).read_bytes()) == bound_inventory[name], "complete consumed header/source binding")
    with contextlib.redirect_stdout(io.StringIO()):
        need(tracking.main(root, validate_product=False) == 0, "current ledger consistency")
    return dict(cold_report_sha256=sha(raw_report), recipe_sha256=report["recipe_sha256"],
                vendor_header_sha256=report["vendor_header_sha256"],
                source_inventory_sha256=digest(refresh['current_source_inventory_sha256']), source_files=len(files),
                outputs_per_round=938, project_objects_per_round=36, crt_objects_per_round=6, rounds=2,
                library=library, decoded_sha256=sha(decoded), stored_sha256=sha(stored), scope=scope,
                prior_acceptance=dict(baseline_commit=BASELINE, publication_sha256=sha(previous_raw),
                    complete_prior_scope_sha256=old_scope_digest, unchanged_prior_native_graph=True,
                    prior_verifier_inputs_unchanged_except=sorted(adapted), prior_runtime_observations_reexecuted=False),
                product_exact=False, canonical_unit_credit_changed=False)


def verify(root, publication):
    import validate_tracking as tracking
    root = Path(root)
    need(publication["schema"] == "mainl-current-source-acceptance-v1"
         and publication["state"] == "repository-local-accepted", "accepted publication schema")
    current_inputs = proof_inputs(root)
    recorded_inputs = {name: value for name, value in publication['proof_inputs'].items()
                       if name != 'scripts/status.py'}
    drift = sorted((name for name in set(recorded_inputs) | set(current_inputs)
                    if recorded_inputs.get(name) != current_inputs.get(name)),
                   key=lambda name: (not name.startswith('src/'), name))
    need(not drift, "proof verifier input drift: " + ", ".join(drift))
    proof = audit(root, stage=publication['audit']['scope'].get('current_native_refresh', {}).get('stage'))
    need(publication["audit"] == proof, "current source-bound physical audit drift")
    now = publication["observed_utc"]
    need(now.endswith("Z"), "UTC Z observation time")
    policy = tomllib.loads((root / "config/oracles.toml").read_text())
    rows = oracle_rows(proof, now, policy)
    need(rows == publication["owner_oracles"], "owner gate witness binding")
    for owner in proof["scope"]["owners"]:
        own = rows[owner["unit_id"]]
        passed = tracking.accepted_oracle_passes(list(own), own, {s["id"]: s for s in policy["oracles"]},
            set(policy["policy"]["non_acceptance_evidence_classes"]), artifact="th03-mainl", unit_id=owner["unit_id"],
            extent_start=owner["start"], extent_size=owner["size"],
            global_evidence_oracles=set(policy["policy"]["global_evidence_oracles"]),
            artifact_evidence_oracles=set(policy["policy"]["artifact_evidence_oracles"]))
        need(set(GATES) <= passed, "eleven scoped/classed Oracle gates")
    owners = proof['scope']['owners']
    authored = [o for o in owners if o.get('origin', 'authored') == 'authored']
    libraries = [o for o in owners if o.get('origin') == 'library']
    need(len(authored) + len(libraries) == len(owners), 'every accepted owner has an explicit supported origin')
    return dict(repository_local=True, current_cold_source_scopes=True, reviewed_proof_ready=True,
                native_refresh_stage=proof['scope'].get('current_native_refresh', {}).get('stage'),
                native_objects_rebuilt_per_round=2 if 'current_native_refresh' in proof['scope'] else 0,
                decoded_exact_units=len(owners), decoded_authored_exact_units=len(authored), decoded_library_exact_units=len(libraries),
                decoded_authored_procedures=sum(o.get('procedure_count',1) for o in authored),
                decoded_authored_code_bytes=sum(o.get('code_bytes',o['size']) for o in authored),
                decoded_authored_initialized_data_bytes=sum(o.get('initialized_data_bytes',0) for o in authored),
                decoded_authored_bytes=sum(o['size'] for o in authored), decoded_library_bytes=sum(o['size'] for o in libraries),
                decoded_library_procedures=sum(o.get('procedure_count',1) for o in libraries),
                decoded_source_bytes=sum(o['size'] for o in owners), decoded_procedures=sum(o.get('procedure_count',1) for o in owners),
                decoded_code_bytes=sum(o.get('code_bytes',o['size']) for o in owners),
                decoded_initialized_data_bytes=sum(o.get('initialized_data_bytes',0) for o in owners),
                decoded_uninitialized_file_data_bytes=sum(o.get('uninitialized_file_data_bytes',0) for o in owners),
                decoded_exact_unit_ids=sorted(o["unit_id"] for o in owners),
                target_provenance="candidate-local-attested", product_exact=False, mixed_physical_exact_bytes=0,
                mixed_authored_credit_bytes=0, canonical_file_backed_authored_credit_unchanged=True,
                factory_accepted=False, whole_game_percentage=None, whole_game_code_denominator_known=False)
