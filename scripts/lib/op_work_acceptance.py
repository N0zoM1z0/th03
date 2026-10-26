"""Current cold-build acceptance of decoded OP lifecycle and shared input owners.

No canonical packed-file offsets or whole-product source ownership are inferred.
Historical 33-owner publications keep their independent verifier and namespace.
"""

import contextlib
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import tomllib

from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, read_verified_artifact
from lib.toolchain import attest_surface
from lib.op_exit_layout import OWNERS, verify as layout
from lib.op_exit_runtime import verify as runtime, negative_controls
from review_th03_shared_input_work import current_scope as input_scope
from review_th03_op_cfg_work import current_scope as cfg_scope
from review_th03_op_dispatch_work import current_scope as dispatch_scope
from review_th03_op_attract_work import current_scope as attract_scope
from review_th03_op_sound_work import current_scope as sound_scope
from review_th03_op_helpers_work import current_scope as helpers_scope
from review_th03_op_render_work import current_scope as render_scope
from review_th03_op_vs_work import current_scope as vs_scope
from review_th03_op_story_work import current_scope as story_scope
from review_th03_op_option_work import current_scope as option_scope
from review_th03_op_main_menu_work import current_scope as main_menu_scope
from review_th03_op_startup_work import current_scope as startup_scope
from review_th03_op_entry_data_work import current_scope as entry_data_scope
from lib.op_helpers_layout import FORWARDING as HELPER_FORWARDING
from lib.op_cfg_layout import OBJECT as CFG_OBJECT, SOURCE as CFG_SOURCE, WRAPPER as CFG_WRAPPER, PUBLICS as CFG_PUBLICS


PUBLICATION = "config/op_work/scoped_acceptance.json"
GATES = ("target-identity", "format-integrity", "boundary-ownership", "toolchain-identity",
         "toolchain-replay", "object-format-integrity", "cold-build-determinism",
         "layout-relocations", "raw-bytes", "ledger-consistency", "cold-aggregate-replay")
PROOF_INPUTS = ("scripts/lib/op_work_acceptance.py", "scripts/publish_th03_op_work_scopes.py",
                "scripts/lib/op_decoded_progress.py", "scripts/validate_tracking.py", "config/oracles.toml",
                "scripts/review_th03_shared_input_work.py", "scripts/lib/shared_input_layout.py",
                "scripts/lib/shared_input_runtime.py", "scripts/review_th03_op_cfg_work.py",
                "scripts/lib/op_cfg_layout.py", "scripts/lib/op_cfg_runtime.py",
                "scripts/review_th03_op_dispatch_work.py", "scripts/lib/op_dispatch_layout.py", "scripts/lib/op_dispatch_runtime.py",
                "scripts/review_th03_op_attract_work.py", "scripts/lib/op_attract_layout.py", "scripts/lib/op_attract_runtime.py",
                "scripts/review_th03_op_sound_work.py", "scripts/lib/op_sound_layout.py", "scripts/lib/op_sound_runtime.py",
                "scripts/lib/shared_sound_runtime.py", "scripts/lib/decoded_mainl_sound_layout.py", "scripts/lib/decoded_mainl_sound_runtime.py",
                "scripts/review_th03_op_helpers_work.py", "scripts/lib/op_helpers_layout.py",
                "scripts/lib/op_helpers_sound_runtime.py", "scripts/lib/op_init_runtime.py",
                "scripts/review_th03_op_render_work.py", "scripts/lib/op_render_layout.py", "scripts/lib/op_render_runtime.py",
                "scripts/review_th03_op_vs_work.py", "scripts/lib/op_vs_layout.py", "scripts/lib/op_vs_runtime.py",
                "scripts/review_th03_op_story_work.py", "scripts/lib/op_story_layout.py", "scripts/lib/op_story_runtime.py",
                "scripts/review_th03_op_option_work.py", "scripts/lib/op_option_layout.py", "scripts/lib/op_option_runtime.py",
                "scripts/review_th03_op_main_menu_work.py", "scripts/lib/op_main_menu_layout.py", "scripts/lib/op_main_menu_runtime.py", "scripts/lib/op_nested_context.py",
                "scripts/review_th03_op_startup_work.py", "scripts/lib/op_startup_layout.py",
                "scripts/lib/op_startup_state.py", "scripts/lib/op_startup_primitives.py",
                "scripts/lib/op_startup_children.py", "scripts/lib/op_startup_runtime.py",
                "scripts/lib/op_startup_cold.py", "scripts/review_th03_op_entry_data_work.py",
                "scripts/lib/op_entry_data_layout.py", "scripts/lib/op_entry_data_runtime.py")


def need(value, message):
    if not value:
        raise ValueError("current OP acceptance: " + message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(value):
    return sha(json.dumps(value, sort_keys=True).encode())


def proof_inputs(root):
    return {n: sha((root / n).read_bytes()) for n in PROOF_INPUTS}


def audit(root):
    import build_th03_op_work as build
    import validate_tracking as tracking
    root = Path(root)
    need(root.resolve() == build.ROOT, "live repository root")
    work = build.WORK
    report_raw = (build.OUT / "op-build.json").read_bytes()
    report = json.loads(report_raw)
    need(report["complete"] and report["raw_repeat_equal"] and report["retained_project_objects"] == 0,
         "complete source-only cold build")
    need(report["recipe_sha256"] == build.recipe_inventory(), "cold recipe drift")
    files = build.source_graph()
    need(report["source_sha256"] == {n: sha(b) for n, b in sorted(files.items())}, "cold source graph drift")
    need(all((work / n).read_bytes() == b for n, b in files.items()), "staged source drift")
    producers = build.producers(files)
    need(len(report["rounds"]) == 2 and [r["round"] for r in report["rounds"]] == [1, 2], "two cold rounds")
    outputs = report["rounds"][0]["outputs"]
    need(outputs == report["rounds"][1]["outputs"] and len(outputs) == 32, "complete raw cold output vector")
    need(set(outputs) == {p["output"] for p in producers} | {"bin/th03/op.exe", "obj/th03/op.map"},
         "all thirty native objects and EXE/MAP required")
    for n, row in outputs.items():
        raw = (work / n).read_bytes()
        need(row == dict(bytes=len(raw), sha256=sha(raw)), "current cold output drift: " + n)
        if n.endswith(".obj"):
            need(describe_omf(raw)["valid"], "fresh OMF integrity: " + n)
    phases = report["native_phases"]
    expected = [f"round{r}:" + name for r in (1, 2) for name in
                [p["output"] for p in producers] + ["link"]] + ["diet:selfcheck", "diet:restore-target"]
    need([p["label"] for p in phases] == expected and
         all(p["returncode"] == (1 if p["label"] == "diet:restore-target" else 0) for p in phases),
         "complete serial native execution schedule")
    config = tomllib.loads((root / "config/toolchain.toml").read_text())
    surfaces = [attest_surface(root, s) for s in config["surfaces"] if not s.get("bootstrap_only")]
    need(report["toolchain_surfaces"] == surfaces and all(s["pass"] or not s["required"] for s in surfaces),
         "current toolchain identity")
    targets = tomllib.loads((root / "config/targets.toml").read_text())
    stored = read_verified_artifact(root, find_artifact(targets, "th03-op"))
    diet = tomllib.loads((root / "config/th03_diet.toml").read_text())
    declaration, = [a for a in diet["artifacts"] if a["id"] == "th03-op"]
    decoded = (work / "bin/th03/op.target.exe").read_bytes()
    need(len(decoded) == declaration["decoded_size"] and sha(decoded) == declaration["decoded_sha256"],
         "pinned DIET-restored target identity")
    candidate_raw = (work / "bin/th03/op.exe").read_bytes()
    target, candidate = parse_mz(decoded), parse_mz(candidate_raw)
    need(target.valid and candidate.valid and decoded == candidate_raw, "complete decoded file/format equality")
    need(build.compare_mz(candidate_raw, decoded) == report["comparison"], "independent MZ comparison")
    need((work / "bin/th03/op.packed.exe").read_bytes() == stored, "canonical stored equality")
    packing = report["packing"]
    need(packing["options"] == ["-B"] and packing["stored_equal"] and packing["raw_repeat_equal"]
         and packing["same_tool_roundtrip"] and len(packing["rounds"]) == 2, "two verified pack/restore rounds")
    for p in packing["rounds"]:
        need(p["packed_sha256"] == sha(stored) and p["packed_bytes"] == len(stored)
             and p["stored_equal"] and p["decoded_roundtrip_equal"], "stored/decoded roundtrip proof")
    lifecycle_owners = layout(work, target, candidate)
    base_scope = dict(owners=lifecycle_owners, runtime=runtime(target, candidate), negative_controls=negative_controls(target))
    need(base_scope == report["exit_scopes"], "fresh independent scope replay")
    shared = input_scope(root, "op", work, target, candidate, report_raw)
    configuration = cfg_scope(root, work, target, candidate, report_raw)
    dispatch = dispatch_scope(root, work, target, candidate, report_raw)
    attract = attract_scope(root, work, target, candidate, report_raw)
    sound = sound_scope(root, work, target, candidate, report_raw)
    helpers = helpers_scope(root, work, target, candidate, report_raw)
    renderers = render_scope(root, work, target, candidate, report_raw)
    vs = vs_scope(root, work, target, candidate, report_raw)
    story = story_scope(root, work, target, candidate, report_raw)
    option = option_scope(root, work, target, candidate, report_raw)
    main_menu = main_menu_scope(root, work, target, candidate, report_raw)
    startup = startup_scope(root, work, target, candidate, report_raw)
    entry_data = entry_data_scope(root, work, target, candidate, report_raw)
    owners = lifecycle_owners + shared["layout"]["owners"] + configuration["layout"]["owners"] + dispatch["layout"]["owners"] + attract["layout"]["owners"] + sound["layout"]["owners"] + helpers["layout"]["owners"] + renderers["layout"]["owners"] + vs["layout"]["owners"] + story["layout"]["owners"] + option["layout"]["owners"] + main_menu["layout"]["owners"] + startup["layout"]["owners"] + entry_data["layout"]["owners"]
    entry_owners = sorted((o for o in owners if o["object"] == CFG_OBJECT and o.get("procedure_count", 1)), key=lambda o: o["start"])
    entry_boundaries = [offset for offset, _ in CFG_PUBLICS] + [3094]
    need([(o["start"] - (0x990 * 16 + 8), o["size"]) for o in entry_owners]
         == [(offset, end - offset) for offset, end in zip(entry_boundaries, entry_boundaries[1:])],
         "all fifteen native entry procedures cover the complete3094-byte CODE producer without overlaps")
    map_text = (work / "obj/th03/op.map").read_text()
    for suffix, offset in (("B", 0x19FA), ("R", 0x19FE), ("G", 0x1A02), ("E", 0x1A06)):
        need(len(re.findall(rf"(?m)^\s*0D7F:{offset:04X}\s+_VRAM_PLANE_{suffix}\s*$", map_text)) == 2,
             "external plane storage address in both MAP public tables")
    with (root / "config/units.csv").open() as stream:
        units = {u["id"]: u for u in csv.DictReader(stream)}
    for o in owners:
        u = units[o["unit_id"]]
        segment = o.get("segment", 0xBEB)
        need(u["artifact"] == "th03-op" and u["segment"].lower() == f"decoded:{segment:04x}"
             and int(u["offset"], 0) + segment * 16 == o["start"] and int(u["size"], 0) == int(u["compare_size"], 0) == o["size"]
             and u["state"] == "source-present" and u["origin"] == "authored" and u["boundary_state"] == "reviewed"
             and not u["file_offset"] and u["source"] == o["source"], "current decoded ownership ledger")
        producer, = [p for p in producers if p["output"] == o["object"]]
        if o["object"] == CFG_OBJECT:
            need(producer["source"] == CFG_WRAPPER and producer["maintained_owner_sources"] == [CFG_SOURCE, "src/op/menu/menu_state.inl"],
                 "actual containing CFG source producer; menu sibling stays context")
        elif o["object"] in HELPER_FORWARDING:
            chain = HELPER_FORWARDING[o["object"]]
            need(producer["source"] == chain[0] and o["forwarding_chain"] == list(chain)
                 and chain[-1] == o["source"], "complete reviewed helper forwarding chain")
            # The generic producer inventory labels these historical outer wrappers
            # as context. Actual native dependencies and every literal include below
            # establish the scoped maintained producer independently of that label.
            need(producer["ownership"] == "frozen-reference-context" and producer["maintained_owner_sources"] == [],
                 "generic helper wrapper inventory remains context")
            for parent, child in zip(chain, chain[1:]):
                need(files[parent] == ('#include "' + child + '"\n').encode(), "source-bound helper forwarding: " + parent)
        else:
            need(producer["maintained_owner_sources"] == [o["source"]], "current source producer ownership")
        obj = describe_omf((work / o["object"]).read_bytes())
        for name in obj["dependency_paths"]:
            name = re.sub(r"/+", "/", name.replace(chr(92), "/"))
            if name.startswith("C:/TC4/INCLUDE/"):
                need(name in configuration["sdk_sha256"], "consumed CFG SDK declaration")
            else:
                need(name in files and sha((work / name).read_bytes()) == report["source_sha256"][name],
                     "complete source/header dependency binding: " + name)
    scope = dict(base_scope, owners=owners, input_modes=shared, configuration=configuration, dispatch=dispatch, attract=attract, sound=sound, helpers=helpers, renderers=renderers, vs=vs, story=story, option=option, main_menu=main_menu, startup=startup, entry_data=entry_data)
    with contextlib.redirect_stdout(io.StringIO()):
        need(tracking.main(root, validate_product=False) == 0, "current global ledger consistency")
    return dict(cold_report_sha256=sha(report_raw), recipe_sha256=report["recipe_sha256"],
                source_inventory_sha256=digest(report["source_sha256"]), source_files=len(files),
                outputs_per_round=32, project_objects_per_round=30, rounds=2,
                decoded_sha256=sha(decoded), stored_sha256=sha(stored),
                scope=scope, product_exact=False, canonical_unit_credit_changed=False)


def oracle_rows(proof, now, policy, *, artifact="th03-op", publication_path=PUBLICATION,
                prefix="ev-op-current-", command=".venv/bin/python scripts/publish_th03_op_work_scopes.py"):
    product = artifact
    specs = {o["id"]: o for o in policy["oracles"]}
    need(set(GATES) == set(policy["policy"]["exact_requires"]), "eleven required gates")
    proof_digest = digest(proof)
    result = {}
    for owner in proof["scope"]["owners"]:
        rows = {}
        for gate in GATES:
            glob = gate in policy["policy"]["global_evidence_oracles"]
            artifact_wide = gate in policy["policy"]["artifact_evidence_oracles"]
            key = prefix + owner["unit_id"] + "-" + gate
            rows[key] = dict(id=key, claim_id=owner["unit_id"], oracle=gate,
                artifact="" if glob else product, unit_id="" if glob or artifact_wide else owner["unit_id"],
                extent_start="" if glob or artifact_wide else str(owner["start"]),
                extent_size="" if glob or artifact_wide else str(owner["size"]), location=publication_path,
                evidence_class=specs[gate]["accepts_evidence_classes"][0], result="pass",
                tool="current source-only " + product.removeprefix("th03-").upper() + " cold pair and independent native owner/runtime audit",
                command=command,
                input_sha256=owner["target_sha256"] if gate == "raw-bytes" else proof_digest,
                output_sha256=owner["candidate_sha256"] if gate == "raw-bytes" else proof_digest, observed_utc=now)
        result[owner["unit_id"]] = rows
    return result


def verify(root, publication):
    import validate_tracking as tracking
    root = Path(root)
    need(publication["schema"] == "op-current-source-acceptance-v1"
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
            set(policy["policy"]["non_acceptance_evidence_classes"]), artifact="th03-op", unit_id=owner["unit_id"],
            extent_start=owner["start"], extent_size=owner["size"],
            global_evidence_oracles=set(policy["policy"]["global_evidence_oracles"]),
            artifact_evidence_oracles=set(policy["policy"]["artifact_evidence_oracles"]))
        need(set(GATES) <= passed, "eleven scoped/classed Oracle gates")
    owners = proof["scope"]["owners"]
    return dict(repository_local=True, decoded_accepted=True, current_cold_source_scopes=True,
                reviewed_proof_ready=True, decoded_exact_units=len(owners),
                decoded_authored_procedures=sum(o.get("procedure_count",1) for o in owners),
                decoded_authored_code_bytes=sum(o.get("code_bytes",o["size"]) for o in owners),
                decoded_authored_initialized_data_bytes=sum(o.get("initialized_data_bytes",0) for o in owners),
                decoded_authored_bytes=sum(o["size"] for o in owners),
                decoded_exact_unit_ids=sorted(o["unit_id"] for o in proof["scope"]["owners"]), product_exact=False,
                mixed_physical_exact_bytes=0, canonical_credit_changed=False, factory_accepted=False,
                whole_game_percentage=None)
