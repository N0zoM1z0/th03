"""Complete native character-selection CODE across its two actual TC4 TUs."""
import hashlib
import re

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

CS, DS = 0x990, 0xD7F
SOURCE = 'src/op/menu/character_selection.inl'
LOAD_SOURCE = 'src/op/formats/score_load.inl'
LOAD_UNIT = 'th03-op-decoded-score-load'
SOURCES = {SOURCE, LOAD_SOURCE}
UNLOCK_UNIT = 'th03-op-decoded-select-unlock'
TAIL_UNIT = 'th03-op-decoded-select-tail'
UNITS = {LOAD_UNIT, UNLOCK_UNIT, TAIL_UNIT}
OBJECTS = {'obj/th03/selhelp.obj', 'obj/th03/seltail.obj'}
# Complete physical public boundaries, Pascal cleanup and MAP spellings.
HELPER = ((0, '@SCOREDAT_LOAD_AND_DECODE$Q6RANK_T', 107, 2, 'scoredat_load_and_decode(rank_t)'),
          (107, '@playchars_available_load$qv', 48, 0, 'playchars_available_load()'))
TAIL = (
    (0, '@select_cdg_load_part1_of_4$qv', 54, 0, 'select_cdg_load_part1_of_4()'),
    (54, '@select_cdg_load_part2_of_4$qv', 44, 0, 'select_cdg_load_part2_of_4()'),
    (98, '@select_cdg_load_part3_of_4$qv', 53, 0, 'select_cdg_load_part3_of_4()'),
    (151, '@select_init_and_load$qv', 179, 0, 'select_init_and_load()'),
    (330, '@select_free$qv', 28, 0, 'select_free()'),
    (358, '@vs_sel_pics_put$qv', 66, 0, 'vs_sel_pics_put()'),
    (424, '@story_sel_pics_put$qv', 48, 0, 'story_sel_pics_put()'),
    (472, '@stats_put$qv', 209, 0, 'stats_put()'),
    (681, '@names_put$qv', 58, 0, 'names_put()'),
    (739, '@extras_put$qv', 80, 0, 'extras_put()'),
    (819, '@CURVE_PUT$QUCUCIII', 135, 10, 'curve_put(unsigned char,unsigned char,int,int,int)'),
    (954, '@select_curves_update_and_render$qv', 351, 0, 'select_curves_update_and_render()'),
    (1305, '@CURSOR_PUT$QIUC', 98, 4, 'cursor_put(int,unsigned char)'),
    (1403, '@SELECT_UPDATE_PLAYER$QUII', 384, 4, 'select_update_player(unsigned int,int)'),
    (1787, '@select_1p_vs_2p_menu$qv', 407, 0, 'select_1p_vs_2p_menu()'),
    (2194, '@select_vs_cpu_menu$qv', 379, 0, 'select_vs_cpu_menu()'),
    (2573, '@select_story_menu$qv', 285, 0, 'select_story_menu()'),
)
ALIASES = {
    '@scoredat_decode$qv': 'scoredat_decode()', '@scoredat_recreate$qv': 'scoredat_recreate()',
    '@scoredat_sum_invalid$qv': 'scoredat_sum_invalid()', '@FRAME_DELAY$QI': 'frame_delay(int)',
    '@INPUT_MODE_INTERFACE$QV': 'input_mode_interface()', '@INPUT_MODE_KEY_VS_KEY$QV': 'input_mode_key_vs_key()',
    '@INPUT_MODE_JOY_VS_KEY$QV': 'input_mode_joy_vs_key()', '@INPUT_MODE_KEY_VS_JOY$QV': 'input_mode_key_vs_joy()',
    '@input_reset_sense_key_held$qv': 'input_reset_sense_key_held()', '@polar$qiii': 'polar(int,int,int)',
    '@playchars_available_load$qv': 'playchars_available_load()',
}


def need(value, message):
    if not value:
        raise ValueError('OP Select native: ' + str(message))


def address(table, name):
    symbol = ALIASES.get(name, name)
    values = re.findall(rf'(?m)^\s*([0-9A-F]{{4}}):([0-9A-F]{{4}})\s+(?:idle\s+)?{re.escape(symbol)}\s*$', table)
    need(len(values) == 2 and values[0] == values[1], 'both MAP public tables: ' + symbol)
    return tuple(int(v, 16) for v in values[0])


def resolved_code(raw, base, data_base, bss_base, table, lookup=address):
    code, blocks = code_bytes(raw, 1)
    need([b['offset'] for b in blocks] == [sum(p['size'] for p in blocks[:i]) for i in range(len(blocks))],
         'complete natural CODE records without holes')
    image, names, fields, relocs, block = bytearray(code), [], [], [], None
    for record in parse_omf(raw):
        if record.name == 'EXTDEF':
            at = 0
            while at < len(record.data):
                size = record.data[at]
                at += 1
                names.append(record.data[at:at + size].decode())
                at += size
                need(record.data[at] == 0, 'untyped external identity')
                at += 1
        elif record.name == 'LEDATA':
            block = record.data[0], int.from_bytes(record.data[1:3], 'little')
        elif record.name == 'FIXUPP' and block[0] == 1:
            at = 0
            while at < len(record.data):
                loc, low, method = record.data[at:at + 3]
                at += 3
                need(method in (20, 22, 86), 'native field form')
                frame = None
                if method in (20, 22):
                    frame = record.data[at]
                    at += 1
                index = record.data[at]
                at += 1
                site, kind = block[1] + (loc & 3) * 256 + low, loc >> 2 & 15
                width = 4 if kind == 3 else 2
                need(kind in (1, 2, 3) and site + width <= len(code), 'complete native field')
                addend = int.from_bytes(code[site:site + width], 'little')
                name = None
                if method == 20:
                    need(frame == 2 and kind == 1 and index in (2, 3) and loc & 0x40, 'local DGROUP field')
                    value = {2: data_base, 3: bss_base}[index] + addend
                else:
                    name = names[index - 1]
                    seg, off = lookup(table, name)
                    if method == 22:
                        need(kind == 1, 'external WORD field')
                        if not loc & 0x40:
                            need(frame == 1 and seg == CS and code[site - 1] == 0xE8, 'ordinary external near CALL')
                            value = (off + addend - (base + site + 2)) & 65535
                        else:
                            need(frame == 2 and seg == DS, 'external DGROUP data')
                            value = off + addend
                    else:
                        need(loc & 0x40 and addend == 0, 'ordinary absolute external code field')
                        if kind == 3:
                            need(code[site - 1] == 0x9A and seg != CS, 'ordinary unrelaxed far CALL')
                            value = (seg << 16) | off
                            relocs.append([CS, base + site + 2])
                        elif kind == 2:
                            value = seg
                            relocs.append([CS, base + site])
                        else:
                            value = off
                image[site:site + width] = value.to_bytes(width, 'little')
                fields.append(dict(site=site, width=width, locat=loc, method=method, frame=frame,
                                   target=index, name=name, addend=addend))
    return bytes(image), fields, relocs


def verify(root, work, target, candidate, files):
    helper_part, tail_part = 'probe/select155_helper.inl', 'probe/select155_tail.inl'
    source = (root / SOURCE).read_bytes()
    need(files[helper_part] + files[tail_part] == source == files[SOURCE], 'literal complete maintained source split')
    table = (work / 'obj/th03/op.map').read_text()
    owners, objects = [], []
    for stem, base, size, data_base, data_size, bss_base, bss_size, procedures, part in (
        ('selhelp', 0x19F2, 155, 0xA02, 0, 0x2394, 0, HELPER, helper_part),
        ('seltail', 0x1A8D, 2858, 0xA0E, 227, 0x2462, 23, TAIL, tail_part)):
        wrapper, obj = f'th03/{stem}.cpp', f'obj/th03/{stem}.obj'
        raw = (work / obj).read_bytes()
        native = describe_omf(raw)
        need(native['valid'] and native['module_name'] == wrapper and
             native['translator_comments'] == ['TC86 Borland C++ 4.02'], 'actual complete TC4 translation unit')
        need(segment_definitions(raw) == [dict(index=i, name=n, **{'class':c}, overlay='', size=s) for i,n,c,s in
             ((1,'OP_SEL_TEXT','CODE',size),(2,'_DATA','DATA',data_size),(3,'_BSS','BSS',bss_size))], 'whole natural segment layout')
        need(tuple(code_publics(raw, 1)) == tuple((off, symbol) for off,symbol,*_ in procedures), 'all complete native public boundaries')
        need((work / part).read_bytes() == files[part] and (work / wrapper).read_bytes() == files[wrapper] and
             files[wrapper].count(('#include "' + part + '"').encode()) == 1, 'actual literal slice inclusion')
        deps = [n.replace(chr(92), '/') for n in native['dependency_paths']]
        need(wrapper in deps and part in deps and all(n in files for n in deps), 'actual complete source/header dependencies')
        need(len(re.findall(rf'(?m)^\s*{CS:04X}:{base:04X}\s+{size:04X}\s+C=CODE\s+S=OP_SEL_TEXT\s+G=GROUP_01\s+M={re.escape(wrapper)}\s+ACBP=28\s*$', table)) == 1,
             'whole BYTE-aligned CODE MAP contribution')
        code, fields, relocs = resolved_code(raw, base, data_base, bss_base, table)
        start = CS * 16 + base
        need(code == target.program_image[start:start + size] == candidate.program_image[start:start + size], 'complete independently resolved native/target/candidate bytes')
        for image in (target, candidate):
            need([[r.segment, r.offset] for r in image.relocations if start <= r.linear < start + size] == relocs,
                 'complete literal ordered MZ vector')
            need(not any(r.linear < start < r.linear + 2 or r.linear < start + size < r.linear + 2 for r in image.relocations), 'no straddling relocation')
        need([(off, length) for off,_,length,*_ in procedures] ==
             [(off, end-off) for (off,*_), end in zip(procedures, [p[0] for p in procedures[1:]] + [size])],
             'complete contiguous public procedure partition')
        decoded = []
        for off, symbol, length, pop, mapname in procedures:
            need(address(table, symbol if symbol in ALIASES else mapname) == (CS, base + off), 'native public MAP address')
            body = code[off:off + length]
            instructions = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(body, start + off))
            need(sum(i.size for i in instructions) == length and instructions[-1].mnemonic == 'ret' and
                 (int(instructions[-1].op_str, 0) if instructions[-1].op_str else 0) == pop, 'whole near procedure and native argument cleanup: ' + mapname)
            decoded.append(dict(name=mapname, offset=off, size=length, callee_pop_bytes=pop, instruction_count=len(instructions)))
        ranges = ((LOAD_UNIT, LOAD_SOURCE, 0, 107), (UNLOCK_UNIT, SOURCE, 107, 48)) if stem == 'selhelp' else ((TAIL_UNIT, SOURCE, 0, 2858),)
        for owned_unit, owned_source, begin, length in ranges:
            selected = [p for p in decoded if begin <= p['offset'] < begin + length]
            body = code[begin:begin + length]
            h = hashlib.sha256(body).hexdigest()
            owned_part = LOAD_SOURCE if owned_unit == LOAD_UNIT else part
            need(owned_part in deps and files[wrapper].count(('#include "' + owned_part + '"').encode()) == 1,
                 'actual bounded include owner: ' + owned_part)
            owners.append(dict(unit_id=owned_unit, name=selected[0]['name'] if len(selected)==1 else 'Character selection menu/render tail',
                source=owned_source, object=obj, segment=CS, offset=base + begin, start=start + begin, size=length,
                coordinate_space='decoded-load', canonical_file_offset=None, target_sha256=h, candidate_sha256=h,
                ordered_relocations=[r for r in relocs if base + begin <= r[1] < base + begin + length],
                procedure_count=len(selected), procedures=selected, code_bytes=length, initialized_data_bytes=0,
                private_data_bytes=0, private_bss_bytes=0, forwarding_chain=[wrapper,owned_part],
                source_slice=[owned_source,0 if stem=='selhelp' else len(files[helper_part]),len(files[owned_part])],
                abi='near C/Pascal; loader pop2, curve pop10, cursor/update pop4; far callback pointer halves preserved'))
        objects.append(dict(object=obj, complete_CODE_bytes=size, native_fields=fields, ordered_relocations=relocs,
                            containing_DATA_bytes=data_size, containing_BSS_bytes=bss_size))
    need(sum(o['size'] for o in owners) == 3013 and sum(o['procedure_count'] for o in owners) == 19,
         'all nineteen complete functions across both native translation units')
    return dict(owners=owners, code_bytes=3013, procedures=19, selection_CODE_bytes=2906, selection_procedures=18, native_objects=objects,
                containing_DATA_BSS_accepted=False, score_loader_CODE_bytes=107,
                source_split_is_literal=True, runtime_matrix_required=False, whole_product_accepted=False)


if __name__ == '__main__':
    import json
    from pathlib import Path
    import build_th03_op_work as build
    from review_th03_op_cfg_work import images
    from lib.op_startup_cold import verify as cold_graph
    root = Path(__file__).resolve().parents[2]
    work, target, candidate, cold, cold_raw = images(root)
    cold_graph(root, work, target, candidate, cold)
    print(json.dumps(dict(cold_report_sha256=hashlib.sha256(cold_raw).hexdigest(),
        scope=verify(root, work, target, candidate, build.source_graph())), indent=2))
