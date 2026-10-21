"""Compose maintained MAINL linked-game providers without changing original statements."""
from pathlib import Path
import hashlib
CPP_HEADER = b'// Maintained TH03 MAINL linked-game provider.\n// Historical source statements, declarations, inline assembly and compiler pragmas\n// are retained. The composer uses the actual cached first-use GAME/BINARY slot.\n// Contextual headers retain the original real-mode ABI; no MAIN acceptance is inherited.\n\n'
ASM_HEADER = b'; Maintained TH03 MAINL early STAFF_TEXT music and ending flow.\n; Original near interfaces, FAR script pointer, signed division and unchecked execl\n; return path are retained. The flake procdesc is contextual, not an extra body.\n\n'
STAFF_BEGIN = b"\nSTAFF_TEXT segment byte public 'CODE' use16\n"
STAFF_END = b"\nSTAFF_TEXT ends"
def lf(raw):return raw.replace(b"\r\n",b"\n")
def sha(raw):return hashlib.sha256(raw).hexdigest()
def load_inputs(root, recipe):
    root=Path(root)
    def read(row):
        raw=(root/row["path"]).read_bytes()
        if sha(raw)!=row["sha256"]:raise ValueError("input identity differs: "+row["path"])
        return raw
    for row in recipe["compatibility_inputs"]:
        if read(row)!=row["text"].encode():raise ValueError("compat forwarding header differs")
    providers={p["name"]:read(p["provider"]) for p in recipe["providers"]}
    wrappers={p["name"]:read(p["wrapper"]) for p in recipe["providers"]}
    maintained={p["name"]:read(p["source"]) for p in recipe["providers"]}
    return read(recipe["previous_generated_root"]),providers,wrappers,maintained,read(recipe["staff_source"])
def compose(root_asm, providers, wrappers, maintained, staff, recipe):
    names={p["name"] for p in recipe["providers"]}
    if len(names)!=15 or any(set(x)!=names for x in (providers,wrappers,maintained)):
        raise ValueError("complete fifteen-provider set required")
    generated={row["path"]:row["text"].replace("\n","\r\n").encode() for row in recipe["compatibility_inputs"]}
    for row in recipe["providers"]:
        name=row["name"];source=row["source"]["path"]
        old=lf(providers[name]);new=lf(maintained[name])
        # Only the fixed header and declared compatibility forwarding paths change.
        for shim in recipe["compatibility_inputs"]:
            old=old.replace(('#include "'+shim["original_include"]+'"').encode(),('#include "'+shim["path"]+'"').encode())
        if new!=CPP_HEADER+old:raise ValueError("original C/C++ statements differ: "+name)
        expected=('#include "'+row["provider_relative"]+'"\n').encode()
        if lf(wrappers[name])!=expected:raise ValueError("original wrapper differs: "+name)
        generated[row["wrapper_relative"]]=('#include "'+source+'"\r\n').encode()
        generated[source]=new.replace(b"\n",b"\r\n")
    root=lf(root_asm)
    if root.count(STAFF_BEGIN)!=1 or root.count(STAFF_END)!=1:
        raise ValueError("early STAFF_TEXT boundaries differ")
    a=root.index(STAFF_BEGIN)+len(STAFF_BEGIN);b=root.index(STAFF_END,a)
    if lf(staff)!=ASM_HEADER+root[a:b]:
        raise ValueError("early STAFF_TEXT symbolic body differs")
    path=recipe["staff_source"]["path"]
    generated[path]=lf(staff).replace(b"\n",b"\r\n")
    root=root[:a]+("include "+path+"\n").encode()+root[b:]
    generated["th03_mainl.asm"]=root.replace(b"\n",b"\r\n")
    return generated
def stage(destination,generated):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=False)
    for name,raw in generated.items():
        p=destination/name;p.parent.mkdir(parents=True,exist_ok=True)
        with p.open("xb") as out:out.write(raw)
