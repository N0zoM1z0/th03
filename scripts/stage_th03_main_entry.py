"""Transfer the complete MAIN entry; export views of existing code and storage."""

from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ALIASES = {
    "@GameExecl$qnxc": ("MAIN_EXEC", "far"),
    "aCOul": ("_main_archive_name", "byte"),
    "aGameft_bft": ("_main_gaiji_font", "byte"),
    "aOp": ("_main_op_name", "byte"),
    "arg0": ("_main_ending_name", "byte"),
    "farfp_20F20": ("_main_background_init", "dword"),
    "sub_9B14": ("_stage_setup", "near"),
    "sub_9778": ("_round_loop", "near"),
    "sub_A21F": ("_round_start_next", "near"),
}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def transform_root(raw):
    text = raw.decode("latin1")
    a = "public _main\r\n_main\t\tproc far"
    z = "_main\t\tendp"
    need(text.count(a) == text.count(z) == 1, "complete sole MAIN entry")
    lo, hi = text.index(a), text.index(z) + len(z)
    body = text[lo:hi]
    need(
        re.findall(r"^(\S+)\s+proc\s+(near|far)", body, re.M) == [("_main", "far")],
        "one complete far entry",
    )
    # Keep both boundaries and every following procedure/table in their original order.
    text = (
        text[:lo]
        + "; MAIN entry is supplied by src/main/core/entry.cpp.\r\n"
        + text[hi:]
    )
    for old, (new, kind) in ALIASES.items():
        need(new not in text, "alias collision " + new)
        pat = r"^" + re.escape(old) + r"(?=\s+(?:db|dd|proc)\b)"
        need(len(re.findall(pat, text, re.M)) == 1, "sole original owner " + old)
        text = re.sub(
            pat,
            lambda m: "public " + new + "\r\n" + new + " label " + kind + "\r\n" + old,
            text,
            flags=re.M,
        )
    return text.encode("latin1")


def transform_response(raw):
    anchor, new = b"obj\\th03\\main.obj", b"obj\\th03\\entry.obj"
    need(raw.count(anchor) == 1 and new not in raw, "sole MAIN object insertion")
    return raw.replace(anchor, new + b" " + anchor)


INPUT_HASHES = {
    "th03_main.asm": "38b7dc8c1c9acb7f7165da12e014a28e06cb57a0e6f90ae98f24845e77724bb0",
    "obj/th03/main.@l": "77e69e50835882c3fa3683dcfae6b00cc13d3f7fa952c381af9c452ae0446ec6",
}


def stage(baseline, output):
    baseline, output = Path(baseline).resolve(), Path(output).resolve()
    need(
        output.is_relative_to(ROOT / ".analysis") and not output.exists(),
        "fresh ignored output required",
    )
    products = {}
    inputs = {}
    for name, transform in (
        ("th03_main.asm", transform_root),
        ("obj/th03/main.@l", transform_response),
    ):
        path = baseline / name
        need(not any(p.is_symlink() for p in (path, *path.parents)), "source symlink")
        raw = path.read_bytes()
        need(
            hashlib.sha256(raw).hexdigest() == INPUT_HASHES[name],
            "state/shot staging identity: " + name,
        )
        products[name] = transform(raw)
        inputs[name] = hashlib.sha256(raw).hexdigest()
    output.mkdir()
    for name, raw in products.items():
        p = output / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(raw)
    report = dict(
        inputs=inputs,
        outputs={n: hashlib.sha256(raw).hexdigest() for n, raw in products.items()},
        native_invocations=0,
        source_acceptance=False,
        exact_acceptance=False,
    )
    (output / "stage-report.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--baseline",
        type=Path,
        required=True,
        help="output of stage_th03_main_playerstate.py",
    )
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(stage(a.baseline, a.output), indent=2))


if __name__ == "__main__":
    main()
