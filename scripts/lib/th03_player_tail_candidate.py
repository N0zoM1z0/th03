"""Exact four-producer tail candidate on accepted score plus bomb, opt-in only.

Expected relocation model freezes before native; fresh OMF structure is checked
post-build, conjunctively with actual raw/order and complete MAP/provider proof.
No imports from ignored executable scripts and no acceptance promotion.
"""
from pathlib import Path
import hashlib,json,os,re,stat,struct,tomllib
from lib import th03_score_candidate as score, th03_yumemi_bomb_candidate as bomb
from lib.omf import normalize_dependency_timestamps,parse_omf
require=score.require
digest=score.digest
CANDIDATE_PATH='config/th03_main_player_tail_candidate.toml'
BASELINE='.analysis/th03-main-exact/gpt-dots-yumemi-bomb-default-cold-v01'
PROOF_GUARD='.analysis/gpt-dots-player-tail-retained-probe-v06/proof-guards.json'
PROOF_GUARD_SHA='a7bc552685ad423f148f32e870e67441683b33db2d61de4e09b391e5895db993'
EXPECTED_STREAM_SHA='ca8c5677d1b4cb31637142a280bb491e6823ca23c3372a168824b9dd2dfcab98'
ROOT_AFTER='759aea527019dff7355cd831cc33176d60eb62d35ef0a8ce3dbd55f210c8bfa8'
RESPONSE_AFTER='5eb21ee316fc68a7ae0ac083ef9cceb1a20f3a0055a0a4db6c6de3bf427e9c87'
EXTRA_GAME_PATHS=('obj/chain1.obj','obj/chain2.obj')
OBJECTS={'warning':'obj/th03/warning.obj','effects':'obj/th03/effects.obj','chain1':'obj/chain1.obj','chain2':'obj/chain2.obj'}
CANDIDATE_DIGEST='1e481c06b42ccec8a7b8049353ebc8690f447f6fc1b0f3ca72c9535ab7eba039'
UNIT_DIGESTS={'th03-main-player-warning': '4bed49019db49fec8be042932faf336f9d7f68d4a4a055bb20f506317e80b4b6', 'th03-main-player-effects': '788ac6152092555ffcf41976d23d956a1e2f5d28468f527af54cc6b8535b9ae8', 'th03-main-background-chain1': 'bf9c0cf47b1b4a608fdd61df456411654f3c4d608547acae8b8025e5d202a325', 'th03-main-background-chain2': 'd6dc40b14e95bc74f7cefb9dfbb37e1dfbb145efede80a2ee9efd1b67448387f'}
SOURCE_PINS={'src/main/player/warning.cpp': '6e98cfcd5841b821b2f9a5cadbb81d9cbf854c40816ce90b553eae1c3b044c88', 'src/main/player/warning.hpp': '2f49844c5b31ca454550a4998076990d9d0f372bddddad108f32e9096ffc302a', 'compat/rec98/libs/master.lib/master.hpp': '8e279919734d76e7b9b4012255fa19b969733338a69d4aed32d6f2cdc081a7a1', 'compat/rec98/libs/master.lib/pc98_gfx.hpp': '4c2e88288d6143efea4dd835b9966423ddb154959596de52f897a65701ac39a4', 'compat/rec98/platform.h': 'f7223107a5221902365ce989ae1b9483cef3925e75c0f739e439a4ed432875cc', 'compat/rec98/th01/math/subpixel.hpp': 'e36a587c8e6b88d1ce71fb3f891c45f0511c8fcfe118ca2a5c6fbe7b082e33bf', 'compat/rec98/th02/snd/snd.h': '3a19e42a01b74089c5420729316bcb4c3bd5b135a8ceb5b12ec50e3ba96a2f4f', 'compat/rec98/th03/common.h': '0960e997cd75fafc79df7b8626ebd71eaf90023215f5f90d66ebd0f5c15cb349', 'compat/rec98/th03/formats/mrs.hpp': 'c85d70d73c753b0ad8b4cd53cad15dd5dd7aae0c53f193f68ce2273af1956d75', 'compat/rec98/th03/hardware/palette.hpp': '8efa94e00d0e1034df4e390ad105335ff6da5e8e7148cf6dab10b3ef533df153', 'compat/rec98/th03/main/hud/warning.hpp': '1f25e6f733c8a0cdae8b1761e1906201f2fbe47751ac52de40df77a9acbf7b22', 'compat/rec98/th03/main/player/gba.hpp': '935aeed3342e68e46b618cbbe55842fb8065185f5044fe46df52cd8b3e9ca7cd', 'compat/rec98/th03/main/player/stuff.hpp': '1c7e6c04c5bc8d095fb4aacdfb35c89692dd3eb67e33fd87bfbe0efd2c2f5162', 'compat/rec98/th03/main/round.hpp': '859f5128a171ec9c9c1af84dbc10f8910b30c6f0061ee27c1d87936d8f8eea9f', 'compat/rec98/th03/main/sprite16.hpp': '9f115278422305ffa1694653bbca486b1225e6f7faaac417341f27edeb0278b0', 'compat/rec98/th03/resident.hpp': 'a0b051bae0d91f8d2c557e1832d33eb5c46cbef89a8c8f4eda63964893402e76', 'src/main/background/background.hpp': '071a39ad619b3b33e9e7b1af79826feae1b21dcb1f0f06e678972c63c7e78eea', 'src/main/background/chain1.cpp': '424859274a2715d1c12524029ac938e956d0f97f45ea844a0519c3abbc3a282c', 'src/main/background/chain2.cpp': '9df0082943bc6a9b28f59b620f18a70f3a2b3a2cfc584a89ab570649532c3fcd', 'src/main/background/phase.inl': 'c1259cf6088d68ca2bebe916eec8c0ff84074a1721c28802f40b8b1de5c2fe57', 'src/main/hardware/frame_delay.hpp': 'c5eb79972c3e605a906b2a2ad9b9565aca151eb321cd5b1037fe8da53842c229', 'src/main/hud/static.hpp': 'af739792e942fa4aeb8d247f943238ef461b4cee0d29468b49fa44b7900afbff', 'src/main/math/polar.hpp': '18b781662d422ae6f5dce88cd15f2423d87e092493dc9fd1cd3b97c4956d1f3a', 'src/main/math/randring_getters.hpp': '5abdaac6c6ed77ab6dc68f6c0c3590604a08cac533bed6d2bab8025eb2ae0270', 'src/main/math/vector_far.hpp': '8970b384db3a35a784c474d9663d753b2ce777cfe1bbe6ce0fdadf34c533f385', 'src/main/player/effects.cpp': '756cd7a39a43d487dfe5ff26c51fd6c467d9e66fe215ca76be2d299a0397cd53', 'src/main/player/effects.hpp': 'bdafcf01031ea427cb00a41789ca3169564b97ba3d7ec789f61e183bc33f352b', 'src/main/playfield/playfld.hpp': '2688b57cb7d563ee4aa65a33a2ed2563a032670bf83056e14cfdab1b34901046'}

ROOT_SHA='356b650b19c833abbbc3e8daf381879c1519df1e83a460723c3e83f386401446'
RSP_SHA='cfa529524d2e45b5306f6586d5715a3094e9e924fa8dd3c76659ace585baf143'
SYMBOLS=[('sub_C7A5','_round_pause_or_quit','near'),('sub_C830','_round_C830','near'),('sub_C8C4','_round_C8C4','near'),('sub_C9FE','ROUND_C9FE','far'),('sub_CA3C','_round_CA3C','far'),('sub_CACB','WARNING_TEXT_PUT','near'),('sub_CB81','ROUND_CB81','far'),('sub_CDBD','BOMB_EXPLOSION_ADD','far'),('sub_CE0C','BOMB_CENTER_ADD','far'),('sub_CE5B','BOMB_AXIS_ADD','far'),('sub_CEB2','@player_effects_update$qv','far'),('sub_CEE0','@player_effects_render$qv','far'),('sub_D031','@background_pixel_di$qv','near'),('sub_D05D','@background_velocity_reset$qv','far'),('sub_D092','@background_chain1_init$qv','far'),('sub_D0FA','@background_update_di$qv','near'),('sub_D135','@background_chain1_accelerate$qv','far'),('sub_D1E7','@background_chain1_periodic$qv','far'),('sub_D2E8','@background_chain2_init$qv','far'),('sub_D340','@background_chain2_accelerate$qv','far'),('sub_D3F9','@background_chain2_periodic$qv','far')]
HELPERS=[('sub_B398','_hud_gauge_highlight_fill'),('sub_B3A2','_hud_gauge_highlights_restore'),('sub_B3F6','_hud_gauge_bar_fill')]
DATA=[('gbWARNING_1','_warning_title_top','byte'),('gbWARNING_2','_warning_title_middle','byte'),('gbWARNING_3','_warning_title_bottom','byte'),('gpYOU_ARE_FORCED_TO_EVADE_FROM','_warning_forced_to_evade','byte'),('gpGAUGE_ATTACK_LEVEL','_warning_gauge_level','byte'),('gpBOSS_ATTACK_LEVEL','_warning_boss_level','byte'),('gpYOUR_LIFE_IS_IN_PERIL_BE_CAREFUL','_warning_life_in_peril','byte'),('asc_1DD5A','_warning_clear_line','byte'),('byte_23B00','_round_quit_requested','byte'),('byte_20F1E','_player_effect_cursor','byte'),('farfp_20F24','_background_render','dword'),('angle_2142C','_background_angle','byte')]
def sha(b):return hashlib.sha256(b).hexdigest()
def once(t,old,new):
 if t.count(old)!=1:raise ValueError('nonunique anchor '+repr(old))
 return t.replace(old,new)
def transform(raw):
 if sha(raw)!=ROOT_SHA:raise ValueError('baseline root identity')
 return edit_root(raw)
def edit_root(raw):
 """Apply the reviewed whole-function and storage-interface source edits."""
 t=raw.decode('latin1');a=t.index('sub_C7A5\tproc near');b=t.index('sub_D3F9\tendp')+len('sub_D3F9\tendp');removed=t[a:b]
 if re.findall(r'^(\S+)\s+proc\s+(near|far)',removed,re.M)!=[(x,z) for x,y,z in SYMBOLS]:raise ValueError('whole 21-function interval')
 # Preserve the complete genuine module constant group verbatim.
 declarations=re.findall(r'^(\w+)[ \t]*=[ \t]*([^\r\n]+)',removed,re.M)
 globals_=[(n,v) for n,v in declarations if not n.startswith(('var_','arg_'))]
 if globals_!=[('WARNING_FLASH_RED_FRAMES','30'),('WF_NONE','0'),('WF_PORTRAIT','1'),('WF_FLASH_WHITE','2'),('WF_FLASH_RED','3'),('WF_FLASH_RED_END','(WF_FLASH_RED + WARNING_FLASH_RED_FRAMES)')]:raise ValueError('module constant inventory changed')
 outside=t[:a]+t[b:]
 needed=[(n,v) for n,v in globals_ if re.search(r'\b'+re.escape(n)+r'\b',outside)]
 if needed!=[('WF_NONE','0'),('WF_PORTRAIT','1')]:raise ValueError('surviving constant dependency changed')
 retained=removed[removed.index('WARNING_FLASH_RED_FRAMES = 30'):removed.index('WF_FLASH_RED_END = (WF_FLASH_RED + WARNING_FLASH_RED_FRAMES)')+len('WF_FLASH_RED_END = (WF_FLASH_RED + WARNING_FLASH_RED_FRAMES)')]+'\r\n'
 t=t[:a]+retained+'; Complete 3433-byte tail supplied by four maintained semantic producers.'+t[b:]
 t=once(t,'\tpublic sub_B39E, sub_A3D2, sub_CE0C, sub_CE5B, sub_A3A8, sub_CDBD','\tpublic sub_B39E, sub_A3D2, sub_A3A8')
 t=once(t,'\tpublic _bomb_bg_fill, BOMB_EXPLOSION_ADD, PALETTE_RESTORE_FOR_PID','\tpublic _bomb_bg_fill, PALETTE_RESTORE_FOR_PID')
 t=once(t,'\tpublic BOMB_PALETTE_STEP, BOMB_CENTER_ADD, BOMB_AXIS_ADD','\tpublic BOMB_PALETTE_STEP')
 for old,new,distance in SYMBOLS[7:10]:t=once(t,new+' = '+old+'\r\n','')
 refs={}
 for old,new,distance in SYMBOLS:
  pattern=r'\b'+re.escape(old)+r'\b';n=len(re.findall(pattern,t));refs[old]=n;t=re.sub(pattern,lambda m:new,t)
 imports='; Genuine producer linkage, with original call distances.\r\n'+''.join('\textern '+new+':'+distance+'\r\n' for old,new,distance in SYMBOLS if refs[old])
 t=once(t,'WARNING_FLASH_RED_FRAMES = 30\r\n',imports+'WARNING_FLASH_RED_FRAMES = 30\r\n')
 # Local far nopcall was NOP+PUSH CS+E8 (five bytes). A genuine external
 # explicit NOP/PUSH CS/NEAR PTR CALL preserves original far-return stack semantics.
 # Original compatibility NOP and real CS operand; retained linked proof passed.
 lowered=[]
 for old,new,distance in SYMBOLS:
  pattern=r'(?m)^(\t\t)nopcall\t'+re.escape(new)+r'(?=\r?$)'
  count=len(re.findall(pattern,t))
  if count:
   if distance!='far':raise ValueError('near nopcall transition')
   lowered.extend([new]*count)
   t=re.sub(pattern,lambda m:m.group(1)+'nop\r\n'+m.group(1)+'push cs\r\n'+m.group(1)+'call near ptr '+new,t)
 if sorted(lowered)!=sorted(['@player_effects_update$qv','@player_effects_render$qv','_round_CA3C','ROUND_CB81','ROUND_CB81','ROUND_C9FE','ROUND_C9FE','BOMB_EXPLOSION_ADD']):raise ValueError('eight exact nopcall transitions')
 for old,new in HELPERS:
  t=once(t,old+'\tproc near','public '+new+'\r\n'+new+' label near\r\n'+old+'\tproc near')
 for old,new,kind in DATA:
  matches=list(re.finditer(r'^'+re.escape(old)+r'[\t ]+(?:db|dw|dd)\b',t,re.M))
  if len(matches)!=1:raise ValueError('data definition '+old)
  p=matches[0].start();t=t[:p]+'public '+new+'\r\n'+new+' label '+kind+'\r\n'+t[p:]
 # Add labels within the same preexisting uninitialized storage; preserve count/order.
 t=once(t,'\t\tdb 4 dup(?)\r\npublic _gba_flag_next','public _warning_brightness, _warning_fading_out\r\n_warning_brightness label byte\r\n\t\tdb 2 dup(?)\r\n_warning_fading_out label byte\r\n\t\tdb 2 dup(?)\r\npublic _gba_flag_next')
 t=once(t,'include th03/main/player/combo[bss].asm\r\n\t\tdb 120 dup(?)','include th03/main/player/combo[bss].asm\r\npublic _player_effects\r\n_player_effects label byte\r\n\t\tdb 120 dup(?)')
 for old,new,distance in SYMBOLS:
  if re.search(r'\b'+re.escape(old)+r'\b',t):raise ValueError('old deleted entry remains '+old)
 for s in ['MOVE_INVALID = 0','MOVE_VALID = 1','MOVE_NOINPUT = 2','@PLAYER_POS_UPDATE_AND_CLAMP$QR7SPPOINT procdesc pascal near','@PLAYER_MOVE$QUI procdesc pascal near',"BINARY = 'M'"]:
  if t.count(s)!=raw.decode('latin1').count(s):raise ValueError('retained zero-byte declaration '+s)
 return t.encode('latin1'),refs
def response(raw):
 if sha(raw)!=RSP_SHA:raise ValueError('baseline response identity')
 anchor=b'obj\\th03\\main.obj obj\\th03\\score_hud.obj'
 addition=b'obj\\th03\\main.obj obj\\th03\\warning.obj obj\\th03\\effects.obj obj\\chain1.obj obj\\chain2.obj obj\\th03\\score_hud.obj'
 if raw.count(anchor)!=1:raise ValueError('response insertion anchor')
 return raw.replace(anchor,addition)


def is_tail_owner(unit):
    return unit.get('id') in UNIT_DIGESTS and digest(unit)==UNIT_DIGESTS[unit['id']]

def bind_candidate(accepted, additions, manifest_name):
    bomb.bind_default(accepted)
    require(manifest_name==CANDIDATE_PATH and digest(additions)==CANDIDATE_DIGEST,'tail descriptor identity')
    require(len(additions['units'])==4 and all(is_tail_owner(u) for u in additions['units']),'exact four tail owners')
    require(len(additions['functions'])==21 and sum(f['size'] for f in additions['functions'])==3433,'exact tail functions/bytes')

DEFAULT_CONFIG_DIGEST = '8830005f5c1429d04cf49a79fbd0e703eb0667ec42d815548c440c76cc298c05'

def pre_tail_config(accepted):
    """Reverse only the exact final four tail owners and 21 functions."""
    import copy
    require(digest(accepted)==DEFAULT_CONFIG_DIGEST,'default tail configuration drift')
    result=copy.deepcopy(accepted)
    additions={'schema_version':1,'units':result['units'][-4:],'functions':result['functions'][-21:]}
    require(digest(additions)==CANDIDATE_DIGEST,'default exact tail descriptors drift')
    del result['units'][-4:];del result['functions'][-21:]
    bomb.bind_default(result)
    return result

def bind_default(accepted):
    import copy
    _,original=bomb.bind_default(pre_tail_config(accepted))
    return copy.deepcopy(accepted),original

def check_sources(work):
    for n,h in SOURCE_PINS.items():
        p=Path(work)/n
        require(p.is_file() and not p.is_symlink() and sha(p.read_bytes())==h,'tail source changed: '+n)

def guard_baseline(root):
    root=Path(root);raw=(root/PROOF_GUARD).read_bytes();require(sha(raw)==PROOF_GUARD_SHA,'tail historical guard identity')
    saved=json.loads(raw);prefix=BASELINE+'/';files={n[len(prefix):]:h for n,h in saved['files'].items() if n.startswith(prefix)}
    require(files and 'receipt.json' in files,'complete accepted default baseline guard')
    base=root/BASELINE;actual={p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file()}
    require(actual==set(files),'accepted default proof file inventory')
    pins={}
    for n,h in files.items():
        p=base/n;require(not p.is_symlink() and sha(p.read_bytes())==h,'accepted default proof changed: '+n)
        mode=stat.S_IMODE(p.stat().st_mode);require(mode==saved['modes'][prefix+n],'accepted proof mode changed')
        pins[n]={'sha256':h,'bytes':p.stat().st_size,'mode':oct(mode)}
    return pins

def freeze_expected(root):
    from lib import th03_tail_model as model
    root=Path(root);base=root/BASELINE/'round1/source'
    retained=root/'.analysis/gpt-dots-player-tail-retained-probe-v06/run-first-v01/source'
    expected=model.build_model(root,base,retained/'obj/th03/main.obj',{n:retained/p for n,p in OBJECTS.items()},(retained/'obj/th03/main.@l').read_bytes())
    pairs=expected['full_literal_stream'];require(len(pairs)==1553 and sha(b''.join(struct.pack('<HH',o,s) for s,o in pairs))==EXPECTED_STREAM_SHA,'frozen expected stream')
    return {'stream':pairs,'stream_sha256':EXPECTED_STREAM_SHA,'timing':'Frozen before cold native; actual fresh OMF structure is mandatory post-build, not prelink actual-root proof'}

def precompile_and_stage(work,env,logs,execute,default=False):
    from lib import th03_tail_compare as compare
    work,logs=Path(work),Path(logs);check_sources(work);bomb.check_sources(work);bomb.check_build(work,default=True)
    require(sha((work/'th03_main.asm').read_bytes())==ROOT_SHA,'tail must follow accepted bomb stage')
    # Prior successful fresh bomb compilation is a required lifecycle boundary.
    bomb.validate_object((work/bomb.OBJECT).read_bytes())
    require(not (work/bomb.ALIAS).exists() and not (work/'obj/th03/bm_yume.obj').exists(),'duplicate bomb object')
    require(all(not (work/p).exists() for p in OBJECTS.values()),'cached tail object')
    rows=[]
    for name,path in OBJECTS.items():
        source=compare.PRODUCERS[name]['source'];output=work/path
        require(not output.exists() and not output.is_symlink(),'stale producer output')
        output.parent.mkdir(parents=True,exist_ok=True)
        require(all(not p.is_symlink() for p in [output.parent,work/'obj',work]),'symlink producer parent')
        before={p.relative_to(work).as_posix():sha(p.read_bytes()) for p in (work/'obj').rglob('*.obj')}
        dest=Path(path).parent.as_posix()+'/'
        argv=['wine','cmd','/d','/c',r'set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%&&bin\msdos -e -x tcc -c -I. -O -b- -3 -Z -d -DGAME=3 -ml '+"-DBINARY='M' -n"+dest+' '+source]
        result=execute(argv,work,env,logs/(name+'-maintained-compile.log'));require(result.get('exit_code')==0,'tail compile failed: '+name)
        after={p.relative_to(work).as_posix():sha(p.read_bytes()) for p in (work/'obj').rglob('*.obj')}
        require(set(after)-set(before)=={path} and all(after.get(n)==h for n,h in before.items()),'unexpected producer outputs/mutation')
        check_sources(work);bomb.check_build(work,default=True);require(sha((work/'th03_main.asm').read_bytes())==ROOT_SHA,'compile changed unstaged root')
        proof=compare.validate_producer(name,output,Path(__file__).resolve().parents[2],parse_omf)
        rows.append({'name':name,'path':path,'source':source,'compile':result,'schema':proof,'normalized_sha256':sha(normalize_dependency_timestamps(output.read_bytes())),'cached_object_used':False})
    raw=(work/'th03_main.asm').read_bytes();new,_=transform(raw);require(sha(new)==ROOT_AFTER,'tail transformed root pin')
    build=work/'build.bat';rawbuild=build.read_bytes();require(rawbuild.count(bomb.BUILD_BEFORE)==1 and bomb.BUILD_AFTER not in rawbuild,'tail scheduling carrier boundary')
    if default:
        # Default Schedule requires the original carrier and local jobs=1.
        changed=rawbuild
    else:
        changed=rawbuild.replace(bomb.BUILD_BEFORE,bomb.BUILD_AFTER,1)
        require(sha(changed)==bomb.BUILD_STAGED_SHA,'tail scheduling carrier pin')
    (work/'th03_main.asm').write_bytes(new)
    if not default:build.write_bytes(changed)
    bomb.check_build(work,default=default)
    return {'producers':rows,'root_sha256':ROOT_AFTER,'build_sha256':sha(changed),'fresh_native_compilations':4,'root_assembler':'unchanged Tup rule and generated sprite dependencies','cached_objects_used':False,'default_staging':default}


def scoped_game_objects(game_objects,all_objects):
    require(all(n in all_objects and n not in game_objects for n in EXTRA_GAME_PATHS),'two explicit background object paths')
    return {**game_objects,**{n:all_objects[n] for n in EXTRA_GAME_PATHS}}

def check_round(root,work,target,proof,expected,default=False):
    from lib import th03_tail_model as model,th03_tail_compare as compare,pc98
    from lib import th03_score_candidate as parser
    root,work=Path(root),Path(work);check_sources(work);bomb.check_sources(work);bomb.check_build(work,default=default)
    require(sha((work/'th03_main.asm').read_bytes())==ROOT_AFTER,'tail root source changed')
    require(sha((work/'obj/th03/main.@l').read_bytes())==RESPONSE_AFTER,'tail literal response changed')
    bomb.validate_object((work/bomb.OBJECT).read_bytes())
    require(not (work/bomb.ALIAS).exists() and not (work/'obj/th03/bm_yume.obj').exists(),'extra bomb alias object')
    require(sha(normalize_dependency_timestamps((work/'obj/th03/score_hud.obj').read_bytes()))==score.SCORE_OMF_NORMALIZED_SHA,'accepted score object drift')
    producers={n:compare.validate_producer(n,work/p,root,parse_omf) for n,p in OBJECTS.items()}
    base=root/BASELINE/'round1/source'
    actual_model=model.build_model(root,base,work/'obj/th03/main.obj',{n:work/p for n,p in OBJECTS.items()},(work/'obj/th03/main.@l').read_bytes())
    require(actual_model['full_literal_stream']==expected['stream'] and expected['stream_sha256']==EXPECTED_STREAM_SHA,'fresh OMF structure/prediction changed')
    # Structural failure must stop before any linked-byte success can contribute.
    linked=compare.check_link(work,root,base,actual_model,pc98,parser)
    require(linked['pass_'],'complete tail raw/order/MAP/provider conjunction')
    def old(n):return score.read_pinned(root/BASELINE/n,proof[n])
    receipt=json.loads(old('receipt.json'));accepted=tomllib.loads((root/'config/th03_main_exact_units.toml').read_text())
    if default:accepted=pre_tail_config(accepted)
    bomb.bind_default(accepted)
    allpaths={p.relative_to(work).as_posix() for p in (work/'obj').rglob('*.obj')};game={n for n in allpaths if any(n.startswith(d+'/') for d in accepted['determinism_object_roots'])}
    checks=[]
    for number in (1,2):
        prefix=f'round{number}/source/';prior=receipt['rounds'][number-1]
        products=sorted(n[len(prefix):] for n in proof if n.startswith(prefix) and re.fullmatch(r'bin/th0[1-5]/[^/]+\.(?:exe|com)',n[len(prefix):]));maps=sorted(n[len(prefix):] for n in proof if n.startswith(prefix) and n.endswith('.map'))
        require(len(products)==31 and len(maps)==43,'accepted product/MAP vector')
        current_products=sorted(p.relative_to(work).as_posix() for p in (work/'bin').rglob('*') if p.is_file() and re.fullmatch(r'bin/th0[1-5]/[^/]+\.(?:exe|com)',p.relative_to(work).as_posix()))
        require(current_products==products and sorted(p.relative_to(work).as_posix() for p in work.rglob('*.map'))==maps,'cold product/MAP inventory')
        require(game==set(prior['game_objects'])|{OBJECTS['warning'],OBJECTS['effects']},'exact legacy game-root object paths')
        require(allpaths==set(prior['all_objects'])|set(OBJECTS.values()),'exact complete object paths')
        require((work/'obj/th03/main.@l').read_bytes()==response(old(prefix+'obj/th03/main.@l')),'complete literal response composition')
        other_products=all((work/n).read_bytes()==old(prefix+n) for n in products if n!='bin/th03/main.exe')
        other_maps=all((work/n).read_bytes()==old(prefix+n) for n in maps if n!='obj/th03/main.map')
        prior_objects=all(sha(normalize_dependency_timestamps((work/n).read_bytes()))==h for n,h in prior['game_objects'].items() if n!='obj/th03/main.obj')
        require(other_products and other_maps and prior_objects,'accepted non-MAIN products/maps/nonroot objects changed')
        group_inventory=bomb.groups((work/'obj/th03/main.map').read_text('ascii'))==bomb.groups(old(prefix+'obj/th03/main.map').decode('ascii'))
        require(group_inventory,'accepted complete MAP group inventory changed')
        # Every inherited score/bomb raw and storage check remains conjunctive.
        b=pc98.parse_mz(old(prefix+'bin/th03/main.exe'));c=pc98.parse_mz((work/'bin/th03/main.exe').read_bytes());t=pc98.parse_mz(target)
        score_checks={'new366_raw_and_six_literal_order':score.ordered_literal(t,score.SPANS)==score.ordered_literal(c,score.SPANS)==score.PAIRS and all(t.program_image[a:z]==c.program_image[a:z] for a,z in score.SPANS),'score_add88_raw_no_relocations':sha(c.program_image[0xD5B0:0xD608])==score.BINDING['owned_raw_sha256'] and not score.ordered_literal(c,[[0xD5B0,0xD608]]),'storage_equal':all(b.program_image[s*16+o:s*16+o+n]==c.program_image[s*16+o:s*16+o+n] and score.ordered_literal(b,[[s*16+o,s*16+o+n]])==score.ordered_literal(c,[[s*16+o,s*16+o+n]]) for s,o,n,k,*_ in score.map_rows(old(prefix+'obj/th03/main.map').decode('ascii')) if k in ('DATA','BSS','STACK') and n),'complete_score_MAP_contributions':all(r in score.map_rows((work/'obj/th03/main.map').read_text('ascii')) for r in score.map_rows(old(prefix+'obj/th03/main.map').decode('ascii')) if r[6]==score.MODULE)}
        bomb_checks={'bomb698_raw_and_20_literal_order':t.program_image[0x159FF:0x15CB9]==c.program_image[0x159FF:0x15CB9] and score.ordered_literal(c,bomb.SPANS)==bomb.PAIRS,'angle_storage':b.program_image[0x1DCEC:0x1DCF2]==c.program_image[0x1DCEC:0x1DCF2]==bytes.fromhex('c0156b40eb95')}
        require(all(score_checks.values()) and all(bomb_checks.values()),'accepted score/bomb local preservation')
        checks.append({'baseline_round':number,'score_checks':score_checks,'bomb_checks':bomb_checks,'other30_products':other_products,'other42_maps':other_maps,'prior_nonroot_objects':prior_objects,'group_inventory':group_inventory,'pass_':True})
    providers=bomb.check_providers(root,work);require(providers['pass_'],'accepted bomb providers')
    return {'pass_':True,'baselines':checks,'fresh_structural_model':actual_model,'linked':linked,'producer_schemas':producers,'accepted_bomb_providers':providers,'score_preservation':{'pass_':True,'baselines':[x['score_checks'] for x in checks]},'bomb_preservation':{'pass_':True,'baselines':[x['bomb_checks'] for x in checks]},'exact_acceptance':False,'timing':'Expected frozen before native, actual fresh OMF structural proof checked post-build'}
