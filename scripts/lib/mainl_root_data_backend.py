"""Pure genuine root DATA28 compiler ownership composition; no binary inputs."""
import re,hashlib
PINS={'root': '13f2c911f0ceb1594f21fbd959e09fe124356275989d8e53376d1ff4aad5b961', 'response': '8105beaa0d74f5a16ac6d8313457e177d975c20dad31b89fe1c1448a3cae098a', 'root_body': '3e5eaed2a779c8811214564fe34e98e4f1946e86e0723c88d83872a584f68cad', 'cpp': '28d01e9dc2ebb2c5c15993268f9f0946654c4e4fda968f53211b244301441f1a'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def once(b,a,z):
 need(b.count(a)==1,"anchor "+repr(a));return b.replace(a,z)
def generate(root,response,root_body,cpp):
 raw=dict(root=root,response=response,root_body=root_body,cpp=cpp)
 for n,b in raw.items():need(hashlib.sha256(b).hexdigest()==PINS[n],"source drift "+n)
 r=raw['root'].replace(b'\r\n',b'\n');body=raw['root_body'].replace(b'\r\n',b'\n')
 before,data=r.split(b'\t.data\n',1)
 pic,rest=data.split(b'public _WIN_MESSAGE_FN\n',1)
 removed,suffix=rest.split(b'public _mainl_stage_number\n',1)
 suffix=b'public _mainl_stage_number\n'+suffix
 near=re.findall(rb'^\s*dw offset (\S+)',pic,re.M)
 far=re.findall(rb'^\s*(?:\S+[ \t]+)?dd (\S+)',removed,re.M)
 need(len(near)==9 and len(far)==28,'genuine9/28 tables')
 need(pic.count(b'dw ')==9 and removed.count(b'dd ')==28,'no nonpointer storage')
 prefix=b"\t.386\n\t.model use16 large _TEXT\n"+b''.join(b'extern '+n+b':byte\n' for n in near)+b'\t.data\n'+pic+b'\tend\n'
 # Prefix contains no storage except the original eighteen PIC pointer bytes.
 names=[('_mainl_script_'+str(i)).encode() for i in range(9)]+[b'_mainl_story_template']
 for i in range(9):names.extend([('_mainl_title_'+str(i)).encode(),('_mainl_name_'+str(i)).encode()])
 for old,new in zip(far,names):
  anchor=re.findall(rb'^'+re.escape(old)+rb'[ \t]+db[^\n]*$',suffix,re.M);need(len(anchor)==1,'existing string '+repr(old))
  suffix=once(suffix,anchor[0],b'public '+new+b'\n'+new+b' label byte\n'+anchor[0])
 for n in near:
  anchor=re.findall(rb'^'+re.escape(n)+rb'[ \t]+db[^\n]*$',suffix,re.M);need(len(anchor)==1,'PIC string '+repr(n))
  suffix=once(suffix,anchor[0],b'public '+n+b'\n'+anchor[0])
 need(body.count(b'off_E4B6')==4,'four mutable story consumers')
 body=body.replace(b'off_E4B6',b'_mainl_story_script')
 before+=b'extern _mainl_story_script:dword\n'
 r=before+b'\t.data\nmainl_data_origin label byte\n'+suffix
 response=once(raw['response'],br'obj\th03\rootshot.obj ',br'obj\th03\rootpre.obj obj\th03\rootdata.obj ')
 out={'th03_mainl.asm':r.replace(b'\n',b'\r\n'),'rootpre.asm':prefix.replace(b'\n',b'\r\n'),'src/mainl/root/root.asm':body.replace(b'\n',b'\r\n'),'rootdata.cpp':raw['cpp'],'obj/th03/mainl.@l':response}
 return out
