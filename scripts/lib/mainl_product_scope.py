"""Physical union and existing Oracle scope helpers for MAINL acceptance.
Never imports or executes a verifier named by untrusted sidecar data.
"""
from pathlib import Path
import csv, hashlib, importlib.util, io, json, re, tomllib

class Invalid(ValueError): pass

def require(ok, message):
    if not ok: raise Invalid(message)

def file_identity(root, pin):
    name=pin["path"]; relative=Path(name)
    require(not relative.is_absolute() and ".." not in relative.parts, "unsafe path")
    path=root/relative
    require(path.is_file() and not path.is_symlink(), "missing regular input: "+name)
    require(path.resolve().is_relative_to(root.resolve()), "input escapes repository")
    raw=path.read_bytes()
    require(len(raw)==pin["bytes"] and hashlib.sha256(raw).hexdigest()==pin["sha256"], "identity drift: "+name)
    return raw

def union_bytes(extents, artifact_sizes):
    """Physical intervals supplied by an acceptance caller, not this schema check.
    Each tuple is (canonical artifact ID, start, size); nested coverage counts once.
    Never accepts decoded coordinates or mixes artifacts.
    """
    grouped={}
    for artifact,start,size in extents:
        require(artifact in artifact_sizes, "unknown canonical artifact")
        require(type(start) is int and type(size) is int and start>=0 and size>0, "invalid physical extent")
        require(start+size<=artifact_sizes[artifact], "physical extent outside artifact")
        grouped.setdefault(artifact,[]).append((start,start+size))
    total=0
    for spans in grouped.values():
        end=-1
        for left,right in sorted(spans):
            total+=max(0,right-max(left,end));end=max(end,right)
    return total

def scoped_passes(root, evidence_ids, evidence, artifact, owner, start, size):
    """Reuse existing eleven-Oracle classes and exact scope rules unchanged.
    Metadata eligibility is NOT fresh replay verification.
    """
    spec=importlib.util.spec_from_file_location("tracking_product_proposal",root/"scripts/validate_tracking.py")
    tracking=importlib.util.module_from_spec(spec);spec.loader.exec_module(tracking)
    config=tomllib.loads((root/"config/oracles.toml").read_text());policy=config["policy"]
    known={r["id"]:r for r in config["oracles"]}
    require(len(evidence_ids)==len(set(evidence_ids)), "duplicate evidence ID")
    require(all(i in evidence for i in evidence_ids), "unknown evidence ID")
    require(all(evidence[i]["oracle"] in known for i in evidence_ids), "unknown Oracle")
    passed=tracking.accepted_oracle_passes(evidence_ids,evidence,known,set(policy["non_acceptance_evidence_classes"]),artifact=artifact,unit_id=owner,extent_start=start,extent_size=size,global_evidence_oracles=set(policy["global_evidence_oracles"]),artifact_evidence_oracles=set(policy["artifact_evidence_oracles"]))
    return set(policy["exact_requires"])-passed
