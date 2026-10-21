"""Pure genuine stage-introduction ownership extension from MRP05."""
import hashlib,re
PINS = {'root': '2c39331b563e273dcc5dfb757be512d6edc2bb5427d02b4e3fda01046096c7a2', 'response': 'ffab3df19a1135e091c3caa94087fc6a6154983de500a984c3a9a47097e8e002', 'root_body': 'e712323b6d5ca3e3edb90facdf4fdf3304c1b9b58c2d418e2c4a2475294dcd71', 'cpp': 'f080bf138126b5529cf974aaf0a576d175b37857970f75a400d7617cdf62ccf2'}
ALIASES = [('CHAR_TITLE', '_mainl_char_titles', 'dword'), ('CHAR_NAME', '_mainl_char_names', 'dword'), ('aDec_m', '_mainl_dec_bgm', 'byte'), ('aEn2_pi', '_mainl_intro_frame', 'byte'), ('aEnemy00_pi', '_mainl_enemy00', 'byte'), ('aEnemy01_pi', '_mainl_enemy01', 'byte'), ('aEnemy02_pi', '_mainl_enemy02', 'byte'), ('aEnemy03_pi', '_mainl_enemy03', 'byte'), ('aEnemy04_pi', '_mainl_enemy04', 'byte'), ('aYume_efc', '_mainl_sound_effects', 'byte')]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def once(b,old,new):
 need(b.count(old)==1,'nonunique anchor '+repr(old));return b.replace(old,new)
def generate(root,response,root_body,cpp):
 for n,b in [('root',root),('response',response),('root_body',root_body),('cpp',cpp)]:need(hashlib.sha256(b).hexdigest()==PINS[n],'source drift '+n)
 r=root.replace(b'\r\n',b'\n');body=root_body.replace(b'\r\n',b'\n')
 prefix,body=body.split(b'sub_9CB1\tproc near',1)
 need(prefix.count(b'proc near')==1 and prefix.count(b'endp')==1 and prefix.count(b'\tdw offset loc_9B')==9,'one complete intro and real switch table')
 body=b'sub_9CB1\tproc near'+body
 need(body.count(b'call\tsub_9A2C')==2,'intro callers');body=body.replace(b'call\tsub_9A2C',b'call\t_mainl_stage_intro')
 body=once(body,b'sub_9D20\tproc near',b'public MAINL_SHOT_LOAD\nMAINL_SHOT_LOAD\tproc near')
 body=once(body,b'sub_9D20\tendp',b'MAINL_SHOT_LOAD\tendp')
 r=once(r,b'ROOTPRE_TEXT ends',b' extern _mainl_stage_intro:near\nROOTPRE_TEXT ends')
 for old,new,typ in ALIASES:
  anchor=re.findall(rb'^'+re.escape(old.encode())+rb'[ \t]+d[bd][^\n]*$',r,re.M);need(len(anchor)==1,'existing declaration '+old)
  r=once(r,anchor[0],('public '+new+'\n'+new+' label '+typ+'\n').encode()+anchor[0])
 response=once(response,br'obj\th03\rootpre.obj ',br'obj\th03\rootint.obj ')
 crlf=lambda b:b.replace(b'\n',b'\r\n')
 return {'th03_mainl.asm':crlf(r),'src/mainl/root/root.asm':crlf(body),'rootint.cpp':cpp,'obj/th03/mainl.@l':response}
