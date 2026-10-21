"""Pure genuine STAFF paired/hold ownership composition."""
import hashlib
PINS = {'root': '9fb302e33e3d12229540c395d38788a0ac71c4cd582aec21d110d8b329b9a3e0', 'response': 'c97b071ff956219ad457f4c0e68b6acd52e60d6f46466834e2e62f178288d92f', 'staff': '368e34049708c3b7e102e738cf4330f207977c06c56d4b0e6b3c8e443ad17bfa', 'cpp': '25d17eb58ed527f7d71f2e9b04bbf64aeb770e21eeee0842f31d9ff0469e158e'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def once(b,old,new):
 need(b.count(old)==1,'nonunique source anchor '+repr(old));return b.replace(old,new)
def generate(root,response,staff,cpp):
 for n,b in [('root',root),('response',response),('staff',staff),('cpp',cpp)]:
  need(hashlib.sha256(b).hexdigest()==PINS[n],'source drift '+n)
 r=root.replace(b'\r\n',b'\n');s=staff.replace(b'\r\n',b'\n')
 start=s.index(b'sub_C097\tproc near')
 end=s.index(b'sub_C1FD\tendp')+len(b'sub_C1FD\tendp')
 need(s[start:end].count(b'proc near')==2,'two genuine procedure boundary')
 s=s[end:].lstrip(b'\n')
 s=once(s,b'call\tsub_C097',b'call\tMAINL_STAFF_PAIR')
 s=once(s,b'call\tsub_C1FD',b'call\tMAINL_STAFF_HOLD')
 r=once(r,b'STAFFP_TEXT ends',b""" extern MAINL_STAFF_PAIR:near
 extern MAINL_STAFF_HOLD:near
STAFFP_TEXT ends""")
 r=once(r,b'word_10BC2\tdw ?',b'public _mainl_staff_secondary_y\n_mainl_staff_secondary_y label word\nword_10BC2\tdw ?')
 response=once(response,br'obj\th03\stafftr.obj ',br'obj\th03\staffpr.obj ')
 crlf=lambda b:b.replace(b'\n',b'\r\n')
 return {'th03_mainl.asm':crlf(r),'src/mainl/staff/staff.asm':crlf(s),'staffpr.cpp':cpp,'obj/th03/mainl.@l':response}
