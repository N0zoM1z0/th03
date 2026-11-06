"""Scoped 16-bit TC4 source-native MAIN producer and independent read-only check.

Always compile one complete maintained source translation unit from a fresh
wrapper, then TLINK only its one original slot in a verified native parent.
Never re-run the 99-object cold build, patch target bytes or credit old
functions again. A complete parent receipt must already exist for two rounds.
"""
import fcntl
import json
import os
import subprocess
from pathlib import Path

from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.pc98 import parse_mz
from lib.main_mz_compact import compact_mz
from lib.targets import find_artifact,load_target_manifest,read_verified_artifact
from probe_th03_main_bomb_rikako_cpp import segment_definitions


# Name, original full natural source, wrapper, CODE size, original PUBLIC
# count, complete original ordered OMF fixups, original MAP module provenance.
EXPECTED = {
    "ch_setup": (
        "src/main/player/character_setup.cpp",
        "src/main/player/producers/character_setup_native.cpp",
        3888, 12, 1135, "th03/ch_setup.cpp"
    ),
    "core": (
        "src/main/player/core.cpp",
        "src/main/player/producers/core_native.cpp",
        3135, 21, 260, "src/main/player/core.cpp"
    ),
    "entry": (
        "src/main/core/entry.cpp",
        "src/main/core/producers/entry_native.cpp",
        3050, 8, 433, "src/main/core/entry.cpp"
    ),
}

class NativeMainCPP:
    HELPER = "scripts/lib/native_main_cpp_layer.py"

    def __init__(self, parent, config, driver, stage, prefix):
        self.parent = parent
        self.ROOT = parent.ROOT
        self.WORK = parent.WORK
        self.CONFIG = config
        self.DRIVER = driver
        self.STAGE = stage
        self.PREFIX = prefix
        self.REPORT = prefix + "build.json"
        self.SCRATCH = self.WORK / ("probe/" + stage)

    def inputs(self):
        c = json.loads((self.ROOT/self.CONFIG).read_text())
        name = c["stem"]
        need(c["schema"] == "th03-main-large-cpp-forward-native-v1" and
             name in EXPECTED and
             (c["source"],c["wrapper"],c["CODE_bytes"],
              c["original_PUBLICs"],c["ordered_FIXUPP_fields"],
              c["original_MAP_module"]) == EXPECTED[name] and
             c["original_object"] == f"obj/th03/{name}.obj" and
             c["parent_report"] == self.parent.REPORT and
             c["stage"] == self.STAGE and
             c["GAME"] == 3 and c["BINARY"] == "M" and
             c["original_CODE_segment_index"] == 4 and
             c["original_Japanese_file_bytes"] == 130882 and
             c["original_ordered_MZ_relocations"] == 1553 and
             c["historic_vendor_raw_OMF_packet_identity"] is False and
             c["canonical_factory_credit_changed"] is False and
             c["whole_project_source_accepted"] is False,
             "one complete original MAIN large C++ TU, native code width and byte limits")
        raw = (self.ROOT/c["parent_report"]).read_bytes()
        prior = json.loads(raw)
        need(prior["complete"] and
             len(prior["rounds"]) == 2 and
             sha(raw) == c["parent_report_sha256"],
             "retained source-native previous 99-project-object MAIN parent")
        return c,sha((self.ROOT/self.CONFIG).read_bytes()),prior

    def sources(self,c):
        body = (self.ROOT/c["source"]).read_bytes()
        wrapper = (self.ROOT/c["wrapper"]).read_bytes()
        include = f'#include "{c["source"]}"\n'.encode()
        original = (self.WORK/c["source"]).read_bytes()
        need(body and b"\r" not in body and
             b"\r" not in wrapper and
             wrapper.count(include.strip()) == 1 and
             wrapper.endswith(include) and
             original.replace(b"\r\n",b"\n") == body and
             b"codestring" not in wrapper.lower(),
             "actual complete unmodified natural C++ implementation and one original source wrapper")
        return body,wrapper

    def original_object_scope(self,c,obj,original):
        native = payload(obj)
        original_code = payload(original)
        pubs = public_offsets(obj)
        defs = segment_definitions(obj)
        need(native == original_code and
             len(native) == c["CODE_bytes"] and
             all(seg == c["original_CODE_segment_index"] for seg,off in native) and
             literal_fields(obj) == literal_fields(original) and
             len(literal_fields(obj)) == c["ordered_FIXUPP_fields"] and
             pubs == public_offsets(original) and
             len(pubs) == c["original_PUBLICs"] and
             all(info["segment_index"] == 4 for info in pubs.values()) and
             defs == segment_definitions(original) and
             defs[3]["size"] == c["CODE_bytes"] and
             defs[3]["class"] == "CODE",
             "all original MAIN source instructions/PUBLIC ABI/ordered fixups and complete segments")
        return dict(
            complete_original_CODE_bytes=c["CODE_bytes"],
            original_PUBLIC_functions=c["original_PUBLICs"],
            original_ordered_FIXUPP_fields=c["ordered_FIXUPP_fields"],
            original_segment_index=4,
            initialized_original_CODE_equal=True,
            historical_full_OMF_packet_identity=False
        )

    def response(self,c,n):
        old = self.parent.response(n)
        for a,z in [
            (f"obj\\th03\\{c['stem']}.obj",
             f"probe\\{self.STAGE}\\r{n}\\{c['stem']}.obj"),
            (f"probe\\{self.parent.STAGE}\\r{n}.exe",
             f"probe\\{self.STAGE}\\r{n}.exe"),
            (f"probe\\{self.parent.STAGE}\\r{n}.map",
             f"probe\\{self.STAGE}\\r{n}.map"),
        ]:
            before,after = a.encode(),z.encode()
            need(old.count(before) == 1,
                 "exactly one original MAIN project source or link output slot "+a)
            old = old.replace(before,after)
        return old

    def read_pin(self,pin):
        path = Path(pin["path"])
        need(not path.is_absolute() and ".." not in path.parts,
             "retain source-native evidence inside repository")
        raw = (self.ROOT/path).read_bytes()
        need(len(raw) == pin["bytes"] and sha(raw) == pin["sha256"],
             "pinned source-native raw output hash and length "+str(path))
        return raw

    def normalize_map(self,c,raw,n):
        before = f"M=probe/{self.STAGE}/r{n}/{c['stem']}.cpp".encode()
        after = f"M={c['original_MAP_module']}".encode()
        need(raw.count(before) >= 3 and raw.count(after) == 0,
             "all original native source-module MAP rows have the new diagnostic name")
        # The entire parent MAP must match after this exact diagnostic change.
        return raw.replace(before,after)

    def run(self):
        c,cfg_sha,prev = self.inputs()
        source,wrapper = self.sources(c)
        original = (self.WORK/c["original_object"]).read_bytes()
        target = read_verified_artifact(
            self.ROOT,find_artifact(load_target_manifest(
                self.ROOT/"config/targets.toml"),"th03-main"))
        original_mz = parse_mz(target)
        need(len(target)==130882 and len(original_mz.relocations)==1553,
             "pinned candidate-local-attested original Japanese MAIN and relocations")
        record = dict(complete=False,cold_rebuilt=False,library_rebuilt=False,
            project_objects_recompiled_per_round=1,other_project_objects_reused=98,
            full_original_CODE_bytes=c["CODE_bytes"],
            original_PUBLIC_functions=c["original_PUBLICs"],
            original_ordered_FIXUPP_fields=c["ordered_FIXUPP_fields"],
            canonical_factory_credit_changed=False,whole_project_source_accepted=False,
            config_sha256=cfg_sha,driver_sha256=sha((self.ROOT/self.DRIVER).read_bytes()),
            helper_sha256=sha((self.ROOT/self.HELPER).read_bytes()),
            parent_report_sha256=c["parent_report_sha256"],
            original_OMF_sha256=sha(original),
            maintained_source_sha256=sha(source),wrapper_sha256=sha(wrapper),
            japanese_target_sha256=sha(target),phases=[],rounds=[])
        save=lambda:(self.ROOT/self.REPORT).write_text(json.dumps(record,indent=2)+"\n")
        env=dict(os.environ,DISPLAY="",WAYLAND_DISPLAY="",WINEDEBUG="-all",
            WINEPREFIX=str(self.ROOT/".analysis/toolchain/wineprefix"),
            MSDOS_PATH=r"C:\TC4\BIN",TZ="UTC",LANG="C",LC_ALL="C")
        dos=["/usr/bin/wine-stable",str(self.ROOT/"_reference/ReC98/bin/msdos.exe"),"-e","-x"]
        def run_native(argv,label):
            p = subprocess.run(argv,cwd=self.WORK,env=env,stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,timeout=115)
            log = self.PREFIX+label+".log"
            (self.ROOT/log).write_bytes(p.stdout)
            record["phases"].append(dict(label=label,argv=argv,returncode=p.returncode,
                                        log=log,log_sha256=sha(p.stdout)))
            save()
            need(p.returncode==0,label+": "+p.stdout.decode(errors="replace")[-1300:])
        with (self.ROOT/".analysis/borland-wine-writer.lock").open("ab") as lock:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            need(not self.SCRATCH.exists(),
                 "fresh source-native single MAIN C++ large producer stage")
            self.SCRATCH.mkdir()
            for name,file in [("driver.py",self.DRIVER),
                              ("config.json",self.CONFIG),
                              ("helper.py",self.HELPER)]:
                (self.SCRATCH/name).write_bytes((self.ROOT/file).read_bytes())
            pair=[]
            for n in (1,2):
                folder=self.SCRATCH/f"r{n}"
                folder.mkdir()
                inp=folder/f"{c['stem']}.cpp"
                inp.write_bytes(wrapper.replace(b"\n",b"\r\n"))
                os.utime(inp,(946684800,946684800))
                cmd=dos+["tcc","-c","-I.","-O","-b-","-3","-Z","-d",
                    "-DGAME=3","-ml","-DBINARY='M'",
                    f"-nprobe/{self.STAGE}/r{n}/",
                    f"probe/{self.STAGE}/r{n}/{c['stem']}.cpp"]
                run_native(cmd,f"round{n}-{c['stem']}-TC4-compile")
                obj=(folder/f"{c['stem']}.obj").read_bytes()
                scope=self.original_object_scope(c,obj,original)
                rsp=self.response(c,n)
                (self.SCRATCH/f"r{n}.@l").write_bytes(rsp)
                run_native(dos+["tlink",f"@probe\\{self.STAGE}\\r{n}.@l"],
                    f"round{n}-normal-TLINK")
                exe=(self.SCRATCH/f"r{n}.exe").read_bytes()
                mapped=(self.SCRATCH/f"r{n}.map").read_bytes()
                before=prev["rounds"][n-1]["outputs"]
                old_exe=self.read_pin(before["exe"])
                old_map=self.read_pin(before["map"])
                need(exe==old_exe and
                     self.normalize_map(c,mapped,n)==old_map and
                     parse_mz(exe).program_image==original_mz.program_image and
                     parse_mz(exe).relocations==original_mz.relocations,
                     "whole source-native MAIN EXE and every original Japanese image byte / 1553 relocation / MAP")
                packed=compact_mz(exe)
                need(packed==target and len(packed)==130882,
                     "original Japanese full file from independent standard DOS MZ serializer")
                outputs={}
                for name,blob in dict(obj=obj,exe=exe,map=mapped,compact_mz=packed).items():
                    path=self.PREFIX+f"round{n}-{name}.bin"
                    (self.ROOT/path).write_bytes(blob)
                    outputs[name]=dict(path=path,bytes=len(blob),sha256=sha(blob))
                record["rounds"].append(dict(round=n,outputs=outputs,
                    original_full_object_semantics=scope,
                    actual_original_link_response_sha256=sha(rsp),
                    whole_japanese_original_file_exact_after_explicit_MZ_format=True))
                save()
                pair.append(dict(obj=obj,exe=exe,map=mapped,compact_mz=packed))
                print(f"{c['stem']} source-native C++ round {n}: {c['CODE_bytes']} CODE /{c['original_PUBLICs']} functions /{c['ordered_FIXUPP_fields']} OMF, Japanese full MAIN exact",flush=True)
            need(pair[0]["exe"]==pair[1]["exe"] and
                 pair[0]["compact_mz"]==pair[1]["compact_mz"] and
                 payload(pair[0]["obj"])==payload(pair[1]["obj"]) and
                 literal_fields(pair[0]["obj"])==literal_fields(pair[1]["obj"]) and
                 public_offsets(pair[0]["obj"])==public_offsets(pair[1]["obj"]) and
                 self.sources(c)==(source,wrapper),
                 "two complete independent original natural C++ object and whole MAIN vectors repeat")
        record["complete"]=True
        save()

    def review(self):
        c,cfg_sha,prev = self.inputs()
        record=json.loads((self.ROOT/self.REPORT).read_text())
        report_sha=sha((self.ROOT/self.REPORT).read_bytes())
        source,wrapper=self.sources(c)
        original=(self.WORK/c["original_object"]).read_bytes()
        target=read_verified_artifact(self.ROOT,find_artifact(
            load_target_manifest(self.ROOT/"config/targets.toml"),"th03-main"))
        reference=parse_mz(target)
        need(record["complete"] and record["cold_rebuilt"] is False and
             record["library_rebuilt"] is False and
             record["project_objects_recompiled_per_round"]==1 and
             record["other_project_objects_reused"]==98 and
             record["full_original_CODE_bytes"]==c["CODE_bytes"] and
             record["original_PUBLIC_functions"]==c["original_PUBLICs"] and
             record["original_ordered_FIXUPP_fields"]==c["ordered_FIXUPP_fields"] and
             record["canonical_factory_credit_changed"] is False and
             record["whole_project_source_accepted"] is False and
             record["config_sha256"]==cfg_sha and
             record["driver_sha256"]==sha((self.ROOT/self.DRIVER).read_bytes()) and
             record["helper_sha256"]==sha((self.ROOT/self.HELPER).read_bytes()) and
             record["parent_report_sha256"]==c["parent_report_sha256"] and
             record["original_OMF_sha256"]==sha(original) and
             record["maintained_source_sha256"]==sha(source) and
             record["wrapper_sha256"]==sha(wrapper) and
             record["japanese_target_sha256"]==sha(target),
             "real original major source object/linker/target/parent pinned")
        for name,path in [("driver.py",self.DRIVER),("config.json",self.CONFIG),
                          ("helper.py",self.HELPER)]:
            need((self.SCRATCH/name).read_bytes()==(self.ROOT/path).read_bytes(),
                 "actual driver, config, reusable reviewed source-native helper immutable")
        expect=[f"round{n}-{label}" for n in (1,2) for label in
                (f"{c['stem']}-TC4-compile","normal-TLINK")]
        need(len(record["phases"])==4 and
             [p["label"] for p in record["phases"]]==expect and
             all(p["returncode"]==0 and
                 sha((self.ROOT/p["log"]).read_bytes())==p["log_sha256"]
                 for p in record["phases"]),
             "two full genuine original 16-bit Turbo C++/TLINK compiler logs")
        outputs=[]
        for n,row in enumerate(record["rounds"],1):
            before=prev["rounds"][n-1]["outputs"]
            need(row["round"]==n and
                 row["actual_original_link_response_sha256"]==sha(self.response(c,n)) and
                 (self.SCRATCH/f"r{n}.@l").read_bytes()==self.response(c,n) and
                 row["whole_japanese_original_file_exact_after_explicit_MZ_format"],
                 "the actual source-native original 99-object linker response has only one new slot")
            vals={k:self.read_pin(pin) for k,pin in row["outputs"].items()}
            need(set(vals)=={"obj","exe","map","compact_mz"} and
                 (self.SCRATCH/f"r{n}/{c['stem']}.cpp").read_bytes()==
                   wrapper.replace(b"\n",b"\r\n") and
                 (self.SCRATCH/f"r{n}/{c['stem']}.obj").read_bytes()==vals["obj"],
                 "actual complete original source/OMF/EXE/MAP/compact files SHA-pinned")
            scope=self.original_object_scope(c,vals["obj"],original)
            need(scope==row["original_full_object_semantics"] and
                 vals["exe"]==self.read_pin(before["exe"]) and
                 self.normalize_map(c,vals["map"],n)==self.read_pin(before["map"]) and
                 len(vals["exe"])==132322 and
                 parse_mz(vals["exe"]).program_image==reference.program_image and
                 parse_mz(vals["exe"]).relocations==reference.relocations and
                 len(reference.relocations)==1553 and
                 vals["compact_mz"]==compact_mz(vals["exe"])==target,
                 "whole original Japanese machine program and all 1553 ordered MZ, separate explicit MZ layout")
            outputs.append(vals)
        need(len(outputs)==2 and outputs[0]["exe"]==outputs[1]["exe"] and
             outputs[0]["compact_mz"]==outputs[1]["compact_mz"] and
             payload(outputs[0]["obj"])==payload(outputs[1]["obj"]) and
             literal_fields(outputs[0]["obj"])==literal_fields(outputs[1]["obj"]) and
             public_offsets(outputs[0]["obj"])==public_offsets(outputs[1]["obj"]),
             "two genuine original Turbo C++ independently produced OMFs and full MZ outputs repeat")
        return dict(complete=True,source_module=c["stem"],
            original_complete_CODE_bytes=c["CODE_bytes"],
            original_PUBLIC_functions=c["original_PUBLICs"],
            original_ordered_OMF_FIXUPP=c["ordered_FIXUPP_fields"],
            native_source_TC4_rounds=2,
            real_complete_original_CODE_and_native_OMF_sites_equal=True,
            original_FULL_japanese_program_124642_bytes_equal=True,
            original_all_1553_ordered_MZ_relocations_equal=True,
            original_FULL_130882_byte_japanese_EXE_equal_after_explicit_standard_MZ=True,
            direct_TLINK_original_header_equal=False,
            original_vendor_raw_OMF_packet_identity=False,
            canonical_factory_credit_changed=False,
            whole_project_source_accepted=False,
            source_native_report_sha256=report_sha)
