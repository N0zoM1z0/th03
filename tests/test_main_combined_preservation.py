"""Synthetic portable unit tests, never replay/build/acceptance evidence."""
import copy
import importlib.util
import sys
import tomllib
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'scripts'))
from lib import th03_combined_preservation_layout as c
spec=importlib.util.spec_from_file_location('verifier',ROOT/'scripts/verify_th03_main_combined_preservation.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def image(payload=b'abcdef',sites=()):
    return NS(program_image=payload,relocations=[NS(segment=s,offset=o,linear=s*16+o) for s,o in sites])
class Gates(unittest.TestCase):
    def setUp(self):
        self.rows=[(0x139D,o,n,'CODE','HITBOX_TEXT','MAIN_04',m,28) for o,n,m in c.PARTS]
        self.rows += [(0x1D56,0,0,k,'_DATA' if k=='DATA' else '_BSS','DGROUP',m,48) for _,_,m in c.PARTS[:5] for k in ('DATA','BSS')]
        self.rows += [(0x139D,0x1F25,0,'CODE','HITBOX_TEXT','MAIN_04','th03_main.asm',28),(0x139D,0x3673,0,'CODE','BULLET_TEXT','MAIN_04','th03/ex_ord.cpp',28),(0x139D,0x3673,833,'CODE','BULLET_TEXT','MAIN_04','th03/bm_mima.cpp',28),(0x139D,0x39B4,0,'CODE','BULLET_TEXT','MAIN_04','th03_main.asm',28),(0x139D,0x39B4,0xA2A,'CODE','BULLET_TEXT','MAIN_04','th03/bullet.cpp',28)]
        self.rows += [(0x1D56,0,0,k,'_DATA' if k=='DATA' else '_BSS','DGROUP','th03/bm_mima.cpp',48) for k in ('DATA','BSS')]
    def test_good_layout(self):c.check_layout(self.rows)
    def test_shift_each_producer(self):
        for i in range(6):
            rows=self.rows[:];r=list(rows[i]);r[1]+=1;rows[i]=tuple(r)
            with self.assertRaises(ValueError):c.check_layout(rows)
    def test_data_bss_nonzero(self):
        for i in [j for j,r in enumerate(self.rows) if r[3] in ('DATA','BSS')]:
            rows=self.rows[:];r=list(rows[i]);r[2]=1;rows[i]=tuple(r)
            with self.assertRaises(ValueError):c.check_layout(rows)
    def test_missing_zero_contribution(self):
        for i in [j for j,r in enumerate(self.rows) if r[3] in ('DATA','BSS')]:
            with self.assertRaises(ValueError):c.check_layout(self.rows[:i]+self.rows[i+1:])
    def test_extra_overlap(self):
        with self.assertRaises(ValueError):c.check_layout(self.rows+[self.rows[0]])
    def test_aliases(self):
        text='\n'.join(f'1D56:{o:04X} {n}' for n,o in c.ALIASES.items());c.check_aliases(text)
        for name in c.ALIASES:
            with self.assertRaises(ValueError):c.check_aliases(text.replace(name,name+'_wrong'))
        with self.assertRaises(ValueError):c.check_aliases(text+'\n1D56:0000 _reimu_bomb_particle_p')
    def test_actual_bytes(self):
        c.actual_span(image(),image(),0,6)
        with self.assertRaises(ValueError):c.actual_span(image(b'abcXef'),image(),0,6)
    def test_order_is_literal(self):
        a=image(sites=[(0,0),(0,2)]);b=image(sites=[(0,2),(0,0)])
        with self.assertRaises(ValueError):c.actual_span(a,b,0,6)
    def test_segment_encoding_is_literal(self):
        a=image(b'x'*40,[(0,20)]);b=image(b'x'*40,[(1,4)])
        with self.assertRaises(ValueError):c.actual_span(a,b,0,40)
    def test_relocation_boundary(self):
        with self.assertRaises(ValueError):c.actual_span(image(sites=[(0,1)]),image(),2,2)
    def test_combined_outside_boundary(self):
        im=image(sites=[(0,v.LO-1)])
        with self.assertRaises(ValueError):v.outside_relocs(im)
        im=image(sites=[(0,v.HI-1)])
        with self.assertRaises(ValueError):v.outside_relocs(im)
    def test_only_combined_excluded(self):
        sites=[(0,v.LO-2),(0,v.LO),(0,0x14A76),(0,v.HI),(0,0x17043),(0,0x17384)]
        self.assertEqual(v.outside_relocs(image(sites=sites)),[sites[0],sites[3],sites[5]])
    def test_pending_launch_rejected(self):
        for p in ({},{'launch_ready':True,'unresolved':['source pins']}):
            with self.assertRaises(ValueError):c.check_launch(p,ROOT,lambda p:b'')
    def test_carrier_edits(self):
        units=[dict(carrier_edits=[dict(kind='replace-once',path='th03_main.asm',before='old',after='alias'),dict(kind='remove-between',path='th03_main.asm',start_marker='<a>',end_marker='<b>',replacement='new')])]
        self.assertEqual(c.apply_carrier(b'old<a>body<b>mima',units),b'aliasnewmima')
        with self.assertRaises(ValueError):c.apply_carrier(b'oldold<a>body<b>mima',units)
    def test_receipt_scope_and_order_fail_closed(self):
        from datetime import datetime,timezone
        now=datetime(2026,10,19,tzinfo=timezone.utc)
        row=dict(raw_equal=True,relocations_equal=True,ordered_relocations_equal=True)
        r=dict(kind='th03-main-owned-extent-cold-replay',pass_=True,target_sha256=c.TARGET_SHA,observed_utc=now.isoformat(),candidate_manifest='combined',selected_units=['a'],aggregate_units=['a'],owned_extent_bytes=59624,objects_metadata_normalized_equal=True,candidate_equal=True,all_products_equal=True,game_objects_metadata_normalized_equal=True)
        r['pass']=r.pop('pass_')
        r['rounds']=[dict(round=n,fresh_owned_objects=True,behavior_pass=True,units=[dict(row) for _ in range(78)],functions=[dict(row) for _ in range(371)],producer_ranges=[dict(row)],auxiliary_map_contributions=[]) for n in (1,2)]
        v.receipt_shape(r,True,now)
        for field in ('units','functions','producer_ranges'):
            bad=copy.deepcopy(r);bad['rounds'][0][field][0]['ordered_relocations_equal']=False
            with self.assertRaises(ValueError):v.receipt_shape(bad,True,now)
        for field in ('units','functions'):
            bad=copy.deepcopy(r);bad['rounds'][0][field].pop()
            with self.assertRaises(ValueError):v.receipt_shape(bad,True,now)
        bad=copy.deepcopy(r);bad['rounds'][1]['fresh_owned_objects']=False
        with self.assertRaises(ValueError):v.receipt_shape(bad,True,now)
        bad=copy.deepcopy(r);bad['owned_extent_bytes']=55080
        with self.assertRaises(ValueError):v.receipt_shape(bad,True,now)
        bad=copy.deepcopy(r);bad['observed_utc']='2026-10-18T00:00:00+00:00'
        with self.assertRaises(ValueError):v.receipt_shape(bad,True,now)
    def actual_fixture(self):
        # Synthetic in-memory payload only, never saved as an output/receipt.
        base=tomllib.loads((ROOT/'config/th03_main_exact_units.toml').read_text())
        prop=tomllib.loads((ROOT/'config/th03_main_mima_gameplay_candidate.toml').read_text())
        us,fs,ps=c.scope(base);u,f,p=c.scope(prop);us+=u;fs+=f;ps+=p
        rd={'units':[dict(zip(('id','extent','ledger_id','payload_offset','size'),x)) for x in us], 'functions':[dict(zip(('name','payload_offset','size'),x)) for x in fs], 'producer_ranges':[dict(zip(('id','extent','kind','relative','payload_offset','size'),x)) for x in ps]}
        for rows in rd.values():
            for row in rows:row.update(raw_equal=True,relocations_equal=True,ordered_relocations_equal=True)
        size=max(x[-2]+x[-1] for x in us)+16
        payload=bytes(size)
        sites=[(0,0x142D2),(0,0x142D4)]*15+[(0,0x14A78)]*23+[(0,0x153BD)]*9+[(0,0x17045)]*13
        return base,prop,rd,image(payload,sites),image(payload,sites)
    def test_actual_composition_good(self):
        base,prop,rd,im,target=self.actual_fixture()
        c.check_actual(im,target,rd,base,prop,True)
        bu,bf,bp=c.scope(base)
        rd={k:rd[k][:n] for k,n in [('units',len(bu)),('functions',len(bf)),('producer_ranges',len(bp))]}
        c.check_actual(im,target,rd,base,prop,False)
    def test_actual_composition_lying_byte_gate(self):
        for which in ('old','marisa','reimu','mima_charge','mima_bomb'):
            base,prop,rd,im,target=self.actual_fixture()
            lo=rd['units'][0]['payload_offset'] if which=='old' else dict(marisa=0x142D0,reimu=0x14A76,mima_charge=0x153BB,mima_bomb=0x17043)[which]
            b=bytearray(im.program_image);b[lo]=1;im.program_image=bytes(b)
            with self.assertRaises(ValueError):c.check_actual(im,target,rd,base,prop,True)
    def test_actual_composition_lying_relocation_gate(self):
        base,prop,rd,im,target=self.actual_fixture()
        # Same linear site under a different literal segment:offset representation.
        im.relocations[0].segment=1;im.relocations[0].offset-=16
        with self.assertRaises(ValueError):c.check_actual(im,target,rd,base,prop,True)
    def test_actual_composition_reordered_relocations(self):
        base,prop,rd,im,target=self.actual_fixture()
        im.relocations[0],im.relocations[1]=im.relocations[1],im.relocations[0]
        with self.assertRaises(ValueError):c.check_actual(im,target,rd,base,prop,True)
    def test_actual_composition_identity_range_and_missing(self):
        for field,key,value in [('units','id','wrong'),('functions','payload_offset',0),('producer_ranges','size',999)]:
            base,prop,rd,im,target=self.actual_fixture();rd[field][0][key]=value
            with self.assertRaises(ValueError):c.check_actual(im,target,rd,base,prop,True)
        for i in (-1,-2):
            base,prop,rd,im,target=self.actual_fixture();rd['units'].pop(i)
            with self.assertRaises(ValueError):c.check_actual(im,target,rd,base,prop,True)
        base,prop,rd,im,target=self.actual_fixture();rd['functions'][-1]=rd['functions'][-2].copy()
        with self.assertRaises(ValueError):c.check_actual(im,target,rd,base,prop,True)
    def test_actual_composition_duplicate_pinned_scope(self):
        base,prop,rd,im,target=self.actual_fixture()
        prop['functions'][-1]=prop['functions'][-2].copy()
        rd['functions'][-1]=rd['functions'][-2].copy()
        with self.assertRaises(ValueError):c.check_actual(im,target,rd,base,prop,True)
    def test_real_manifest_scope(self):
        base=tomllib.loads((ROOT/'config/th03_main_exact_units.toml').read_text())
        prop=tomllib.loads((ROOT/'config/th03_main_mima_gameplay_candidate.toml').read_text())
        bu,bf,bp=c.scope(base);pu,pf,pp=c.scope(prop)
        self.assertEqual((len(bu),len(bf),sum(x[-1] for x in bu)),(74,334,53122))
        self.assertEqual((len(pu),len(pf),sum(x[-1] for x in pu)),(4,37,6502))
        self.assertEqual(pu[-1][-2:],(0x17043,833))
        self.assertEqual(sum(x[-1] for x in pf[24:]),2171)

    def test_all_discontiguous_boundaries(self):
        for lo,hi in c.EXCLUSIONS:
            for site in (lo-1,hi-1):
                with self.assertRaises(ValueError):c.outside_relocs(image(sites=[(0,site)]))
        sites=[(0,0x158F5),(0,0x17041),(0,0x17384)]
        self.assertEqual(c.outside_relocs(image(sites=sites)),sites)
    def test_gap_payload_is_not_excluded(self):
        payload=bytes(0x18000);ref=image(payload)
        for site in (0x142CF,0x158F5,0x17042,0x17384):
            b=bytearray(payload);b[site]=1
            self.assertNotEqual(c.outside_bytes(ref),c.outside_bytes(image(bytes(b))))
        for site in (0x142D0,0x158F4,0x17043,0x17383):
            b=bytearray(payload);b[site]=1
            self.assertEqual(c.outside_bytes(ref),c.outside_bytes(image(bytes(b))))
    def test_outside_order_and_representation_preserved(self):
        a=image(sites=[(0,0x9F39),(0,0x9F3E)])
        b=image(sites=[(0,0x9F3E),(0,0x9F39)])
        self.assertNotEqual(c.outside_relocs(a),c.outside_relocs(b))
        b=image(sites=[(1,0x9F29),(0,0x9F3E)])
        self.assertNotEqual(c.outside_relocs(a),c.outside_relocs(b))
    def test_allocation_zero_rows_and_data_alias_drift(self):
        row=(0x1D56,0,0,'DATA','_DATA','DGROUP','old.cpp',48)
        self.assertNotEqual(c.allocation_rows([row],False),c.allocation_rows([],True))
        row2=(*row[:2],1,*row[3:])
        self.assertNotEqual(c.allocation_rows([row],False),c.allocation_rows([row2],True))
        public='1D56:1234 old_public'
        c.check_publics(c.publics(public),public)
        for altered in ('','1D56:1235 old_public',public+'\n1D56:1235 old_public'):
            with self.assertRaises(ValueError):c.check_publics(c.publics(public),altered)
    def test_independent_map_metadata(self):
        config={'segment':0x139D,'units':[{'id':'test','object':'cs_mima','start':0x19EB,'size':1338,'map_segment':'HITBOX_TEXT','map_group':'MAIN_04'}]}
        c.check_map_scope(self.rows,[config])
        for column,value in ((0,0),(1,0),(2,1),(3,'DATA'),(4,'wrong'),(5,'wrong'),(6,'wrong'),(7,48)):
            rows=self.rows[:];row=list(rows[4]);row[column]=value;rows[4]=tuple(row)
            with self.assertRaises(ValueError):c.check_map_scope(rows,[config])
    def test_real_unresolved_template(self):
        import json
        plan={'launch_ready':False,'unresolved':['fresh inventories, authorization and scheduling pins']}
        with self.assertRaises(ValueError):c.check_launch(plan,ROOT,lambda p:p.read_bytes())
if __name__=='__main__':unittest.main()
