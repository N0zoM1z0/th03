"""Bounded first-use TC4 C++ source-unit compiler/linker and read-only reviewer.

Only a single real original OMF source producer is recompiled per round.
All other original MAINL CRT and 35 project objects are taken from a
SHA-pinned source-native parent. Direct native link and target/OMF checks
are mandatory; no project cold replay, target patch, or fabricated code.
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
from probe_th03_main_bomb_rikako_cpp import segment_definitions


class NativeCPP:
    def __init__(self,parent,config,driver,stage,prefix):
        self.parent=parent
        self.ROOT=parent.ROOT
        self.WORK=parent.WORK
        self.base=parent.base
        self.CONFIG=config
        self.DRIVER=driver
        self.STAGE=stage
        self.PREFIX=prefix
        self.REPORT=prefix+"build.json"
        self.SCRATCH=self.WORK/("probe/"+stage)
        self.HELPER="scripts/lib/native_cpp_forward.py"

    def inputs(self):
        cfg,cfg_hash=self.base.load(self.CONFIG)
        stem=cfg["stem"]
        need(cfg["schema"]=="th03-mainl-forward-native-CPP-v1" and
             cfg["stage"]==self.STAGE and cfg["parent_report"]==self.parent.REPORT and
             cfg["original_object"]==f"obj/th03/{stem}.obj" and
             cfg["wrapper"].startswith("src/mainl/") and
             cfg["source"].startswith("src/shared/") and
             stem in ("cdg_load","grppsafx") and
             cfg["binary"]=="O" and cfg["game"]==3 and
             cfg["data_bytes"]==0 and cfg["BSS_bytes"]==0 and
             cfg["historical_raw_OMF_packets_identical"] is False and
             cfg["canonical_credit_changed"] is False and
             cfg["whole_project_source_accepted"] is False and
             isinstance(cfg["upstream_diagnostic_paths"],list) and
             len(cfg["upstream_diagnostic_paths"]) in (4,5),
             "source-first-use C++ module config")
        # Keep source variants in one bounded implementation; no unrestricted
        # project-wide native recompilation is authorized by this driver.
        expected={
            "cdg_load":("src/shared/formats/cdg_load.cpp",593,5,35),
            "grppsafx":("src/shared/graphics/text.cpp",613,1,6)}
        need((cfg["source"],cfg["CODE_bytes"],cfg["PUBLICs"],cfg["ordered_fixups"])==
             expected[stem], "one original bounded source CODE/PUBLIC/FIXUPP scope")
        need(cfg["historical_raw_OMF_packets_identical"] is False and
             cfg["canonical_credit_changed"] is False and
             cfg["whole_project_source_accepted"] is False and
             cfg["parent_report_sha256"]==sha((self.ROOT/self.parent.REPORT).read_bytes()),
             "genuine preserved completed source-bound parent and no overclaim")
        prior,prior_sha=self.base.load(self.parent.REPORT)
        need(prior["complete"] and len(prior["rounds"])==2 and
             prior_sha==cfg["parent_report_sha256"],
             "complete original source-native ancestor pair, not cold replay")
        return cfg,cfg_hash,prior

    def sources(self,cfg):
        source=(self.ROOT/cfg["source"]).read_bytes()
        wrapper=(self.ROOT/cfg["wrapper"]).read_bytes()
        native=(self.WORK/cfg["source"]).read_bytes()
        need(source and b"\r" not in source and
             native.replace(b"\r\n",b"\n")==source and
             wrapper.count(f'#include "{cfg["source"]}"'.encode())==1 and
             wrapper.endswith(f'#include "{cfg["source"]}"\n'.encode()) and
             b"codestring" not in wrapper.lower() and b"\r" not in wrapper,
             "actual unchanged complete first-use C++ source/header and maintained wrapper")
        return source,wrapper

    def response(self,cfg,n):
        raw=self.parent.response(n)
        stem=cfg["stem"]
        for before,after in [
            (f"obj\\th03\\{stem}.obj".encode(),
             f"probe\\{self.STAGE}\\r{n}\\{stem}.obj".encode()),
            (f"probe\\{self.parent.STAGE}\\r{n}.exe".encode(),
             f"probe\\{self.STAGE}\\r{n}.exe".encode()),
            (f"probe\\{self.parent.STAGE}\\r{n}.map".encode(),
             f"probe\\{self.STAGE}\\r{n}.map".encode())]:
            need(raw.count(before)==1,"exact original project native link source/target slot")
            raw=raw.replace(before,after)
        return raw

    def normalized_map(self,cfg,raw,n):
        stem=cfg["stem"]
        before=f"M=probe/{self.STAGE}/r{n}/{stem}.cpp".encode()
        need(raw.count(before)==3,"all three original CPP CODE/DATA/BSS MAP rows")
        return raw.replace(before,f"M=th03/{stem}.cpp".encode())

    def stable_map(self,cfg,raw,n):
        raw=self.normalized_map(cfg,raw,n)
        for stage,stem in cfg["upstream_diagnostic_paths"]:
            before=f"M=probe/{stage}/r{n}/{stem}.cpp".encode()
            need(raw.count(before)==3, "source-stage diagnostic filename rows "+stem)
            raw=raw.replace(before,f"M=source/{stem}.cpp".encode())
        return raw

    def object_scope(self,cfg,native,original):
        a,b=payload(native),payload(original)
        pubs=public_offsets(native)
        need(a==b and len(a)==cfg["CODE_bytes"] and
             len([site for site in a if site[0]==1])==cfg["CODE_bytes"] and
             len(literal_fields(native))==cfg["ordered_fixups"] and
             literal_fields(native)==literal_fields(original) and
             len(pubs)==cfg["PUBLICs"] and pubs==public_offsets(original) and
             segment_definitions(native)==segment_definitions(original) and
             segment_definitions(native)[1]["size"]==0 and
             segment_definitions(native)[2]["size"]==0,
             "complete original TC4 emitted initialized CODE/ordered fixups/PUBLIC/SEGDEF")
        return dict(original_CODE_bytes=cfg["CODE_bytes"],
            original_PUBLICs=cfg["PUBLICs"],native_ordered_FIXUPP_fields=cfg["ordered_fixups"],
            complete_original_code_AND_ABI_equal=True,
            historical_raw_Borland_OMF_packet_identity=False)

    def run(self):
        cfg,cfg_hash,prior=self.inputs()
        code,wrapper=self.sources(cfg)
        original=(self.WORK/cfg["original_object"]).read_bytes()
        reference=(self.WORK/"bin/th03/mainl.target.exe").read_bytes()
        need(len(reference)==67372 and len(parse_mz(reference).relocations)==677,
             "real Japanese candidate-local-attested decoded MAINL original")
        report=dict(complete=False,cold_rebuilt=False,library_rebuilt=False,
            recompiled_project_objects_per_round=1,other_project_objects_reused=35,
            total_CODE_bytes=cfg["CODE_bytes"],original_PUBLICs=cfg["PUBLICs"],
            original_OMF_FIXUPP_fields=cfg["ordered_fixups"],
            whole_project_source_accepted=False,canonical_factory_credit_changed=False,
            config_sha256=cfg_hash,driver_sha256=sha((self.ROOT/self.DRIVER).read_bytes()),
            helper_sha256=sha((self.ROOT/self.HELPER).read_bytes()),
            source_sha256=sha(code),wrapper_sha256=sha(wrapper),
            original_object_sha256=sha(original),
            parent_report_sha256=cfg["parent_report_sha256"],
            original_japanese_exe_sha256=sha(reference),phases=[],rounds=[])
        save=lambda:(self.ROOT/self.REPORT).write_text(json.dumps(report,indent=2)+"\n")
        env=dict(os.environ,DISPLAY="",WAYLAND_DISPLAY="",WINEDEBUG="-all",
                 WINEPREFIX=str(self.ROOT/".analysis/toolchain/wineprefix"),
                 MSDOS_PATH=r"C:\TC4\BIN",TZ="UTC",LANG="C",LC_ALL="C")
        dos=["/usr/bin/wine-stable",str(self.ROOT/"_reference/ReC98/bin/msdos.exe"),"-e","-x"]
        def run_native(argv,label):
            p=subprocess.run(argv,cwd=self.WORK,env=env,stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,timeout=105)
            log=self.PREFIX+label+".log"
            (self.ROOT/log).write_bytes(p.stdout)
            report["phases"].append(dict(label=label,argv=argv,
                 returncode=p.returncode,log=log,log_sha256=sha(p.stdout)))
            save()
            need(p.returncode==0,label+": "+p.stdout.decode(errors="replace")[-1400:])

        with (self.ROOT/".analysis/borland-wine-writer.lock").open("ab") as lock:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            need(not self.SCRATCH.exists(),"fresh scoped single module original-source native stage")
            self.SCRATCH.mkdir()
            (self.SCRATCH/"driver.py").write_bytes((self.ROOT/self.DRIVER).read_bytes())
            (self.SCRATCH/"config.json").write_bytes((self.ROOT/self.CONFIG).read_bytes())
            (self.SCRATCH/"helper.py").write_bytes((self.ROOT/self.HELPER).read_bytes())
            results=[]
            for n in (1,2):
                folder=self.SCRATCH/f"r{n}"
                folder.mkdir()
                (folder/f'{cfg["stem"]}.cpp').write_bytes(wrapper.replace(b"\n",b"\r\n"))
                os.utime(folder/f'{cfg["stem"]}.cpp',(946684800,946684800))
                run_native(dos+["tcc","-c","-I.","-O","-b-","-3","-Z","-d",
                    "-DGAME=3","-ml","-DBINARY='O'",
                    f"-nprobe/{self.STAGE}/r{n}/",
                    f"probe/{self.STAGE}/r{n}/{cfg['stem']}.cpp"],
                    f"round{n}-{cfg['stem']}-TC4")
                obj=(folder/f'{cfg["stem"]}.obj').read_bytes()
                bound=self.object_scope(cfg,obj,original)
                rsp=self.response(cfg,n)
                (self.SCRATCH/f"r{n}.lnk").write_bytes(rsp)
                run_native(dos+["tlink",f"@probe\\{self.STAGE}\\r{n}.lnk"],
                    f"round{n}-normal-TLINK")
                exe=(self.SCRATCH/f"r{n}.exe").read_bytes()
                native_map=(self.SCRATCH/f"r{n}.map").read_bytes()
                previous=prior["rounds"][n-1]["outputs"]
                need(exe==reference==self.base.checked(previous["exe"]) and
                     self.normalized_map(cfg,native_map,n)==self.base.checked(previous["map"]) and
                     parse_mz(exe).relocations==parse_mz(reference).relocations,
                     "whole original decoded Japanese MAINL source-native EXE and 677 ordered MZ fields")
                vector=dict(obj=obj,exe=exe,map=native_map)
                files={}
                for key,data in vector.items():
                    path=self.PREFIX+f"round{n}-{key}.bin"
                    (self.ROOT/path).write_bytes(data)
                    files[key]=dict(path=path,bytes=len(data),sha256=sha(data))
                report["rounds"].append(dict(round=n,outputs=files,scope=bound,
                    link_response_sha256=sha(rsp),complete_original_decoded_EXE_equal=True))
                save()
                results.append(vector)
                print(f"{cfg['stem']} original first-use C++ round {n}: {cfg['CODE_bytes']} CODE, {cfg['PUBLICs']} functions, full MAINL original-equal",flush=True)
            need(results[0]["exe"]==results[1]["exe"] and
                 payload(results[0]["obj"])==payload(results[1]["obj"]) and
                 literal_fields(results[0]["obj"])==literal_fields(results[1]["obj"]) and
                 public_offsets(results[0]["obj"])==public_offsets(results[1]["obj"]) and
                 self.stable_map(cfg,results[0]["map"],1)==self.stable_map(cfg,results[1]["map"],2) and
                 self.sources(cfg)==(code,wrapper),
                 "two full natural source/native OBJ/EXE/MAP rounds repeat")
        report["complete"]=True
        save()

    def review(self):
        cfg,cfg_hash,prior=self.inputs()
        record,report_sha=self.base.load(self.REPORT)
        source,wrapper=self.sources(cfg)
        original=(self.WORK/cfg["original_object"]).read_bytes()
        target=(self.WORK/"bin/th03/mainl.target.exe").read_bytes()
        need(record["complete"] and record["cold_rebuilt"] is False and
             record["library_rebuilt"] is False and
             record["recompiled_project_objects_per_round"]==1 and
             record["other_project_objects_reused"]==35 and
             record["total_CODE_bytes"]==cfg["CODE_bytes"] and
             record["original_PUBLICs"]==cfg["PUBLICs"] and
             record["original_OMF_FIXUPP_fields"]==cfg["ordered_fixups"] and
             record["whole_project_source_accepted"] is False and
             record["canonical_factory_credit_changed"] is False and
             record["config_sha256"]==cfg_hash and
             record["driver_sha256"]==sha((self.ROOT/self.DRIVER).read_bytes()) and
             record["helper_sha256"]==sha((self.ROOT/self.HELPER).read_bytes()) and
             record["source_sha256"]==sha(source) and
             record["wrapper_sha256"]==sha(wrapper) and
             record["original_object_sha256"]==sha(original) and
             record["parent_report_sha256"]==cfg["parent_report_sha256"] and
             record["original_japanese_exe_sha256"]==sha(target),
             "all real immutable original object/source/writer/parent receipt bindings")
        for name,path in [("driver.py",self.DRIVER),("config.json",self.CONFIG),("helper.py",self.HELPER)]:
            need((self.SCRATCH/name).read_bytes()==(self.ROOT/path).read_bytes(),
                 "retained original source-native writer recipe "+name)
        labels=[f"round{n}-{step}" for n in (1,2) for step in
                (f"{cfg['stem']}-TC4","normal-TLINK")]
        need(len(record["phases"])==4 and [p["label"] for p in record["phases"]]==labels and
             all(p["returncode"]==0 and sha((self.ROOT/p["log"]).read_bytes())==p["log_sha256"]
                 for p in record["phases"]),
             "four original Borland TC4 and TLINK native writer logs")
        pair=[]
        for n,row in enumerate(record["rounds"],1):
            old=prior["rounds"][n-1]["outputs"]
            need(row["round"]==n and
                 row["link_response_sha256"]==sha(self.response(cfg,n)) and
                 (self.SCRATCH/f"r{n}.lnk").read_bytes()==self.response(cfg,n),
                 "one original CODE source slot and normal first-use linker order")
            files={key:self.base.checked(pin) for key,pin in row["outputs"].items()}
            need(set(files)=={"obj","exe","map"} and
                 (self.SCRATCH/f"r{n}/{cfg['stem']}.cpp").read_bytes()==
                    wrapper.replace(b"\n",b"\r\n") and
                 (self.SCRATCH/f"r{n}/{cfg['stem']}.obj").read_bytes()==files["obj"],
                 "literal native object/source file actually passed to compiler and linker")
            check=self.object_scope(cfg,files["obj"],original)
            need(check==row["scope"] and
                 files["exe"]==target==self.base.checked(old["exe"]) and
                 len(files["exe"])==67372 and
                 parse_mz(files["exe"]).relocations==parse_mz(target).relocations and
                 len(parse_mz(files["exe"]).relocations)==677 and
                 self.normalized_map(cfg,files["map"],n)==self.base.checked(old["map"]) and
                 row["complete_original_decoded_EXE_equal"],
                 "complete original Japanese MZ image and all native ordered relocations/MAP")
            pair.append(files)
        need(len(pair)==2 and pair[0]["exe"]==pair[1]["exe"] and
             payload(pair[0]["obj"])==payload(pair[1]["obj"]) and
             literal_fields(pair[0]["obj"])==literal_fields(pair[1]["obj"]) and
             self.stable_map(cfg,pair[0]["map"],1)==self.stable_map(cfg,pair[1]["map"],2),
             "two independent original native source compilation rounds repeat")
        return dict(complete=True,original_module=cfg["stem"],
            complete_original_CODE_bytes=cfg["CODE_bytes"],
            original_public_functions=cfg["PUBLICs"],
            original_ordered_OMF_FIXUPPs=cfg["ordered_fixups"],
            source_Turbo_CPP_rounds=2,
            exact_original_CODE_and_OMF_field_sites=True,
            entire_67372_byte_original_MAINL_EXE_equal=True,
            original_677_ordered_MZ_relocations_equal=True,
            whole_project_source_accepted=False,
            canonical_factory_acceptance=False,
            historical_vendor_RAW_OMF_packet_identity=False,
            source_native_report_SHA256=report_sha)
