"""Pure genuine STAFF transition ownership composition."""
import hashlib
PINS = {'root': '936f93e83473d24b10d93c098ea857c14c855d55796c43384b7fe441fd403e15', 'response': 'b6eaf34b75cb65d2c3835f19a66ca249596ff03644d9b38c39ec541eeb71dd8a', 'staff': '8cf67d38e6b769a5cb9fbdfd9d884e148786a800a0abe8fc5e37dc6358c6294f', 'cpp': '6ae7fbb96ef9a659aefd3130a78eccccada461ff99e89784dbad13897960aaea'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def once(b,old,new):
 need(b.count(old)==1,'nonunique source anchor '+repr(old));return b.replace(old,new)
def generate(root,response,staff,cpp):
 for n,b in [('root',root),('response',response),('staff',staff),('cpp',cpp)]:
  need(hashlib.sha256(b).hexdigest()==PINS[n],'source drift '+n)
 r=root.replace(b'\r\n',b'\n');s=staff.replace(b'\r\n',b'\n')
 start=s.index(b'sub_BDF4\tproc near')
 end=s.index(b'sub_BFB2\tendp')+len(b'sub_BFB2\tendp')
 need(s[start:end].count(b'proc near')==4,'four genuine procedure boundary')
 s=s[end:].lstrip(b'\n')
 for old,new,n in [(b'call\tsub_BDF4',b'call\tMAINL_STAFF_ENTER',2),(b'call\tsub_BEC7',b'call\tMAINL_STAFF_LEAVE',1),(b'call\tsub_BF7E',b'call\tMAINL_STAFF_GALLERY',2),(b'call\tsub_BFB2',b'call\tMAINL_STAFF_SINGLE',7)]:
  need(s.count(old)==n,'remaining staff caller count '+repr(old));s=s.replace(old,new)
 r=once(r,b'STAFFP_TEXT ends',b""" extern MAINL_STAFF_ENTER:near
 extern MAINL_STAFF_LEAVE:near
 extern MAINL_STAFF_GALLERY:near
 extern MAINL_STAFF_SINGLE:near
STAFFP_TEXT ends""")
 for old,new,kind in [(b'word_10BBC\tdw ?',b'_mainl_staff_speed',b'word'),(b'word_10BBE\tdw ?',b'_mainl_staff_duration',b'word'),(b'word_10BC0\tdw ?',b'_mainl_staff_center_limit',b'word'),(b'word_10BC4\tdw ?',b'_mainl_staff_height_offset',b'word'),(b'byte_10BC6\tdb ?',b'_mainl_staff_secondary_slot',b'byte')]:
  r=once(r,old,b'public '+new+b'\n'+new+b' label '+kind+b'\n'+old)
 response=once(response,br'obj\th03\staffext.obj ',br'obj\th03\stafftr.obj ')
 crlf=lambda b:b.replace(b'\n',b'\r\n')
 return {'th03_mainl.asm':crlf(r),'src/mainl/staff/staff.asm':crlf(s),'stafftr.cpp':cpp,'obj/th03/mainl.@l':response}
