"""Source-bound -2/-3/-5 and bounded -4 ownership with cold runtime witnesses.

Publication reruns physical audits and bounded ABI smokes. Full models run in
the cold builder; status binds the exact report, images and recipes rather than
replaying the animation and exhaustive scalar domains on every view.
"""

import contextlib
import csv
import io
import json
from pathlib import Path
import re
import tomllib

from lib.omf import describe_omf
from lib.targets import find_artifact, read_verified_artifact
from lib.toolchain import attest_surface
from lib.zun import parse_launcher
from lib.zun_logo_layout import verify as layout, OBJECT
from lib.zun_logo_runtime import Machine, ENTRIES, BSS_SIZE, put
from lib.zun_resident_layout import verify as resident_layout, OBJECT as RESIDENT_OBJECT
from lib.zun_resident_runtime import Machine as ResidentMachine
from lib.zun_init_layout import verify as init_layout
from lib.zun_init_runtime import Machine as InitMachine
from lib.zun_driver_scalar_layout import verify as driver_layout
from lib.zun_driver_scalar_runtime import Machine as DriverMachine, ENTRIES as DRIVER_ENTRIES
from lib.zun_driver_command_layout import verify as command_layout
from lib.zun_driver_command_runtime import Machine as CommandMachine, ENTRIES as COMMAND_ENTRIES
from review_th03_zun_format_work import current_scope as formatter_scope
from review_th03_zun_graphics_work import current_scope as graphics_scope
from lib.op_work_acceptance import GATES, sha, digest, oracle_rows as shared_oracle_rows


PUBLICATION = "config/zun_work/scoped_acceptance.json"
COMMAND = ".venv/bin/python scripts/publish_th03_zun_work_scopes.py"
PROOF_INPUTS = ("scripts/lib/decoded_zun_acceptance.py", "scripts/publish_th03_zun_work_scopes.py",
                "scripts/lib/op_work_acceptance.py", "scripts/status.py", "scripts/validate_tracking.py",
                "config/oracles.toml", "scripts/review_th03_zun_format_work.py",
                "scripts/lib/zun_driver_format_layout.py", "scripts/lib/zun_driver_format_runtime.py",
                "scripts/review_th03_zun_graphics_work.py", "scripts/lib/zun_driver_graphics_layout.py", "scripts/lib/zun_driver_graphics_runtime.py")


def need(value, message):
    if not value:
        raise ValueError("current ZUN acceptance: " + message)


def proof_inputs(root):
    return {name: sha((root / name).read_bytes()) for name in PROOF_INPUTS}


def oracle_rows(proof, now, policy):
    return shared_oracle_rows(proof, now, policy, artifact="th03-zun", publication_path=PUBLICATION,
                              prefix="ev-zun-current-", command=COMMAND)


def runtime_witness(scope):
    runtime = scope["runtime"]
    need((runtime["cases_per_image"], runtime["images"], runtime["functions"], runtime["executed_owner_bytes"],
          runtime["full_fade_frames"], runtime["data_bytes"], runtime["bss_bytes"],
          runtime["vector_argument_bytes"], runtime["vector_callee_pop_bytes"], runtime["opaque_amplitude_high_bytes"])
         == (5111, 2, 10, 1299, 231, 15, 293, 8, 8, 256), "complete cold runtime dimensions")
    observations = runtime["observations"]
    need([(o["load_segment"], o["cases_per_image"], o["covered_owner_bytes"], o["maximum_observed_stack_depth"])
          for o in observations] == [(0x1000, 2556, 1299, 36), (0x3000, 2555, 1279, 36)]
         and all(re.fullmatch(r"[0-9a-f]{64}", o["trace_sha256"]) for o in observations), "cold load/coverage/stack witnesses")
    controls = scope["negative_controls"]
    need(controls["count"] == len(set(controls["rejected"])) == 18, "all eighteen actual guest mutation controls")


def resident_witness(scope):
    runtime = scope["runtime"]
    need((runtime["cases_per_image"], runtime["images"], runtime["functions"], runtime["executed_owner_bytes"],
          runtime["data_bytes"], runtime["bss_bytes"]) == (3548, 2, 2, 322, 307, 0), "complete resident runtime dimensions")
    need([(o["load_segment"], o["cases"], o["covered_owner_bytes"], o["maximum_observed_stack_depth"])
          for o in runtime["observations"]] == [(0x1000, 1774, 322, 48), (0x3000, 1774, 322, 48)]
         and all(re.fullmatch(r"[0-9a-f]{64}", o["trace_sha256"]) for o in runtime["observations"]),
         "complete resident load/coverage/stack witnesses")
    controls = scope["negative_controls"]
    need(controls["count"] == len(set(controls["rejected"])) == 16, "all sixteen actual resident mutation controls")


def resident_smoke(target, candidate):
    observations = []
    for image in (target, candidate):
        machine = ResidentMachine(image, 0x3000)
        try:
            observations.append([
                machine.run("main", argument=b"-dignored", opened=0x8000, created=0xFFFF),
                machine.run("main", argument=b"/R", existing=0x900),
                machine.run("main", argc=0xFFFF, allocated=0),
                machine.run("cfg_init", opened=0, segment=0xFFFF, debug=0xA7),
                machine.run("cfg_init", opened=0x7FFF, segment=0, flags=2)])
        finally:
            machine.close()
    need(observations[0] == observations[1], "current independent resident smoke")
    return dict(cases_per_image=5, images=2, trace_sha256=digest(observations[0]),
                full_runtime_reexecuted_now=False, full_runtime_witness_bound=True)


def init_witness(scope):
    runtime = scope["runtime"]
    need((runtime["images"], runtime["functions"], runtime["code_bytes"], runtime["data_bytes"],
          runtime["executed_owner_bytes"], runtime["cases_per_image"], runtime["empty_string_attribute_word_writes"])
         == (2, 9, 607, 783, 607, 70116, 65536), "complete original-ASM init runtime dimensions")
    observations = runtime["observations"]
    need([(o["load_segment"], o["scenario_cases"], o["conversions"]["cases"], o["covered_owner_bytes"],
           o["maximum_observed_stack_depth"]) for o in observations]
         == [(0x1000, 1522, 65536, 607, 22), (0x3000, 1522, 1536, 607, 22)]
         and all(re.fullmatch(r"[0-9a-f]{64}", o[k] if k == "trace_sha256" else o["conversions"]["trace_sha256"])
                 for o in observations for k in ("trace_sha256", "conversions")), "init load/scalar/coverage/stack witnesses")
    controls = scope["negative_controls"]
    need(controls["count"] == len(set(controls["rejected"])) == 13, "all thirteen actual init mutation controls")
    need(scope["layout"]["source_lineage"]["origin"] == "original-asm"
         and scope["layout"]["source_lineage"]["newly_authored_bytes"] == 0, "original-ASM source classification")


def init_smoke(target, candidate):
    observations = []
    for image in (target, candidate):
        machine = InitMachine(image, 0x3000)
        try:
            observations.append([
                machine.run("start"), machine.run("start", tail=b"/R", resident=1, failures=(0x5000, 0x6000)),
                machine.run("detect", resident=3, vector_offset=0x880),
                machine.run("error", error=0x8005, flags=0x646), machine.run("stop", latch=0xFF),
                machine.run("copy", flags=0x646), machine.run("show", latch=2),
                machine.run("draw", text=b"\x81\x7F\x81\x9F", offset=1, flags=0x646)])
        finally: machine.close()
    need(observations[0] == observations[1], "current independent original-ASM ABI smoke")
    return dict(cases_per_image=8, images=2, trace_sha256=digest(observations[0]),
                full_runtime_reexecuted_now=False, full_runtime_witness_bound=True)


def driver_witness(scope):
    runtime = scope["runtime"]
    need((runtime["images"], runtime["functions"], runtime["code_bytes"], runtime["private_data_bytes"],
          runtime["private_bss_bytes"], runtime["cases_per_image"], runtime["executed_owner_bytes"], runtime["exhaustive_byte_domains"])
         == (2, 16, 428, 0, 0, 8428, 428, 256), "complete driver scalar runtime dimensions")
    need([(o["load_segment"], o["cases"], o["covered_owner_bytes"], o["maximum_observed_stack_depth"])
          for o in runtime["observations"]] == [(0x1000, 4214, 428, 26), (0x3000, 4214, 428, 26)]
         and all(re.fullmatch(r"[0-9a-f]{64}", o["trace_sha256"]) for o in runtime["observations"]),
         "driver scalar load/coverage/stack witnesses")
    controls = scope["negative_controls"]
    need(controls["count"] == len(set(controls["rejected"])) == 14, "all fourteen driver scalar mutations")
    layout = scope["layout"]
    need(not layout["enclosing_driver_accepted"] and not layout["reserved_spans_owned"]
         and all(o["origin"] == "library" for o in layout["owners"]), "bounded library source classification")


def command_witness(scope):
    runtime = scope["runtime"]
    need((runtime["images"], runtime["functions"], runtime["code_bytes"], runtime["private_data_bytes"],
          runtime["private_bss_bytes"], runtime["cases_per_image"], runtime["executed_owner_bytes"], runtime["exhaustive_byte_domains"])
         == (2, 9, 361, 0, 0, 6678, 361, 256), "complete command runtime dimensions")
    need([(o["load_segment"], o["cases"], o["covered_owner_bytes"], o["maximum_observed_stack_depth"])
          for o in runtime["observations"]] == [(0x1000, 3339, 361, 32), (0x3000, 3339, 361, 32)]
         and all(re.fullmatch(r"[0-9a-f]{64}", o["trace_sha256"]) for o in runtime["observations"]),
         "command load/coverage/stack witnesses")
    controls = scope["negative_controls"]
    need(controls["count"] == len(set(controls["rejected"])) == 19, "all nineteen command guest mutations")
    physical = scope["layout"]
    need(not physical["enclosing_driver_accepted"] and not physical["reserved_spans_owned"]
         and all(o["origin"] == "library" for o in physical["owners"]), "bounded command library classification")


def command_smoke(target, candidate):
    observations = []
    for image in (target, candidate):
        machine = CommandMachine(image, 0x3000)
        try:
            rows = [machine.run(kind) for kind in COMMAND_ENTRIES]
            rows += [machine.run("tokenize_command", text=b'one "open', split_stack=True),
                     machine.run("optional_number_legacy", text=b"ffh", remaining=0),
                     machine.run("dispatch_options", arguments=(b"-r", b"/Z"), flags=0xED7),
                     machine.run("require_number", arguments=(b"garbage",), split_stack=True)]
            observations.append(rows)
        finally: machine.close()
    need(observations[0] == observations[1], "current command ABI/state smoke")
    return dict(cases_per_image=13, images=2, trace_sha256=digest(observations[0]),
                full_runtime_reexecuted_now=False, full_runtime_witness_bound=True)


def driver_smoke(target, candidate):
    observations = []
    for image in (target, candidate):
        machine = DriverMachine(image, 0x3000)
        try:
            observations.append([machine.run(kind, text=b"ffh", other=b"FFH", value=122, before=72, split_stack=True)
                                 for kind in DRIVER_ENTRIES])
        finally: machine.close()
    need(observations[0] == observations[1], "current independent library driver scalar smoke")
    return dict(cases_per_image=16, images=2, trace_sha256=digest(observations[0]),
                full_runtime_reexecuted_now=False, full_runtime_witness_bound=True)


def smoke(target, candidate):
    observations = []
    for image in (target, candidate):
        machine = Machine(image, 0x3000)
        try:
            rows = []
            for kind in ENTRIES:
                state = bytearray(BSS_SIZE)
                put(state, 224, 90)
                state[3:8] = bytes((127, 23, 250, 128, 0xA5))
                rows.append(machine.run(kind, state, key_frame=0, hardware=True,
                                         length=-37, angle=160, flags=0x602, asset_error=0xFFF3))
            observations.append(rows)
        finally:
            machine.close()
    need(observations[0] == observations[1], "current independent ABI/state smoke")
    return dict(cases_per_image=10, images=2, trace_sha256=digest(observations[0]),
                full_runtime_reexecuted_now=False, full_runtime_witness_bound=True)


def audit(root):
    import build_th03_zun_work as build
    import validate_tracking as tracking
    root = Path(root)
    need(root.resolve() == build.ROOT, "live repository root")
    work = build.WORK
    raw_report = (build.OUT / "zun-build.json").read_bytes()
    report = json.loads(raw_report)
    need(report["complete"] and report["raw_repeat_equal"] and report["retained_project_objects"] == 0,
         "complete source-only cold pair")
    need(report["recipe_sha256"] == build.recipe_inventory(), "cold recipe drift")
    need(report["consumed_runtime_sha256"] == build.runtime_inventory(), "consumed tiny runtime drift")
    need(report["consumed_sdk_sha256"] == build.sdk_inventory(), "consumed resident SDK drift")
    files, maintained, context = build.compose(root)
    need(report["source_sha256"] == {name: sha(b) for name, b in sorted(files.items())}
         and report["source_context"] == context, "current source/vendor graph drift")
    need(all((work / n).read_bytes() == b for n, b in files.items()), "staged source/vendor drift")
    need(report["maintained_inputs"] == {n: sha(b) for n, b in sorted(maintained.items())}
         and all((root / n).read_bytes() == b for n, b in maintained.items()), "current maintained source binding")
    need([r["round"] for r in report["rounds"]] == [1, 2], "two independent source rounds")
    outputs = report["rounds"][0]["outputs"]
    expected = {f"{base}.{ext}" for base in ("init/init", "obj/th01/zunsoft", "obj/th03/res_yume",
        "driver/driver", "wrapper/stub", "wrapper/call", "wrapper/helper")
        for ext in (("obj", "map", "com") if base not in ("obj/th01/zunsoft", "obj/th03/res_yume") else ("obj", "map"))}
    expected |= {"bin/th01/zunsoft.com", "bin/th03/res_yume.com", "product/zun.com", "product/zun.packed.com"}
    need(len(outputs) == 23 and set(outputs) == expected and outputs == report["rounds"][1]["outputs"],
         "complete raw cold output vector")
    for name, row in outputs.items():
        raw = (work / name).read_bytes()
        need(row == dict(bytes=len(raw), sha256=sha(raw)), "current cold output drift: " + name)
        if name.endswith(".obj"):
            need(describe_omf(raw)["valid"], "fresh native OMF integrity")
    config = tomllib.loads((root / "config/toolchain.toml").read_text())
    surfaces = [attest_surface(root, s) for s in config["surfaces"] if not s.get("bootstrap_only")]
    need(report["toolchain_surfaces"] == surfaces and all(s["pass"] or not s["required"] for s in surfaces),
         "current toolchain identity")
    need(report["emitter"] == build.emitter.attest(), "current compatible driver emitter identity")
    labels = []
    for rnd in (1, 2):
        labels += [f"round{rnd}:" + phase for phase in ("init-assemble", "init-link", "zunsoft-compile", "zunsoft-link",
            "res_yume-compile", "res_yume-link", "driver-assemble", "driver-link", "wrapper-stub", "wrapper-stub-link",
            "wrapper-call", "wrapper-call-link", "wrapper-helper", "wrapper-helper-link", "pack", "roundtrip")]
    labels += ["restore-target"]
    labels += ["control:" + name + "-" + phase for name in ("word", "no-even") for phase in ("assemble", "link")]
    need([p["label"] for p in report["native_phases"]] == labels and
         all(p["returncode"] == (1 if p["label"] == "restore-target" or p["label"].endswith((":pack", ":roundtrip")) else 0)
             for p in report["native_phases"]), "complete serial native execution schedule")
    targets = tomllib.loads((root / "config/targets.toml").read_text())
    stored = read_verified_artifact(root, find_artifact(targets, "th03-zun"))
    declaration, = [a for a in tomllib.loads((root / "config/th03_diet.toml").read_text())["artifacts"] if a["id"] == "th03-zun"]
    decoded = (work / "product/zun.target.com").read_bytes()
    need(len(decoded) == declaration["decoded_size"] and sha(decoded) == declaration["decoded_sha256"], "pinned decoded target identity")
    candidate = (work / "product/zun.com").read_bytes()
    need(decoded == candidate and (work / "product/zun.packed.com").read_bytes() == stored, "complete decoded/stored equality")
    need(report["same_tool_roundtrip"] and report["comparison"]["decoded_equal"] and report["comparison"]["stored_equal"],
         "complete comparison/roundtrip proof")
    directory = parse_launcher(decoded, 223)
    need(all(r["directory"] == directory for r in report["rounds"]), "complete decoded COM directory/format")
    paths = ("libs/kaja/ongchk.com", "init/init.com", "bin/th01/zunsoft.com", "driver/driver.com", "bin/th03/res_yume.com")
    for row, path in zip(directory["payloads"], paths):
        at, size = row["decoded_file_offset"], row["size"]
        need(decoded[at:at + size] == (work / path).read_bytes(), "complete target payload equality")
    child = directory["payloads"][2]
    at, size = child["decoded_file_offset"], child["size"]
    target_logo = decoded[at:at + size]
    candidate_logo = (work / "bin/th01/zunsoft.com").read_bytes()
    scope = report["logo_scopes"]
    need(scope["layout"] == layout(work, target_logo, candidate_logo, at), "independent physical owner audit")
    runtime_witness(scope)
    child = directory["payloads"][4]
    at, size = child["decoded_file_offset"], child["size"]
    target_resident = decoded[at:at + size]
    candidate_resident = (work / "bin/th03/res_yume.com").read_bytes()
    resident = report["resident_scopes"]
    need(resident["layout"] == resident_layout(work, target_resident, candidate_resident, at),
         "independent physical resident audit")
    resident_witness(resident)
    child = directory["payloads"][1]
    at, size = child["decoded_file_offset"], child["size"]
    target_init = decoded[at:at + size]
    candidate_init = (work / "init/init.com").read_bytes()
    init = report["init_scopes"]
    need(init["layout"] == init_layout(work, target_init, candidate_init, at), "complete native original-ASM ownership")
    init_witness(init)
    child = directory["payloads"][3]
    at, size = child["decoded_file_offset"], child["size"]
    target_driver = decoded[at:at + size]
    candidate_driver = (work / "driver/driver.com").read_bytes()
    driver = report["driver_scalar_scopes"]
    need(driver["layout"] == driver_layout(work, target_driver, candidate_driver, at, files, maintained),
         "complete driver scalar native ownership")
    driver_witness(driver)
    command = report["driver_command_scopes"]
    need(command["layout"] == command_layout(work, target_driver, candidate_driver, at, files, maintained),
         "complete native command ownership")
    command_witness(command)
    formatter = formatter_scope(root, work, target_driver, candidate_driver, at, files, maintained, raw_report)
    graphics = graphics_scope(root, work, target_driver, candidate_driver, at, files, maintained, raw_report)
    controls = report["driver_alignment_controls"]
    need(controls["count"] == 2 and controls["source_only"] and not controls["object_patches"]
         and [c["name"] for c in controls["controls"]] == ["word", "no-even"]
         and all(c["byte_exact_rejected"] and c["all_procedure_includes_unchanged"] and c["changed_inputs"] == ["driver.asm"]
                 and c["target_bytes"] == 4224 and c["differing_bytes"] > 0 for c in controls["controls"]), "two actual native alignment controls")
    owners = scope["layout"]["owners"] + resident["layout"]["owners"] + init["layout"]["owners"] + driver["layout"]["owners"] + command["layout"]["owners"] + formatter["layout"]["owners"] + graphics["layout"]["owners"]
    with (root / "config/units.csv").open() as stream:
        units = {u["id"]: u for u in csv.DictReader(stream)}
    for o in owners:
        u = units[o["unit_id"]]
        need(u["artifact"] == "th03-zun" and u["segment"] == "decoded:" + o["payload_option"] and int(u["offset"], 0) == o["start"]
             and int(u["size"], 0) == int(u["compare_size"], 0) == o["size"] and not u["file_offset"]
             and u["state"] == "source-present" and u["origin"] == o.get("origin", "authored") and u["boundary_state"] == "reviewed"
             and u["source"] == o["source"], "current decoded payload ownership ledger")
    for obj in (OBJECT, RESIDENT_OBJECT):
        for name in describe_omf((work / obj).read_bytes())["dependency_paths"]:
            name = re.sub(r"/+", "/", name.replace(chr(92), "/"))
            if name.upper().startswith("C:/TC4/INCLUDE/"):
                need(name.removeprefix("C:/TC4/INCLUDE/") in report["consumed_sdk_sha256"], "complete consumed SDK declaration")
            else:
                need(name in files and sha((work / name).read_bytes()) == report["source_sha256"][name], "complete consumed source/header binding")
    current_smoke = smoke(target_logo, candidate_logo)
    with contextlib.redirect_stdout(io.StringIO()):
        need(tracking.main(root, validate_product=False) == 0, "current ledger consistency")
    return dict(cold_report_sha256=sha(raw_report), recipe_sha256=report["recipe_sha256"],
                consumed_runtime_sha256=report["consumed_runtime_sha256"], source_inventory_sha256=digest(report["source_sha256"]),
                consumed_sdk_sha256=report["consumed_sdk_sha256"],
                input_files=len(files), vendor_inputs=2, outputs_per_round=23, project_objects_per_round=7, rounds=2,
                decoded_sha256=sha(decoded), stored_sha256=sha(stored), payload_sha256=sha(target_logo),
                resident_payload_sha256=sha(target_resident),
                init_payload_sha256=sha(target_init),
                driver_payload_sha256=sha(target_driver),
                driver_alignment_controls=controls,
                scope=dict(owners=owners, layout=scope["layout"], runtime=scope["runtime"],
                           negative_controls=scope["negative_controls"], resident=resident, init=init, driver=driver, command=command, formatter=formatter, graphics=graphics), current_smoke=current_smoke,
                resident_smoke=resident_smoke(target_resident, candidate_resident),
                init_smoke=init_smoke(target_init, candidate_init),
                driver_smoke=driver_smoke(target_driver, candidate_driver),
                command_smoke=command_smoke(target_driver, candidate_driver),
                product_exact=False, canonical_unit_credit_changed=False)


def verify(root, publication):
    import validate_tracking as tracking
    root = Path(root)
    need(publication["schema"] == "zun-current-source-acceptance-v1"
         and publication["state"] == "repository-local-accepted", "accepted publication schema")
    need(publication["proof_inputs"] == proof_inputs(root), "proof verifier input drift")
    proof = audit(root)
    need(publication["audit"] == proof, "current source-bound physical audit drift")
    now = publication["observed_utc"]
    need(now.endswith("Z"), "UTC Z observation time")
    policy = tomllib.loads((root / "config/oracles.toml").read_text())
    rows = oracle_rows(proof, now, policy)
    need(rows == publication["owner_oracles"], "owner gate witness binding")
    for owner in proof["scope"]["owners"]:
        own = rows[owner["unit_id"]]
        passed = tracking.accepted_oracle_passes(list(own), own, {s["id"]: s for s in policy["oracles"]},
            set(policy["policy"]["non_acceptance_evidence_classes"]), artifact="th03-zun", unit_id=owner["unit_id"],
            extent_start=owner["start"], extent_size=owner["size"],
            global_evidence_oracles=set(policy["policy"]["global_evidence_oracles"]),
            artifact_evidence_oracles=set(policy["policy"]["artifact_evidence_oracles"]))
        need(set(GATES) <= passed, "eleven scoped/classed Oracle gates")
    return dict(repository_local=True, decoded_accepted=True, current_cold_source_scopes=True,
                reviewed_proof_ready=True, decoded_exact_units=60, decoded_authored_bytes=1621, decoded_library_bytes=2280,
                decoded_original_asm_bytes=1390, decoded_original_asm_code_bytes=607, decoded_original_asm_data_bytes=783,
                decoded_source_bytes=5291, decoded_code_bytes=4508, decoded_procedures=68, reviewed_producer_data_bytes=1105,
                decoded_exact_unit_ids=sorted(o["unit_id"] for o in proof["scope"]["owners"]),
                payload_options=["-2", "-3", "-4", "-5"], product_exact=False, mixed_physical_exact_bytes=0,
                canonical_credit_changed=False, factory_accepted=False, whole_game_percentage=None,
                full_runtime_witness_bound=True, current_smoke_cases=150)
