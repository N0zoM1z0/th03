"""Pure source completion of the genuine STAFF compiler translation unit."""
import hashlib,re
PINS = {'root': '874d6539326a1a9f98c13d6abcb629e2b806e583dbd46f4abb9ca60b0b479a82', 'response': '0e48dd2fabded792e6c65043e560376cd200e7bb97d3e22b0ea7537dce59da04', 'staff': 'eb2e41ffe86b78e458159a5afb777315b732042de964de90d9ed1da85a260c55', 'tail': '03e2197b766f83bb6d50a62714ab62e158b9993af812fdc78fbbbc3b9dd2001b', 'cpp': '126c5423bd3eb25ddc909e6366fd530a4dec47335d129f3bc333f21def3667b3'}
ALIASES = [('aEd_m', '_mainl_staff_music', 3112), ('aEdbk1_rgb', '_mainl_staff_palette', 3117), ('aStf1_cdg', '_mainl_stf1', 3127), ('aStf11_cdg', '_mainl_stf11', 3136), ('aStf3_cdg', '_mainl_stf3', 3146), ('aStf4_cdg', '_mainl_stf4', 3155), ('aStf5_cdg', '_mainl_stf5', 3164), ('aStf6_cdg', '_mainl_stf6', 3173), ('aStf7_cdg', '_mainl_stf7', 3182), ('aStf8_cdg', '_mainl_stf8', 3191), ('aStf9_cdg', '_mainl_stf9', 3200), ('aStf10_cdg', '_mainl_stf10', 3209), ('aStf2_cdg', '_mainl_stf2', 3219), ('aStf12_cdg', '_mainl_stf12', 3228)]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def once(b,old,new):
 need(b.count(old)==1,'nonunique source anchor '+repr(old));return b.replace(old,new)
def generate(root,response,staff,tail,cpp):
 for n,b in [('root',root),('response',response),('staff',staff),('tail',tail),('cpp',cpp)]:
  need(hashlib.sha256(b).hexdigest()==PINS[n],'source drift '+n)
 r=root.replace(b'\r\n',b'\n');t=tail.replace(b'\r\n',b'\n')
 need(staff.count(b'proc near')==1 and b'sub_C40D\tendp' in staff,'complete last STAFF procedure')
 r=once(r,b'STAFFP_TEXT, MAINL_STAFF_TEXT',b'STAFFP_TEXT')
 r=once(r,b"MAINL_STAFF_TEXT segment byte public 'CODE' use16\ninclude src/mainl/staff/staff.asm\nMAINL_STAFF_TEXT ends\n",b'')
 r=once(r,b'STAFFP_TEXT ends',b' extern _mainl_staff_roll:near\nSTAFFP_TEXT ends')
 for old,new,offset in ALIASES:
  anchor=re.findall(rb'^'+old.encode()+rb'\s+db[^\n]*$',t,re.M)
  need(len(anchor)==1,'asset declaration boundary '+old)
  t=once(t,anchor[0],b'public '+new.encode()+b'\n'+new.encode()+b' label byte\n'+anchor[0])
 response=once(response,br'obj\th03\staffvd.obj ',br'obj\th03\staffall.obj ')
 crlf=lambda b:b.replace(b'\n',b'\r\n')
 return {'th03_mainl.asm':crlf(r),'regtail.asm':crlf(t),'staffall.cpp':cpp,'obj/th03/mainl.@l':response}
