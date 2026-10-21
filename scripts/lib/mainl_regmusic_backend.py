"""Pure source composition for registration/music producer grouping. No binary inputs."""
import hashlib
PINS = {'root': 'da0a7d22071b84c4d91c4605aa5af919b3bca462d3c69322ee612259a5642b10', 'response': '0ad865d96be57c02962c1d50bb7d5c650faa92ccd23f1d41b3f19239ac7570b2', 'staff': 'd7a5c15c8b7507601f2621bcd47f739073dede4787424a3d1a538752be9db30f', 'root_body': '04382ad4969b9e6b34d92106e07285c9ec55aa98cc72330c8f611efff373eb3c', 'cpp': '7789680f32c0628b8b958e17bf868d790c8f3c3414b3af4ee824f198c2276349'}
def sha(b): return hashlib.sha256(b).hexdigest()
def need(ok, msg):
 if not ok: raise ValueError(msg)
def once(raw, old, new):
 need(raw.count(old)==1,'nonunique source anchor '+repr(old))
 return raw.replace(old,new)
def generate(root, response, staff, root_body, cpp):
 for name,b in [('root',root),('response',response),('staff',staff),('root_body',root_body),('cpp',cpp)]:
  need(sha(b)==PINS[name],'source drift '+name)
 r=root.replace(b'\r\n',b'\n');s=staff.replace(b'\r\n',b'\n');body=root_body.replace(b'\r\n',b'\n')
 start=s.index(b'sub_B92E\tproc near\n')
 end=s.index(b'sub_B92E\tendp',start)+len(b'sub_B92E\tendp')
 removed=s[start:end]
 need(removed.count(b'\tcall\t')==4 and removed.count(b'kajacall')==3,'seven-call music source boundary')
 s=s[:start]+s[end:]
 need(b'sub_B92E' not in s,'old music definition survives')
 body=once(body,b'call\tsub_B92E',b'call\t_mainl_reg_music')
 r=once(r,b"REGIST_TEXT segment byte public 'CODE' use16\n",b"REGIST_TEXT segment byte public 'CODE' use16\n extern _mainl_reg_music:near\n")
 r=once(r,b"aOver_m\t\tdb 'over.m',0",b"public _mainl_over_music\n_mainl_over_music label byte\naOver_m\t\tdb 'over.m',0")
 rsp=once(response,b'obj\\th03\\regist.obj ',b'obj\\th03\\regmusic.obj ')
 crlf=lambda b:b.replace(b'\n',b'\r\n')
 return {'th03_mainl.asm':crlf(r),'src/mainl/linked_game/staff_flow.asm':crlf(s),'src/mainl/root/root.asm':crlf(body),'regmusic.cpp':cpp,'obj/th03/mainl.@l':rsp}
