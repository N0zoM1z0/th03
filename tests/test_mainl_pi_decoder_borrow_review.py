"""Reject false path credit from allocation failure or an unexecuted branch."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_pi_decoder_borrow import require_success


class Probe:
    def __init__(self,ax=0,cf=0,visited=()):
        self.registers={'AX':ax,'EFLAGS':2|cf}
        self.visited=set(visited)
    def get(self,name):return self.registers[name]


class SuccessfulBranchTests(unittest.TestCase):
    def test_allocation_and_disagreeing_returns_cannot_credit_decoder(self):
        for ax,cf,p in ((65528,1,Probe(65528,1,[0x13e1])),(0,0,Probe(65528,1,[0x13e1])),(65528,1,Probe(0,0,[0x13e1]))):
            with self.assertRaisesRegex(ValueError,'successful decoder return'):
                require_success(p,ax,cf,[0x13e1])

    def test_success_must_execute_every_declared_branch(self):
        with self.assertRaisesRegex(ValueError,'branch was not executed'):
            require_success(Probe(visited=[0x1459]),0,0,[0x1459,0x13e1])
        require_success(Probe(visited=[0x1459,0x13e1]),0,0,[0x1459,0x13e1])


if __name__=='__main__':unittest.main()
