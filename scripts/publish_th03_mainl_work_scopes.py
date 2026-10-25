#!/usr/bin/env python3
"""Publish current decoded MAINL source owners, excluding unowned context."""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tomllib

from lib.decoded_mainl_acceptance import PUBLICATION, audit, oracle_rows, proof_inputs, verify


def main():
    root = Path(__file__).resolve().parents[1]
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    proof = audit(root)
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    policy = tomllib.loads((root / "config/oracles.toml").read_text())
    publication = dict(schema="mainl-current-source-acceptance-v1", state="repository-local-accepted",
                       observed_utc=now, proof_inputs=proof_inputs(root), audit=proof,
                       owner_oracles=oracle_rows(proof, now, policy))
    result = verify(root, publication)
    (root / PUBLICATION).write_text(json.dumps(publication, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
