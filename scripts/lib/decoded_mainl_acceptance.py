"""Current cold-source proof for decoded MAINL lifecycle, input and sound owners.

This consumes the live 938-output build, not any archived receipt. The remaining
MAINL source scopes and vendor context retain their separate acceptance state.
"""

import contextlib
import csv
import io
import json
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
from lib.decoded_mainl_root_helpers_layout import OBJECT as ROOT_OBJECT, WRAPPER as ROOT_WRAPPER


PUBLICATION = "config/mainl_work/scoped_acceptance.json"
COMMAND = ".venv/bin/python scripts/publish_th03_mainl_work_scopes.py"
PROOF_INPUTS = ("scripts/lib/decoded_mainl_acceptance.py", "scripts/publish_th03_mainl_work_scopes.py",
                "scripts/lib/op_work_acceptance.py", "scripts/status.py", "scripts/validate_tracking.py",
                "config/oracles.toml", "scripts/review_th03_shared_input_work.py",
                "scripts/lib/shared_input_layout.py", "scripts/lib/shared_input_runtime.py",
                "scripts/lib/mainl_wait_layout.py", "scripts/lib/mainl_wait_runtime.py",
                "scripts/review_th03_mainl_sound_work.py", "scripts/lib/decoded_mainl_sound_layout.py", "scripts/lib/decoded_mainl_sound_runtime.py",
                "scripts/lib/shared_sound_runtime.py", "scripts/lib/op_sound_layout.py",
                "scripts/review_th03_mainl_root_helpers_work.py", "scripts/lib/decoded_mainl_root_helpers_layout.py",
                "scripts/lib/decoded_mainl_root_helpers_runtime.py",
                "scripts/review_th03_mainl_pi_free_work.py", "scripts/lib/decoded_mainl_pi_free_layout.py",
                "scripts/lib/decoded_mainl_pi_free_runtime.py")


def need(value, message):
    if not value:
        raise ValueError("current MAINL acceptance: " + message)


def proof_inputs(root):
    return {n: sha((root / n).read_bytes()) for n in PROOF_INPUTS}


def oracle_rows(proof, now, policy):
    return shared_oracle_rows(proof, now, policy, artifact="th03-mainl", publication_path=PUBLICATION,
                              prefix="ev-mainl-current-", command=COMMAND)


def audit(root):
    import build_th03_mainl_work as build
    from build_th03_op_work import compare_mz
    import validate_tracking as tracking
    root = Path(root)
    need(root.resolve() == build.ROOT, "live repository root")
    work = build.WORK
    raw_report = (build.OUT / "mainl-build.json").read_bytes()
    report = json.loads(raw_report)
    need(report["complete"] and report["raw_repeat_equal"] and report["retained_project_objects"] == 0,
         "complete source-only cold pair")
    need(report["recipe_sha256"] == build.recipe_inventory(), "cold recipe drift")
    need(report["vendor_header_sha256"] == build.vendor_header_inventory(), "consumed vendor header drift")
    files, graph, archive_sha = build.sources()
    need(report["source_sha256"] == {n: sha(b) for n, b in sorted(files.items())}
         and report["archive_sha256"] == archive_sha, "current source graph drift")
    need(all((work / n).read_bytes() == b for n, b in files.items()), "staged source drift")
    need([r["round"] for r in report["rounds"]] == [1, 2], "two independent rounds")
    outputs = report["rounds"][0]["outputs"]
    need(len(outputs) == 938 and outputs == report["rounds"][1]["outputs"], "complete raw cold output vector")
    fresh = {r["output"] for r in graph} | {"owned/" + n + ".obj" for n in build.CRT}
    need(len(fresh) == 42, "36 project and six fresh CRT producers")
    for name, row in outputs.items():
        raw = (work / name).read_bytes()
        need(row == dict(bytes=len(raw), sha256=sha(raw)), "current output drift: " + name)
        if name in fresh:
            need(describe_omf(raw)["valid"], "fresh native OMF integrity: " + name)
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
    lifecycle_owners = layout(work, target, candidate)
    base_scope = dict(owners=lifecycle_owners, runtime=runtime(target, candidate), negative_controls=negative_controls(target))
    need(base_scope == report["lifecycle_scopes"], "fresh independent scope replay")
    shared = input_scope(root, "mainl", work, target, candidate, raw_report)
    sound = sound_scope(root, work, target, candidate, raw_report, graph, files)
    root_helpers = root_helper_scope(root, work, target, candidate, raw_report, graph, files)
    pi_free = pi_free_scope(root, work, target, candidate, raw_report, graph, files)
    owners = lifecycle_owners + shared["layout"]["owners"] + shared["ending_wait"]["layout"]["owners"] + sound["layout"]["owners"] + root_helpers["layout"]["owners"] + pi_free["layout"]["owners"]
    with (root / "config/units.csv").open() as stream:
        units = {u["id"]: u for u in csv.DictReader(stream)}
    for o in owners:
        u = units[o["unit_id"]]
        segment = o.get("segment", 0xC7E)
        need(u["artifact"] == "th03-mainl" and u["segment"].lower() == f"decoded:{segment:04x}"
             and int(u["offset"], 0) + segment*16 == o["start"] and int(u["size"], 0) == int(u["compare_size"], 0) == o["size"]
             and u["state"] == "source-present" and u["origin"] == "authored" and u["boundary_state"] == "reviewed"
             and not u["file_offset"] and u["source"] == o["source"], "current decoded ownership ledger")
        row, = [r for r in graph if r["output"] == o["object"]]
        if o["object"] == ROOT_OBJECT:
            need(row["wrapper"] == ROOT_WRAPPER and row["source"] == ROOT_WRAPPER
                 and row["game"] == 3 and row["binary"] == "L" and row["first_binary"] == "mainl"
                 and ('include '+o["source"]).encode() in files[ROOT_WRAPPER], "actual maintained root include producer")
        else:
            need(row["source"] == o["source"], "actual source producer ownership")
        if o["source"] == INPUT_SOURCE:
            need(row["wrapper"] == INPUT_WRAPPER and row["game"] == 3 and row["binary"] == "O"
                 and row["first_binary"] == "op", "input producer retains GAME3/O first-use slot")
        if o["source"] == WAIT_SOURCE:
            need(row["wrapper"] == WAIT_WRAPPER and row["game"] == 3 and row["binary"] == "L"
                 and row["first_binary"] == "mainl", "ending wait retains GAME3/L first-use slot")
        need(files[o["source"]].replace(b"\r\n", b"\n") == (root / o["source"]).read_bytes().replace(b"\r\n", b"\n"),
             "maintained source and declared line-ending transport")
        for name in describe_omf((work / o["object"]).read_bytes())["dependency_paths"]:
            name = name.replace(chr(92), "/")
            if name.startswith("C:/TC4/INCLUDE/"):
                need(name in report["vendor_header_sha256"], "undeclared consumed vendor header")
            else:
                need(name in files and sha((work / name).read_bytes()) == report["source_sha256"][name], "complete consumed header/source binding")
    scope = dict(base_scope, owners=owners, input_modes=shared, sound=sound, root_helpers=root_helpers, pi_free=pi_free)
    with contextlib.redirect_stdout(io.StringIO()):
        need(tracking.main(root, validate_product=False) == 0, "current ledger consistency")
    return dict(cold_report_sha256=sha(raw_report), recipe_sha256=report["recipe_sha256"],
                vendor_header_sha256=report["vendor_header_sha256"],
                source_inventory_sha256=digest(report["source_sha256"]), source_files=len(files),
                outputs_per_round=938, project_objects_per_round=36, crt_objects_per_round=6, rounds=2,
                library=library, decoded_sha256=sha(decoded), stored_sha256=sha(stored), scope=scope,
                product_exact=False, canonical_unit_credit_changed=False)


def verify(root, publication):
    import validate_tracking as tracking
    root = Path(root)
    need(publication["schema"] == "mainl-current-source-acceptance-v1"
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
            set(policy["policy"]["non_acceptance_evidence_classes"]), artifact="th03-mainl", unit_id=owner["unit_id"],
            extent_start=owner["start"], extent_size=owner["size"],
            global_evidence_oracles=set(policy["policy"]["global_evidence_oracles"]),
            artifact_evidence_oracles=set(policy["policy"]["artifact_evidence_oracles"]))
        need(set(GATES) <= passed, "eleven scoped/classed Oracle gates")
    return dict(repository_local=True, current_cold_source_scopes=True, reviewed_proof_ready=True,
                decoded_exact_units=27, decoded_authored_exact_units=27, decoded_library_exact_units=0,
                decoded_authored_bytes=1261, decoded_library_bytes=0, decoded_exact_unit_ids=sorted(o["unit_id"] for o in proof["scope"]["owners"]),
                target_provenance="candidate-local-attested", product_exact=False, mixed_physical_exact_bytes=0,
                mixed_authored_credit_bytes=0, canonical_file_backed_authored_credit_unchanged=True,
                factory_accepted=False, whole_game_percentage=None, whole_game_code_denominator_known=False)
