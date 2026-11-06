#!/usr/bin/env python3
"""Review the actual typed picture filename table and both native link rounds."""
import json

import build_th03_mainl_picture_files_work as b
from lib.decoded_mainl_picture_files_native import verify, SOURCE
from review_th03_mainl_sound_work import images
from build_th03_mainl_resources_work import sha


def review():
    work, target, candidate, _, _, graph, files = images(b.ROOT)
    result = verify(b.ROOT, work, target, candidate, graph, files)
    return dict(complete=True, source=SOURCE,
        review_driver_sha256=sha((b.ROOT / 'scripts/review_th03_mainl_picture_files_work.py').read_bytes()),
        provenance='candidate-local-attested', scope=result,
        current_mainl_selected_root=b.REPORT, source_root_parent=b.parent.REPORT,
        shared_runtime_root=b.parent.runtime.REPORT,
        fresh_native_rounds=2, fresh_outputs_per_round=3, whole_product_accepted=False)


if __name__ == '__main__':
    result = review()
    (b.ROOT / (b.PREFIX + 'review.json')).write_text(json.dumps(result, indent=2) + '\n')
    print('PIC filename C TU: DATA18 / nine literal near fixups; both raw OBJ/EXE/MAP vectors repeat; '
          'whole original EXE and all677 ordered MZ relocations equal; context ASM fields differ explicitly')
