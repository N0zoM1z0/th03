#!/usr/bin/env python3
"""Generate TH03 progress from current ledgers without guessed denominators."""

import argparse
import csv
import hashlib
from pathlib import Path
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


MAINL_HEAP_UNIT = "th03-mainl-decoded-heap-manager"
MAINL_HEAP_RETAINED = {
    "ev-th03-mainl-heap-retained-structural": (
        "binary", "cb3379b976fd189e5e419c1d0aa6cec8d8e5821f49268b411f28050645680eb3"),
    "ev-th03-mainl-heap-retained-runtime": (
        "runtime", "c9d3ead4db8db4b311e658350c0c33ad28e027de07802508f94048ce0c89c003"),
}


def mainl_unit_progress(units: list[dict[str, str]]) -> dict[str, int]:
    """MAINL has mixed function/module extents, not an authored-function inventory."""
    rows = [u for u in units if u["artifact"] == "th03-mainl"
            and u["state"] != "excluded"]
    if len({u["id"] for u in rows}) != len(rows):
        raise ValueError("duplicate MAINL unit would inflate the tracked denominator")
    present = [u for u in rows if u["state"] in {"source-present", "structural", "exact"}
               and u["source"]]
    return {
        "total": len(rows),
        "reviewed": sum(u["boundary_state"] in {"reviewed", "shared"} for u in rows),
        "source": len(present),
        "source_bytes": sum(int(u["size"], 0) for u in present),
        "exact": sum(u["state"] == "exact" for u in rows),
    }


def mainl_heap_retained(units: list[dict[str, str]],
                        evidence: list[dict[str, str]]) -> bool:
    """A separate diagnostic annotation; never feeds source or exact counts."""
    heaps = [u for u in units if u["id"] == MAINL_HEAP_UNIT]
    if len(heaps) != 1:
        return False
    heap = heaps[0]
    if (heap["artifact"], heap["segment"], heap["offset"], heap["size"],
            heap["boundary_state"], heap["state"], heap["source"]) != (
            "th03-mainl", "decoded:0000", "0x210a", "628", "reviewed",
            "source-present", "src/mainl/memory/heap.inl"):
        return False
    linked = heap["evidence_ids"].split(";")
    for evidence_id, (kind, digest) in MAINL_HEAP_RETAINED.items():
        matches = [e for e in evidence if e["id"] == evidence_id]
        if evidence_id not in linked or len(matches) != 1:
            return False
        row = matches[0]
        if (row["oracle"], row["artifact"], row["unit_id"], row["extent_start"],
                row["extent_size"], row["evidence_class"], row["result"],
                row["output_sha256"]) != (
                "analysis-bundle", "th03-mainl", MAINL_HEAP_UNIT, "0x210a",
                "628", kind, "pass", digest):
            return False
    return True


def zun_init_standalone_retained(units: list[dict[str, str]]) -> bool:
    """Historical standalone diagnostic only; never feeds any progress count."""
    # Reviewed checkpoint: docs/reconstruction/ZUN_INIT_STANDALONE_FEASIBILITY.md.
    # Completion: .analysis/zun-init-cold-continuation-output-20261021-v01/completion.json
    # SHA256: 4fb3cf03ef57da9ae3da738f0f650da385b546abb3fff35975760d75449f70c8.
    # src/zun/init.asm: 078525c35dfa4b499feb661980733964e16fa5654e8403ee55b0de221e828dc2.
    # Two distinct assembler invocations/materializations; first OBJ retained
    # after date-only registry rejection and linked by reviewed continuation.
    # Raw OMF/COM/MAP equal, no normalization. Original transport exit unknown.
    rows = [u for u in units if u["id"] == "th03-zun-decoded-init"]
    return len(rows) == 1 and all(rows[0].get(key) == value for key, value in {
        "artifact": "th03-zun", "segment": "decoded-COM", "offset": "0x6c4",
        "size": "1390", "boundary_state": "reviewed", "state": "boundary-reviewed",
    }.items())


def zun_driver_hybrid_retained(units: list[dict[str, str]]) -> bool:
    """Historical mixed-source wrapper composition; never feeds progress counts."""
    # Reviewed checkpoint: docs/reconstruction/ZUN_SPRITE16_DRIVER_REVIEW.md.
    # Completion: .analysis/zun-driver-wrapper-composition/zun-init-driver-wrapper-20261021-v01/completion.json
    # SHA256: 07719382277e33709bc9b7c5f15992060a8b4b910ae621e9fc8e98277e452d93.
    # Composition receipt SHA256: 3830777630d3c719765a7ab522a068203e10e452e4e7f6072f140995ed31469b.
    # src/zun/driver_services.inl: d57a52b5dc27a4d548259d7174141b86267734b231a2a0cd55203f1a751507af.
    # src/zun/driver_resident.inl: 258a133463e406dcc7fdf936fc417dc8a502a03d0fb1fe3d605b597af77c7cfa.
    # src/zun/driver_command.inl: 9a49039df84a1c4bde277687b1a35dfd5a9f558a4cd20ff4c46a870b1fa593fc.
    # src/zun/driver_strings.inl: 06effd580a81e6989a7f63fea4bda3cfea6e49940561d149963f3cc157dec01a.
    # src/zun/driver_numbers.inl: de3f42440813c414028dde3130deab8f0e00cdc29efcfa8a69839dfc711683e0.
    # src/zun/driver_graphics.inl: 173dbbb12f3d8e2eb25f417acf5ef194551eff4296592878e5cb15104e271ebc.
    # src/zun/driver_format.inl: 1ee883086ae9045f451e57d9da5ff74ccf6f25980d8228bed2885087cfb94d5e.
    # src/zun/driver.asm: 895751c4e7398a581f10c03ced0462fc1cc404b7fdda4a459cdc4eafc2e56c85.
    # src/zun/driver_data.inl: 656aafabb96b2cab664735bc0dd194a74f01433792704f2e87b94d4370799a2c.
    # src/zun/driver_hardware.inc: 50353aac8704d0c9e53d373f9a9524011b2b7c2798063d90c8152503f2e14ab6.
    # Two independent driver materializations have equal raw OBJ/COM/MAP,
    # no normalization/object reuse. First was not a predeclared pair; second
    # source mtimes were declared from observed first inputs. Not target-exact.
    # Ten maintained sources own the complete 4,224-byte standalone driver:
    # 55 procedures / 2,844 B plus 1,380 B data/layout; candidate only.
    # All ten target differences are inside maintained bodies, not target-exact.
    # Two equal 22,812-byte -2/-4 compositions retain three other payloads
    # and wrapper scaffold. Fourteen wrapper-only observations and wrong-transfer
    # negative pass; no payload execution/native build. Packaging/default stay open.
    if not zun_init_standalone_retained(units):
        return False
    rows = [u for u in units if u["id"] == "th03-zun-decoded-sprite16-driver"]
    return len(rows) == 1 and all(rows[0].get(key) == value for key, value in {
        "artifact": "th03-zun", "segment": "decoded-COM", "offset": "0x33a2",
        "size": "4224", "boundary_state": "reviewed", "state": "boundary-reviewed",
    }.items())


def mainl_cutscene_source_pending(units: list[dict[str, str]]) -> bool:
    """Annotation only: a maintained owner does not promote source/exact counts."""
    rows = [u for u in units if u["id"] == "th03-mainl-decoded-cutscene"]
    return (len(rows) == 1 and all(rows[0].get(k) == v for k, v in {
        "artifact": "th03-mainl", "segment": "decoded:095F", "offset": "0xb3e",
        "size": "3195", "boundary_state": "reviewed", "state": "boundary-reviewed",
        "source": "",
    }.items()) and all((ROOT / p).is_file() for p in (
        "src/mainl/cutscene.cpp", "src/mainl/cutscene/cutscene.hpp",
        "src/mainl/cutscene/script.inl", "src/mainl/cutscene/egc_start_copy.inl",
    )))


def mainl_regist_source_pending(units):
    """Pending source files annotate progress without acceptance credit."""
    scopes = {"regist": ("0x189e", "2720"), "scoredat": ("0x17b9", "229")}
    for name, (offset, size) in scopes.items():
        rows = [u for u in units if u["id"] == "th03-mainl-decoded-" + name]
        if len(rows) != 1 or any(rows[0].get(k) != v for k, v in {
            "artifact": "th03-mainl", "segment": "decoded:095F", "offset": offset,
            "size": size, "boundary_state": "reviewed", "state": "boundary-reviewed", "source": "",
        }.items()):
            return False
    return all((ROOT / p).is_file() for p in ('src/mainl/regist.cpp', 'src/mainl/scoredat.cpp', 'src/mainl/hiscore/regist.hpp', 'src/mainl/hiscore/scoredat.hpp', 'src/mainl/hiscore/score_load.inl', 'src/mainl/hiscore/score_save.inl', 'src/mainl/hiscore/scorecry.hpp', 'src/mainl/hiscore/regi.h', 'src/mainl/hiscore/regist_text.hpp'))


MAINL_CUTSCENE_SOURCE_EVIDENCE = {
    "ev-th03-mainl-cutscene-source-compiler": "compiler",
    "ev-th03-mainl-cutscene-source-runtime": "runtime",
    "ev-th03-mainl-cutscene-source-reproducible": "reproducibility",
}
MAINL_CUTSCENE_SOURCE_RECEIPT = "7f68b341f72bff5814593ca4291043ab9c22b3e3ef58f27517d4af0b0a94c82b"

def mainl_cutscene_hybrid_source(units, evidence):
    rows = [u for u in units if u["id"] == "th03-mainl-decoded-cutscene"]
    if len(rows) != 1 or any(rows[0].get(k) != v for k, v in {
        "artifact": "th03-mainl", "segment": "decoded:095F", "offset": "0xb3e",
        "size": "3195", "boundary_state": "reviewed", "state": "source-present",
        "source": "src/mainl/cutscene.cpp",
    }.items()):
        return False
    linked = rows[0].get("evidence_ids", "").split(";")
    for name, kind in MAINL_CUTSCENE_SOURCE_EVIDENCE.items():
        records = [e for e in evidence if e["id"] == name]
        if name not in linked or len(records) != 1 or any(records[0].get(k) != v for k, v in {
            "artifact": "th03-mainl", "unit_id": rows[0]["id"], "oracle": "analysis-bundle",
            "extent_start": "0xb3e", "extent_size": "3195", "evidence_class": kind,
            "result": "pass", "output_sha256": MAINL_CUTSCENE_SOURCE_RECEIPT,
        }.items()):
            return False
    return True


MAINL_REGIST_SOURCE_RECEIPT = "5927d4c368c38e5871a641155bece6b47ff6b54ca54ce0a416a7970622963be7"
MAINL_REGIST_SOURCE_EVIDENCE = {unit: {
    "ev-th03-mainl-" + unit + "-source-compiler": "compiler",
    "ev-th03-mainl-" + unit + "-source-runtime": "runtime",
    "ev-th03-mainl-" + unit + "-source-reproducible": "reproducibility",
} for unit in ("regist", "scoredat")}

def mainl_regist_hybrid_source(units, evidence):
    for unit, offset, size in (("regist", "0x189e", "2720"), ("scoredat", "0x17b9", "229")):
        rows = [u for u in units if u["id"] == "th03-mainl-decoded-" + unit]
        if len(rows) != 1 or any(rows[0].get(k) != v for k, v in {
            "artifact": "th03-mainl", "segment": "decoded:095F", "offset": offset,
            "size": size, "boundary_state": "reviewed", "state": "source-present",
            "source": "src/mainl/" + unit + ".cpp",
        }.items()):
            return False
        linked = rows[0].get("evidence_ids", "").split(";")
        for name, kind in MAINL_REGIST_SOURCE_EVIDENCE[unit].items():
            records = [e for e in evidence if e["id"] == name]
            if name not in linked or len(records) != 1 or any(records[0].get(k) != v for k, v in {
                "artifact": "th03-mainl", "unit_id": rows[0]["id"], "oracle": "analysis-bundle",
                "extent_start": offset, "extent_size": size, "evidence_class": kind,
                "result": "pass", "output_sha256": MAINL_REGIST_SOURCE_RECEIPT,
            }.items()):
                return False
    return True


MAINL_PI_COMPOSITION_RECEIPT = "ee68c2cd2d34f3efb87310c09521133f184168a25d177162df43995c6dc610ee"
def mainl_pi_composed(units, evidence):
    for unit, offset, size in (("cutscene","0xb3e","3195"),("scoredat","0x17b9","229"),("regist","0x189e","2720")):
        uid="th03-mainl-decoded-"+unit; eid="ev-th03-mainl-"+unit+"-pi-composition-raw"
        rows=[u for u in units if u["id"]==uid]
        if len(rows)!=1 or rows[0].get("state")!="source-present" or rows[0].get("source")!="src/mainl/"+unit+".cpp" or eid not in rows[0].get("evidence_ids", "").split(";"):
            return False
        records=[e for e in evidence if e["id"]==eid]
        if len(records)!=1 or any(records[0].get(k)!=v for k,v in {
            "artifact":"th03-mainl","unit_id":uid,"oracle":"analysis-bundle","extent_start":offset,
            "extent_size":size,"evidence_class":"binary","result":"pass","output_sha256":MAINL_PI_COMPOSITION_RECEIPT,
        }.items()):
            return False
    return True


MAINL_GRAPHICS_PRODUCER_PINS = {'src/mainl/formats/cdg_effects.cpp': '5e3be578cc77c6a7b9de786b069266b32fe54b7f5fcf1884f2aabbc13e4ef024', 'config/th03_mainl_graphics_producer.json': '805154cfcb4121e3404c9b6b8a51a61532b9c998602e8d93e835cb40e7ead43a'}
def mainl_graphics_producer_pending(root=None):
    """Compiler-only annotation; never feeds a ledger count or exact acceptance."""
    root = ROOT if root is None else root
    return all((root / path).is_file() and
               hashlib.sha256((root / path).read_bytes()).hexdigest() == digest
               for path, digest in MAINL_GRAPHICS_PRODUCER_PINS.items())


MAINL_GRAPHICS_LINK_PINS = {'src/mainl/formats/cdg_effects.cpp': '5e3be578cc77c6a7b9de786b069266b32fe54b7f5fcf1884f2aabbc13e4ef024', 'config/th03_mainl_graphics_link.json': '309d695609b2a13a1e3cbf70e1071895d311a68cf7378f5d0ba82b80de7f600f', 'scripts/lib/mainl_graphics_source.py': 'd5ab687731d0648827a75ece94eff739b205f6963ebf896802dfba82dc5c6ddb', 'scripts/lib/mainl_graphics_link.py': 'e664c5c49c5c690e795103bd4b5df658075330e8f463e9721e5f0d6f938a199d'}
def mainl_graphics_linked(root=None):
    """Retained opt-in link diagnostic, not source or exact acceptance."""
    root = ROOT if root is None else root
    return all((root / path).is_file() and
               hashlib.sha256((root / path).read_bytes()).hexdigest() == digest
               for path, digest in MAINL_GRAPHICS_LINK_PINS.items())


MAINL_STAFF_PROOF_SHA = 'ba7de2dedab11e959ab867f0ffcfb7ed008109db4c45cbf4e3b80ca328887b4e'
MAINL_STAFF_SOURCE_UNITS = {'th03-mainl-decoded-staff-unput': {'source': 'src/mainl/formats/cdg_effects.cpp', 'size': '123', 'evidence': ['ev-th03-mainl-decoded-staff-unput-maintained-compiler', 'ev-th03-mainl-decoded-staff-unput-maintained-runtime', 'ev-th03-mainl-decoded-staff-unput-maintained-reproducibility']}, 'th03-mainl-decoded-snow-cluster': {'source': 'src/mainl/formats/cdg_effects.cpp', 'size': '464', 'evidence': ['ev-th03-mainl-decoded-snow-cluster-maintained-compiler', 'ev-th03-mainl-decoded-snow-cluster-maintained-runtime', 'ev-th03-mainl-decoded-snow-cluster-maintained-reproducibility']}, 'th03-mainl-decoded-staff-dissolve': {'source': 'src/mainl/formats/cdg_effects.cpp', 'size': '211', 'evidence': ['ev-th03-mainl-decoded-staff-dissolve-maintained-compiler', 'ev-th03-mainl-decoded-staff-dissolve-maintained-runtime', 'ev-th03-mainl-decoded-staff-dissolve-maintained-reproducibility']}, 'th03-mainl-decoded-staff-entrance': {'source': 'src/mainl/staff/staff.asm', 'size': '211', 'evidence': ['ev-th03-mainl-decoded-staff-entrance-maintained-compiler', 'ev-th03-mainl-decoded-staff-entrance-maintained-runtime', 'ev-th03-mainl-decoded-staff-entrance-maintained-reproducibility']}, 'th03-mainl-decoded-staff-leave': {'source': 'src/mainl/staff/staff.asm', 'size': '183', 'evidence': ['ev-th03-mainl-decoded-staff-leave-maintained-compiler', 'ev-th03-mainl-decoded-staff-leave-maintained-runtime', 'ev-th03-mainl-decoded-staff-leave-maintained-reproducibility']}, 'th03-mainl-decoded-staff-gallery': {'source': 'src/mainl/staff/staff.asm', 'size': '52', 'evidence': ['ev-th03-mainl-decoded-staff-gallery-maintained-compiler', 'ev-th03-mainl-decoded-staff-gallery-maintained-runtime', 'ev-th03-mainl-decoded-staff-gallery-maintained-reproducibility']}, 'th03-mainl-decoded-staff-normal': {'source': 'src/mainl/staff/staff.asm', 'size': '229', 'evidence': ['ev-th03-mainl-decoded-staff-normal-maintained-compiler', 'ev-th03-mainl-decoded-staff-normal-maintained-runtime', 'ev-th03-mainl-decoded-staff-normal-maintained-reproducibility']}, 'th03-mainl-decoded-staff-double': {'source': 'src/mainl/staff/staff.asm', 'size': '358', 'evidence': ['ev-th03-mainl-decoded-staff-double-maintained-compiler', 'ev-th03-mainl-decoded-staff-double-maintained-runtime', 'ev-th03-mainl-decoded-staff-double-maintained-reproducibility']}, 'th03-mainl-decoded-staff-hold': {'source': 'src/mainl/staff/staff.asm', 'size': '139', 'evidence': ['ev-th03-mainl-decoded-staff-hold-maintained-compiler', 'ev-th03-mainl-decoded-staff-hold-maintained-runtime', 'ev-th03-mainl-decoded-staff-hold-maintained-reproducibility']}, 'th03-mainl-decoded-staff-verdict': {'source': 'src/mainl/staff/staff.asm', 'size': '389', 'evidence': ['ev-th03-mainl-decoded-staff-verdict-maintained-compiler', 'ev-th03-mainl-decoded-staff-verdict-maintained-runtime', 'ev-th03-mainl-decoded-staff-verdict-maintained-reproducibility']}, 'th03-mainl-decoded-staff-staff': {'source': 'src/mainl/staff/staff.asm', 'size': '980', 'evidence': ['ev-th03-mainl-decoded-staff-staff-maintained-compiler', 'ev-th03-mainl-decoded-staff-staff-maintained-runtime', 'ev-th03-mainl-decoded-staff-staff-maintained-reproducibility']}}
def mainl_staff_source_proven(units, evidence):
    by_unit = {r["id"]: r for r in units}
    by_evidence = {r["id"]: r for r in evidence}
    for name, expected in MAINL_STAFF_SOURCE_UNITS.items():
        u = by_unit.get(name, {})
        if (u.get("state"), u.get("source"), u.get("size")) != ("source-present", expected["source"], expected["size"]):
            return False
        for eid, kind in zip(expected["evidence"], ("compiler", "runtime", "reproducibility")):
            e = by_evidence.get(eid, {})
            if eid not in u.get("evidence_ids", "").split(";") or any(e.get(k) != v for k, v in {
                "unit_id": name, "artifact": "th03-mainl", "result": "pass",
                "extent_size": expected["size"], "evidence_class": kind,
                "output_sha256": MAINL_STAFF_PROOF_SHA}.items()):
                return False
    return True


MAINL_ROOT_PROOF_SHA = '332c8c632fb6f51f8aaea09378ce96c0f8225c9bf5b76127971c6a2bd5cd9f61'
MAINL_ROOT_SOURCE_EVIDENCE = ['ev-th03-mainl-root-source-compiler', 'ev-th03-mainl-root-source-runtime', 'ev-th03-mainl-root-source-reproducibility']
def mainl_root_source_proven(units, evidence):
    roots = [u for u in units if u["id"] == "th03-mainl-decoded-root"]
    if len(roots) != 1:
        return False
    u = roots[0]
    if (u.get("state"), u.get("source"), u.get("size")) != ("source-present", "src/mainl/root/root.asm", "2488"):
        return False
    by = {e["id"]: e for e in evidence}
    for eid, kind in zip(MAINL_ROOT_SOURCE_EVIDENCE, ("compiler", "runtime", "reproducibility")):
        e = by.get(eid, {})
        if eid not in u.get("evidence_ids", "").split(";") or any(e.get(k) != v for k, v in {
            "unit_id": u["id"], "artifact": "th03-mainl", "result": "pass",
            "extent_size": "2488", "evidence_class": kind,
            "output_sha256": MAINL_ROOT_PROOF_SHA}.items()):
            return False
    return True


MAINL_PI_DECODER_PROOF_SHA = '9017ab9b5a8f85debdf0c73553acd817505ceb8977fdd8bd531a11364489df9e'
MAINL_PI_DECODER_EVIDENCE = ['ev-th03-mainl-pi-decoder-source-compiler', 'ev-th03-mainl-pi-decoder-source-runtime', 'ev-th03-mainl-pi-decoder-source-reproducibility']
def mainl_pi_decoder_source_proven(units, evidence):
    found = [u for u in units if u["id"] == "th03-mainl-decoded-pi-decoder-load"]
    if len(found) != 1:
        return False
    u = found[0]
    if (u.get("state"), u.get("source"), u.get("size")) != ("source-present", "src/mainl/formats/pi_decode.asm", "1524"):
        return False
    by = {e["id"]: e for e in evidence}
    for eid, kind in zip(MAINL_PI_DECODER_EVIDENCE, ("compiler", "runtime", "reproducibility")):
        e = by.get(eid, {})
        if eid not in u.get("evidence_ids", "").split(";") or any(e.get(k) != v for k, v in {
            "unit_id": u["id"], "artifact": "th03-mainl", "result": "pass", "extent_size": "1524",
            "evidence_class": kind, "output_sha256": MAINL_PI_DECODER_PROOF_SHA}.items()):
            return False
    return True


MAINL_RESOURCES_PROOF_SHA = '6f8141634832721e4140f57e03715ad181abe25f1554050115aeeb3f36fcd15e'
MAINL_RESOURCES_SOURCE_UNITS = {'th03-mainl-decoded-draw-gaiji': {'source': 'src/mainl/resources/graph_gaiji_putc.asm', 'size': '148', 'evidence': ['ev-th03-mainl-decoded-draw-gaiji-resources-source-compiler', 'ev-th03-mainl-decoded-draw-gaiji-resources-source-runtime', 'ev-th03-mainl-decoded-draw-gaiji-resources-source-reproducibility']}, 'th03-mainl-decoded-draw-pack': {'source': 'src/mainl/resources/graph_pack_put_8.asm', 'size': '212', 'evidence': ['ev-th03-mainl-decoded-draw-pack-resources-source-compiler', 'ev-th03-mainl-decoded-draw-pack-resources-source-runtime', 'ev-th03-mainl-decoded-draw-pack-resources-source-reproducibility']}, 'th03-mainl-decoded-draw-scroll': {'source': 'src/mainl/resources/graph_scrollup.asm', 'size': '88', 'evidence': ['ev-th03-mainl-decoded-draw-scroll-resources-source-compiler', 'ev-th03-mainl-decoded-draw-scroll-resources-source-runtime', 'ev-th03-mainl-decoded-draw-scroll-resources-source-reproducibility']}, 'th03-mainl-decoded-draw-show': {'source': 'src/mainl/resources/graph_show.asm', 'size': '6', 'evidence': ['ev-th03-mainl-decoded-draw-show-resources-source-compiler', 'ev-th03-mainl-decoded-draw-show-resources-source-runtime', 'ev-th03-mainl-decoded-draw-show-resources-source-reproducibility']}, 'th03-mainl-decoded-draw-noclip': {'source': 'src/mainl/resources/graph_pack_put_8_noclip.asm', 'size': '202', 'evidence': ['ev-th03-mainl-decoded-draw-noclip-resources-source-compiler', 'ev-th03-mainl-decoded-draw-noclip-resources-source-runtime', 'ev-th03-mainl-decoded-draw-noclip-resources-source-reproducibility']}, 'th03-mainl-decoded-draw-table': {'source': 'src/mainl/resources/rottbl.asm', 'size': '1024', 'evidence': ['ev-th03-mainl-decoded-draw-table-resources-source-compiler', 'ev-th03-mainl-decoded-draw-table-resources-source-runtime', 'ev-th03-mainl-decoded-draw-table-resources-source-reproducibility']}, 'th03-mainl-decoded-bfnt-library': {'source': 'src/mainl/resources/bfnt_entry_pat.asm', 'size': '512', 'evidence': ['ev-th03-mainl-decoded-bfnt-library-resources-source-compiler', 'ev-th03-mainl-decoded-bfnt-library-resources-source-runtime', 'ev-th03-mainl-decoded-bfnt-library-resources-source-reproducibility']}, 'th03-mainl-decoded-super-library': {'source': 'src/mainl/resources/super_free.asm', 'size': '1008', 'evidence': ['ev-th03-mainl-decoded-super-library-resources-source-compiler', 'ev-th03-mainl-decoded-super-library-resources-source-runtime', 'ev-th03-mainl-decoded-super-library-resources-source-reproducibility']}, 'th03-mainl-decoded-dos-close': {'source': 'src/mainl/resources/dos_close.asm', 'size': '22', 'evidence': ['ev-th03-mainl-decoded-dos-close-resources-source-compiler', 'ev-th03-mainl-decoded-dos-close-resources-source-runtime', 'ev-th03-mainl-decoded-dos-close-resources-source-reproducibility']}, 'th03-mainl-decoded-gdc-outpw': {'source': 'src/mainl/resources/gdc_outpw.asm', 'size': '11', 'evidence': ['ev-th03-mainl-decoded-gdc-outpw-resources-source-compiler', 'ev-th03-mainl-decoded-gdc-outpw-resources-source-runtime', 'ev-th03-mainl-decoded-gdc-outpw-resources-source-reproducibility']}, 'th03-mainl-decoded-pi-decoder-free': {'source': 'src/mainl/resources/graph_pi_free.asm', 'size': '76', 'evidence': ['ev-th03-mainl-decoded-pi-decoder-free-resources-source-compiler', 'ev-th03-mainl-decoded-pi-decoder-free-resources-source-runtime', 'ev-th03-mainl-decoded-pi-decoder-free-resources-source-reproducibility']}, 'th03-mainl-decoded-stack-memory': {'source': 'src/mainl/resources/smem_release.asm', 'size': '76', 'evidence': ['ev-th03-mainl-decoded-stack-memory-resources-source-compiler', 'ev-th03-mainl-decoded-stack-memory-resources-source-runtime', 'ev-th03-mainl-decoded-stack-memory-resources-source-reproducibility']}, 'th03-mainl-decoded-palette-bfnt': {'source': 'src/mainl/resources/bfnt_palette_set.asm', 'size': '64', 'evidence': ['ev-th03-mainl-decoded-palette-bfnt-resources-source-compiler', 'ev-th03-mainl-decoded-palette-bfnt-resources-source-runtime', 'ev-th03-mainl-decoded-palette-bfnt-resources-source-reproducibility']}, 'th03-mainl-decoded-buffer-dos-open': {'source': 'src/mainl/resources/dos_ropen.asm', 'size': '26', 'evidence': ['ev-th03-mainl-decoded-buffer-dos-open-resources-source-compiler', 'ev-th03-mainl-decoded-buffer-dos-open-resources-source-runtime', 'ev-th03-mainl-decoded-buffer-dos-open-resources-source-reproducibility']}}
def mainl_resources_source_proven(units, evidence):
    by_unit = {r["id"]: r for r in units}
    by_evidence = {r["id"]: r for r in evidence}
    for name, expected in MAINL_RESOURCES_SOURCE_UNITS.items():
        u = by_unit.get(name, {})
        if (u.get("state"), u.get("source"), u.get("size")) != ("source-present", expected["source"], expected["size"]):
            return False
        for eid, kind in zip(expected["evidence"], ("compiler", "runtime", "reproducibility")):
            e = by_evidence.get(eid, {})
            if eid not in u.get("evidence_ids", "").split(";") or any(e.get(k) != v for k, v in {
                "unit_id": name, "artifact": "th03-mainl", "result": "pass",
                "extent_size": expected["size"], "evidence_class": kind,
                "output_sha256": MAINL_RESOURCES_PROOF_SHA}.items()):
                return False
    return True

MAINL_ARCHIVE_IO_PROOF_SHA = 'f7684a4fc3d222c07ad7ff00354358a2139109341df796c813d901a1f60f1140'
MAINL_ARCHIVE_IO_SOURCE_UNITS = {'th03-mainl-decoded-file-library': {'source': 'src/mainl/archive_io/file_append.asm', 'size': '786', 'evidence': ['ev-th03-mainl-decoded-file-library-archive-source-compiler', 'ev-th03-mainl-decoded-file-library-archive-source-runtime', 'ev-th03-mainl-decoded-file-library-archive-source-reproducibility']}, 'th03-mainl-decoded-file-dos-helpers': {'source': 'src/mainl/archive_io/dos_axdx.asm', 'size': '80', 'evidence': ['ev-th03-mainl-decoded-file-dos-helpers-archive-source-compiler', 'ev-th03-mainl-decoded-file-dos-helpers-archive-source-runtime', 'ev-th03-mainl-decoded-file-dos-helpers-archive-source-reproducibility']}, 'th03-mainl-decoded-pfint21': {'source': 'src/mainl/archive_io/pfint21.asm', 'size': '605', 'evidence': ['ev-th03-mainl-decoded-pfint21-archive-source-compiler', 'ev-th03-mainl-decoded-pfint21-archive-source-runtime', 'ev-th03-mainl-decoded-pfint21-archive-source-reproducibility']}, 'th03-mainl-decoded-pfopen': {'source': 'src/mainl/archive_io/pfopen.asm', 'size': '281', 'evidence': ['ev-th03-mainl-decoded-pfopen-archive-source-compiler', 'ev-th03-mainl-decoded-pfopen-archive-source-runtime', 'ev-th03-mainl-decoded-pfopen-archive-source-reproducibility']}, 'th03-mainl-decoded-pfread-close': {'source': 'src/mainl/archive_io/pfclose.asm', 'size': '26', 'evidence': ['ev-th03-mainl-decoded-pfread-close-archive-source-compiler', 'ev-th03-mainl-decoded-pfread-close-archive-source-runtime', 'ev-th03-mainl-decoded-pfread-close-archive-source-reproducibility']}, 'th03-mainl-decoded-pfread-getc': {'source': 'src/mainl/archive_io/pfgetc.asm', 'size': '15', 'evidence': ['ev-th03-mainl-decoded-pfread-getc-archive-source-compiler', 'ev-th03-mainl-decoded-pfread-getc-archive-source-runtime', 'ev-th03-mainl-decoded-pfread-getc-archive-source-reproducibility']}, 'th03-mainl-decoded-pfread-len': {'source': 'src/mainl/archive_io/pfgetc.asm', 'size': '78', 'evidence': ['ev-th03-mainl-decoded-pfread-len-archive-source-compiler', 'ev-th03-mainl-decoded-pfread-len-archive-source-runtime', 'ev-th03-mainl-decoded-pfread-len-archive-source-reproducibility']}, 'th03-mainl-decoded-pfread-plain': {'source': 'src/mainl/archive_io/pfgetc.asm', 'size': '68', 'evidence': ['ev-th03-mainl-decoded-pfread-plain-archive-source-compiler', 'ev-th03-mainl-decoded-pfread-plain-archive-source-runtime', 'ev-th03-mainl-decoded-pfread-plain-archive-source-reproducibility']}, 'th03-mainl-decoded-pfread-keyed': {'source': 'src/mainl/archive_io/pfgetc.asm', 'size': '13', 'evidence': ['ev-th03-mainl-decoded-pfread-keyed-archive-source-compiler', 'ev-th03-mainl-decoded-pfread-keyed-archive-source-runtime', 'ev-th03-mainl-decoded-pfread-keyed-archive-source-reproducibility']}, 'th03-mainl-decoded-pfread-read': {'source': 'src/mainl/archive_io/pfread.asm', 'size': '46', 'evidence': ['ev-th03-mainl-decoded-pfread-read-archive-source-compiler', 'ev-th03-mainl-decoded-pfread-read-archive-source-runtime', 'ev-th03-mainl-decoded-pfread-read-archive-source-reproducibility']}, 'th03-mainl-decoded-pfread-rewind': {'source': 'src/mainl/archive_io/pfrewind.asm', 'size': '59', 'evidence': ['ev-th03-mainl-decoded-pfread-rewind-archive-source-compiler', 'ev-th03-mainl-decoded-pfread-rewind-archive-source-runtime', 'ev-th03-mainl-decoded-pfread-rewind-archive-source-reproducibility']}, 'th03-mainl-decoded-pfread-seek': {'source': 'src/mainl/archive_io/pfseek.asm', 'size': '48', 'evidence': ['ev-th03-mainl-decoded-pfread-seek-archive-source-compiler', 'ev-th03-mainl-decoded-pfread-seek-archive-source-runtime', 'ev-th03-mainl-decoded-pfread-seek-archive-source-reproducibility']}, 'th03-mainl-decoded-buffer-close': {'source': 'src/mainl/archive_io/bcloser.asm', 'size': '24', 'evidence': ['ev-th03-mainl-decoded-buffer-close-archive-source-compiler', 'ev-th03-mainl-decoded-buffer-close-archive-source-runtime', 'ev-th03-mainl-decoded-buffer-close-archive-source-reproducibility']}, 'th03-mainl-decoded-buffer-fill': {'source': 'src/mainl/archive_io/bfill.asm', 'size': '59', 'evidence': ['ev-th03-mainl-decoded-buffer-fill-archive-source-compiler', 'ev-th03-mainl-decoded-buffer-fill-archive-source-runtime', 'ev-th03-mainl-decoded-buffer-fill-archive-source-reproducibility']}, 'th03-mainl-decoded-buffer-getc': {'source': 'src/mainl/archive_io/bgetc.asm', 'size': '48', 'evidence': ['ev-th03-mainl-decoded-buffer-getc-archive-source-compiler', 'ev-th03-mainl-decoded-buffer-getc-archive-source-runtime', 'ev-th03-mainl-decoded-buffer-getc-archive-source-reproducibility']}, 'th03-mainl-decoded-buffer-open': {'source': 'src/mainl/archive_io/bopenr.asm', 'size': '83', 'evidence': ['ev-th03-mainl-decoded-buffer-open-archive-source-compiler', 'ev-th03-mainl-decoded-buffer-open-archive-source-runtime', 'ev-th03-mainl-decoded-buffer-open-archive-source-reproducibility']}, 'th03-mainl-decoded-buffer-read': {'source': 'src/mainl/archive_io/bread.asm', 'size': '48', 'evidence': ['ev-th03-mainl-decoded-buffer-read-archive-source-compiler', 'ev-th03-mainl-decoded-buffer-read-archive-source-runtime', 'ev-th03-mainl-decoded-buffer-read-archive-source-reproducibility']}, 'th03-mainl-decoded-buffer-seek': {'source': 'src/mainl/archive_io/bseek.asm', 'size': '65', 'evidence': ['ev-th03-mainl-decoded-buffer-seek-archive-source-compiler', 'ev-th03-mainl-decoded-buffer-seek-archive-source-runtime', 'ev-th03-mainl-decoded-buffer-seek-archive-source-reproducibility']}, 'th03-mainl-decoded-buffer-seek-base': {'source': 'src/mainl/archive_io/bseek_.asm', 'size': '47', 'evidence': ['ev-th03-mainl-decoded-buffer-seek-base-archive-source-compiler', 'ev-th03-mainl-decoded-buffer-seek-base-archive-source-runtime', 'ev-th03-mainl-decoded-buffer-seek-base-archive-source-reproducibility']}}
def mainl_archive_io_source_proven(units, evidence):
    by_unit = {r["id"]: r for r in units}
    by_evidence = {r["id"]: r for r in evidence}
    for name, expected in MAINL_ARCHIVE_IO_SOURCE_UNITS.items():
        u = by_unit.get(name, {})
        if (u.get("state"), u.get("source"), u.get("size")) != ("source-present", expected["source"], expected["size"]):
            return False
        for eid, kind in zip(expected["evidence"], ("compiler", "runtime", "reproducibility")):
            e = by_evidence.get(eid, {})
            if eid not in u.get("evidence_ids", "").split(";") or any(e.get(k) != v for k, v in {
                "unit_id": name, "artifact": "th03-mainl", "result": "pass",
                "extent_size": expected["size"], "evidence_class": kind,
                "output_sha256": MAINL_ARCHIVE_IO_PROOF_SHA}.items()):
                return False
    return True

MAINL_DISPLAY_HARDWARE_PROOF_SHA = 'f9fdfc7a3ee6ab751e1c21041fd66bf3c31d1789cdc272f46cf4d61247e93812'
MAINL_DISPLAY_HARDWARE_SOURCE_UNITS = {'th03-mainl-decoded-palette-black-fades': {'source': 'src/mainl/display_hardware/palette_black_in.asm', 'size': '130', 'evidence': ['ev-th03-mainl-decoded-palette-black-fades-display-source-compiler', 'ev-th03-mainl-decoded-palette-black-fades-display-source-runtime', 'ev-th03-mainl-decoded-palette-black-fades-display-source-reproducibility']}, 'th03-mainl-decoded-palette-show': {'source': 'src/mainl/display_hardware/palette_show.asm', 'size': '266', 'evidence': ['ev-th03-mainl-decoded-palette-show-display-source-compiler', 'ev-th03-mainl-decoded-palette-show-display-source-runtime', 'ev-th03-mainl-decoded-palette-show-display-source-reproducibility']}, 'th03-mainl-decoded-palette-rgb': {'source': 'src/mainl/display_hardware/palette_entry_rgb.asm', 'size': '66', 'evidence': ['ev-th03-mainl-decoded-palette-rgb-display-source-compiler', 'ev-th03-mainl-decoded-palette-rgb-display-source-runtime', 'ev-th03-mainl-decoded-palette-rgb-display-source-reproducibility']}, 'th03-mainl-decoded-palette-wait-white-fades': {'source': 'src/mainl/display_hardware/vsync_wait.asm', 'size': '166', 'evidence': ['ev-th03-mainl-decoded-palette-wait-white-fades-display-source-compiler', 'ev-th03-mainl-decoded-palette-wait-white-fades-display-source-runtime', 'ev-th03-mainl-decoded-palette-wait-white-fades-display-source-reproducibility']}, 'th03-mainl-decoded-vsync-library': {'source': 'src/mainl/display_hardware/vsync.asm', 'size': '250', 'evidence': ['ev-th03-mainl-decoded-vsync-library-display-source-compiler', 'ev-th03-mainl-decoded-vsync-library-display-source-runtime', 'ev-th03-mainl-decoded-vsync-library-display-source-reproducibility']}, 'th03-mainl-decoded-dos-setvect': {'source': 'src/mainl/display_hardware/dos_setvect.asm', 'size': '32', 'evidence': ['ev-th03-mainl-decoded-dos-setvect-display-source-compiler', 'ev-th03-mainl-decoded-dos-setvect-display-source-runtime', 'ev-th03-mainl-decoded-dos-setvect-display-source-reproducibility']}, 'th03-mainl-decoded-graph-extmode': {'source': 'src/mainl/display_hardware/graph_extmode.asm', 'size': '86', 'evidence': ['ev-th03-mainl-decoded-graph-extmode-display-source-compiler', 'ev-th03-mainl-decoded-graph-extmode-display-source-runtime', 'ev-th03-mainl-decoded-graph-extmode-display-source-reproducibility']}, 'th03-mainl-decoded-egc-library': {'source': 'src/mainl/display_hardware/egc.asm', 'size': '98', 'evidence': ['ev-th03-mainl-decoded-egc-library-display-source-compiler', 'ev-th03-mainl-decoded-egc-library-display-source-runtime', 'ev-th03-mainl-decoded-egc-library-display-source-reproducibility']}, 'th03-mainl-decoded-grcg-box-library': {'source': 'src/mainl/display_hardware/grcg_boxfill.asm', 'size': '366', 'evidence': ['ev-th03-mainl-decoded-grcg-box-library-display-source-compiler', 'ev-th03-mainl-decoded-grcg-box-library-display-source-runtime', 'ev-th03-mainl-decoded-grcg-box-library-display-source-reproducibility']}, 'th03-mainl-decoded-gaiji-backup': {'source': 'src/mainl/display_hardware/gaiji_backup.asm', 'size': '64', 'evidence': ['ev-th03-mainl-decoded-gaiji-backup-display-source-compiler', 'ev-th03-mainl-decoded-gaiji-backup-display-source-runtime', 'ev-th03-mainl-decoded-gaiji-backup-display-source-reproducibility']}, 'th03-mainl-decoded-gaiji-load': {'source': 'src/mainl/display_hardware/gaiji_entry_bfnt.asm', 'size': '150', 'evidence': ['ev-th03-mainl-decoded-gaiji-load-display-source-compiler', 'ev-th03-mainl-decoded-gaiji-load-display-source-runtime', 'ev-th03-mainl-decoded-gaiji-load-display-source-reproducibility']}, 'th03-mainl-decoded-gaiji-read': {'source': 'src/mainl/display_hardware/gaiji_read.asm', 'size': '108', 'evidence': ['ev-th03-mainl-decoded-gaiji-read-display-source-compiler', 'ev-th03-mainl-decoded-gaiji-read-display-source-runtime', 'ev-th03-mainl-decoded-gaiji-read-display-source-reproducibility']}, 'th03-mainl-decoded-gaiji-write': {'source': 'src/mainl/display_hardware/gaiji_write.asm', 'size': '112', 'evidence': ['ev-th03-mainl-decoded-gaiji-write-display-source-compiler', 'ev-th03-mainl-decoded-gaiji-write-display-source-runtime', 'ev-th03-mainl-decoded-gaiji-write-display-source-reproducibility']}, 'th03-mainl-decoded-screen-mode': {'source': 'src/mainl/display_hardware/graph_400line.asm', 'size': '78', 'evidence': ['ev-th03-mainl-decoded-screen-mode-display-source-compiler', 'ev-th03-mainl-decoded-screen-mode-display-source-runtime', 'ev-th03-mainl-decoded-screen-mode-display-source-reproducibility']}, 'th03-mainl-decoded-screen-clear': {'source': 'src/mainl/display_hardware/graph_clear.asm', 'size': '36', 'evidence': ['ev-th03-mainl-decoded-screen-clear-display-source-compiler', 'ev-th03-mainl-decoded-screen-clear-display-source-runtime', 'ev-th03-mainl-decoded-screen-clear-display-source-reproducibility']}, 'th03-mainl-decoded-screen-copy': {'source': 'src/mainl/display_hardware/graph_copy_page.asm', 'size': '108', 'evidence': ['ev-th03-mainl-decoded-screen-copy-display-source-compiler', 'ev-th03-mainl-decoded-screen-copy-display-source-runtime', 'ev-th03-mainl-decoded-screen-copy-display-source-reproducibility']}}
def mainl_display_hardware_source_proven(units, evidence):
    by_unit = {r["id"]: r for r in units}
    by_evidence = {r["id"]: r for r in evidence}
    for name, expected in MAINL_DISPLAY_HARDWARE_SOURCE_UNITS.items():
        u = by_unit.get(name, {})
        if (u.get("state"), u.get("source"), u.get("size")) != ("source-present", expected["source"], expected["size"]):
            return False
        for eid, kind in zip(expected["evidence"], ("compiler", "runtime", "reproducibility")):
            e = by_evidence.get(eid, {})
            if eid not in u.get("evidence_ids", "").split(";") or any(e.get(k) != v for k, v in {
                "unit_id": name, "artifact": "th03-mainl", "result": "pass",
                "extent_size": expected["size"], "evidence_class": kind,
                "output_sha256": MAINL_DISPLAY_HARDWARE_PROOF_SHA}.items()):
                return False
    return True

MAINL_ROOT_TAIL_PROOF_SHA = 'cf42b89579870aa717b08317aa1ad96db1daf8e50005357c1782f38af852668d'
MAINL_ROOT_TAIL_SOURCE_UNITS = {'th03-mainl-decoded-root-tail-align-bfnt': {'source': 'src/mainl/archive_io/bfill.asm', 'size': '1', 'evidence': ['ev-th03-mainl-decoded-root-tail-align-bfnt-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-align-bfnt-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-align-bfnt-root-tail-source-reproducibility']}, 'th03-mainl-decoded-root-tail-align-bread': {'source': 'src/mainl/archive_io/bopenr.asm', 'size': '1', 'evidence': ['ev-th03-mainl-decoded-root-tail-align-bread-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-align-bread-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-align-bread-root-tail-source-reproducibility']}, 'th03-mainl-decoded-root-tail-align-bseek': {'source': 'src/mainl/archive_io/bseek.asm', 'size': '1', 'evidence': ['ev-th03-mainl-decoded-root-tail-align-bseek-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-align-bseek-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-align-bseek-root-tail-source-reproducibility']}, 'th03-mainl-decoded-root-tail-align-filesize': {'source': 'src/mainl/archive_io/bseek_.asm', 'size': '1', 'evidence': ['ev-th03-mainl-decoded-root-tail-align-filesize-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-align-filesize-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-align-filesize-root-tail-source-reproducibility']}, 'th03-mainl-decoded-root-tail-keyclear': {'source': 'src/mainl/root_tail/dos_keyclear.asm', 'size': '6', 'evidence': ['ev-th03-mainl-decoded-root-tail-keyclear-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-keyclear-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-keyclear-root-tail-source-reproducibility']}, 'th03-mainl-decoded-root-tail-grcg': {'source': 'src/mainl/root_tail/grcg_setcolor.asm', 'size': '48', 'evidence': ['ev-th03-mainl-decoded-root-tail-grcg-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-grcg-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-grcg-root-tail-source-reproducibility']}, 'th03-mainl-decoded-root-tail-root-zero-font': {'source': 'src/mainl/root_tail/root_zero_font.asm', 'size': '1', 'evidence': ['ev-th03-mainl-decoded-root-tail-root-zero-font-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-root-zero-font-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-root-zero-font-root-tail-source-reproducibility']}, 'th03-mainl-decoded-root-tail-atan-end': {'source': 'src/mainl/root_tail/iatan2.asm', 'size': '114', 'evidence': ['ev-th03-mainl-decoded-root-tail-atan-end-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-atan-end-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-atan-end-root-tail-source-reproducibility']}, 'th03-mainl-decoded-root-tail-align-pfgetc': {'source': 'src/mainl/archive_io/pfgetc.asm', 'size': '1', 'evidence': ['ev-th03-mainl-decoded-root-tail-align-pfgetc-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-align-pfgetc-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-align-pfgetc-root-tail-source-reproducibility']}, 'th03-mainl-decoded-root-tail-pfgetc-zero': {'source': 'src/mainl/archive_io/pfgetc.asm', 'size': '1', 'evidence': ['ev-th03-mainl-decoded-root-tail-pfgetc-zero-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-pfgetc-zero-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-pfgetc-zero-root-tail-source-reproducibility']}, 'th03-mainl-decoded-root-tail-align-pfread': {'source': 'src/mainl/archive_io/pfrewind.asm', 'size': '1', 'evidence': ['ev-th03-mainl-decoded-root-tail-align-pfread-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-align-pfread-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-align-pfread-root-tail-source-reproducibility']}, 'th03-mainl-decoded-root-tail-rand': {'source': 'src/mainl/root_tail/random.asm', 'size': '42', 'evidence': ['ev-th03-mainl-decoded-root-tail-rand-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-rand-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-rand-root-tail-source-reproducibility']}, 'th03-mainl-decoded-root-tail-sound-text': {'source': 'src/mainl/root_tail/soundio.asm', 'size': '116', 'evidence': ['ev-th03-mainl-decoded-root-tail-sound-text-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-sound-text-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-sound-text-root-tail-source-reproducibility']}, 'th03-mainl-decoded-root-tail-resident': {'source': 'src/mainl/root_tail/respal_exist.asm', 'size': '226', 'evidence': ['ev-th03-mainl-decoded-root-tail-resident-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-resident-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-resident-root-tail-source-reproducibility']}, 'th03-mainl-decoded-root-tail-joystick': {'source': 'src/mainl/root_tail/joystick_prefix.asm', 'size': '105', 'evidence': ['ev-th03-mainl-decoded-root-tail-joystick-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-joystick-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-joystick-root-tail-source-reproducibility']}, 'th03-mainl-decoded-root-tail-compare-align': {'source': 'src/mainl/root_tail/pf_str_ieq.asm', 'size': '57', 'evidence': ['ev-th03-mainl-decoded-root-tail-compare-align-root-tail-source-compiler', 'ev-th03-mainl-decoded-root-tail-compare-align-root-tail-source-runtime', 'ev-th03-mainl-decoded-root-tail-compare-align-root-tail-source-reproducibility']}}
def mainl_root_tail_source_proven(units, evidence):
    by_unit = {r["id"]: r for r in units}
    by_evidence = {r["id"]: r for r in evidence}
    for name, expected in MAINL_ROOT_TAIL_SOURCE_UNITS.items():
        u = by_unit.get(name, {})
        if (u.get("state"), u.get("source"), u.get("size")) != ("source-present", expected["source"], expected["size"]):
            return False
        for eid, kind in zip(expected["evidence"], ("compiler", "runtime", "reproducibility")):
            e = by_evidence.get(eid, {})
            if eid not in u.get("evidence_ids", "").split(";") or any(e.get(k) != v for k, v in {
                "unit_id": name, "artifact": "th03-mainl", "result": "pass",
                "extent_size": expected["size"], "evidence_class": kind,
                "output_sha256": MAINL_ROOT_TAIL_PROOF_SHA}.items()):
                return False
    return True

MAINL_LINKED_GAME_PROOF_SHA = '5adc20861132a415af80e0dff614cb0f82a888506d0eae35bb1f4544cd77b714'
MAINL_LINKED_GAME_SOURCE_UNITS = {'th03-mainl-decoded-linked-tail-planes': {'source': 'src/mainl/linked_game/planes.cpp', 'size': '41', 'evidence': ['ev-th03-mainl-decoded-linked-tail-planes-linked-game-source-compiler', 'ev-th03-mainl-decoded-linked-tail-planes-linked-game-source-runtime', 'ev-th03-mainl-decoded-linked-tail-planes-linked-game-source-reproducibility']}, 'th03-mainl-decoded-sound-mode': {'source': 'src/mainl/linked_game/sound_mode.c', 'size': '29', 'evidence': ['ev-th03-mainl-decoded-sound-mode-linked-game-source-compiler', 'ev-th03-mainl-decoded-sound-mode-linked-game-source-runtime', 'ev-th03-mainl-decoded-sound-mode-linked-game-source-reproducibility']}, 'th03-mainl-decoded-linked-tail-producer-0049': {'source': 'src/mainl/linked_game/sound_mode.c', 'size': '1', 'evidence': ['ev-th03-mainl-decoded-linked-tail-producer-0049-linked-game-source-compiler', 'ev-th03-mainl-decoded-linked-tail-producer-0049-linked-game-source-runtime', 'ev-th03-mainl-decoded-linked-tail-producer-0049-linked-game-source-reproducibility']}, 'th03-mainl-decoded-sound-pmd': {'source': 'src/mainl/linked_game/sound_pmd.c', 'size': '57', 'evidence': ['ev-th03-mainl-decoded-sound-pmd-linked-game-source-compiler', 'ev-th03-mainl-decoded-sound-pmd-linked-game-source-runtime', 'ev-th03-mainl-decoded-sound-pmd-linked-game-source-reproducibility']}, 'th03-mainl-decoded-linked-tail-producer-0083': {'source': 'src/mainl/linked_game/sound_pmd.c', 'size': '1', 'evidence': ['ev-th03-mainl-decoded-linked-tail-producer-0083-linked-game-source-compiler', 'ev-th03-mainl-decoded-linked-tail-producer-0083-linked-game-source-runtime', 'ev-th03-mainl-decoded-linked-tail-producer-0083-linked-game-source-reproducibility']}, 'th03-mainl-decoded-sound-volume': {'source': 'src/mainl/linked_game/sound_volume.c', 'size': '27', 'evidence': ['ev-th03-mainl-decoded-sound-volume-linked-game-source-compiler', 'ev-th03-mainl-decoded-sound-volume-linked-game-source-runtime', 'ev-th03-mainl-decoded-sound-volume-linked-game-source-reproducibility']}, 'th03-mainl-decoded-linked-tail-producer-009f': {'source': 'src/mainl/linked_game/sound_volume.c', 'size': '1', 'evidence': ['ev-th03-mainl-decoded-linked-tail-producer-009f-linked-game-source-compiler', 'ev-th03-mainl-decoded-linked-tail-producer-009f-linked-game-source-runtime', 'ev-th03-mainl-decoded-linked-tail-producer-009f-linked-game-source-reproducibility']}, 'th03-mainl-decoded-sound-reset': {'source': 'src/mainl/linked_game/sound_reset.cpp', 'size': '11', 'evidence': ['ev-th03-mainl-decoded-sound-reset-linked-game-source-compiler', 'ev-th03-mainl-decoded-sound-reset-linked-game-source-runtime', 'ev-th03-mainl-decoded-sound-reset-linked-game-source-reproducibility']}, 'th03-mainl-decoded-linked-tail-producer-0669': {'source': 'src/mainl/linked_game/sound_reset.cpp', 'size': '1', 'evidence': ['ev-th03-mainl-decoded-linked-tail-producer-0669-linked-game-source-compiler', 'ev-th03-mainl-decoded-linked-tail-producer-0669-linked-game-source-runtime', 'ev-th03-mainl-decoded-linked-tail-producer-0669-linked-game-source-reproducibility']}, 'th03-mainl-decoded-lifecycle-exit': {'source': 'src/mainl/linked_game/exit.cpp', 'size': '67', 'evidence': ['ev-th03-mainl-decoded-lifecycle-exit-linked-game-source-compiler', 'ev-th03-mainl-decoded-lifecycle-exit-linked-game-source-runtime', 'ev-th03-mainl-decoded-lifecycle-exit-linked-game-source-reproducibility']}, 'th03-mainl-decoded-input-sense': {'source': 'src/mainl/linked_game/input_sense.cpp', 'size': '417', 'evidence': ['ev-th03-mainl-decoded-input-sense-linked-game-source-compiler', 'ev-th03-mainl-decoded-input-sense-linked-game-source-runtime', 'ev-th03-mainl-decoded-input-sense-linked-game-source-reproducibility']}, 'th03-mainl-decoded-sound-kaja': {'source': 'src/mainl/linked_game/sound_kaja.cpp', 'size': '30', 'evidence': ['ev-th03-mainl-decoded-sound-kaja-linked-game-source-compiler', 'ev-th03-mainl-decoded-sound-kaja-linked-game-source-runtime', 'ev-th03-mainl-decoded-sound-kaja-linked-game-source-reproducibility']}, 'th03-mainl-decoded-cfg-resident': {'source': 'src/mainl/linked_game/cfg_resident.cpp', 'size': '49', 'evidence': ['ev-th03-mainl-decoded-cfg-resident-linked-game-source-compiler', 'ev-th03-mainl-decoded-cfg-resident-linked-game-source-runtime', 'ev-th03-mainl-decoded-cfg-resident-linked-game-source-reproducibility']}, 'th03-mainl-decoded-lifecycle-init': {'source': 'src/mainl/linked_game/init.cpp', 'size': '62', 'evidence': ['ev-th03-mainl-decoded-lifecycle-init-linked-game-source-compiler', 'ev-th03-mainl-decoded-lifecycle-init-linked-game-source-runtime', 'ev-th03-mainl-decoded-lifecycle-init-linked-game-source-reproducibility']}, 'th03-mainl-decoded-sound-play': {'source': 'src/mainl/linked_game/sound_se.cpp', 'size': '60', 'evidence': ['ev-th03-mainl-decoded-sound-play-linked-game-source-compiler', 'ev-th03-mainl-decoded-sound-play-linked-game-source-runtime', 'ev-th03-mainl-decoded-sound-play-linked-game-source-reproducibility']}, 'th03-mainl-decoded-sound-update': {'source': 'src/mainl/linked_game/sound_se.cpp', 'size': '60', 'evidence': ['ev-th03-mainl-decoded-sound-update-linked-game-source-compiler', 'ev-th03-mainl-decoded-sound-update-linked-game-source-runtime', 'ev-th03-mainl-decoded-sound-update-linked-game-source-reproducibility']}, 'th03-mainl-decoded-win-load': {'source': 'src/mainl/linked_game/win.cpp', 'size': '282', 'evidence': ['ev-th03-mainl-decoded-win-load-linked-game-source-compiler', 'ev-th03-mainl-decoded-win-load-linked-game-source-runtime', 'ev-th03-mainl-decoded-win-load-linked-game-source-reproducibility']}, 'th03-mainl-decoded-win-text': {'source': 'src/mainl/linked_game/win.cpp', 'size': '56', 'evidence': ['ev-th03-mainl-decoded-win-text-linked-game-source-compiler', 'ev-th03-mainl-decoded-win-text-linked-game-source-runtime', 'ev-th03-mainl-decoded-win-text-linked-game-source-reproducibility']}, 'th03-mainl-decoded-staff-flake': {'source': 'src/mainl/linked_game/flake.cpp', 'size': '76', 'evidence': ['ev-th03-mainl-decoded-staff-flake-linked-game-source-compiler', 'ev-th03-mainl-decoded-staff-flake-linked-game-source-runtime', 'ev-th03-mainl-decoded-staff-flake-linked-game-source-reproducibility']}, 'th03-mainl-decoded-lifecycle-exit-to-main': {'source': 'src/mainl/linked_game/exit_to_main.cpp', 'size': '40', 'evidence': ['ev-th03-mainl-decoded-lifecycle-exit-to-main-linked-game-source-compiler', 'ev-th03-mainl-decoded-lifecycle-exit-to-main-linked-game-source-runtime', 'ev-th03-mainl-decoded-lifecycle-exit-to-main-linked-game-source-reproducibility']}, 'th03-mainl-decoded-sound-measure': {'source': 'src/mainl/linked_game/sound_measure.cpp', 'size': '49', 'evidence': ['ev-th03-mainl-decoded-sound-measure-linked-game-source-compiler', 'ev-th03-mainl-decoded-sound-measure-linked-game-source-runtime', 'ev-th03-mainl-decoded-sound-measure-linked-game-source-reproducibility']}, 'th03-mainl-decoded-staff-music': {'source': 'src/mainl/linked_game/staff_flow.asm', 'size': '68', 'evidence': ['ev-th03-mainl-decoded-staff-music-linked-game-source-compiler', 'ev-th03-mainl-decoded-staff-music-linked-game-source-runtime', 'ev-th03-mainl-decoded-staff-music-linked-game-source-reproducibility']}, 'th03-mainl-decoded-staff-ending': {'source': 'src/mainl/linked_game/staff_flow.asm', 'size': '280', 'evidence': ['ev-th03-mainl-decoded-staff-ending-linked-game-source-compiler', 'ev-th03-mainl-decoded-staff-ending-linked-game-source-runtime', 'ev-th03-mainl-decoded-staff-ending-linked-game-source-reproducibility']}}
def mainl_linked_game_source_proven(units, evidence):
    by_unit = {r["id"]: r for r in units}
    by_evidence = {r["id"]: r for r in evidence}
    for name, expected in MAINL_LINKED_GAME_SOURCE_UNITS.items():
        u = by_unit.get(name, {})
        if (u.get("state"), u.get("source"), u.get("size")) != ("source-present", expected["source"], expected["size"]):
            return False
        for eid, kind in zip(expected["evidence"], ("compiler", "runtime", "reproducibility")):
            e = by_evidence.get(eid, {})
            if eid not in u.get("evidence_ids", "").split(";") or any(e.get(k) != v for k, v in {
                "unit_id": name, "artifact": "th03-mainl", "result": "pass",
                "extent_size": expected["size"], "evidence_class": kind,
                "output_sha256": MAINL_LINKED_GAME_PROOF_SHA}.items()):
                return False
    return True

MAINL_CRT_PROOF_SHA = '1a3410e17561ec3a812782c667d2c5ff320d63b0acdaf52244f7c178a385ef96'
MAINL_CRT_SOURCE_UNITS = {'th03-mainl-decoded-crt-h_llsh': {'source': 'src/mainl/crt/h_llsh.asm', 'size': '33', 'evidence': ['ev-th03-mainl-decoded-crt-h_llsh-crt-source-compiler', 'ev-th03-mainl-decoded-crt-h_llsh-crt-source-runtime', 'ev-th03-mainl-decoded-crt-h_llsh-crt-source-reproducibility']}, 'th03-mainl-decoded-crt-h_padd': {'source': 'src/mainl/crt/h_padd.asm', 'size': '96', 'evidence': ['ev-th03-mainl-decoded-crt-h_padd-crt-source-compiler', 'ev-th03-mainl-decoded-crt-h_padd-crt-source-runtime', 'ev-th03-mainl-decoded-crt-h_padd-crt-source-reproducibility']}, 'th03-mainl-decoded-crt-ioerror': {'source': 'src/mainl/crt/ioerror.asm', 'size': '82', 'evidence': ['ev-th03-mainl-decoded-crt-ioerror-crt-source-compiler', 'ev-th03-mainl-decoded-crt-ioerror-crt-source-runtime', 'ev-th03-mainl-decoded-crt-ioerror-crt-source-reproducibility']}, 'th03-mainl-decoded-crt-n_pcmp': {'source': 'src/mainl/crt/n_pcmp.asm', 'size': '33', 'evidence': ['ev-th03-mainl-decoded-crt-n_pcmp-crt-source-compiler', 'ev-th03-mainl-decoded-crt-n_pcmp-crt-source-runtime', 'ev-th03-mainl-decoded-crt-n_pcmp-crt-source-reproducibility']}, 'th03-mainl-decoded-crt-fbrk': {'source': 'src/mainl/crt/fbrk.asm', 'size': '352', 'evidence': ['ev-th03-mainl-decoded-crt-fbrk-crt-source-compiler', 'ev-th03-mainl-decoded-crt-fbrk-crt-source-runtime', 'ev-th03-mainl-decoded-crt-fbrk-crt-source-reproducibility']}, 'th03-mainl-decoded-crt-setblock': {'source': 'src/mainl/crt/setblock.asm', 'size': '32', 'evidence': ['ev-th03-mainl-decoded-crt-setblock-crt-source-compiler', 'ev-th03-mainl-decoded-crt-setblock-crt-source-runtime', 'ev-th03-mainl-decoded-crt-setblock-crt-source-reproducibility']}}
def mainl_crt_source_proven(units, evidence):
    by_unit = {r["id"]: r for r in units}
    by_evidence = {r["id"]: r for r in evidence}
    for name, expected in MAINL_CRT_SOURCE_UNITS.items():
        u = by_unit.get(name, {})
        if (u.get("state"), u.get("source"), u.get("size")) != ("source-present", expected["source"], expected["size"]):
            return False
        for eid, kind in zip(expected["evidence"], ("compiler", "runtime", "reproducibility")):
            e = by_evidence.get(eid, {})
            if eid not in u.get("evidence_ids", "").split(";") or any(e.get(k) != v for k, v in {
                "unit_id": name, "artifact": "th03-mainl", "result": "pass",
                "extent_size": expected["size"], "evidence_class": kind,
                "output_sha256": MAINL_CRT_PROOF_SHA}.items()):
                return False
    return True

def mainl_diet_packing_diagnostic():
    path = ROOT / "config/mainl_diet_packing/proof.json"
    return path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == "aecaba2d80de4d140699d44c7e9bfece1cddb4ade579c08dd07bd49f66b62416"

def mainl_vsync_alignment_proven():
    path = ROOT / "config/mainl_vsync_alignment/proof.json"
    return path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == "671f024d1a3b9ad0ca9fc1615a9f170ea984186836c182a1311e0b4418e073c9"

def mainl_regdata_backend_proven():
    path = ROOT / "config/mainl_regdata_backend/proof.json"
    return path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == "b36ff9508ade648c81d28825ec0e6d12be241900db57891ec42cf3197cda528d"

def mainl_continue_backend_proven():
    path = ROOT / "config/mainl_continue_backend/proof.json"
    return path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == "c26a9420ab0147934d161f8a9c6b8a26c31f760e808d4a44606ca7805058b9c9"

def render_svg(units: list[dict[str, str]], functions: list[dict[str, str]],
               evidence: list[dict[str, str]] | None = None) -> str:
    rows = []
    graphics_pending = mainl_graphics_producer_pending()
    for index, (artifact, label) in enumerate((
        ("th03-op", "OP.EXE"), ("th03-main", "MAIN.EXE"),
        ("th03-mainl", "MAINL.EXE"), ("th03-zun", "ZUN.COM"),
    )):
        if artifact == "th03-mainl":
            counts = mainl_unit_progress(units)
            total = counts["total"]
            reviewed = counts["reviewed"]
            source = counts["source"]
            exact = counts["exact"]
            y = 128 + index * 62
            retained = (" · Heap: 8 procedures / 628 B retained-only"
                        if mainl_heap_retained(units, evidence or []) else "")
            rows.append(f"""  <g aria-label="MAINL bars count tracked unit extents, not functions; source-present is not exact">
  <text x="24" y="{y}" fill="#f4f4f5" font-family="sans-serif" font-size="14" font-weight="600">{label}</text>
  <text x="24" y="{y+20}" fill="#c8cad2" font-family="monospace" font-size="11">{total} tracked unit extents</text>
  <rect x="200" y="{y-7}" width="250" height="12" rx="4" fill="#353b52"/>
  <rect x="488" y="{y-7}" width="270" height="12" rx="4" fill="#353b52"/>
  <rect x="200" y="{y-7}" width="{250*reviewed/total if total else 0:.2f}" height="5" fill="#9b6de3"/>
  <rect x="200" y="{y}" width="{250*source/total if total else 0:.2f}" height="5" fill="#e0af68"/>
  <rect x="488" y="{y-7}" width="{270*exact/total if total else 0:.2f}" height="12" fill="#55c7a6"/>
  <text x="200" y="{y+22}" fill="#c8cad2" font-family="monospace" font-size="11">Reviewed {reviewed} · Source {source}/{total}</text>
  <text x="488" y="{y+22}" fill="#c8cad2" font-family="monospace" font-size="11">Unit acceptance: exact {exact}/{total}</text>
  <text x="200" y="{y+40}" fill="#e0af68" font-family="sans-serif" font-size="10">Source-present: {counts['source_bytes']:,} B{retained}</text>
  </g>""")
            if mainl_pi_composed(units, evidence or []):
                rows.append(f'<text x="200" y="{y+52}" fill="#e0af68" font-family="sans-serif" font-size="10">Historical PI composition: 6,144 B target-equal · 9 gaps closed · not current total</text>')
            elif mainl_regist_source_pending(units):
                rows.append(f'<text x="200" y="{y+52}" fill="#e0af68" font-family="sans-serif" font-size="10">Registration + score: 17 bodies / 2,949 B owned · native proof pending · not counted</text>')
            elif mainl_regist_hybrid_source(units, evidence or []):
                rows.append(f'<text x="200" y="{y+52}" fill="#e0af68" font-family="sans-serif" font-size="10">Regist + score: 2,949 B source · repeat OBJ/EXE/MAP · 6 PI bytes still differ</text>')
            elif mainl_cutscene_source_pending(units):
                rows.append(f'<text x="200" y="{y+52}" fill="#e0af68" font-family="sans-serif" font-size="10">Cutscene owner: 13 bodies / 3,195 B · native proof pending · not counted</text>')
            elif mainl_cutscene_hybrid_source(units, evidence or []):
                rows.append(f'<text x="200" y="{y+52}" fill="#e0af68" font-family="sans-serif" font-size="10">Cutscene: 3,195 B source · repeat OBJ/EXE/MAP · 3 PI bytes still differ</text>')
            if mainl_crt_source_proven(units, evidence or []) and mainl_linked_game_source_proven(units, evidence or []) and mainl_root_tail_source_proven(units, evidence or []) and mainl_display_hardware_source_proven(units, evidence or []) and mainl_archive_io_source_proven(units, evidence or []) and mainl_resources_source_proven(units, evidence or []) and mainl_pi_decoder_source_proven(units, evidence or []) and mainl_root_source_proven(units, evidence or []) and mainl_staff_source_proven(units, evidence or []):
                rows.append(f'<text x="200" y="{y+66}" fill="#e0af68" font-family="sans-serif" font-size="10">CRT + prior source: 24,680 B target-equal · {'full program equal / order open' if mainl_vsync_alignment_proven() else '1 DATA byte / relocation order open'}</text>')
            elif mainl_linked_game_source_proven(units, evidence or []) and mainl_root_tail_source_proven(units, evidence or []) and mainl_display_hardware_source_proven(units, evidence or []) and mainl_archive_io_source_proven(units, evidence or []) and mainl_resources_source_proven(units, evidence or []) and mainl_pi_decoder_source_proven(units, evidence or []) and mainl_root_source_proven(units, evidence or []) and mainl_staff_source_proven(units, evidence or []):
                rows.append(f'<text x="200" y="{y+66}" fill="#e0af68" font-family="sans-serif" font-size="10">Linked game + prior source: 24,052 B target-equal · 1 DATA byte / relocation order open</text>')
            elif mainl_root_tail_source_proven(units, evidence or []) and mainl_display_hardware_source_proven(units, evidence or []) and mainl_archive_io_source_proven(units, evidence or []) and mainl_resources_source_proven(units, evidence or []) and mainl_pi_decoder_source_proven(units, evidence or []) and mainl_root_source_proven(units, evidence or []) and mainl_staff_source_proven(units, evidence or []):
                rows.append(f'<text x="200" y="{y+66}" fill="#e0af68" font-family="sans-serif" font-size="10">Root-tail + prior source: 22,287 B target-equal · 1 DATA byte / relocation order open</text>')
            elif mainl_display_hardware_source_proven(units, evidence or []) and mainl_archive_io_source_proven(units, evidence or []) and mainl_resources_source_proven(units, evidence or []) and mainl_pi_decoder_source_proven(units, evidence or []) and mainl_root_source_proven(units, evidence or []) and mainl_staff_source_proven(units, evidence or []):
                rows.append(f'<text x="200" y="{y+66}" fill="#e0af68" font-family="sans-serif" font-size="10">Display + prior source: 21,565 B target-equal · 1 DATA byte / relocation order open</text>')
            elif mainl_archive_io_source_proven(units, evidence or []) and mainl_resources_source_proven(units, evidence or []) and mainl_pi_decoder_source_proven(units, evidence or []) and mainl_root_source_proven(units, evidence or []) and mainl_staff_source_proven(units, evidence or []):
                rows.append(f'<text x="200" y="{y+66}" fill="#e0af68" font-family="sans-serif" font-size="10">Archive + prior source: 19,449 B target-equal · 1 DATA byte / relocation order open</text>')
            elif mainl_resources_source_proven(units, evidence or []) and mainl_pi_decoder_source_proven(units, evidence or []) and mainl_root_source_proven(units, evidence or []) and mainl_staff_source_proven(units, evidence or []):
                rows.append(f'<text x="200" y="{y+66}" fill="#e0af68" font-family="sans-serif" font-size="10">Resources + prior source: 16,970 B target-equal · 1 DATA byte / relocation order open</text>')
            elif mainl_pi_decoder_source_proven(units, evidence or []) and mainl_root_source_proven(units, evidence or []) and mainl_staff_source_proven(units, evidence or []):
                rows.append(f'<text x="200" y="{y+66}" fill="#e0af68" font-family="sans-serif" font-size="10">PI + root + staff: composed 13,495 B target-equal · 1 DATA byte / relocation order open</text>')
            elif mainl_root_source_proven(units, evidence or []) and mainl_staff_source_proven(units, evidence or []):
                rows.append(f'<text x="200" y="{y+66}" fill="#e0af68" font-family="sans-serif" font-size="10">Root + staff source: composed 11,971 B target-equal · 1 DATA byte / relocation order open</text>')
            elif mainl_staff_source_proven(units, evidence or []):
                rows.append(f'<text x="200" y="{y+66}" fill="#e0af68" font-family="sans-serif" font-size="10">Staff + graphics: 3,339 B source · composed 9,483 B target-equal · exact acceptance open</text>')
            elif mainl_graphics_linked():
                rows.append(f'<text x="200" y="{y+66}" fill="#e0af68" font-family="sans-serif" font-size="10">Linked graphics: 355 B target-equal · decoded 1 DATA byte remains · no exact credit</text>')
            elif graphics_pending:
                rows.append(f'<text x="200" y="{y+66}" fill="#e0af68" font-family="sans-serif" font-size="10">Graphics: 355 B compiled · 333 non-fixup B match · 9 fixups / 22 B await link · not counted</text>')
            continue
        candidates = [f for f in functions if f["artifact"] == artifact]
        reviewed = sum(f["boundary_state"] in {"reviewed", "shared"} for f in candidates)
        exact = sum(f["state"] == "exact" for f in candidates)
        total = len(candidates)
        y = 128 + index * 62 + (14 if graphics_pending and index > 2 else 0)
        inventory = f"{total} tracked functions" if total else "Inventory pending"
        rows.append(f'''  <text x="24" y="{y}" fill="#f4f4f5" font-family="sans-serif" font-size="14" font-weight="600">{label}</text>
  <text x="24" y="{y+20}" fill="#c8cad2" font-family="monospace" font-size="11">{inventory}</text>
  <rect x="200" y="{y-7}" width="250" height="12" rx="4" fill="#353b52"/>
  <rect x="488" y="{y-7}" width="270" height="12" rx="4" fill="#353b52"/>
  <rect x="200" y="{y-7}" width="{250*reviewed/total if total else 0:.2f}" height="12" fill="#9b6de3"/>
  <rect x="488" y="{y-7}" width="{270*exact/total if total else 0:.2f}" height="12" fill="#55c7a6"/>
  <text x="200" y="{y+22}" fill="#c8cad2" font-family="monospace" font-size="11">Reviewed {reviewed} · Pending {total-reviewed}</text>
  <text x="488" y="{y+22}" fill="#c8cad2" font-family="monospace" font-size="11">Exact {exact} · Pending {total-exact}</text>''')
        if artifact == "th03-zun" and zun_init_standalone_retained(units):
            rows.append(f'<text x="200" y="{y+40}" fill="#e0af68" font-family="sans-serif" font-size="10">Retained standalone init: 2 materializations · 9 procedures / 1,390 B · no exact credit</text>')
        if artifact == "th03-zun" and zun_driver_hybrid_retained(units):
            rows.append(f'<text x="200" y="{y+56}" fill="#e0af68" font-family="sans-serif" font-size="10" aria-label="Two equal 22,812-byte mixed-source outputs: maintained init (-2) and driver (-4), three retained other payloads and retained wrapper scaffold. Two independent driver materializations have raw OBJ/COM/MAP equality, no normalization or object reuse; first was not a predeclared pair, and second source mtimes were declared from observed first inputs. Fourteen wrapper-only observations and wrong-transfer negative pass; no payload execution or native composition build. Ten target differences remain; no exact acceptance or DIET closure">Maintained -2/-4 composition: 22,812 B · mixed retained inputs · 10 target differences · no exact credit</text>')
    exact_units = [u for u in units if u["artifact"] == "th03-main" and u["state"] == "exact"]
    exact_bytes = sum(int(u["size"], 0) for u in exact_units)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="788" height="496" viewBox="0 0 788 496" role="img" aria-label="TH03 reviewed subset reconstruction progress">
  <title>TH03 reconstruction progress by artifact</title>
  <desc>Boundary review and exact function acceptance for the tracked subset. Whole-game function and authored-byte totals remain unknown.</desc>
  <rect width="788" height="496" rx="8" fill="#1f2335"/>
  <text x="24" y="31" fill="#f4f4f5" font-family="sans-serif" font-size="18" font-weight="600">TH03 reconstruction progress</text>
  <text x="24" y="52" fill="#c8cad2" font-family="sans-serif" font-size="12">Reviewed ledger subset · whole-game totals remain unknown</text>
  <text x="200" y="83" fill="#f4f4f5" font-family="sans-serif" font-size="13" font-weight="600">Boundary confidence</text>
  <text x="488" y="83" fill="#f4f4f5" font-family="sans-serif" font-size="13" font-weight="600">Function acceptance</text>
  <text x="200" y="100" fill="#c8cad2" font-family="sans-serif" font-size="11">Reviewed contiguous bodies</text>
  <text x="488" y="100" fill="#c8cad2" font-family="sans-serif" font-size="11">Complete raw bytes and relocations</text>
{chr(10).join(rows)}
  <path d="M24 398 H764" stroke="#4b526d"/>
  <text x="24" y="423" fill="#f4f4f5" font-family="sans-serif" font-size="13" font-weight="600">MAIN verified exact extents: {exact_bytes:,} bytes · {len(exact_units)} owners</text>
  <text x="24" y="446" fill="#c8cad2" font-family="sans-serif" font-size="12">Whole-game source/link/product graph: OPEN · no whole-game completion percentage</text>
{('<text x="24" y="472" fill="#e0af68" font-family="sans-serif" font-size="11">MAINL DIET: control 37,975 B exact · source 38,048 B / 2,259 differences · exact credit 0</text>' if mainl_diet_packing_diagnostic() and not mainl_vsync_alignment_proven() else '')}
{('<text x="24" y="472" fill="#e0af68" font-family="sans-serif" font-size="11">MAINL full program equal · packed 38,050 B / 1,212 differences · relocation order 461 · exact 0</text>' if mainl_vsync_alignment_proven() and not mainl_regdata_backend_proven() else '')}
{('<text x="24" y="472" fill="#e0af68" font-family="sans-serif" font-size="11">MAINL program equal · order 460 · prior DIET 1,212 differences · exact 0</text>' if mainl_regdata_backend_proven() and not mainl_continue_backend_proven() else '')}
{('<text x="24" y="472" fill="#e0af68" font-family="sans-serif" font-size="11">MAINL program equal · order 144 · prior DIET 1,212 differences · exact 0</text>' if mainl_continue_backend_proven() else '')}
</svg>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    with (ROOT / "config/units.csv").open(newline="") as stream:
        units = list(csv.DictReader(stream))
    with (ROOT / "config/th03_main_authored_functions.csv").open(newline="") as stream:
        functions = list(csv.DictReader(stream))
    with (ROOT / "config/evidence.csv").open(newline="") as stream:
        evidence = list(csv.DictReader(stream))
    targets = tomllib.loads((ROOT / "config/targets.toml").read_text())["artifacts"]
    lines = ["# TH03 reconstruction progress", "",
             "| Artifact | Target bytes | Source-present units | Exact units | Exact functions | Exact owned bytes |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for target in (a for a in targets if a["game"] == "th03"):
        rows = [u for u in units if u["artifact"] == target["id"] and u["state"] != "excluded"]
        present = sum(bool(u["source"]) and (ROOT / u["source"]).is_file() for u in rows)
        exact = sum(u["state"] == "exact" for u in rows)
        exact_functions = sum(f["state"] == "exact" for f in functions if f["artifact"] == target["id"])
        exact_bytes = sum(int(u["size"], 0) for u in rows if u["state"] == "exact")
        lines.append(f"| {target['id']} | {target['size']} | {present} | {exact} | {exact_functions} | {exact_bytes} |")
    lines.extend([
        "",
        "Reviewed authored-byte coverage is scoped to currently reviewed file-backed unit extents; "
        "the whole-product authored denominator remains unknown.",
        "Infrastructure and reference builds do not count as game reconstruction.",
        "",
    ])
    if mainl_pi_composed(units, evidence):
        lines.extend(["Historical MAINL PI composition: 6,144 owned decoded bytes and 110 scoped ordered relocation words match target. Nine PI operand gaps close in this composition; historical failures remain preserved. That image retained 21 other byte differences and relocation-order differences. This historical composition did not change source or exact counts.", ""])
    if mainl_crt_source_proven(units, evidence) and mainl_linked_game_source_proven(units, evidence) and mainl_root_tail_source_proven(units, evidence) and mainl_display_hardware_source_proven(units, evidence) and mainl_archive_io_source_proven(units, evidence) and mainl_resources_source_proven(units, evidence) and mainl_pi_decoder_source_proven(units, evidence) and mainl_root_source_proven(units, evidence) and mainl_staff_source_proven(units, evidence):
        lines.extend(['MAINL CRT source promotion: six existing units / 628 bytes added, now source 145/145 (28,381 bytes), exact 0. Six fresh semantic ASM producers replace only six members in the original893-member private library order;887 contextual members remain unchanged. Independent repeated producers/library/link yield nine raw-identical products. All24,680 scoped maintained CODE bytes and93 CRT DATA bytes match target; DATA is not extra CODE ledger credit. Fresh target and final-repeat candidate runtime runs each passed7,858 scenarios and277 instruction positions; first/repeat EXE identity avoids a redundant third run. Fast replay retains the two actual model receipts without rerunning. Known DATA linear60473 (90 to00),461 global relocation-order differences and canonical packed/full cold aggregate gates remain open. Source145/145 is not whole-game exact completion.', ""])
    elif mainl_linked_game_source_proven(units, evidence) and mainl_root_tail_source_proven(units, evidence) and mainl_display_hardware_source_proven(units, evidence) and mainl_archive_io_source_proven(units, evidence) and mainl_resources_source_proven(units, evidence) and mainl_pi_decoder_source_proven(units, evidence) and mainl_root_source_proven(units, evidence) and mainl_staff_source_proven(units, evidence):
        lines.extend(['MAINL linked-game source promotion: 23 existing units / 1,765 bytes added, now source 139/145 (27,753 bytes), exact 0. Two actual rounds each rebuilt 15 C/C++ providers plus root and link: 34 successful native phases and 18 raw-identical repeat products. Nineteen contextual objects per round remain retained, not a cold whole program. All 24,052 scoped maintained bytes match target. Six model families cover 3,496 cases per image and nine CFG/window mutants; fast replay retains results without rerunning matrices. STAFF music/ending retain relocation membership but seven/thirteen ordered positions differ. Four original sound producer bytes are owned; scanner NOP remains context. One DATA byte and 461 global relocation-order differences, full cold aggregate and canonical packing remain open.', ""])
    elif mainl_root_tail_source_proven(units, evidence) and mainl_display_hardware_source_proven(units, evidence) and mainl_archive_io_source_proven(units, evidence) and mainl_resources_source_proven(units, evidence) and mainl_pi_decoder_source_proven(units, evidence) and mainl_root_source_proven(units, evidence) and mainl_staff_source_proven(units, evidence):
        lines.extend(['MAINL root-tail source promotion: 16 existing units / 722 bytes added, now source 116/145 (25,988 bytes), exact 0. Two independent include-consuming root assemblies and hybrid links have equal raw root OBJ/EXE/MAP. All 22,287 scoped maintained bytes match target; root-tail scopes have empty relocations. The 722 bytes are 701 bodies plus 21 actual source-traced producers, with no duplicate archive body credit. Target and candidate models each passed 3,895 scenarios / 8,445 calls, including 10 actual DIV stops. SAJOUT remains private/unreferenced and structural-only. Fast replay retains models, not reruns. One DATA0849 byte and 461 global relocation-order differences remain; retained objects are contextual, not a cold aggregate.', ""])
    elif mainl_display_hardware_source_proven(units, evidence) and mainl_archive_io_source_proven(units, evidence) and mainl_resources_source_proven(units, evidence) and mainl_pi_decoder_source_proven(units, evidence) and mainl_root_source_proven(units, evidence) and mainl_staff_source_proven(units, evidence):
        lines.extend(['MAINL display/hardware source promotion: 16 existing units / 2,116 bytes added, now source 100/145 (25,266 bytes), exact 0. Two independent include-consuming root assemblies and hybrid links have equal raw root OBJ/EXE/MAP. All 21,565 scoped maintained bytes match target. Eight fresh VSYNC/graphics/gaiji/screen model phases passed; palette contract retained by complete EXE identity. Fast replay does not rerun models. Target screen outer terminal status is unknown after transport timeout; durable success is verified. One DATA byte and 461 global relocation-order differences remain. Retained objects are contextual, not a cold aggregate.', ""])
    elif mainl_archive_io_source_proven(units, evidence) and mainl_resources_source_proven(units, evidence) and mainl_pi_decoder_source_proven(units, evidence) and mainl_root_source_proven(units, evidence) and mainl_staff_source_proven(units, evidence):
        lines.extend(["MAINL archive/file source promotion: 19 existing units /2,479 bytes added, now source 84/145 (23,150 bytes), exact 0. Two independent include-consuming root assemblies and hybrid links have equal raw root OBJ/EXE/MAP. All 19,449 scoped maintained bytes match target; the archive scope has one matching ordered relocation. Eight fresh model phase receipts and the buffer1754 contract are retained by complete EXE identity, not rerun by fast replay. FILE outer model terminal statuses are unknown after transport timeout; durable successes are verified. One DATA byte and 461 global relocation-order differences remain; no gap/DOSopen/close/STR_IEQ/heap double credit or cold aggregate.", ""])
    elif mainl_resources_source_proven(units, evidence) and mainl_pi_decoder_source_proven(units, evidence) and mainl_root_source_proven(units, evidence) and mainl_staff_source_proven(units, evidence):
        lines.extend(["MAINL resource source promotion: 14 existing units /3,475 bytes added, now source 65/145 (20,671 bytes), exact 0. RotTbl's 1,024 bytes are generated semantic table data, not functions; retained heap is not credited again. Two fresh include-consuming root assemblies and hybrid links have equal raw root OBJ/EXE/MAP. All 16,970 scoped maintained bytes match target; resource relocation sets are empty. One DATA byte and 461 global relocation-order differences remain. Ten fresh model phase receipts plus PI_FREE lifecycle proof are retained by complete EXE identity, not rerun by fast replay; no cold aggregate.", ""])
    elif mainl_pi_decoder_source_proven(units, evidence) and mainl_root_source_proven(units, evidence) and mainl_staff_source_proven(units, evidence):
        lines.extend(["MAINL PI decoder source promotion: one existing 1,524-byte unit added, now source 51/145 (17,196 bytes), exact 0. Two fresh include-consuming root assemblies and hybrid links have equal raw root OBJ/EXE/MAP. All 13,495 scoped maintained bytes match target; four ordered PI relocations match. One DATA byte and 461 global relocation-order differences remain. Full decoder models passed and are retained by complete EXE identity in fast replay, not rerun. Other objects remain contextual, not a cold aggregate.", ""])
    elif mainl_root_source_proven(units, evidence) and mainl_staff_source_proven(units, evidence):
        lines.extend(["MAINL root source promotion: one existing 2,488-byte unit added, now source 50/145 (15,672 bytes), exact 0. Two fresh include-consuming root assemblies and hybrid links have equal raw root OBJ/EXE/MAP. All 11,971 scoped maintained bytes match target. Root 114 relocation entries retain membership but 112 ordered positions differ; one DATA byte and 461 global relocation-order differences remain. Root CPU models rerun; prior staff models retained by complete EXE identity. Other objects remain contextual, not a cold aggregate.", ""])
    elif mainl_staff_source_proven(units, evidence):
        lines.extend(["MAINL staff/graphics source promotion: 11 existing units / 3,339 bytes added, now source 49/145 (13,184 bytes), exact 0. Two fresh include-consuming root assemblies and hybrid links have equal raw root OBJ/EXE/MAP; second link retains the first two graphics objects and 32 contextual objects, not a cold aggregate. All 9,483 scoped maintained bytes match target. Existing 112 ordered relocation words remain equal; new snow/staff relocation membership matches but ordering differs. One DATA byte and 461 global relocation-order differences remain. Full runtime models are retained by complete EXE identity, not rerun in fast replay.", ""])
    elif mainl_graphics_linked():
        lines.extend(["MAINL opt-in linked graphics: 355 target-equal bytes and two scoped ordered relocations preserve the earlier 6,144 bytes / 110 relocations, totaling 6,499 scoped bytes / 112 relocations. One decoded DATA byte remains; all 677 relocation entries retain membership with 461 order differences. One mixed-source link with 32 retained objects, not two cold products; original segment identity is not preserved. Source and exact counts remain unchanged.", ""])
    elif mainl_graphics_producer_pending():
        lines.extend(["MAINL graphics producer checkpoint: three complete functions / 355 compiled bytes; 333 non-fixup bytes match target. Nine genuine symbolic fixups covering 22 bytes await a legitimate link. These candidates are not counted as source-present units or exact acceptance; existing totals remain unchanged.", ""])
    if mainl_diet_packing_diagnostic():
        lines.extend(['MAINL DIET diagnostic: default DIET packs the decoded target twice to the exact canonical37,975-byte stored image, validating the packing control. The maintained-source MCO02 image packs twice to38,048 bytes, with2,259 packed differences; both source roundtrips restore its exact input. The461 decoded relocation-order differences and one DATA byte remain. Same-tool restoration is a separate invocation, not an independent decoder proof. Source145/145 and28,381 bytes remain unchanged; formal exact credit stays0.', ""])
    if mainl_vsync_alignment_proven():
        lines.extend(['MAINL natural VSync DATA alignment now yields the complete decoded target program, without byte injection. Independent root/link repeats have identical raw OBJ/EXE/MAP. Aligned-source DIET packing repeats and roundtrips, but produces38,050 bytes versus canonical37,975 (+75), with1,212 packed differences;677 relocation entries retain membership with461 ordered differences. This is not a full cold-build or new runtime proof. Source145/145 and28,381 bytes remain unchanged, formal exact0. Status CLI distinguishes27,753 decoded authored-owner bytes plus628 library-origin heap bytes; aggregation and JSON are unchanged. Historical pre-alignment DATA and2,259 packed-difference receipts remain preserved.', ""])
    if mainl_regdata_backend_proven():
        lines.extend(['The opt-in registration pointer-array producer now supplies the genuine ten-pointer DATA array. Four fresh MRD04 compiler/root/tail/link phases preserve the complete decoded target program, all 71 mixed registration/music/DATA relocation pairs and six prior snow pairs. Global ordered differences decrease from 461 to 460. Exact DATA ownership remains root2166 + compiler40 + tail888 bytes; no extra CODE credit is granted. The failed MRD03 duplicate _address_0 link remains preserved. This is not a repeat, runtime, full cold build, default graph or packed-product proof. MAINL stays 145/145 source units, 28,381 source bytes and exact zero. The earlier DIET 38,050-byte/1,212-difference result belongs to the prior alignment product, not MRD04. See [registration DATA backend proof](reconstruction/MAINL_REGDATA_BACKEND_REVIEW.md).', ""])
    if mainl_continue_backend_proven():
        lines.extend(['The opt-in 417-byte continue-menu producer and whole unchanged shared-object placement reduce global relocation-order differences from 460 to 144, with 321 positions changed versus MSD03. Three fresh native phases pass all 25 linked gates: full target/prior program bytes, headers, all prior publics, 677 relocation members, registration71, STAFF mixed107 and continue20 target-order streams. MCM01 naturally emitted 414 bytes; its failed hypothesis is preserved beside the genuine explicit-assignment correction. MCM03 missing-call root failure is also retained, with the successor preserving the two existing caller migrations from actual consumed source. No repeat, runtime, full cold build, default graph, packing, count or exact promotion is claimed. MAINL stays 145/145 source units, 28,381 source bytes and exact zero. The earlier DIET 38,050-byte/1,212-difference result belongs to the prior alignment product, not MCM04. See [continue-menu backend proof](reconstruction/MAINL_CONTINUE_BACKEND_REVIEW.md).', ""])
    content = "\n".join(lines)
    destination = ROOT / "docs/PROGRESS.md"
    svg = render_svg(units, functions, evidence)
    svg_path = ROOT / "resources/progress.svg"
    if args.check:
        return 0 if (destination.is_file() and destination.read_text() == content
                     and svg_path.is_file() and svg_path.read_text() == svg) else 1
    destination.write_text(content)
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(svg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
