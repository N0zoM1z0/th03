"""Pure genuine continue-menu ownership and whole-object placement composition."""
import hashlib,re
PINS = {'root': '5b36424ca0639994fdc871d77b7c973de3255dc4a93ae1cab465216ea97bdf1a', 'response': 'ca7d76a009d5654f5d5768d385769211f30015f481e0662d2524b540e4f4f5d0', 'root_body': '8d7d81d9774c8afb3f90ea01d46f75ab67c8cea0f66b56d340fac07f3edd20de', 'cpp': '885b243ef2d7ca1aaba96f766d740d976707206a08e1b232969906b19f49521d'}
ALIASES = [('a0', '_mainl_continue_digit', 3647, 2264), ('aOver_pi', '_mainl_continue_over', 3647, 2266)]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def once(b,old,new):
 need(b.count(old)==1,'nonunique source anchor '+repr(old));return b.replace(old,new)
def generate(root,response,root_body,cpp):
 for n,b in [('root',root),('response',response),('root_body',root_body),('cpp',cpp)]:
  need(hashlib.sha256(b).hexdigest()==PINS[n],'source drift '+n)
 r=root.replace(b'\r\n',b'\n');body=root_body.replace(b'\r\n',b'\n')
 body,removed=body.split(b'sub_9F8D\tproc near',1)
 need(removed.count(b'endp')==1 and removed.rstrip().endswith(b'sub_9F8D\tendp'),'one final complete procedure')
 body=once(body,b'call\tsub_9F8D',b'call\t_mainl_continue_menu')
 r=once(r,b'include src/mainl/root/root.asm',b' extern _mainl_continue_menu:near\ninclude src/mainl/root/root.asm')
 for old,new,seg,off in ALIASES:
  anchor=re.findall(rb'^'+re.escape(old.encode())+rb'[ \t]+db[^\n]*$',r,re.M)
  need(len(anchor)==1,'existing string declaration '+old)
  r=once(r,anchor[0],('public '+new+'\n'+new+' label byte\n').encode()+anchor[0])
 cpp=once(cpp,b'-zCCONTINUE_TEXT',b'-zCCUTSCENE_TEXT')
 start=response.index(br'obj\th01\vplanset.obj ');end=response.index(b',',start)
 shared=response[start:end];need(shared.endswith(br'obj\th03\hfliplut.obj'),'complete retained shared-object group')
 response=response[:start]+response[end:]
 response=once(response,br'obj\th03\mainl.obj ',br'obj\th03\mainl.obj '+shared+b' '+br'obj\th03\contmenu.obj ')
 crlf=lambda b:b.replace(b'\n',b'\r\n')
 return {'th03_mainl.asm':crlf(r),'src/mainl/root/root.asm':crlf(body),'contmenu.cpp':cpp,'obj/th03/mainl.@l':response}
