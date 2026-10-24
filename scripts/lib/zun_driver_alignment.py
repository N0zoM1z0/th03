"""Native source controls for the driver's natural paragraph and WORD layout."""

import hashlib
from pathlib import Path
import re
from tempfile import TemporaryDirectory

from lib.omf import describe_omf


def need(value, message):
    if not value: raise ValueError("ZUN alignment control: " + message)


def variants(files):
    driver = {n.removeprefix("driver/"): raw for n, raw in files.items() if n.startswith("driver/")}
    text = driver["driver.asm"]
    para = b" segment para public 'CODE' use16"
    need(text.count(para) == 16 and text.count(b"\r\neven\r\n") == 1, "actual eight PARA declarations/contributions and WORD boundary")
    for name, replacement in (("word", text.replace(para, b" segment word public 'CODE' use16")),
                              ("no-even", text.replace(b"\r\neven\r\n", b"\r\n", 1))):
        yield name, dict(driver, **{"driver.asm": replacement})


def run(files, parent, emitter_command, linker_command, execute, target):
    results = []
    for name, changed in variants(files):
        with TemporaryDirectory(prefix=".ZUN-align-", dir=parent) as folder:
            work = Path(folder)
            for path, raw in changed.items():
                output = work / path; output.parent.mkdir(parents=True, exist_ok=True); output.write_bytes(raw)
            execute(emitter_command, work, "control:" + name + "-assemble")
            execute(linker_command, work, "control:" + name + "-link")
            obj = (work / "driver.obj").read_bytes()
            candidate = (work / "driver.com").read_bytes()
            need(describe_omf(obj)["valid"] and candidate != target, "actual changed-alignment native output must fail raw equality")
            if name == "word": need(len(candidate) < len(target), "WORD contributions remove paragraph storage")
            else: need(len(candidate) == len(target), "removed EVEN remains observable inside unchanged total span")
            text = (work / "driver.map").read_text()
            rows = re.findall(r"(?m)^\s*0000:[0-9A-F]+\s+(?:idle\s+)?(sprite16_\w+|start)\s*$", text)
            need(len(rows) == 112 and len(set(rows)) == 56, "both complete public tables survive native source control")
            results.append(dict(name=name, byte_exact_rejected=True, target_bytes=len(target), candidate_bytes=len(candidate),
                differing_bytes=sum(a != b for a, b in zip(candidate, target)) + abs(len(candidate) - len(target)),
                changed_inputs=["driver.asm"], candidate_sha256=hashlib.sha256(candidate).hexdigest(),
                object_sha256=hashlib.sha256(obj).hexdigest(), all_procedure_includes_unchanged=True))
    return dict(count=len(results), controls=results, source_only=True, object_patches=False)
