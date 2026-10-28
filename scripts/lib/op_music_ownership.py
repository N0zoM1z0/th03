"""Native ownership of the remaining complete Music Room CODE procedures."""
import hashlib
import json
import re

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.op_music_state_layout import CS, OFFSET, START, OBJECT, WRAPPER, PUBLICS
from review_th03_op_music_menu_work import examine, REPORT

COPY_UNIT = 'th03-op-decoded-music-copy'
TAIL_UNIT = 'th03-op-decoded-music-animation-and-menu'
UNITS = {COPY_UNIT, TAIL_UNIT}
SOURCES = ('src/op/music/nopoly_blit.inl', 'src/op/music/animation_and_menu.inl')
# Native public boundaries, source ABI and both emitted MAP public tables.
PROCEDURES = (
    ('nopoly_B_put', 216, 30, 'near', 0, 'nopoly_b_put()'),
    ('polygon_build', 246, 143, 'near', 12, 'polygon_build(screen_point_t near*,int,space_changing_pixel_t,int,int,unsigned char)'),
    ('polygons_update_and_render', 389, 502, 'near', 0, 'polygons_update_and_render()'),
    ('music_update_render_and_flip', 891, 54, 'near', 0, 'music_update_render_and_flip()'),
    ('cmt_bg_snap', 945, 315, 'near', 0, 'cmt_bg_snap()'),
    ('cmt_load', 1260, 73, 'near', 2, 'cmt_load(int)'),
    ('cmt_bg_free', 1333, 41, 'near', 0, 'cmt_bg_free()'),
    ('cmt_unput', 1374, 285, 'near', 0, 'cmt_unput()'),
    ('cmt_load_unput_and_put', 1659, 109, 'near', 2, 'cmt_load_unput_and_put(int)'),
    ('musicroom_menu', 1768, 476, 'far', 0, 'musicroom_menu()'),
)


def need(value, message):
    if not value:
        raise ValueError('OP Music native ownership: ' + str(message))


def verify(root, work, target, candidate):
    native = examine(root)
    raw = (root / REPORT.relative_to(REPORT.parents[2])).read_bytes()
    need(native == json.loads(raw), 'current complete native receipt')
    need([(offset, size) for _, offset, size, *_ in PROCEDURES] ==
         [(offset, end - offset) for (offset, _), end in zip(PUBLICS[4:], [o for o, _ in PUBLICS[5:]] + [2244])],
         'complete public partition from byte216 through2244')
    table = (work / 'obj/th03/op.map').read_text()
    decoded = []
    for name, offset, size, distance, cleanup, symbol in PROCEDURES:
        need(len(re.findall(rf'(?m)^\s*{CS:04X}:{OFFSET + offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$', table)) == 2,
             'both MAP public tables: ' + name)
        body = target.program_image[START + offset:START + offset + size]
        need(body == candidate.program_image[START + offset:START + offset + size], 'complete raw procedure: ' + name)
        instructions = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(body, START + offset))
        need(sum(i.size for i in instructions) == size, 'complete instruction partition: ' + name)
        ret = instructions[-1]
        need(ret.mnemonic == ('retf' if distance == 'far' else 'ret') and
             (int(ret.op_str, 0) if ret.op_str else 0) == cleanup, 'native return/argument cleanup: ' + name)
        decoded.append(dict(name=name, offset=offset, size=size, distance=distance, callee_pop_bytes=cleanup,
                            instruction_count=len(instructions)))
    owners = []
    for unit, source, offset, size, procedures in (
        (COPY_UNIT, SOURCES[0], 216, 30, decoded[:1]),
        (TAIL_UNIT, SOURCES[1], 246, 1998, decoded[1:])):
        body = target.program_image[START + offset:START + offset + size]
        digest = hashlib.sha256(body).hexdigest()
        owners.append(dict(unit_id=unit, name='Music Room copy' if offset == 216 else 'Music Room animation and menu',
            source=source, object=OBJECT, segment=CS, offset=OFFSET + offset, start=START + offset, size=size,
            coordinate_space='decoded-load', canonical_file_offset=None, target_sha256=digest, candidate_sha256=digest,
            ordered_relocations=[[r.segment, r.offset] for r in target.relocations if START + offset <= r.linear < START + offset + size],
            procedure_count=len(procedures), procedures=procedures, code_bytes=size,
            initialized_data_bytes=0, private_data_bytes=0, private_bss_bytes=0,
            forwarding_chain=[WRAPPER, source], abi='native near/far returns and Pascal cleanup checked per complete procedure'))
    return dict(owners=owners, procedures=10, code_bytes=2028, complete_carrier_CODE_bytes=2244,
        complete_carrier_procedures=14, complete_carrier_ordered_relocations=50,
        native_receipt_sha256=hashlib.sha256(raw).hexdigest(), runtime_matrix_required=False,
        initialized_DATA_and_BSS_accepted=False, whole_product_accepted=False)
