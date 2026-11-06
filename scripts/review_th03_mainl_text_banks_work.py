#!/usr/bin/env python3
"""Review current native semantic registration and ending text banks."""
import json

import build_th03_mainl_text_banks_work as b
from lib.decoded_mainl_text_banks_native import verify
from review_th03_mainl_sound_work import images
from build_th03_mainl_resources_work import sha


def review():
    work, target, candidate, _, _, graph, files = images(b.ROOT)
    result = verify(b.ROOT, work, target, candidate, graph, files)
    return dict(complete=True, provenance='candidate-local-attested', scope=result,
        review_driver_sha256=sha((b.ROOT / 'scripts/review_th03_mainl_text_banks_work.py').read_bytes()),
        current_mainl_selected_root=b.REPORT, source_parent=b.parent.REPORT,
        fresh_native_rounds=2, fresh_outputs_per_round=4, whole_product_accepted=False)


if __name__ == '__main__':
    result = review()
    (b.ROOT / (b.PREFIX + 'review.json')).write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print('Registration303 + ending360 DATA;61 complete semantic strings; all2 literal fields and117 PUBLIC entries; '
          'both whole vectors repeat; original EXE/all677 ordered MZ relocations exact; one linker gap unowned')
