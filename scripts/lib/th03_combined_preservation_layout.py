"""Pure combined-candidate gates. No compiler, runner, or acceptance side effects."""
import hashlib
import importlib.util
import re
from pathlib import Path
from lib.pc98 import parse_mz
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('historical_layout',ROOT/'scripts/lib/th03_preservation_layout.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
TARGET_SHA=old.TARGET_SHA
require=old.require
relocs=old.relocs
contributions=old.contributions
ALIASES=dict(old.ALIASES,**{'_reimu_gauge_frame':0x2D68,'_reimu_chargeshots':0x2D6A,'_reimu_chargeshot_p':0x306A,'_reimu_chargeshot_alternate_hit_f':0x306C,'_reimu_bomb_particles':0x3080,'_reimu_bomb_particle_p':0x3280})
ALIASES.update({'_mima_chargeshot_angles': 1656, '_mima_gauge_angle': 14224, '_mima_gauge_angle_step': 14226, '_mima_gauge_frame': 14228, '_mima_chargeshots': 14230, '_mima_chargeshot_p': 14530, '_mima_chargeshot_active': 14532, '_mima_chargeshot_frame': 14534, '_mima_bomb_columns': 26778, '_mima_bomb_column_p': 26842})
PARTS=[(0x900,1509,'th03/cs_mari.cpp'),(0xEE5,449,'th03/bm_mari.cpp'),(0x10A6,1448,'th03/cs_reimu.cpp'),(0x164E,925,'th03/bm_reish.cpp'),(0x19EB,1338,'th03/cs_mima.cpp'),(0x1F25,266,'th03/hitbox.cpp')]
def check_layout(rows,split=True):
    require(split is True,'combined candidate requires six producers')
    for off,size,module in PARTS:
        require(rows.count((0x139D,off,size,'CODE','HITBOX_TEXT','MAIN_04',module,28))==1,'MAP ownership mismatch: '+module)
    overlap=[r for r in rows if r[3]=='CODE' and r[2] and r[0]*16+r[1]<0x159FF and r[0]*16+r[1]+r[2]>0x142D0]
    require(len(overlap)==6,'unexpected overlapping CODE contribution')
    for _,_,module in PARTS[:5]:
        for kind in ('DATA','BSS'):
            found=[r for r in rows if r[6]==module and r[3]==kind]
            require(bool(found) and all(r[2]==0 for r in found),'missing/nonzero '+kind+': '+module)
    for row in [(0x139D,0x1F25,0,'CODE','HITBOX_TEXT','MAIN_04','th03_main.asm',28),(0x139D,0x3673,0,'CODE','BULLET_TEXT','MAIN_04','th03/ex_ord.cpp',28),(0x139D,0x3673,833,'CODE','BULLET_TEXT','MAIN_04','th03/bm_mima.cpp',28),(0x139D,0x39B4,0,'CODE','BULLET_TEXT','MAIN_04','th03_main.asm',28),(0x139D,0x39B4,0xA2A,'CODE','BULLET_TEXT','MAIN_04','th03/bullet.cpp',28)]:
        require(rows.count(row)==1,'Mima bomb/tail MAP mismatch: '+repr(row))
    overlap=[r for r in rows if r[3]=='CODE' and r[2] and r[0]*16+r[1]<0x17384 and r[0]*16+r[1]+r[2]>0x17043]
    require(len(overlap)==1,'unexpected bomb contributor')
    for kind in ('DATA','BSS'):
        found=[r for r in rows if r[6]=='th03/bm_mima.cpp' and r[3]==kind]
        require(bool(found) and all(r[2]==0 for r in found),'missing/nonzero bomb '+kind)
def check_aliases(text):
    for name,off in ALIASES.items():
        found=re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+'+re.escape(name)+r'\s*$',text,re.M)
        require(bool(found) and set(found)=={('1D56',f'{off:04X}')},'alias moved/absent: '+name)
def check_launch(plan,root,read):
    require(plan.get('launch_ready') is True and plan.get('unresolved')==[], 'launch pins unresolved; proposal is not executable evidence')
    for key in ('verifier_sha256','layout_helper_sha256','supervisor_script_sha256','schedule_adapter_sha256','original_replay_sha256','candidate_manifest_sha256','source_bindings_sha256'):
        require(isinstance(plan.get(key),str) and re.fullmatch('[0-9a-f]{64}',plan[key]),'missing launch pin: '+key)
    require(set(plan.get('expected_source_inputs',{}))=={'default','candidate'} and all(plan['expected_source_inputs'].values()),'fresh frozen source inventories unresolved')
    require(plan.get('input_pins') and plan.get('source_bindings'),'complete source/tool pins required')
    for path,pin in plan['input_pins'].items():
        require(hashlib.sha256(read(root/path)).hexdigest()==pin,'launch input drift: '+path)
    require(hashlib.sha256(read(root/plan['source_bindings'])).hexdigest()==plan['source_bindings_sha256'],'source binding drift')
def scope(config):
    units=[];producers=[]
    for u in config['units']:
        extents=u.get('code_extents')
        if extents is None:
            extents=[dict(name='code',ledger_id=u['id'],start=u['start'],size=u['size'],segment=u.get('segment',config.get('segment')),producer_ranges=[dict(relative=o,size=n,kind='padding') for o,n in u.get('padding_ranges',[])])]
        for e in extents:
            lo=e.get('segment',u.get('segment',config.get('segment')))*16+e['start']
            units.append((u['id'],e.get('name','code'),e.get('ledger_id',u['id']),lo,e['size']))
            for p in e.get('producer_ranges',[]): producers.append((u['id'],e.get('name','code'),p['kind'],p['relative'],lo+p['relative'],p['size']))
    functions=[(f['name'],f.get('segment',config.get('segment'))*16+f['offset'],f['size']) for f in config['functions']]
    return units,functions,producers

def actual_span(im,target,lo,size):
    hi=lo+size
    require(size>0 and 0<=lo<hi<=len(im.program_image)==len(target.program_image),'invalid extent')
    require(im.program_image[lo:hi]==target.program_image[lo:hi],'actual target bytes mismatch')
    require(relocs(im,lo,hi)==relocs(target,lo,hi),'actual literal ordered relocations mismatch')

def check_actual(im,target,rd,base,candidate,is_candidate):
    configs=[base]+([candidate] if is_candidate else [])
    us=[];fs=[];ps=[]
    for config in configs:
        u,f,p=scope(config);us+=u;fs+=f;ps+=p
    require(len(us)==(78 if is_candidate else 74) and len(fs)==(371 if is_candidate else 334),'scope cardinality changed')
    gotu=[(x['id'],x['extent'],x['ledger_id'],x['payload_offset'],x['size']) for x in rd['units']]
    gotf=[(x['name'],x['payload_offset'],x['size']) for x in rd['functions']]
    gotp=[(x['id'],x['extent'],x['kind'],x['relative'],x['payload_offset'],x['size']) for x in rd['producer_ranges']]
    require(gotu==us and gotf==fs and gotp==ps,'receipt identities/ranges differ from pinned source scope')
    for items in (us,fs,ps):
        require(len(items)==len(set(items)),'duplicate scope')
        for row in items: actual_span(im,target,*row[-2:])
    if is_candidate:
        for lo,hi,count in [(0x142D0,0x14A76,30),(0x14A76,0x153BB,23),(0x153BB,0x158F5,9),(0x17043,0x17384,13)]:
            actual_span(im,target,lo,hi-lo)
            require(len(relocs(target,lo,hi))==count,'target literal relocation count changed')
        require(len(candidate['functions'])==37,'all 37 Marisa/Reimu/Mima functions required')

def apply_carrier(source,units):
    for unit in units:
        for edit in unit['carrier_edits']:
            if edit.get('path')!='th03_main.asm': continue
            kind=edit['kind']
            if kind in ('replace-once','replace-exact-count'):
                before=edit['before'].encode('ascii');after=edit['after'].encode('ascii')
                count=1 if kind=='replace-once' else edit['count']
                require(source.count(before)==count,'carrier replacement count')
                source=source.replace(before,after)
            elif kind=='remove-between':
                begin=edit['start_marker'].encode('ascii');end=edit['end_marker'].encode('ascii')
                require(source.count(begin)==1 and source.count(end)==1,'carrier carve boundary')
                lo=source.index(begin);hi=source.index(end,lo)+len(end)
                source=source[:lo]+edit.get('replacement','').encode('ascii')+source[hi:]
            else: raise ValueError('unsupported carrier edit: '+kind)
    return source


EXCLUSIONS=((0x142D0,0x158F5),(0x17043,0x17384))
def outside_relocs(im):
    out=[]
    for r in im.relocations:
        p=r.linear
        for lo,hi in EXCLUSIONS:
            require(not(p<lo<p+2 or p<hi<p+2),'relocation crosses excluded owner boundary')
        if not any(lo<=p<hi for lo,hi in EXCLUSIONS):out.append((r.segment,r.offset))
    return out
def outside_bytes(im):
    cuts=(0,)+tuple(x for pair in EXCLUSIONS for x in pair)+(len(im.program_image),)
    return tuple(im.program_image[cuts[i]:cuts[i+1]] for i in range(0,len(cuts),2))
def check_map_scope(rows,configs):
    for config in configs:
        for unit in config['units']:
            extents=unit.get('code_extents',[unit])
            for extent in extents:
                seg=extent.get('segment',unit.get('segment',config.get('segment')))
                default=dict(start=extent.get('map_start',extent['start']),size=extent.get('map_size',extent['size']))
                for part in extent.get('map_parts',[default]):
                    def value(key,fallback):return part.get(key,extent.get(key,unit.get(key,fallback)))
                    row=(seg,part['start'],part['size'],'CODE',value('map_segment','SHARED'),value('map_group','(none)'),value('map_module',unit.get('wrapper',f"th03/{unit['object']}.cpp")).replace(chr(92),'/'),value('map_acbp',28))
                    require(rows.count(row)==1,'independent pinned MAP mismatch: '+repr(row))
def publics(text):
    result={}
    for off,name in re.findall(r"^\s*1D56:([0-9A-F]{4})\s+(?:idle\s+)?(\S+)\s*$",text,re.M):
        result.setdefault(name,set()).add(off)
    return result
def check_publics(reference,text):
    found=publics(text)
    require(reference and all(found.get(name)==offsets for name,offsets in reference.items()),'preexisting DGROUP public moved or disappeared')

NEW_MODULES={'th03/cs_mari.cpp','th03/bm_mari.cpp','th03/cs_reimu.cpp','th03/bm_reish.cpp','th03/cs_mima.cpp','th03/bm_mima.cpp'}
def allocation_rows(rows,is_candidate):
    result=[]
    for row in rows:
        if row[3] not in ('DATA','BSS'):continue
        if is_candidate and row[6] in NEW_MODULES:
            require(row[2]==0,'new owner allocated DATA/BSS')
            continue
        result.append(row)
    return sorted(result)
