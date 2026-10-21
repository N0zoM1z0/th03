"""Pure genuine CFG/win/root-prefix compiler ownership composition."""
import hashlib,re
PINS = {'root': '599ceeceb857d0c65dc9d2bdba4defb9147b47623aa1aebcb1c55578a838ff68', 'response': '9208b6b870f7908b369a316063f1757fcada1cf47308998166f7f9b79d567d6c', 'root_body': 'b5c78ef137ca45bb58ee262fe840148275de78652c7ad696b32a4438c85e9853', 'cpp': 'a3be00dd221d3295fbcddd69cbad283604538b8afc334357f406b92749c27767'}
ALIASES = [('aLogo1_rgb', '_mainl_logo_palette', 'byte', 3647, 896), ('word_E502', '_mainl_stage_number', 'word', 3647, 274), ('word_E504', '_mainl_stage_bg', 'word', 3647, 276), ('aStnx0_pi', '_mainl_stage_blank', 'byte', 3647, 922)]
CALLS = [('sub_978D','_mainl_win_animate',1),('sub_9887','_mainl_story_dispatch',2),('sub_990C','_mainl_stage_load',2),('cdg_free_all','CDG_FREE_ALL',3)]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def once(b,old,new):
 need(b.count(old)==1,'nonunique source anchor '+repr(old));return b.replace(old,new)
def generate(root,response,root_body,cpp):
 for n,b in [('root',root),('response',response),('root_body',root_body),('cpp',cpp)]:
  need(hashlib.sha256(b).hexdigest()==PINS[n],'source drift '+n)
 r=root.replace(b'\r\n',b'\n');body=root_body.replace(b'\r\n',b'\n')
 prefix,body=body.split(b'sub_9A2C\tproc near',1)
 need(prefix.count(b'proc near')==4 and prefix.count(b'endp')==4,'four whole original procedures')
 body=b'sub_9A2C\tproc near'+body
 for old,new,count in CALLS:
  a=('call\t'+old).encode();need(body.count(a)==count,'caller count '+old);body=body.replace(a,('call\t'+new).encode())
 r=once(r,b'CFG_LRES_TEXT, MAINL_SC_TEXT, CUTSCENE_TEXT',b'ROOTPRE_TEXT, CUTSCENE_TEXT')
 start=r.index(b'CFG_LRES_TEXT\tsegment');end=r.index(b'MAINL_SC_TEXT ends',start)+len(b'MAINL_SC_TEXT ends')
 r=r[:start]+b"ROOTPRE_TEXT segment byte public 'CODE' use16\n @cfg_load_resident_ptr$qv procdesc near\n @win_load$qv procdesc pascal near\n @win_text_put$qv procdesc pascal near\n CDG_FREE_ALL procdesc pascal near\n extern _mainl_win_animate:near\n extern _mainl_story_dispatch:near\n extern _mainl_stage_load:near\nROOTPRE_TEXT ends"+r[end:]
 for old,new,typ,seg,off in ALIASES:
  anchor=re.findall(rb'^'+re.escape(old.encode())+rb'[ \t]+d[bw][^\n]*$',r,re.M)
  need(len(anchor)==1,'existing asset declaration '+old)
  r=once(r,anchor[0],('public '+new+'\n'+new+' label '+typ+'\n').encode()+anchor[0])
 response=once(response,br'obj\th03\cfg_lres.obj obj\th03\mainl_sc.obj ',br'obj\th03\rootpre.obj ')
 crlf=lambda b:b.replace(b'\n',b'\r\n')
 return {'th03_mainl.asm':crlf(r),'src/mainl/root/root.asm':crlf(body),'rootpre.cpp':cpp,'obj/th03/mainl.@l':response}
