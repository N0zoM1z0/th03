"""Lightweight source-bound status for reviewed MAINL product/decoded acceptance.

This consumes a frozen replay publication, not arbitrary success flags. It does
not rerun native tools or the 94-phase receipt replay. Any input or receipt drift
fails closed. Decoded ownership never enters the canonical physical numerator.
"""
from __future__ import annotations
import csv
import hashlib
import importlib.util
import json
import tomllib
from pathlib import Path

PUBLICATION = 'config/mainl_product_acceptance/publication.json'

class AcceptanceError(ValueError):
    pass

def require(ok, message):
    if not ok:
        raise AcceptanceError(message)

def resolve(root, name, source_root=None):
    relative = Path(name)
    require(not relative.is_absolute() and '..' not in relative.parts, 'unsafe binding path')
    base = source_root if source_root and (source_root / relative).is_file() else root
    path = base / relative
    require(path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(base.resolve()), 'missing regular binding: ' + name)
    return path

def checked(root, pin, source_root=None):
    data = resolve(root, pin['path'], source_root).read_bytes()
    require(len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256'], 'binding drift: ' + pin['path'])
    return data

def verify(root, publication, source_root=None, allow_review=False):
    root = Path(root)
    source_root = Path(source_root) if source_root else None
    require(publication['schema'] == 'mainl-product-acceptance-publication-v1', 'publication schema')
    require(publication['state'] == 'repository-local-accepted' or (allow_review and publication['state'] == 'review-ready'), 'acceptance publication is pending')
    pins = publication['input_bindings']
    require(len({p['path'] for p in pins}) == len(pins), 'duplicate input binding')
    bound = {p['path'] for p in pins}
    required = {'config/units.csv', 'config/oracles.toml', 'config/targets.toml', 'scripts/validate_tracking.py', 'scripts/lib/mainl_product_acceptance.py', 'scripts/lib/mainl_product_scope.py', 'scripts/lib/mainl_product_audit.py', 'scripts/lib/mainl_owner_migrations.py', 'scripts/replay_th03_mainl_product_acceptance.py', 'config/mainl_product_acceptance/owner-migrations.json'}
    required.update(['config/evidence.csv', 'config/hypotheses.csv', 'config/knowledge.csv', 'config/th03_main_authored_functions.csv', 'config/th03_function_boundaries.csv'])
    require(required <= bound, 'incomplete acceptance input binding')
    for pin in pins:
        checked(root, pin, source_root)
    receipt = json.loads(checked(root, publication['receipt'], source_root))
    accepted = publication['state'] == 'repository-local-accepted'
    require(receipt['proposal_only'] is (not accepted) and receipt['publication_review_required'] is (not accepted), 'publication/replay state mismatch')
    require(receipt['decoded_owner_acceptance_published'] == (145 if accepted else 0), 'unpublished owner acceptance')
    for pin in publication['evidence_files']:
        checked(root, pin, source_root)
    require(receipt['factory_accepted'] is False and receipt['canonical_units_changed'] is False and receipt['canonical_exact_credit_changed'] is False, 'accounting boundary')
    require(receipt['target_provenance'] == 'candidate-local-attested', 'unsupported target provenance')
    require(receipt['scope'] == dict(artifact='th03-mainl', coordinate_space='canonical-file', start=0, size=37975, origin='mixed-product', authored_credit_bytes=0), 'mixed product boundary')
    scope_path = resolve(root, 'scripts/lib/mainl_product_scope.py', source_root)
    spec = importlib.util.spec_from_file_location('mainl_accepted_scope', scope_path)
    scope = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scope)
    evidence = receipt['oracle_evidence']
    require(not scope.scoped_passes(root, list(evidence), evidence, 'th03-mainl', 'th03-mainl-mixed-stored-product', 0, 37975), 'product Oracle gate')
    units = {u['id']: u for u in csv.DictReader(resolve(root, 'config/units.csv', source_root).read_text().splitlines()) if u['artifact'] == 'th03-mainl' and u['state'] != 'excluded'}
    owners = receipt['decoded_owners']
    require(len(owners) == 145 and len({u['unit_id'] for u in owners}) == 145 and {u['unit_id'] for u in owners} == set(units), 'decoded inventory mismatch')
    totals = {}; spans = []
    for owner in owners:
        unit = units[owner['unit_id']]
        start = int(unit['segment'].split(':')[1], 16) * 16 + int(unit['offset'], 0)
        size = int(unit['compare_size'], 0)
        require(owner['coordinate_space'] == 'decoded-load' and owner['canonical_file_offset'] is None and not unit['file_offset'], 'invented canonical offset')
        require(owner['decoded_linear_start'] == start and owner['size'] == size and owner['origin'] == unit['origin'] and owner['source'] == unit['source'], 'owner ledger drift')
        require(owner['reviewed_boundary'] and owner['raw_equal'] and owner['ordered_relocations_equal'] and owner['map_covered_bytes'] == size and not owner['lineage_gaps'], 'owner proof gap')
        require(unit['boundary_state'] in ['reviewed', 'shared'], 'unreviewed owner boundary')
        require(not any(start < right and left < start + size for left, right in spans), 'decoded ownership overlap')
        spans.append((start, start + size))
        evidence = owner['oracle_evidence']
        require(not scope.scoped_passes(root, list(evidence), evidence, 'th03-mainl', owner['unit_id'], start, size), 'owner Oracle gate')
        totals[owner['origin']] = totals.get(owner['origin'], 0) + size
    require(totals == {'authored': 27753, 'library': 628}, 'decoded origin totals')
    accepted = publication['state'] == 'repository-local-accepted'
    return dict(repository_local=True, factory_accepted=False, target_provenance='candidate-local-attested', product_exact=accepted, mixed_physical_exact_bytes=37975 if accepted else 0, mixed_authored_credit_bytes=0, decoded_exact_units=145 if accepted else 0, decoded_authored_exact_units=144 if accepted else 0, decoded_library_exact_units=1 if accepted else 0, decoded_authored_bytes=27753 if accepted else 0, decoded_library_bytes=628 if accepted else 0, canonical_file_backed_authored_credit_unchanged=True, whole_game_percentage=None, whole_game_code_denominator_known=False, reviewed_proof_ready=True, decoded_exact_unit_ids=sorted(units) if accepted else [])

def load_status(root, publication_path=PUBLICATION):
    """Fail closed for normal progress rendering; no full replay and no native work."""
    try:
        root = Path(root)
        return verify(root, json.loads((root / publication_path).read_text()))
    except (OSError, ValueError, KeyError, TypeError, ImportError) as error:
        return dict(repository_local=True, factory_accepted=False, product_exact=False, mixed_physical_exact_bytes=0, mixed_authored_credit_bytes=0, decoded_exact_units=0, decoded_authored_bytes=0, decoded_library_bytes=0, decoded_exact_unit_ids=[], whole_game_percentage=None, reason=str(error))
