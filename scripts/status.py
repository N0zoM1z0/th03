#!/usr/bin/env python3
"""Derive reconstruction status from machine-readable ledgers."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import json
import os
from pathlib import Path
import subprocess
import sys
import tomllib


# Support importlib.spec_from_file_location callers without PYTHONPATH.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.op_decoded_progress import op_decoded_status, decoded_summary

ROOT = Path(__file__).resolve().parents[1]
MAINL_SCOPED_PUBLICATION = 'config/mainl_work/scoped_acceptance.json'
ZUN_SCOPED_PUBLICATION = 'config/zun_work/scoped_acceptance.json'


def zun_product_status(root, units):
    pending = dict(repository_local=True, decoded_accepted=False, product_exact=False,
                   decoded_exact_units=0, decoded_authored_bytes=0, decoded_exact_unit_ids=[],
                   mixed_physical_exact_bytes=0, canonical_credit_changed=False,
                   factory_accepted=False, whole_game_percentage=None)
    current = Path(root) / ZUN_SCOPED_PUBLICATION
    if not current.is_file():
        return dict(pending, reason='current ZUN source publication missing')
    try:
        with (Path(root) / 'config/units.csv').open() as stream:
            expected = [u for u in csv.DictReader(stream) if u['artifact'] == 'th03-zun' and u['state'] != 'excluded']
        provided = [u for u in units if u['artifact'] == 'th03-zun' and u['state'] != 'excluded']
        if (not expected or len({u['id'] for u in provided}) != len(provided)
                or sorted(provided, key=lambda u: u['id']) != sorted(expected, key=lambda u: u['id'])):
            raise ValueError('caller inventory does not match the current ZUN ledger')
        from lib.decoded_zun_acceptance import verify
        return verify(Path(root), json.loads(current.read_bytes()))
    except (OSError, ValueError, KeyError, TypeError, ImportError) as error:
        return dict(pending, reason=str(error))


def mainl_product_status(root, units):
    """Separate accepted decoded/product axes; never alter file-backed counters.

    The source-bound publication must cover the identical active unit inventory
    supplied by this caller. Synthetic fixtures cannot inherit live acceptance.
    """
    current = Path(root) / MAINL_SCOPED_PUBLICATION
    if current.is_file():
        try:
            with (Path(root) / 'config/units.csv').open() as stream:
                expected = [u for u in csv.DictReader(stream) if u['artifact'] == 'th03-mainl' and u['state'] != 'excluded']
            provided = [u for u in units if u['artifact'] == 'th03-mainl' and u['state'] != 'excluded']
            if (not expected or len({u['id'] for u in provided}) != len(provided)
                    or sorted(provided, key=lambda u: u['id']) != sorted(expected, key=lambda u: u['id'])):
                raise ValueError('caller inventory does not match the current MAINL ledger')
            from lib.decoded_mainl_acceptance import verify
            return verify(Path(root), json.loads(current.read_bytes()))
        except (OSError, ValueError, KeyError, TypeError, ImportError) as error:
            reason = str(error)
            # A stale publication can stop before inspecting the native graph.
            # Report its first real source/recipe blocker too, without rebuilding.
            if 'verifier input drift' in reason:
                try:
                    from lib.decoded_mainl_acceptance import audit
                    audit(Path(root))
                except (OSError, ValueError, KeyError, TypeError, ImportError) as audit_error:
                    if str(audit_error) != reason:
                        reason += '; native audit: ' + str(audit_error)
            return dict(repository_local=True, factory_accepted=False, product_exact=False,
                        mixed_physical_exact_bytes=0, mixed_authored_credit_bytes=0,
                        decoded_exact_units=0, decoded_authored_exact_units=0, decoded_library_exact_units=0,
                        decoded_authored_bytes=0, decoded_library_bytes=0, decoded_exact_unit_ids=[],
                        whole_game_percentage=None, reason=reason)
    # The frozen mixed-product proposal is a historical diagnostic. Missing
    # current evidence must not silently select its obsolete 145-owner cohort.
    return dict(repository_local=True, factory_accepted=False, product_exact=False,
                mixed_physical_exact_bytes=0, mixed_authored_credit_bytes=0,
                decoded_exact_units=0, decoded_authored_exact_units=0, decoded_library_exact_units=0,
                decoded_authored_bytes=0, decoded_library_bytes=0, decoded_exact_unit_ids=[],
                whole_game_percentage=None, reason='current MAINL source publication missing')


def native_source_reviews(root, artifact):
    """Recheck selected current physical owners, independently of cold publication.

    Existing read-only reviewers own the complete source/output/relocation checks.
    Run them in separate interpreters: historical builders hold mutable globals.
    These scopes never contribute decoded publication or canonical ledger credit.
    """
    root = Path(root)
    if artifact == 'th03-main':
        # Select disjoint current source-bound overlays. The former full
        # af1092k composite had superseded owners and the old shared BOSS
        # af1056c source was separately refined. The replaced owners now
        # have separate current reports; don't claim an all-owner live link
        # or Factory credit from any historical composite.
        selected = [(label, stage, f'.analysis/work/exatt-layout-{stage}/report.json',
                     'review_th03_main_source_overlay.py', []) for label, stage in (
            ('VRAM plane initializer', 'af1359g'),
            ('Stage demo transition', 'af1333a'),
            ('Shared BOSS', 'af1351g'),
            ('PI image loader', 'af1358n'),
            ('DOS executable handoff', 'af1359i'),
            ('Resident CFG loader', 'af1182a'),
            ('PC-98 shutdown', 'af1184d'),
            ('Input modes and keyboard wait', 'af1353i'),
            ('PMD/MIDI audio services', 'af1364k'),
            ('Signed Q8 polar geometry', 'af1322h'),
            ('Volatile VSYNC frame delay', 'af1352i'),
            ('DOS MAIN initializer', 'af1316f'),
            ('Ellen Extra Attack', 'af1129e'),
            ('Yumemi Extra Attack', 'af1200c'),
            ('Mima Extra Attack', 'af1306e'),
            ('Reimu Extra Attack', 'af1112h'),
            ('Marisa Extra Attack', 'af1196d'),
            ('Kotohime Extra Attack', 'af1199e'),
            ('Chiyuri Extra Attack', 'af1122c'),
            ('Rikako Extra Attack', 'af1301f'),
            ('Kana Extra Attack', 'af1302f'),
            ('Rikako BOSS', 'af1361f'),
            ('Kana BOSS', 'af1364f'),
            ('Chiyuri BOSS', 'af1365f'),
            ('Kotohime BOSS', 'af1363f'),
            ('Reimu BOSS', 'af1362f'),
            ('Mima BOSS', 'af1359d'),
            ('Marisa BOSS', 'af1356f'),
            ('Ellen BOSS', 'af1360k'),
            ('Yumemi BOSS', 'af1366f'),
            ('Bullet engine', 'af1351j'),
            ('Fireball engine', 'af1361j'),
            ('Enemy engine', 'af1358g'),
            ('Explosion collision', 'af1198g'),
            ('Hitbox and HitCircle', 'af1365j'),
            ('Background chains', 'af1115b'),
            ('MAIN entry and round', 'af1314c'),
            ('Round results and reset', 'af1164e'),
            ('Round intro HUD', 'af1166i'),
            ('Static HUD', 'af1165h'),
            ('Player core', 'af1191e'),
            ('Player loss and defeat', 'af1163i'),
            ('Gauge and shared Extra Attack', 'af1363i'),
            ('Marisa Chargeshot', 'af1134f'),
            ('Chiyuri Chargeshot', 'af1135h'),
            ('Reimu Chargeshot', 'af1136f'),
            ('Ellen Chargeshot', 'af1138f'),
            ('Rikako Chargeshot', 'af1140e'),
            ('Kana Chargeshot', 'af1141f'),
            ('Mima Chargeshot', 'af1142d'),
            ('Yumemi Chargeshot', 'af1143h'),
            ('Kotohime Chargeshot', 'af1146d'),
            ('Ellen Bomb', 'af1147c'),
            ('Rikako Bomb', 'af1148f'),
            ('Mima Bomb', 'af1149e'),
            ('Yumemi Bomb', 'af1152f'),
            ('Reimu Bomb and shared lifecycle', 'af1153d'),
            ('Kotohime Bomb', 'af1154d'),
            ('Kana Bomb', 'af1155b'),
            ('Chiyuri Bomb', 'af1156b'),
            ('Marisa Bomb', 'af1159d'),
            ('Combo HUD and chain', 'af1360o'),
            ('Player shots', 'af1132b'),
            ('Player effects', 'af1133a'),
            ('Warning and Gauge HUD', 'af1362n'),
            ('Character callback setup', 'af1161f'),
            ('CPU controller', 'af1357k'),
        )]
        # Original TASM sound leaves are physically distinct from the TC4
        # sources above, and reuse the same unchanged MAIN linker parent.
        selected.append(('Shared sound assembler leaves', 'af1328b',
                         '.analysis/work/main-sound-asm-af1328b/report.json',
                         'probe_th03_main_sound_asm.py', ['--check']))
        selected.append(('Graphics and asset assembler leaves', 'af1330f',
                         '.analysis/work/main-graphics-asm-af1330f/report.json',
                         'probe_th03_main_graphics_asm.py', ['--check']))
        selected.append(('Vector, playfield and collision ASM', 'af1332c',
                         '.analysis/work/main-geometry-asm-af1332c/report.json',
                         'probe_th03_main_geometry_asm.py', ['--check']))
        selected.append(('Round RNG and collision reset ASM', 'af1333c',
                         '.analysis/work/main-roundpr-asm-af1333c/report.json',
                         'probe_th03_main_roundpr_asm.py', ['--check']))
        selected.append(('VSYNC initialized storage ASM', 'af1337i',
                         '.analysis/work/main-vsync-storage-asm-af1337i/report.json',
                         'probe_th03_main_vsync_storage_asm.py', ['--check']))
        selected.append(('Original master library CODE carriers', 'af1338c',
                         '.analysis/work/main-master-library-asm-af1338c/report.json',
                         'probe_th03_main_master_library_asm.py', ['--check']))
        selected.append(('MAIN master DATA and BSS carrier', 'af1340d',
                         '.analysis/work/main-master-tail-data-af1340d/report.json',
                         'probe_th03_main_master_tail_storage.py', ['--check']))
        selected.append(('MAIN aggregate root CODE and DATA', 'af1341b',
                         '.analysis/work/main-root-carrier-af1341b/report.json',
                         'probe_th03_main_root_carrier.py', ['--check']))
        selected.append(('Original zero-byte segment-order carriers', 'af1342c',
                         '.analysis/work/main-zero-order-af1342c/report.json',
                         'probe_th03_main_zero_order_carriers.py', ['--check']))
    elif artifact == 'th03-mainl':
        selected = [
            ('Staff Roll', 'af942s', '.analysis/work/mainl-staff-af942s-native-build.json',
             'review_th03_mainl_staff_native_probe.py', ['--check']),
            ('Root controller', 'af944r', '.analysis/work/mainl-root-af944r-native-build.json',
             'review_th03_mainl_root_native_probe.py', ['--check']),
        ]
    else:
        return []
    results = []
    python = root / '.venv/bin/python'
    for label, stage, report, script, options in selected:
        row = dict(scope=label, stage=stage, report=report, verified=False)
        if not (root / report).is_file():
            results.append(dict(row, reason='native evidence unavailable in this checkout'))
            continue
        try:
            command = [str(python) if python.is_file() else sys.executable,
                       '-B', str(root / 'scripts' / script), '--stage', stage, *options]
            run = subprocess.run(command, cwd=root, capture_output=True, text=True,
                                 timeout=60, env={**os.environ, 'DISPLAY': '', 'WAYLAND_DISPLAY': ''})
            if run.returncode:
                reason = (run.stderr or run.stdout).strip().splitlines()
                raise ValueError(reason[-1] if reason else f'reviewer exited {run.returncode}')
            proof = json.loads(run.stdout)
            if artifact == 'th03-main':
                if proof.get('full_Japanese_MAIN_equal') is not True or proof.get('native_rounds') != 2:
                    raise ValueError('incomplete current MAIN native review')
                row.update(modules=proof['complete_original_units'],
                           code_bytes=proof['original_scope']['CODE_bytes'],
                           public_symbols=proof['original_scope']['PUBLICs'],
                           ordered_native_fields=proof['original_scope']['ordered_native_fields'],
                           native_rounds=proof['native_rounds'])
            elif stage == 'af942s':
                if (proof.get('complete') is not True or proof.get('native_Turbo_CPP_rounds') != 2
                        or proof.get('complete_original_native_CODE_and_DATA_equal') is not True
                        or proof.get('original_67372_byte_japanese_decoded_MAINL_EXE_equal') is not True
                        or proof.get('original_ordered_677_MZ_relocations_equal') is not True):
                    raise ValueError('incomplete current Staff Roll native review')
                row.update(modules=1, procedures=proof['original_exported_code_procedures'],
                           code_bytes=proof['complete_original_CODE_bytes'],
                           initialized_data_bytes=proof['original_initialized_DATA_bytes'],
                           ordered_native_fields=proof['original_literal_OMF_fixups'],
                           native_rounds=proof['native_Turbo_CPP_rounds'])
            else:
                if (proof.get('complete') is not True or proof.get('native_Turbo_CPP_rounds') != 2
                        or proof.get('original_complete_67372_byte_japanese_MAINL_EXE_equal') is not True
                        or proof.get('original_ordered_MZ_relocations') != 677):
                    raise ValueError('incomplete current root-controller native review')
                row.update(modules=1, procedures=proof['major_original_root_functions'],
                           code_bytes=proof['original_CODE_bytes'],
                           initialized_data_bytes=proof['initialized_DATA_bytes'],
                           bss_bytes=proof['original_BSS_bytes'],
                           ordered_native_fields=proof['original_ordered_OMF_FIXUPP_fields'],
                           native_rounds=proof['native_Turbo_CPP_rounds'])
            row.update(verified=True, report_sha256=proof.get('report_sha256') or
                       proof.get('independent_source_build_report_sha256') or
                       proof.get('native_source_build_report_sha256'))
        except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
            row['reason'] = str(error)
        results.append(row)
    return results


def reviewed_authored_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Return current reviewed authored byte owners for denominator accounting.

    Excluded authored rows are historical/superseded records kept so prior
    evidence remains addressable. They are not current physical ownership and
    therefore must not be counted in the reviewed authored-byte denominator.
    """

    return [
        row
        for row in rows
        if row["origin"] == "authored"
        and row["boundary_state"] in {"reviewed", "shared"}
        and row["state"] != "excluded"
    ]


def artifact_report(
    artifact: dict[str, object],
    units: list[dict[str, str]],
    functions: list[dict[str, str]],
    boundaries: list[dict[str, str]],
) -> dict[str, object]:
    """Keep packed-file byte accounting separate from decoded function state."""

    artifact_id = str(artifact["id"])
    rows = [row for row in units if row["artifact"] == artifact_id]
    active = [row for row in rows if row['state'] != 'excluded']
    state_counts = Counter(row["state"] for row in rows)
    state_bytes: dict[str, int] = defaultdict(int)
    for row in rows:
        state_bytes[row["state"]] += int(row["size"], 0)

    reviewed_authored = reviewed_authored_rows(rows)
    file_backed = [row for row in reviewed_authored if row["file_offset"]]
    decoded_only = [row for row in reviewed_authored if not row["file_offset"]]
    known_authored = sum(int(row["size"], 0) for row in file_backed)
    exact_authored = sum(
        int(row["size"], 0) for row in file_backed if row["state"] == "exact"
    )
    reviewed_functions = [
        row
        for row in functions
        if row["artifact"] == artifact_id
        and row["boundary_state"] in {"reviewed", "shared"}
    ]
    exact_functions = [row for row in reviewed_functions if row["state"] == "exact"]
    artifact_boundaries = [row for row in boundaries if row["artifact"] == artifact_id]
    reconstruction_candidates = [
        row for row in artifact_boundaries if row["work_queue"] == "reconstruct"
    ]
    asm_candidates = [
        row for row in artifact_boundaries if row["work_queue"] == "attest-asm"
    ]
    candidate_states = Counter(row["accepted_state"] for row in reconstruction_candidates)
    boundary_states = Counter(row["boundary_state"] for row in reconstruction_candidates)
    return {
        "target_size": artifact["size"],
        "unit_count": len(rows),
        "active_unit_count": len(active),
        "excluded_unit_count": len(rows) - len(active),
        "source_present_units": sum(bool(row.get('source')) and (ROOT / row['source']).is_file()
                                    for row in active),
        "states": dict(sorted(state_counts.items())),
        "state_bytes": dict(sorted(state_bytes.items())),
        "known_authored_bytes": known_authored,
        "exact_authored_bytes": exact_authored,
        "exact_authored_percent": (
            round(exact_authored * 100 / known_authored, 6) if known_authored else None
        ),
        # Authored-origin subset only; state_bytes separately includes maintained
        # library-origin owners. Preserve this JSON key for existing consumers.
        "decoded_only_source_owner_bytes": sum(int(row["size"], 0) for row in decoded_only),
        # The separate function ledger currently covers MAIN only. A zero for
        # another artifact would incorrectly imply that no functions exist.
        "reviewed_authored_functions": len(reviewed_functions) if artifact_id == "th03-main" else None,
        "exact_authored_functions": len(exact_functions) if artifact_id == "th03-main" else None,
        "exact_authored_function_percent": (
            round(len(exact_functions) * 100 / len(reviewed_functions), 6)
            if artifact_id == "th03-main" and reviewed_functions
            else None
        ),
        "boundary_observations": len(artifact_boundaries),
        "authored_function_candidates": len(reconstruction_candidates),
        "authored_boundary_states": dict(sorted(boundary_states.items())),
        "authored_candidate_states": dict(sorted(candidate_states.items())),
        "accepted_exact_authored_functions": candidate_states["exact"],
        "unresolved_target_derived_asm_candidates": sum(
            row["source_form"] == "target-derived-asm"
            and row["accepted_state"] not in {"exact", "excluded"}
            for row in reconstruction_candidates
        ),
        "original_asm_attestation_candidates": len(asm_candidates),
        "original_asm_provisional_boundaries": sum(
            row["boundary_state"] == "provisional" for row in asm_candidates
        ),
        "excluded_boundary_observations": sum(
            row["work_queue"] == "exclude" for row in artifact_boundaries
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    manifest = tomllib.loads(
        (ROOT / "config" / "targets.toml").read_text(encoding="utf-8")
    )
    with (ROOT / "config" / "units.csv").open(newline="", encoding="utf-8") as stream:
        units = list(csv.DictReader(stream))
    function_path = ROOT / "config" / "th03_main_authored_functions.csv"
    if function_path.is_file():
        with function_path.open(newline="", encoding="utf-8") as stream:
            functions = list(csv.DictReader(stream))
    else:
        functions = []
    boundary_path = ROOT / "config" / "th03_function_boundaries.csv"
    if boundary_path.is_file():
        with boundary_path.open(newline="", encoding="utf-8") as stream:
            boundaries = list(csv.DictReader(stream))
    else:
        boundaries = []

    per_artifact: dict[str, dict[str, object]] = {}
    for artifact in (item for item in manifest["artifacts"] if item["game"] == "th03"):
        per_artifact[artifact["id"]] = artifact_report(
            artifact, units, functions, boundaries
        )
    per_artifact["th03-op"]["decoded_acceptance"] = op_decoded_status(ROOT, units)
    per_artifact["th03-mainl"]["product_acceptance"] = mainl_product_status(ROOT, units)
    per_artifact["th03-zun"]["decoded_acceptance"] = zun_product_status(ROOT, units)
    for artifact_id in ('th03-main', 'th03-mainl'):
        per_artifact[artifact_id]['native_source_reviews'] = native_source_reviews(ROOT, artifact_id)
    output = {
        "schema_version": 1,
        "canonicality": manifest["source"]["canonicality"],
        "artifacts": per_artifact,
        "warning": (
            "Byte percentages cover only reviewed file-backed unit extents; "
            "decoded function acceptance and boundary confidence are separate. "
            "null means no honest denominator exists yet."
        ),
    }
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"target canonicality: {output['canonicality']}")
        for artifact_id, report in per_artifact.items():
            percent = report["exact_authored_percent"]
            percent_text = "n/a" if percent is None else f"{percent:.6f}%"
            function_percent = report["exact_authored_function_percent"]
            function_percent_text = (
                "n/a" if function_percent is None else f"{function_percent:.6f}%"
            )
            function_text = (
                f"{report['exact_authored_functions']}/{report['reviewed_authored_functions']} "
                f"({function_percent_text})"
                if report["reviewed_authored_functions"] is not None else "n/a"
            )
            byte_text = (f"{report['exact_authored_bytes']}/{report['known_authored_bytes']} ({percent_text})"
                         if report['known_authored_bytes'] else 'n/a (decoded coordinates)')
            print(f"{artifact_id:12} active-units={report['active_unit_count']:4} "
                  f"source={report['source_present_units']}/{report['active_unit_count']} "
                  f"file-backed-ledger={byte_text} main-function-ledger={function_text}")
            candidate_states = report["authored_candidate_states"]
            boundary_states = report["authored_boundary_states"]
            if report['boundary_observations']:
                print(
                    f"{'':12} boundary-observations={report['boundary_observations']:4} "
                    f"authored-candidates={report['authored_function_candidates']:4} "
                    f"boundary-r/c/p={boundary_states.get('reviewed', 0)}/"
                    f"{boundary_states.get('corroborated', 0)}/"
                    f"{boundary_states.get('provisional', 0)} "
                    f"function-exact={report['accepted_exact_authored_functions']:3} "
                    f"blocked={candidate_states.get('blocked', 0):2} "
                    f"unreviewed={candidate_states.get('unreviewed', 0):3} "
                    f"origin-open={report['unresolved_target_derived_asm_candidates']:2} "
                    f"asm-attest={report['original_asm_attestation_candidates']:2} "
                    f"asm-provisional={report['original_asm_provisional_boundaries']:2}"
                )
        product = per_artifact['th03-mainl']['product_acceptance']
        print('MAINL repository-local mixed product: ' + ('accepted' if product['product_exact'] else 'pending'))
        mainl_total = sum(u['artifact']=='th03-mainl' and u['state']!='excluded' for u in units)
        if product.get('current_cold_source_scopes') or product.get('product_exact'):
            print(f"MAINL decoded accepted units={product['decoded_exact_units']}/{mainl_total} "
                  f"authored={product['decoded_authored_bytes']} B library={product['decoded_library_bytes']} B")
        else:
            print(f"MAINL broad decoded acceptance: PENDING ({mainl_total} tracked extents); "
                  "current scoped native reviews are independent")
        if product.get('reason'):
            print('MAINL broad decoded acceptance pending: ' + product['reason'])
        for artifact_id in ('th03-main', 'th03-mainl'):
            for review in per_artifact[artifact_id]['native_source_reviews']:
                if review['verified']:
                    print(f"{artifact_id} current source-native {review['scope']} ({review['stage']}): "
                          f"{review['modules']} physical owners / {review['code_bytes']:,} CODE B; "
                          "two original compiler rounds and complete normal links verified")
                else:
                    print(f"{artifact_id} source-native {review['scope']} unavailable: {review['reason']}")
        print(decoded_summary(per_artifact["th03-op"]["decoded_acceptance"]))
        zun = per_artifact['th03-zun']['decoded_acceptance']
        if zun.get('decoded_accepted'):
            print(f"ZUN current decoded source acceptance: {zun['decoded_exact_units']} extents; "
                  f"authored={zun['decoded_authored_bytes']} B original-ASM={zun.get('decoded_original_asm_bytes', 0)} B "
                  f"library={zun.get('decoded_library_bytes', 0)} B; "
                  "canonical unit credit unchanged; whole-product source ownership open")
        else:
            print('ZUN decoded acceptance PENDING: ' + zun.get('reason', 'publication unavailable'))
        print(output["warning"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
