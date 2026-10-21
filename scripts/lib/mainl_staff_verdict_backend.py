"""Pure genuine STAFF verdict ownership composition."""
import hashlib
PINS = {'root': '6e89bf8bbb564e96104241a8fcf39da714729078cb5d561a6c797bc6f7793768', 'response': '286106a8a13c3a92a44e40c0f47c6ce5f488bd664e66f3899f6299490d286320', 'staff': '6671ede6276be5eafe270ce612af964154243dcb2a889d263a708fba7ae3bb96', 'tail': '2142f246d4f6a69f1b3136da2235eead7563db35bdb4b3aca00d83fd51424e38', 'cpp': '4b16c8d192250315651a7e23ce55bb751325a59abcc418997d33e13a53a21bcf'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def once(b,old,new):
 need(b.count(old)==1,'nonunique source anchor '+repr(old));return b.replace(old,new)
def generate(root,response,staff,tail,cpp):
 for n,b in [('root',root),('response',response),('staff',staff),('tail',tail),('cpp',cpp)]:
  need(hashlib.sha256(b).hexdigest()==PINS[n],'source drift '+n)
 r=root.replace(b'\r\n',b'\n');s=staff.replace(b'\r\n',b'\n');t=tail.replace(b'\r\n',b'\n')
 start=s.index(b'sub_C288\tproc near')
 end=s.index(b'sub_C288\tendp')+len(b'sub_C288\tendp')
 need(s[start:end].count(b'proc near')==1,'one genuine procedure boundary')
 s=s[end:].lstrip(b'\n')
 need(s.count(b'call\tsub_C288')==2,'two verdict callers')
 s=s.replace(b'call\tsub_C288',b'call\t_mainl_staff_verdict')
 r=once(r,b'STAFFP_TEXT ends',b' extern _mainl_staff_verdict:near\nSTAFFP_TEXT ends')
 for old,new in [(b'_rank\tdb ?',b'_mainl_verdict_rank'),(b'playchar_10BD7\tdb ?',b'_mainl_verdict_playchar'),(b'_skill\tdb ?',b'_mainl_verdict_skill')]:
  r=once(r,old,b'public '+new+b'\n'+new+b' label byte\n'+old)
 for old,new,kind in [(b'aVERDICT_PLAYCHARS label dword',b'_mainl_verdict_playchars',b'dword'),(b'aVERDICT_RANKS label dword',b'_mainl_verdict_ranks',b'dword'),(b'aVERDICT_NUMBERS label dword',b'_mainl_verdict_numbers',b'dword'),(b'aU_\t\tdb',b'_mainl_verdict_unit',b'byte')]:
  t=once(t,old,b'public '+new+b'\n'+new+b' label '+kind+b'\n'+old)
 response=once(response,br'obj\th03\staffpr.obj ',br'obj\th03\staffvd.obj ')
 crlf=lambda b:b.replace(b'\n',b'\r\n')
 return {'th03_mainl.asm':crlf(r),'src/mainl/staff/staff.asm':crlf(s),'regtail.asm':crlf(t),'staffvd.cpp':cpp,'obj/th03/mainl.@l':response}
