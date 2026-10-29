"""Read-only OP decoded progress adapter. Never prepare, publish, or replay cold builds."""
import csv
import importlib.util
import json
from pathlib import Path
import subprocess

PUBLICATION = 'config/op_decoded_acceptance/publication.json'


def unavailable(reason):
    return dict(repository_local=True, decoded_accepted=False, factory_accepted=False,
                product_exact=False, mixed_physical_exact_bytes=0,
                canonical_credit_changed=False, whole_game_percentage=None,
                decoded_exact_units=0, decoded_authored_bytes=0,
                decoded_exact_unit_ids=[], reason=reason)


def read_publication(root):
    """Use installed verifier; missing optional decoder must be visible, not silent.

    Both Python environments currently have Capstone. The fallback only handles
    its absence; it does not retry a failed proof or import the prepare CLI.
    No persisted cache: a new invocation rechecks all publication bindings.
    """
    root = Path(root)
    current = root / 'config/op_work/scoped_acceptance.json'
    if not current.is_file() and not (root / PUBLICATION).is_file():
        return unavailable('publication missing')
    if importlib.util.find_spec('capstone') is None:
        python = root / '.venv/bin/python'
        if not python.is_file():
            return unavailable('verification unavailable: Capstone missing and no repository Python')
        try:
            verifier = ("from lib.op_decoded_progress import read_publication as load_status; "
                        if current.is_file() else "from lib.op_decoded_acceptance import load_status; ")
            run = subprocess.run([str(python), '-B', '-c',
                "import json,sys; from pathlib import Path; sys.path.insert(0,'scripts'); "
                + verifier +
                "print(json.dumps(load_status(Path.cwd())))"],
                cwd=root, capture_output=True, text=True, timeout=120, check=True)
            result = json.loads(run.stdout)
            result['status_interpreter'] = 'repository-venv'
            return result
        except Exception as exc:
            return unavailable('verification unavailable: repository Python fallback failed: ' + str(exc))
    if current.is_file():
        try:
            from lib.op_work_acceptance import verify
            return verify(root, json.loads(current.read_bytes()))
        except Exception as exc:
            return unavailable('current source acceptance invalid: ' + str(exc))
    try:
        from lib.op_decoded_acceptance import load_status
        return load_status(root)
    except Exception as exc:
        return unavailable('verification unavailable: ' + str(exc))


def op_decoded_status(root, units):
    """Separate fixed decoded cohort, checked against the caller's current inventory."""
    active = [u for u in units if u['artifact'] == 'th03-op' and u['state'] != 'excluded']
    ids = [u['id'] for u in active]
    # Reject synthetic/partial caller inventories before the costly verifier.
    try:
        with (Path(root) / 'config/units.csv').open(newline='') as stream:
            current = [u for u in csv.DictReader(stream)
                       if u['artifact'] == 'th03-op' and u['state'] != 'excluded']
        if (len(ids) != len(set(ids)) or len(ids) < 33
                or sorted(active, key=lambda u: u['id']) != sorted(current, key=lambda u: u['id'])):
            return dict(unavailable('caller inventory does not match current OP ledger'),
                        tracked_decoded_extents=len(ids))
    except Exception as exc:
        return dict(unavailable('caller inventory unavailable: ' + str(exc)),
                    tracked_decoded_extents=len(ids))
    result = read_publication(root)
    accepted = result.get('decoded_exact_unit_ids', [])
    try:
        current_scopes = result.get('current_cold_source_scopes') is True
        expected_count, expected_bytes = (49, 13644) if current_scopes else (33, 9530)
        valid = (result.get('reviewed_proof_ready') is True
                 and result.get('product_exact') is False
                 and result.get('factory_accepted') is False
                 and result.get('canonical_credit_changed') is False
                 and result.get('whole_game_percentage') is None
                 and result.get('mixed_physical_exact_bytes') == 0
                 and result.get('decoded_exact_units') == expected_count
                 and result.get('decoded_authored_bytes') == expected_bytes
                 and len(accepted) == len(set(accepted)) == expected_count
                 and len(ids) == len(set(ids)) and set(accepted) <= set(ids))
        if current_scopes:
            from lib.op_exit_layout import OWNERS
            from lib.shared_input_layout import unit_ids
            from lib.op_cfg_layout import FUNCTIONS as CFG_FUNCTIONS
            from lib.op_dispatch_layout import FUNCTIONS as DISPATCH_FUNCTIONS
            from lib.op_sound_layout import PRODUCERS as SOUND_PRODUCERS
            from lib.op_helpers_layout import PRODUCERS as HELPER_PRODUCERS
            from lib.op_render_layout import FUNCTIONS as RENDER_FUNCTIONS
            from lib.op_option_layout import FUNCTIONS as OPTION_FUNCTIONS
            from lib.op_main_menu_layout import FUNCTIONS as MAIN_MENU_FUNCTIONS
            from lib.op_startup_layout import FUNCTIONS as STARTUP_FUNCTIONS
            from lib.op_entry_data_layout import UNIT as ENTRY_DATA_UNIT
            from lib.op_music_state_layout import UNIT as MUSIC_STATE_UNIT
            from lib.op_music_ownership import UNITS as MUSIC_CODE_UNITS
            from lib.op_music_storage import UNIT as MUSIC_DATA_UNIT
            from lib.op_select_native import UNITS as SELECT_UNITS
            from lib.op_title_native import TITLE_UNIT, COLUMN_UNIT
            from lib.op_score_native import DATA_UNIT as SCORE_DATA_UNIT
            from lib.op_shared_native import UNITS as SHARED_NATIVE_UNITS
            from lib.op_cdg_draw_native import UNITS as CDG_DRAW_UNITS
            valid = valid and (result.get("decoded_authored_procedures"), result.get("decoded_authored_code_bytes"),
                               result.get("decoded_authored_initialized_data_bytes")) == (83, 12138, 1506)
            valid = valid and set(accepted) == {o[0] for o in OWNERS} | unit_ids("op") | {o[0] for o in CFG_FUNCTIONS+DISPATCH_FUNCTIONS} | {"th03-op-decoded-entry-attract-wait", "th03-op-decoded-entry-vs-menu", "th03-op-decoded-entry-screens"} | {o[0] for o in SOUND_PRODUCERS+HELPER_PRODUCERS+RENDER_FUNCTIONS+OPTION_FUNCTIONS+MAIN_MENU_FUNCTIONS+STARTUP_FUNCTIONS} | {ENTRY_DATA_UNIT, MUSIC_STATE_UNIT} | MUSIC_CODE_UNITS | {MUSIC_DATA_UNIT} | SELECT_UNITS | {TITLE_UNIT, COLUMN_UNIT, SCORE_DATA_UNIT, 'th03-op-decoded-score-encode', 'th03-op-decoded-score-score-data'} | SHARED_NATIVE_UNITS | CDG_DRAW_UNITS
        if not valid:
            return dict(unavailable(result.get('reason', 'publication or caller inventory invalid')),
                        tracked_decoded_extents=len(ids))
    except Exception as exc:
        return dict(unavailable('publication or caller inventory invalid: ' + str(exc)),
                    tracked_decoded_extents=len(ids))
    return dict(result, decoded_accepted=True, tracked_decoded_extents=len(ids))


def decoded_summary(status):
    if status['decoded_accepted']:
        if status.get('current_cold_source_scopes'):
            return (f"OP current decoded source acceptance: {status['decoded_exact_units']} extents / "
                    f"{status['decoded_authored_procedures']} procedures / {status['decoded_authored_bytes']:,} bytes "
                    f"({status['decoded_authored_code_bytes']:,} CODE + {status['decoded_authored_initialized_data_bytes']:,} initialized DATA). "
                    "Validated source-only cold pair and complete native ownership/ABI "
                    "pass; older runtime observations remain historical support. Canonical packed-file unit credit and whole-product "
                    "source exactness remain unchanged; whole-game percentage is unknown.")
        return (f"OP repository-local decoded acceptance is published: "
                f"{status['decoded_exact_units']}/{status['tracked_decoded_extents']} tracked decoded extents, "
                f"{status['decoded_authored_bytes']:,} scoped decoded bytes. "
                "The fixed historical 33-owner cohort excludes selection and all later source promotions. "
                "Canonical ledger credit, whole-product exactness and Factory acceptance remain unchanged/false; "
                "whole-game percentage remains unknown. This is not a pure-instruction or whole-authored-byte total.")
    return ('OP decoded publication contributes zero; ' + status['reason'] +
            '. Retained cold-pair evidence remains historical build proof only; canonical ledger counters are unchanged.')
