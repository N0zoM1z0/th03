"""Read-only validation of current MAINL decoded ownership migration parts."""
from pathlib import Path
import sys,json,hashlib,re,importlib

def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
S=[('ending',0,280,'_mainl_ending','mainl_ending','staff_prefix'),('flake_put',280,76,'@FLAKE_PUT$QIII','flake_put','staff_prefix'),('unput',356,123,'CDG_UNPUT_FOR_UPWARDS_MOTION_E_8','cdg_unput_for_upwards_motion_e_8','staff_prefix'),('clear_blue',479,21,'_mainl_clear_blue','mainl_clear_blue','staff_prefix'),('reset',500,26,'@flakes_reset$qv','flakes_reset','staff_prefix'),('spawn',526,169,'_mainl_snow_spawn','mainl_snow_spawn','snow'),('update',695,70,'_mainl_snow_update','mainl_snow_update','staff_extension'),('render',765,54,'_mainl_snow_render','mainl_snow_render','staff_extension'),('gate',819,48,'MAINL_SNOW_GATE','mainl_snow_gate','staff_extension'),('tick',867,76,'_mainl_snow_tick','mainl_snow_tick','staff_extension'),('dissolve',943,211,'CDG_PUT_DISSOLVE_E_8','cdg_put_dissolve_e_8','staff_extension'),('entrance',1154,211,'MAINL_STAFF_ENTER','mainl_staff_enter','staff_transition'),('exit',1365,183,'MAINL_STAFF_LEAVE','mainl_staff_leave','staff_transition'),('gallery',1548,52,'MAINL_STAFF_GALLERY','mainl_staff_gallery','staff_transition'),('single',1600,229,'MAINL_STAFF_SINGLE','mainl_staff_single','staff_transition'),('pair',1829,358,'MAINL_STAFF_PAIR','mainl_staff_pair','staff_paired'),('hold',2187,139,'MAINL_STAFF_HOLD','mainl_staff_hold','staff_paired'),('verdict',2326,389,'_mainl_staff_verdict','mainl_staff_verdict','staff_verdict'),('roll',2715,980,'_mainl_staff_roll','mainl_staff_roll','staff_complete')]
T=[('free_all',387,23,'CDG_FREE_ALL','cdg_free_all','root_prefix'),('win_animate',410,250,'_mainl_win_animate','mainl_win_animate','root_prefix'),('story_dispatch',660,133,'_mainl_story_dispatch','mainl_story_dispatch','root_prefix'),('stage_load',793,288,'_mainl_stage_load','mainl_stage_load','root_prefix'),('stage_intro',1081,627,'_mainl_stage_intro','mainl_stage_intro','root_intro'),('enemy_switch',1708,18,None,'mainl_stage_intro','root_intro'),('shot_pair',1726,111,'MAINL_SHOT_PAIR','mainl_shot_pair','root_shots'),('shot_load',1837,93,'MAINL_SHOT_LOAD','mainl_shot_load','root_shots'),('main',1930,528,'_main','main','root_complete_data')]
bands={'staffdat.cpp':S,'rootdata.cpp':T,'contmenu.cpp':[('continue_menu',0,417,'_mainl_continue_menu','mainl_continue_menu','continue')],'regdata.cpp':[('registration_music',2720,68,'_mainl_reg_music','mainl_reg_music','regmusic')]}
def public_offsets(raw):
 rows={}
 from lib.omf import parse_omf
 for r in parse_omf(raw):
  if r.record_type not in [0x90,0x91]:continue
  d=r.data;i=0
  def idx():
   nonlocal i
   v=d[i];i+=1
   if v&128:v=((v&127)<<8)|d[i];i+=1
   return v
  group=idx();seg=idx()
  if seg==0:i+=2
  while i<len(d):
   size=d[i];i+=1;name=d[i:i+size].decode('ascii');i+=size;w=4 if r.record_type==0x91 else 2;offset=int.from_bytes(d[i:i+w],'little');i+=w;idx();rows[name]=dict(offset=offset,segment_index=seg,group_index=group)
 return rows

def validate_mapping(root,mapping,owner_audit,work):
 """Validate15 migrated owners against source, real OMF/MAP and current compiler proof.
 Parameters: root/work Path-compatible; mapping/owner_audit parsed JSON mappings.
 Returns a compact check result; never writes a file or invokes native tooling.
 """
 root=Path(root).resolve();work=Path(work)
 if not work.is_absolute():work=root/work
 work=work.resolve();need(work.is_relative_to(root),'work outside repository')
 def file(n):
  p=root/n;need(p.is_file() and not p.is_symlink(),'missing or symlink input '+str(n));return p.read_bytes()
 def checkpin(row):
  p=Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'invalid pin path')
  b=file(p);need(sha(b)==row['sha256'] and len(b)==row['bytes'],'pin drift '+str(p));return b
 need(mapping['schema']=='mainl-current-source-owner-migrations-v1','mapping schema')
 need(mapping['resolved_owners']==15 and not mapping['remaining_gaps'],'mapping summary')
 bindings={r['path']:r for r in mapping['bindings']};need(len(bindings)==len(mapping['bindings']),'duplicate binding')
 for row in bindings.values():checkpin(row)
 proof=json.loads(checkpin(mapping['linked_proof']));linked=proof['linked']
 need(proof['diagnostic_checks_pass'] and proof['two_round_raw_repeat_equal'],'current cold proof unsuccessful')
 mapraw=checkpin(mapping['map']);need(mapraw==(work/'obj/th03/mainl.map').read_bytes(),'wrong actual work MAP');maptext=mapraw.decode('latin1')
 sys.path.insert(0,str(root/'scripts'))
 stage=importlib.import_module('stage_th03_mainl_fullcold');oldroot=stage.base.ROOT
 try:
  stage.base.ROOT=root;f,_,_,graph,_=stage.compose_all(root/'config/mainl_cold_context')
 finally:stage.base.ROOT=oldroot
 g={r['output']:r for r in graph}
 comp={'rootdata.cpp':linked['root_data_compiler']['compiler_code'],'staffdat.cpp':linked['compiler']['compiler_code'],'contmenu.cpp':linked['continue_compiler']}
 source={'rootdata.cpp':'src/mainl/root/complete_data.cpp','staffdat.cpp':'src/mainl/staff/data.cpp','contmenu.cpp':'src/mainl/root/continue.cpp','regdata.cpp':'src/mainl/hiscore/regdata.cpp'}
 pointers={'rootdata.cpp':'/linked/root_data_compiler/compiler_code','staffdat.cpp':'/linked/compiler/compiler_code','contmenu.cpp':'/linked/continue_compiler'}
 aud={r['unit_id']:r for r in owner_audit['owners']};ids=[r['unit_id'] for r in mapping['owners']]
 need(len(ids)==len(set(ids))==15,'duplicate or missing owners')
 count=0;byte_count=0
 for migration in mapping['owners']:
  owner=aud[migration['unit_id']];start=owner['decoded_linear_start'];end=start+owner['size'];expected=[]
  for old,new in [('source','historical_source'),('source_sha256','historical_source_sha256'),('decoded_linear_start','decoded_linear_start'),('size','size'),('raw_sha256','raw_sha256')]:need(owner[old]==migration[new],'historical owner drift '+new)
  need(owner['raw_equal'] and owner['ordered_relocations_equal'] and owner['reviewed_boundary'],'owner raw/relocation/boundary failed')
  need(migration['raw_equal'] and migration['ordered_relocations_equal'] and migration['reviewed_boundary'] and migration['lineage_closed'] and migration['historical_source_is_not_claimed_as_current_producer'],'invalid owner claims')
  for mp in owner['map_parts']:
   module=mp['map_module'];need(module in bands,'unexpected migrated module')
   need(len(mp['object_candidates'])==1,'ambiguous object candidate');obj=mp['object_candidates'][0];raw=(work/obj).read_bytes();digest=sha(raw)
   need(digest==owner_audit['fresh_objects'][obj]['sha256'],'actual object drift');pubs=public_offsets(raw)
   src=source[module];need(src in bindings,'unbound maintained source');maintained=file(src)
   transformed=maintained.replace(b'-zCCONTINUE_TEXT',b'-zCCUTSCENE_TEXT') if module=='contmenu.cpp' else maintained
   need(transformed==f[module]==(work/module).read_bytes(),'maintained/composed/consumed source mismatch');need(g[obj]['source']==src and g[obj]['wrapper']==module,'object source graph mismatch')
   if module in comp:
    c=comp[module];need(c['module']==module and c['object_sha256']==digest and c['diagnostic_checks_pass'] and c['non_fixup_bytes_equal'],'compiler object/band proof mismatch')
   for name,off,size,symbol,function,family in bands[module]:
    pos=mp['start']+off;stop=pos+size
    if not(start<=pos and stop<=end):continue
    need(stop<=mp['end'],'part outside MAP contribution')
    if symbol:
     need(symbol in pubs and pubs[symbol]['offset']==off and pubs[symbol]['segment_index']==1,'OMF public boundary mismatch')
     label={'@FLAKE_PUT$QIII':'flake_put(int,int,int)','@flakes_reset$qv':'flakes_reset()'}.get(symbol,symbol)
     found={int(x,16)*16+int(y,16) for x,y in re.findall(r'^\s*([0-9A-Fa-f]{4}):([0-9A-Fa-f]{4})\s+(?:idle\s+)?'+re.escape(label)+r'\s*$',maptext,re.M)}
     need(found=={pos},'MAP public coordinate mismatch')
    band=[]
    if module in comp:
     band=[b for b in comp[module]['body_bands'] if b['offset']<=off and off+size<=b['offset']+b['size']]
     need(len(band)==1 and not band[0]['non_fixup_difference_offsets'],'compiler band containment mismatch')
    lines=[i+1 for i,line in enumerate(maintained.decode().splitlines()) if re.search(r'\b'+re.escape(function)+r'\s*\(',line) and not line.rstrip().endswith(';')];need(lines,'source function absent')
    familyproof='config/mainl_'+family+'_backend/proof.json';need(familyproof in bindings,'unbound migration proof');pf=json.loads(file(familyproof));need(pf['composer_path'] in bindings,'unbound migration composer')
    expected.append(dict(decoded_linear_start=pos,size=size,object=obj,object_sha256=digest,module=module,map_segment=mp['map_segment'],map_module_start=mp['start'],object_segment_offset=off,public=symbol,source=src,source_sha256=sha(maintained),generated_source_sha256=sha(f[module]),source_transport=('declared CONTINUE_TEXT to CUTSCENE_TEXT pragma by mainl_continue_backend.generate' if module=='contmenu.cpp' else 'byte-identical maintained source'),source_function=function,source_line_candidates=lines,compiler_band=band[0] if band else None,compiler_evidence_pointer=pointers.get(module),migration_backend=family,migration_proof=familyproof,migration_composer=pf['composer_path']))
  expected.sort(key=lambda r:r['decoded_linear_start']);need(migration['parts']==expected,'migration parts differ from actual source/OMF/MAP/compiler evidence')
  cursor=start
  for part in expected:need(part['decoded_linear_start']==cursor,'noncontiguous owner partition');cursor+=part['size']
  need(cursor==end,'owner extent incomplete');count+=len(expected);byte_count+=end-start
 need(count==30 and byte_count==6251,'migration scope changed')
 return dict(valid=True,owners=15,parts=count,decoded_bytes=byte_count,native_execution_performed=False,output_mutations=False)
