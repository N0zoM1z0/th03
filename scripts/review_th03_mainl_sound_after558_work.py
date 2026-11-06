#!/usr/bin/env python3
"""Read-only review of the after558 four-source sound C/C++ native producer pair."""
import json

import build_th03_mainl_sound_group_work as b
from build_th03_mainl_resources_work import need, sha
from build_th03_mainl_display_work import payload, literal_fields
from lib.mainl_owner_migrations import public_offsets


def review():
    cfg, cfg_sha = b.inputs()
    report, report_sha = b.base.load(b.REPORT)
    previous, parent_sha = b.base.load(b.parent.REPORT)
    original = b.original_checks(cfg)
    sources = {x['source']: (b.ROOT / x['source']).read_bytes() for x in cfg['units']}
    staged = {key: b.source_transport(raw) for key, raw in sources.items()}
    need(previous['complete'] and parent_sha == cfg['parent_report_sha256'],
         'actual retained after557 parent and 2-round vector CODE source')
    need(report['complete'] and report['source_acceptance'] is False and
         report['whole_product_accepted'] is False and
         report['canonical_credit_changed'] is False and
         report['cold_rebuilt'] is False and report['library_rebuilt'] is False and
         report['game_objects_recompiled'] == 4 and
         (report['CODE_function_bytes'], report['explicit_context_code_bytes']) == (124, 4) and
         report['driver_sha256'] == sha((b.ROOT / b.DRIVER).read_bytes()) and
         report['config_sha256'] == cfg_sha and report['parent_report_sha256'] == parent_sha and
         report['source_sha256'] == {k: sha(raw) for k, raw in sources.items()} and
         report['transported_source_sha256'] == {k: sha(raw) for k, raw in staged.items()} and
         report['original_objects_sha256'] == {k: sha(raw) for k, raw in original.items()} and
         report['wrappers_sha256'] == {
             x['wrapper']: sha(b.wrapper(x['source'].rsplit('/', 1)[-1])) for x in cfg['units']},
         'all four genuine first-use GAME/BINARY source and original OMF bindings')
    need((b.SCRATCH / 'driver.py').read_bytes() == (b.ROOT / b.DRIVER).read_bytes() and
         (b.SCRATCH / 'config.json').read_bytes() == (b.ROOT / b.CONFIG).read_bytes(),
         'staged source configuration and driver are unchanged')
    for u in cfg['units']:
        leaf = u['source'].rsplit('/', 1)[-1]
        need((b.SCRATCH / leaf).read_bytes() == staged[u['source']] and
             (b.SCRATCH / u['wrapper']).read_bytes() == b.wrapper(leaf),
             'actual source consumed by Borland compiler ' + leaf)
    expected_phase_names = [
        label for n in (1, 2)
        for label in ([f'round{n}-compile-{x["name"]}' for x in cfg['units']] + [f'round{n}-link'])
    ]
    need([p['label'] for p in report['phases']] == expected_phase_names and
         all(p['returncode'] == 0 and
             sha((b.ROOT / p['log']).read_bytes()) == p['log_sha256'] for p in report['phases']),
         'ten full native writer logs and build phase ordering')
    vectors = []
    fields = 0
    for number, row in enumerate(report['rounds'], 1):
        prior = previous['rounds'][number-1]
        need(row['round'] == number and row['response_sha256'] == sha(b.response(number)) and
             row['reused'] == prior['reused'] and
             row['reused_banks'] == prior['reused_banks'] and
             row['reused_root'] == prior['reused_root'] and
             row['reused_vector'] == prior['outputs']['obj'],
             'actual prior C0/CRT, root DATA, registration, picture and vector inputs reused')
        native = {k: b.base.checked(v) for k, v in row['outputs'].items()}
        for u in cfg['units']:
            raw = native[u['name'] + '_obj']
            ref = original[u['name']]
            need(payload(raw) == payload(ref) and
                 len(payload(raw)) == u['CODE_bytes'] and
                 literal_fields(raw) == literal_fields(ref) and
                 public_offsets(raw) == public_offsets(ref) and
                 b.parent.module_metadata(raw) == b.parent.module_metadata(ref),
                 'entire sound code and original literal fields / publics / other OMF ' + u['name'])
        need(native['exe'] == b.base.checked(prior['outputs']['exe']) and
             b.map_normalized(native['map']) ==
             b.parent.map_normalized(b.base.checked(prior['outputs']['map'])),
             'full target-equivalent MZ EXE, all ordered relocations and link layout')
        need(len(native['exe']) == 67372 and
             native['exe'][:2] == b'MZ' and
             int.from_bytes(native['exe'][6:8], 'little') == 677, 'actual original MZ header')
        vectors.append(native)
        fields = sum(len(literal_fields(original[x['name']])) for x in cfg['units'])
    need(len(vectors) == 2 and vectors[0] == vectors[1],
         'both complete four OBJ/EXE/MAP native vectors repeat exactly')
    return dict(complete=True, native_rounds=2, original_sound_C_producers=4,
                complete_natural_C_CPP_function_bytes=124,
                historical_contextual_codestring_tail_bytes=4,
                complete_CODE_contribution_bytes=128,
                original_literal_fixups=fields,
                complete_original_MZ_EXE_equal=True,
                decoded_EXE_bytes=67372, original_MZ_relocations=677,
                original_OMF_packet_order_proved=False,
                canonical_factory_acceptance=False,
                whole_product_source_accepted=False,
                native_source_report_sha256=report_sha)


if __name__ == '__main__':
    checked = review()
    (b.ROOT / (b.PREFIX + 'review.json')).write_text(json.dumps(checked, indent=2) + '\n')
    print('Four sound C/C++ original body extents (124 B), four old context tails, 2 complete native EXE/MAP rounds exact.')
