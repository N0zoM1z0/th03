"""Pure source extension of the proved STAFF prefix through snow and dissolve."""
import hashlib
PINS = {'root': '817be0daf24a2cf2dd55c13fd12d81bddfbedc63f0101d0d2217d8d6c10d9c29', 'response': '13ce7861ab25ea7b8963efa75ae912268d872370710363f1ea232760a86aa7ed', 'staff': '86fd6a48cb29f5b2b8ad7b683ce654b4ddde9bacc47def3e829bc344da6e6df2', 'cpp': '7b31db27d59b001d3a75d45933c91935ce8b5f28e168ecf056272efec2ff45e8'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def once(b,old,new):
 need(b.count(old)==1,'source anchor not unique '+repr(old));return b.replace(old,new)
def generate(root,response,staff,cpp):
 for n,b in [('root',root),('response',response),('staff',staff),('cpp',cpp)]:
  need(hashlib.sha256(b).hexdigest()==PINS[n],'source drift '+n)
 r=root.replace(b'\r\n',b'\n');s=staff.replace(b'\r\n',b'\n')
 r=once(r,b'STAFFP_TEXT, MAINL_SNOW_TAIL_TEXT, MAINL_DISSOLVE_TEXT, MAINL_STAFF_TEXT',b'STAFFP_TEXT, MAINL_STAFF_TEXT')
 a=r.index(b"MAINL_SNOW_TAIL_TEXT segment byte public 'CODE' use16\n")
 z=r.index(b"MAINL_STAFF_TEXT segment byte public 'CODE' use16\n",a)
 r=r[:a]+r[z:]
 r=once(r,b'STAFFP_TEXT ends',b""" extern _mainl_snow_update:near
 extern _mainl_snow_render:near
 extern MAINL_SNOW_GATE:near
 extern _mainl_snow_tick:near
 extern CDG_PUT_DISSOLVE_E_8:near
STAFFP_TEXT ends""")
 r=once(r,b'byte_10BB6\tdb ?',b'public _mainl_snow_auto_adjust\n_mainl_snow_auto_adjust label byte\nbyte_10BB6\tdb ?')
 for old,new,count in [(b'call\tsub_BCD5',b'call\t_mainl_snow_tick',13),(b'call\tsub_BCA5',b'call\tMAINL_SNOW_GATE',8)]:
  need(s.count(old)==count,'staff caller count '+repr(old));s=s.replace(old,new)
 response=once(response,br'obj\th03\staffpre.obj ',br'obj\th03\staffext.obj ')
 response=once(response,br'obj\th03\gfxdis.obj ',b'')
 crlf=lambda b:b.replace(b'\n',b'\r\n')
 return {'th03_mainl.asm':crlf(r),'src/mainl/staff/staff.asm':crlf(s),'staffext.cpp':cpp,'obj/th03/mainl.@l':response}
