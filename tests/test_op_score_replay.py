"""Receipt serialization must preserve score contract comparison semantics."""
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from replay_th03_op_score import normalized_contracts


class ReceiptTests(unittest.TestCase):
    def test_live_tuples_equal_receipt_lists_without_ignoring_behavior(self):
        live = [dict(args=(), events=[dict(args=(0, 206, 0))], result=1,
                     stores_sha256='abc', memory_before_sha256='old-image')]
        receipt = json.loads(json.dumps(live))
        receipt[0]['memory_before_sha256'] = 'new-image'
        self.assertEqual(normalized_contracts(live), normalized_contracts(receipt))
        for key,value in [('result',0), ('stores_sha256','changed'), ('args',[3]),
                          ('events',[dict(args=[0, 178, 0])])]:
            changed = json.loads(json.dumps(receipt))
            changed[0][key] = value
            self.assertNotEqual(normalized_contracts(live), normalized_contracts(changed))


if __name__ == '__main__':
    unittest.main()
