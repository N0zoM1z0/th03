"""Strict conjunctive retained-tail cold comparator. No acceptance ledger writes."""
from pathlib import Path
from lib import th03_tail_model as tail_model
from lib import th03_tail_map as tail_map
from collections import Counter
import hashlib,struct,re
SPANS=[[0xC7A5,0xCDBD],[0xCDBD,0xD031],[0xD031,0xD2E8],[0xD2E8,0xD50E]]
PRODUCERS={
 'warning':{'path':'obj/th03/warning.obj','source':'src/main/player/warning.cpp','bytes':1560,'fixups':125,'literal':37,'proof':'.analysis/gpt-dots-tail-warning-probe-v08/compile-first-v01/source/obj/th03/warning.obj','sha256':'67197a27bb95516f2322c218cc516544fc480c71c74de0db03158df8ff4cd02a'},
 'effects':{'path':'obj/th03/effects.obj','source':'src/main/player/effects.cpp','bytes':628,'fixups':33,'literal':11,'proof':'.analysis/gpt-dots-effects-established-linkage-probe-v01/compile-first-v01/source/obj/th03/effects.obj','sha256':'d37d84309d2cc4d66ef62e67c2685839ac05c74bc1ea90be60d408cb4272d13a'},
 'chain1':{'path':'obj/chain1.obj','source':'src/main/background/chain1.cpp','bytes':695,'fixups':43,'literal':19,'proof':'.analysis/gpt-dots-background-cpp-tail-probe-v01/compile-first-v01/source/obj/chain1.obj','sha256':'5f88e781027458dfa4cefbcf59097e31d2cf57396074cd7d43845e448c16eb76'},
 'chain2':{'path':'obj/chain2.obj','source':'src/main/background/chain2.cpp','bytes':550,'fixups':43,'literal':16,'proof':'.analysis/gpt-dots-background-chain2-typed-probe-v02/compile-first-v01/source/obj/chain2.obj','sha256':'867773a6a70739f6494bf50b01a17b0fcd581170e0fef741c5feee9c3725d775'}}
def need(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def validate_producer(name,path,repo,parse_omf):
 if name=='warning':
  from lib.th03_tail_warning_gate import validate
  return validate(path,repo)
 spec=PRODUCERS[name];prior=(repo/spec['proof']).read_bytes();need(sha(prior)==spec['sha256'],'prior object pin '+name);raw=path.read_bytes();a=parse_omf(prior);b=parse_omf(raw)
 # Preserve every executable/linkage record byte and order. Only non-executable
 # COMENT metadata is outside this comparison; no record/object is rewritten.
 names={'THEADR','LHEADR','LNAMES','SEGDEF','SEGDEF32','GRPDEF','EXTDEF','LEXTDEF','PUBDEF','LPUBDEF','PUBDEF32','LEDATA','LEDATA32','FIXUPP','FIXUPP32','MODEND','MODEND32','LIDATA','LIDATA32','COMDEF','LCOMDEF','COMDAT','COMDAT32'}
 need([(r.record_type,r.data) for r in a if r.name in names]==[(r.record_type,r.data) for r in b if r.name in names],'whole object code/fixup/public/framing identity '+name)
 need(all(r.name in names or r.name=='COMENT' for r in b),'unknown record outside proof '+name)
 need(not any(r.name.startswith(('LIDATA','COMDEF','LCOMDEF','COMDAT')) for r in b),'storage allocation '+name)
 return {'object_sha256':sha(raw),'whole_code_linkage_records_equal':True,'code_bytes':spec['bytes'],'fixups':spec['fixups'],'literal_sites':spec['literal'],'full_body_ABI_proof_rebound':True,'actual_linked_proof':False}
def literal(image,span=None,outside=False):
 out=[]
 for r in image.relocations:
  inside=span is None or any(a<=r.linear and r.linear+2<=b for a,b in span)
  if span:
   need(not any(r.linear<b and r.linear+2>a and not a<=r.linear<=b-2 for a,b in span),'scope straddling relocation')
  if (not inside if outside else inside):out.append([r.segment,r.offset])
 return out
def header_parts(raw):
 need(len(raw)>=28,'MZ short');n=struct.unpack_from('<H',raw,6)[0];start=struct.unpack_from('<H',raw,24)[0];end=start+n*4;h=struct.unpack_from('<H',raw,8)[0]*16;need(28<=start<=end<=h<=len(raw),'MZ relocation bounds')
 return [raw[:start],raw[end:h]]
def check_link(work,repo,baseline,model,pc98,parser):
 # Structural proof is mandatory even if the final executable is byte-exact.
 producer_paths={n:work/spec['path'] for n,spec in PRODUCERS.items()}
 fresh=tail_model.build_model(repo,baseline,work/'obj/th03/main.obj',producer_paths,(work/'obj/th03/main.@l').read_bytes())
 need(fresh['full_literal_stream']==model['full_literal_stream'] and fresh['packed_stream_sha256']==model['packed_stream_sha256'],'post-build actual OMF agrees with frozen pre-native prediction')
 raw=(work/'bin/th03/main.exe').read_bytes();prior=(baseline/'bin/th03/main.exe').read_bytes();target=(repo/'.analysis/targets/th03/main.exe').read_bytes()
 a=pc98.parse_mz(prior);b=pc98.parse_mz(raw);t=pc98.parse_mz(target)
 need(len(a.program_image)==len(b.program_image),'program size')
 need(a.program_image[:0xC7A5]==b.program_image[:0xC7A5] and a.program_image[0xD50E:]==b.program_image[0xD50E:],'all outside raw bytes')
 need(b.program_image[0xC7A5:0xD50E]==t.program_image[0xC7A5:0xD50E],'all3433 owned raw bytes')
 actual=literal(b);need(actual==model['full_literal_stream'],'complete frozen-before-native literal stream, conjunctively validated against post-build OMF')
 need(len(actual)==1553,'complete literal count')
 owned=literal(b,SPANS);need(owned==literal(t,SPANS) and len(owned)==83,'owned83 literal order')
 outside=literal(b,SPANS,True);need(outside==literal(a,SPANS,True) and len(outside)==1470,'outside1470 literal order')
 need(header_parts(raw)==header_parts(prior),'all nonrelocation header bytes')
 # Exact image slices above plus identical file/header size cover any overlay.
 need(len(raw)==len(prior),'complete file size');ha=struct.unpack_from('<H',prior,8)[0]*16;hb=struct.unpack_from('<H',raw,8)[0]*16
 need(raw[hb+len(b.program_image):]==prior[ha+len(a.program_image):],'overlay bytes')
 special={}
 for name,span,count in [('accepted_bomb',[[0x159FF,0x15CB9]],20),('accepted_score',[[0xD50E,0xD6D4]],6),('retained_root',[[0xC0D8,0xC7A5]],None)]:
  pairs=literal(b,span);need(pairs==literal(a,span),name+' literal order');need(all(a.program_image[x:y]==b.program_image[x:y] for x,y in span),name+' raw');need(count is None or len(pairs)==count,name+' count');special[name]={'raw_equal':True,'literal_pairs':pairs}
 maps=tail_map.validate(repo,baseline,work)
 return {'raw_literal_header_overlay_pass':True,'full_raw_owned_bytes':3433,'whole_literal_count':1553,'outside_literal_count':1470,'owned_literal_count':83,'accepted_special_preservation':special,'map':maps,'pass_':True,'actual_fresh_OMF_structure_pass':True,'strict_diagnostic_match':True,'state':'PASS_RETAINED_COMPARISON','exact_acceptance':False,'limitations':['Retained comparison only; cold provenance and canonical acceptance are separate.','No global original relocation interposition proof.']}
