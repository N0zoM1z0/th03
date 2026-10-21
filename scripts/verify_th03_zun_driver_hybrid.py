"""Strict boundaries and raw comparison for a hybrid diagnostic, not acceptance."""
import hashlib,re
NAMES=('sprite16_set_mono_enabled','sprite16_set_mono_color','sprite16_set_overlap','sprite16_set_access_plane','sprite16_set_rop','sprite16_set_mask')
PUBLICS=dict(start=0x100,**dict(zip(NAMES,range(0x340,0x364,6))))
RESIDENT_PROCS=(('sprite16_entry', 268, 412), ('sprite16_allocate_buffers', 412, 471), ('sprite16_set_interrupt_argument', 471, 478), ('sprite16_mask_test_command', 478, 513), ('sprite16_draw_command', 513, 554), ('sprite16_interrupt_dispatch', 554, 579), ('sprite16_install', 579, 685), ('sprite16_uninstall', 685, 832))
COMMAND_PROCS=(('sprite16_tokenize_command', 2336, 2434),
 ('sprite16_skip_separators', 2434, 2457),
 ('sprite16_find_token_end', 2457, 2485),
 ('sprite16_find_quote_end', 2485, 2509),
 ('sprite16_require_argument', 2509, 2543),
 ('sprite16_optional_argument', 2543, 2570),
 ('sprite16_require_number', 2570, 2596),
 ('sprite16_optional_number_legacy', 2596, 2614),
 ('sprite16_dispatch_options', 2614, 2697),
 ('sprite16_parse_number', 2704, 2821),
 ('sprite16_parse_decimal', 2821, 2891),
 ('sprite16_parse_hex', 2891, 2933),
 ('sprite16_parse_binary', 2933, 2978),
 ('sprite16_parse_switch', 2978, 3014),
 ('sprite16_string_length', 3136, 3154),
 ('sprite16_string_equal_folded', 3154, 3190))
DIFFS=[0x298,0x299,0x30c,0x30d,0x30e,0x31d,0x31e,0x31f,0x7b1,0x7b2]
CANDIDATE='bab3769aa32184cdc71364138bc616b59faa9f2ae79f49837006f1cf87cc9c5c'
TARGET='9122344545f977ee0be7e3326814518a8ec1d3b670bd848d7deef459054594cb'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def index(raw,p):
 need(p<len(raw),'truncated OMF index');x=raw[p];p+=1
 if x&128:need(p<len(raw),'truncated OMF index');x=((x&127)<<8)|raw[p];p+=1
 return x,p
def omf(raw,expected_publics=PUBLICS):
 p=0;records=[];publics={};segments=[]
 while p<len(raw):
  need(p+3<=len(raw),'truncated OMF header');kind=raw[p];record_length=int.from_bytes(raw[p+1:p+3],'little')
  rec=raw[p:p+3+record_length];need(record_length>=1 and len(rec)==3+record_length and sum(rec)%256==0,'OMF checksum/length');body=rec[3:-1];records.append(kind)
  if kind==0x98:
   need(len(body)>=6 and body[0]==0x48,'OMF segment attributes');size=int.from_bytes(body[1:3],'little');at=3
   name,at=index(body,at);cls,at=index(body,at);overlay,at=index(body,at);need(at==len(body),'SEGDEF tail')
   segments.append((size,name,cls,overlay))
  if kind==0x90:
   group,at=index(body,0);seg,at=index(body,at);need((group,seg)==(1,1),'unexpected PUBDEF segment')
   while at<len(body):
    n=body[at];at+=1;need(n>0 and at+n+2<len(body),'truncated PUBDEF');name=body[at:at+n].decode('ascii');at+=n
    offset=int.from_bytes(body[at:at+2],'little');at+=2;typ,at=index(body,at)
    need(name not in publics and typ==0,'duplicate/typed PUBDEF');publics[name]=offset
  p+=3+record_length
 need(records[0]==0x80 and records[-1]==0x8a,'OMF endpoints')
 need(segments==[(0x1180,2,3,1),(0,4,5,1)],'complete tiny segment layout')
 need(publics==expected_publics,'OMF complete public boundaries')
 return dict(records=len(records),publics=publics,segment_lengths=[x[0] for x in segments])
def map_boundaries(raw,expected_publics=PUBLICS):
 text=raw.decode('ascii')
 need(len(re.findall(r'(?m)^\s*00000H\s+0117FH\s+01180H\s+_TEXT\s+CODE\s*$',text))==1,'MAP TEXT length')
 need(len(re.findall(r'(?m)^\s*01180H\s+01180H\s+00000H\s+_DATA\s+DATA\s*$',text))==1,'MAP empty DATA')
 sections=re.split(r'Address\s+Publics by (?:Name|Value)',text)
 need(len(sections)==3,'MAP two public tables')
 tables=[]
 for section in sections[1:]:
  rows={}
  for line in section.splitlines():
   if not line.strip():continue
   match=re.fullmatch(r'\s*0000:([0-9A-Fa-f]+)\s+(?:idle\s+)?([A-Za-z_][A-Za-z_0-9]*)\s*',line)
   need(match is not None,'unexpected MAP public row');name=match[2]
   need(name not in rows,'duplicate MAP public');rows[name]=int(match[1],16)
  need(rows==expected_publics,'MAP complete public boundaries');tables.append(rows)
 return tables
def verify(obj,com,map_raw,candidate,target,scope="setters"):
 need(scope in ("setters","resident-services","command-resident-services"),"unknown ownership scope")
 procedures=[(n,a,a+6) for n,a in PUBLICS.items() if n!="start"]
 if scope!="setters":procedures=list(RESIDENT_PROCS)+procedures
 if scope=="command-resident-services":procedures+=list(COMMAND_PROCS)
 expected_publics=dict(start=0x100,**{n:a for n,a,b in procedures})
 need(len(com)==len(candidate)==len(target)==4224,'full driver length')
 need(sha(candidate)==CANDIDATE and sha(target)==TARGET,'candidate/target identity')
 need(com==candidate,'complete cached-candidate raw inequality')
 need([i for i,(a,b) in enumerate(zip(com,target)) if a!=b]==DIFFS,'known ten target differences changed')
 layout=omf(obj,expected_publics);tables=map_boundaries(map_raw,expected_publics)
 for name,address,end in procedures:
  at=address-0x100;stop=end-0x100;need(com[at:stop]==target[at:stop],'maintained raw body differs '+name)
 return dict(complete_candidate_raw_equal=True,raw_bytes=4224,target_raw_equal=False,target_differing_bytes=10,
             target_difference_offsets=DIFFS,scope=scope,maintained_procedures=len(procedures),maintained_instruction_bytes=sum(b-a for n,a,b in procedures),
             maintained_bodies_target_raw_equal=True,object=layout,map_publics=tables,
             object_sha256=sha(obj),com_sha256=sha(com),map_sha256=sha(map_raw),
             complete_driver_source_owned=False,exact_acceptance=False)
