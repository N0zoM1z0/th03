"""Materialize source plus two named vendor inputs; no old project outputs.

Only the literal include closure of the two tiny C++ roots is selected from the
pinned reference archive. Maintained forwarders keep every borrowed dependency
visible. The other producers use their existing bounded source stages.
"""

import hashlib
import io
from pathlib import Path
import posixpath
import re
import subprocess
import tarfile
import tomllib

import stage_th03_zun_driver_jwasm as driver
from stage_th03_zun_init import stage_bytes
import stage_th03_zun_resident as resident
import stage_th03_zunsoft as logo

PROFILE = "config/th03_zun_work.toml"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def need(value, message):
    if not value:
        raise ValueError(message)


def include_closure(data, roots):
    include = re.compile(rb'^\s*#\s*include\s*["<]([^">]+)[">]', re.M)
    selected, external = {}, []
    queue = list(roots)
    while queue:
        name = queue.pop()
        if name in selected:
            continue
        need(name in data, "missing source dependency: " + name)
        selected[name] = data[name]
        for match in include.finditer(data[name]):
            token = match[1].decode("ascii").replace("\\", "/")
            choices = [posixpath.normpath(str(Path(name).parent / token)), token]
            dependency = next((n for n in choices if n in data), None)
            if dependency is None:
                external.append(dict(source=name, include=token))
            else:
                queue.append(dependency)
    return selected, external


def compose(root):
    root = Path(root)
    config = tomllib.loads((root / PROFILE).read_text())
    raw = subprocess.check_output(["git", "archive", "--format=tar", config["reference_revision"]],
                                  cwd=root / "_reference/ReC98")
    need(sha(raw) == config["reference_archive_sha256"], "reference source archive identity drift")
    vendor = {v["path"]: v for v in config["vendor_inputs"]}
    suffixes = {".c", ".cpp", ".h", ".hpp", ".inc", ".inl", ".asm", ".asp", ".csp"}
    data = {}
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        for item in archive.getmembers():
            path = Path(item.name)
            need(not path.is_absolute() and ".." not in path.parts and not item.issym()
                 and not item.islnk(), "unsafe reference archive member")
            if item.isfile() and (path.suffix.lower() in suffixes or item.name in vendor):
                need(item.name not in data, "duplicate reference input")
                data[item.name] = archive.extractfile(item).read()
    maintained = logo.read_inputs(root)
    _, overlay = resident.read_inputs(root, root / "config/zun_resident/source.json")
    maintained.update(overlay)
    data.update(maintained)
    data["th01/zunsoft.cpp"] = b'#include "src/zun/zunsoft.cpp"\n'
    data["th03/res_yume.cpp"] = b'#include "src/zun/res_yume.cpp"\n'
    files, external = include_closure(data, ["th01/zunsoft.cpp", "th03/res_yume.cpp"])
    libraries = " ".join(config["tiny_libraries"])
    for name, game in (("zunsoft", 1), ("res_yume", 3)):
        files[f"obj/th0{game}/{name}.rsp"] = (
            f"-c -s -t c0t.obj obj\\th0{game}\\{name}.obj, bin\\th0{game}\\{name}.com, "
            f"obj\\th0{game}\\{name}.map, {libraries}\r\n").encode()
    for source, alias in (("launcher", "stub"), ("transfer_call", "call"), ("transfer_helper", "helper"), ("directory", "meta")):
        name = "src/zun/" + source + ".asm"
        maintained[name] = (root / name).read_bytes()
        files["wrapper/" + alias + ".asm"] = maintained[name]
        files["wrapper/" + alias + ".rsp"] = f"-c -s -t -3 {alias}.obj,{alias}.com,{alias}.map,\r\n".encode()
    maintained["src/zun/init.asm"] = (root / "src/zun/init.asm").read_bytes()
    files["init/src/zun/init.asm"] = stage_bytes(maintained["src/zun/init.asm"])
    files["init/link.rsp"] = b"-c -s -t -3 init.obj,init.com,init.map,\r\n"
    driver_files, driver_inputs = driver.payload(root)
    maintained.update(driver_inputs)
    files.update({"driver/" + n: b for n, b in driver_files.items()})
    for name, identity in vendor.items():
        value = data[name]
        need(len(value) == identity["bytes"] and sha(value) == identity["sha256"], "vendor identity drift: " + name)
        files[name] = value
    need({n for n in files if Path(n).suffix.lower() in {".obj", ".com", ".exe", ".lib", ".map"}}
         == set(vendor), "undeclared native binary seed")
    return files, maintained, dict(profile=PROFILE, archive_sha256=sha(raw),
                                    vendor_inputs=config["vendor_inputs"], external_includes=external)
