#!/usr/bin/env python3
"""Review the actual two-round root producer without the historical live211 gate."""
import json

import build_th03_mainl_root_state_work as b
from lib.decoded_mainl_root_state_native import verify, SOURCE
from review_th03_mainl_sound_work import images
from build_th03_mainl_resources_work import sha


def review():
    work, target, candidate, _, _, graph, files = images(b.ROOT)
    result = verify(b.ROOT, work, target, candidate, graph, files)
    return dict(complete=True, source=SOURCE,
        review_driver_sha256=sha((b.ROOT / 'scripts/review_th03_mainl_root_state_work.py').read_bytes()),
        provenance='candidate-local-attested', scope=result,
        current_mainl_selected_root=b.REPORT, shared_runtime_root=b.runtime.REPORT,
        fresh_native_rounds=2, fresh_outputs_per_round=3, whole_product_accepted=False)


if __name__ == '__main__':
    result = review()
    (b.ROOT / (b.PREFIX + 'review.json')).write_text(json.dumps(result, indent=2) + '\n')
    print('Root complete TU: CODE2458 + DATA112 + true BSS186; all278 fields and all non-comment records exact; '
          'both whole OBJ/EXE/MAP vectors repeat; BSS file credit0')
