"""Pure source composition of the genuine first STAFF translation-unit prefix."""
import hashlib,re
PINS = {'root': 'da633edb3a181b5f1f2ed45633e1443482124aa1348732bb20c5f540fe265352', 'response': '770870991f34070cfc1d14a21c2ad35e88da88bc7350f05bef9b2b95648e6ce2', 'tail': '4d5c4d0769adbdaf97ad1a713e50cacbc11830fe7f3278980b82e85bd9e2b4b2', 'root_body': 'e7d75a362956e777a6a11b7d7713b9513161d8ecc98f9d28a6cf6d0423152318', 'staff_body': '78287d447508d172489ef224c4cb742a9716a37234a15d13b4e88c13eaaa3e5c', 'flow': '4032356bfc42b9e967b1834268560055fdcb211a29f9f29e278c39bc0f302042', 'cpp': '8a5a507ee1f2dbb2bd1a67c3ff837215e504ce8f000817ece93626957a9bc2fa', 'snow_prefix': 'f35fa1c58398051ccebe92b5d08e0ba23e5ebb436a919e77045b8efcfe8a4924'}
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def once(raw,old,new):
 need(raw.count(old)==1,'nonunique source anchor '+repr(old));return raw.replace(old,new)
def generate(root,response,tail,root_body,staff_body,flow,cpp,snow_prefix):
 for n,b in [('root',root),('response',response),('tail',tail),('root_body',root_body),('staff_body',staff_body),('flow',flow),('cpp',cpp),('snow_prefix',snow_prefix)]:need(sha(b)==PINS[n],'source drift '+n)
 r=root.replace(b'\r\n',b'\n');t=tail.replace(b'\r\n',b'\n');rb=root_body.replace(b'\r\n',b'\n');sb=staff_body.replace(b'\r\n',b'\n');f=flow.replace(b'\r\n',b'\n')
 group=b'STAFF_TEXT, mainl_03_TEXT, MAINL_SNOW_TEXT, MAINL_SPAWN_TEXT, MAINL_SNOW_TAIL_TEXT'
 r=once(r,group,b'STAFFP_TEXT, MAINL_SNOW_TAIL_TEXT')
 a=r.index(b"STAFF_TEXT segment byte public 'CODE' use16\n")
 end=r.index(b"MAINL_SNOW_TAIL_TEXT segment byte public 'CODE' use16\n",a)
 descriptor=f[f.index(b'\t@FLAKE_PUT$QIII procdesc'):]
 need(descriptor.count(b'procdesc')==1 and b'proc near' not in descriptor,'flake interface boundary')
 geometry=b'\n'.join(re.findall(rb'^FLAKE_(?:W|H|CELS) = [0-9]+$',snow_prefix.replace(b'\r\n',b'\n'),re.M))+b'\n'
 need(geometry.count(b' = ')==3,'shared snow geometry source declarations')
 replacement=geometry+b"""STAFFP_TEXT segment byte public 'CODE' use16
 extern _mainl_ending:near
 extern _mainl_snow_spawn:near
 extern _mainl_clear_blue:near
 extern CDG_UNPUT_FOR_UPWARDS_MOTION_E_8:near
 extern @flakes_reset$qv:near
"""+descriptor+b'\nSTAFFP_TEXT ends\n'
 r=r[:a]+replacement+r[end:]
 rb=once(rb,b'call\tsub_B972',b'call\t_mainl_ending')
 sb=once(sb,b'sub_C40D\tproc near',b'public _mainl_staff_roll\n_mainl_staff_roll label near\nsub_C40D\tproc near')
 r=once(r,b'include th03/formats/cdg[bss].asm',b'public _mainl_staff_cdg_slots\n_mainl_staff_cdg_slots label byte\ninclude th03/formats/cdg[bss].asm')
 r=once(r,b'_flakes\tflake_t FLAKE_COUNT dup(<?>)',b'public _mainl_spawn_flakes\n_mainl_spawn_flakes label byte\n_flakes\tflake_t FLAKE_COUNT dup(<?>)')
 for old,new,kind in [(b'off_EE4E\tdd',b'_mainl_ending_script',b'dword'),(b'a@99ed_txt\tdb',b'_mainl_bonus_script',b'byte'),(b'aOp_0\t\tdb',b'_mainl_op_name',b'byte')]:
  t=once(t,old,b'public '+new+b'\n'+new+b' label '+kind+b'\n'+old)
 rsp=once(response,br'obj\th03\snow_cpp.obj ',br'obj\th03\staffpre.obj ')
 rsp=once(rsp,br'obj\th03\gfxpre.obj ',b'')
 rsp=once(rsp,br'obj\th03\staff.obj ',b'')
 crlf=lambda b:b.replace(b'\n',b'\r\n')
 return {'th03_mainl.asm':crlf(r),'regtail.asm':crlf(t),'src/mainl/root/root.asm':crlf(rb),'src/mainl/staff/staff.asm':crlf(sb),'staffpre.cpp':cpp,'obj/th03/mainl.@l':rsp}
