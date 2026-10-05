#!/usr/bin/env python3
"""Compare frozen compiler CODE coordinates to DIET-restored bytes.

MAP coordinates are candidate observations, not established target ownership.
This diagnostic neither relocates/normalizes bytes nor grants acceptance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import tomllib

from inventory_rec98_th03 import frozen_files, link_roots
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
MAP_ROW = re.compile(
    r" ([0-9A-F]{4}):([0-9A-F]{4}) ([0-9A-F]+) C=CODE\s+"
    r"S=(\S+)\s+G=\S+\s+M=(\S+)\s+ACBP=([0-9A-F]+)$"
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pinned(path: str, digest: str) -> bytes:
    data = (ROOT / path).read_bytes()
    if sha(data) != digest:
        raise ValueError(f"changed diagnostic input: {path}")
    return data


def code_rows(text: str, image_size: int) -> list[dict]:
    rows = []
    intervals = []
    for line in text.splitlines():
        match = MAP_ROW.fullmatch(line)
        if not match:
            if " C=CODE" in line:
                raise ValueError(f"unparsed CODE contribution: {line}")
            continue
        segment, offset, size = (int(match[i], 16) for i in (1, 2, 3))
        start = segment * 16 + offset
        if start + size > image_size:
            raise ValueError("CODE contribution exceeds program image")
        if size:
            intervals.append((start, start + size))
        rows.append(dict(segment=segment, offset=offset, start=start, size=size,
                         name=match[4], module=match[5].replace("\\", "/"),
                         acbp=match[6]))
    if not rows:
        raise ValueError("no CODE contributions")
    intervals.sort()
    if any(a[1] > b[0] for a, b in zip(intervals, intervals[1:])):
        raise ValueError("overlapping CODE contributions")
    return rows


def extent_observation(target, candidate, row: dict) -> dict:
    start, size = row["start"], row["size"]
    end = start + size
    if end > min(len(target.program_image), len(candidate.program_image)):
        raise ValueError("candidate coordinates exceed a compared image")
    left = target.program_image[start:end]
    right = candidate.program_image[start:end]
    def relocations(image):
        found = []
        for record in image.relocations:
            if size and record.linear < end and record.linear + 2 > start:
                if record.linear < start or record.linear + 2 > end:
                    raise ValueError("relocation word straddles CODE boundary")
                found.append([record.segment, record.offset])
        return found
    left_relocs, right_relocs = relocations(target), relocations(candidate)
    different = [i for i, (a, b) in enumerate(zip(left, right)) if a != b]
    return dict(row, target_slice_sha256=sha(left), candidate_slice_sha256=sha(right),
                different_bytes=len(different), first_difference_relative=(
                    different[0] if different else None),
                raw_slice_equal=left == right,
                target_ordered_relocations=left_relocs,
                candidate_ordered_relocations=right_relocs,
                ordered_relocations_equal=left_relocs == right_relocs,
                target_boundary_reviewed=False, source_acceptance=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config_path = ROOT / "config/th03_decoded_code_review.toml"
    config_bytes = config_path.read_bytes()
    config = tomllib.loads(config_bytes.decode())
    if config["schema_version"] != 1 or [a["id"] for a in config["artifacts"]] != [
            "th03-op", "th03-mainl"]:
        raise ValueError("unsupported diagnostic configuration")
    diet = tomllib.loads((ROOT / "config/th03_diet.toml").read_text())
    targets = load_target_manifest(ROOT / "config/targets.toml")
    inputs = {str(config_path.relative_to(ROOT)): sha(config_bytes),
              "scripts/review_th03_decoded_code.py": sha(Path(__file__).read_bytes())}
    for path in ["config/th03_diet.toml", "config/targets.toml",
                 "scripts/inventory_rec98_th03.py", "scripts/lib/pc98.py",
                 "scripts/lib/targets.py"]:
        inputs[path] = sha((ROOT / path).read_bytes())
    inputs[config["replay_receipt"]] = config["replay_receipt_sha256"]
    inputs[config["diet_receipt"]] = config["diet_receipt_sha256"]
    replay = json.loads(pinned(config["replay_receipt"], config["replay_receipt_sha256"]))
    restoration = json.loads(pinned(config["diet_receipt"], config["diet_receipt_sha256"]))
    if not (replay["pass"] and replay["all_products_equal"] and
            replay["reference_revision"] == config["reference_revision"] ==
            diet["reference_revision"]):
        raise ValueError("cold scaffold receipt does not support diagnostic lineage")
    if not (restoration["restoration_checks_pass"] and
            restoration["canonical_targets_unchanged"] and
            restoration["reference_revision"] == config["reference_revision"]):
        raise ValueError("restoration receipt does not support decoded lineage")
    files = frozen_files(config["reference_revision"])
    roots = link_roots(files)
    products = []
    for artifact in config["artifacts"]:
        aid = artifact["id"]
        stored = read_verified_artifact(ROOT, find_artifact(targets, aid))
        decoded_pin = next(a for a in diet["artifacts"] if a["id"] == aid)
        decoded = pinned(artifact["decoded_path"], decoded_pin["decoded_sha256"])
        lineage = next(o for o in restoration["observations"] if o["artifact"] == aid)
        if (lineage["stored"]["sha256"] != sha(stored) or
                lineage["decoded"]["sha256"] != sha(decoded)):
            raise ValueError("restoration receipt disagrees with compared images")
        inputs[artifact["decoded_path"]] = sha(decoded)
        if [r["round"] for r in artifact["rounds"]] != [1, 2]:
            raise ValueError("diagnostic needs both ordered cold rounds")
        target = parse_mz(decoded)
        if not target.valid or len(decoded) != decoded_pin["decoded_size"]:
            raise ValueError("invalid decoded MZ")
        rounds = []
        for entry in artifact["rounds"]:
            replay_round = next(r for r in replay["rounds"] if r["round"] == entry["round"])
            if replay_round["products"][f"bin/th03/{aid.removeprefix('th03-')}.exe"] != \
                    entry["candidate_sha256"]:
                raise ValueError("candidate is not a recorded cold product")
            candidate_bytes = pinned(entry["candidate_path"], entry["candidate_sha256"])
            map_bytes = pinned(entry["map_path"], entry["map_sha256"])
            inputs[entry["candidate_path"]] = sha(candidate_bytes)
            inputs[entry["map_path"]] = sha(map_bytes)
            candidate = parse_mz(candidate_bytes)
            if not candidate.valid:
                raise ValueError("invalid candidate MZ")
            rows = code_rows(map_bytes.decode("ascii"), len(candidate.program_image))
            observations = [extent_observation(target, candidate, row) for row in rows]
            direct = {path: [o for o in observations if o["module"] == path]
                      for path in sorted(roots[aid])}
            if any(not values for values in direct.values()):
                raise ValueError("direct link source absent from detailed CODE MAP")
            rounds.append(dict(round=entry["round"], contributions=observations,
                               direct_sources=[dict(path=path, source_sha256=sha(files[path]),
                                                    contributions=values)
                                               for path, values in direct.items()],
                               full_file_raw_equal=decoded == candidate_bytes,
                               target_header_size=target.header.header_size,
                               candidate_header_size=candidate.header.header_size,
                               target_program_size=len(target.program_image),
                               candidate_program_size=len(candidate.program_image),
                               program_raw_different_bytes=sum(a != b for a, b in zip(
                                   target.program_image, candidate.program_image)) + abs(
                                       len(target.program_image) - len(candidate.program_image))))
        if rounds[0]["contributions"] != rounds[1]["contributions"]:
            raise ValueError("cold rounds disagree on CODE observations")
        products.append(dict(artifact=aid, canonical_stored_sha256=sha(stored),
                             decoded_sha256=sha(decoded), rounds=rounds))
    # Re-read pinned inputs before publishing evidence.
    for path, digest in inputs.items():
        pinned(path, digest)
    for product in products:
        if sha(read_verified_artifact(ROOT, find_artifact(targets, product["artifact"]))) != \
                product["canonical_stored_sha256"]:
            raise ValueError("canonical stored target changed during diagnostic")
    result = dict(kind="th03-decoded-candidate-code-diagnostic", inputs=inputs,
                  reference_revision=config["reference_revision"], products=products,
                  diagnostic_checks_pass=True, source_acceptance=False,
                  exact_acceptance=False,
                  scope="Unmodified raw slices at compiler MAP coordinates; target boundaries unreviewed")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    for product in products:
        r = product["rounds"][0]
        nonempty = [o for o in r["contributions"] if o["size"]]
        direct = r["direct_sources"]
        same = sum(all(o["raw_slice_equal"] and o["ordered_relocations_equal"]
                       for o in s["contributions"] if o["size"]) and
                   any(o["size"] for o in s["contributions"]) for s in direct)
        print(f"{product['artifact']}: {len(direct)} direct sources, {same} nonempty matching "
              f"candidate contributions; {len(nonempty)} CODE contributions; "
              f"{r['program_raw_different_bytes']} different program bytes; no acceptance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
