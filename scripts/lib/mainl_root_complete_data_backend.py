"""Pure complete MAINL root compiler ownership composition; source inputs only."""
import hashlib,re
PINS={'root': '64f3539d759527821be33a9afc165fe68f16cddb52d1617cd42d24f4eaa4986b', 'response': 'd3fa50e97e7ecfae2c04c5b0be96805327bfe550d75d86f488911eb3b75e1566', 'root_body': '0a497285e2333858f710db2ae6ee3053bcfeccb25d22078e6f0a7c2e27a8cb28', 'cpp': 'cc7c580e75a7f4ad452c3926bacfb6c07523d3840ce4a2f12a007319e0717b40', 'rootpre': 'ce8f14419d20c91f49005f2c88bcf7c651af01fc1829a845e2f84d7001888502'}
def need(ok,message):
 if not ok:raise ValueError(message)
def generate(root,response,root_body,cpp,rootpre):
 raw=dict(root=root,response=response,root_body=root_body,cpp=cpp,rootpre=rootpre)
 for name,data in raw.items():need(hashlib.sha256(data).hexdigest()==PINS[name],'source drift '+name)
 r=root.replace(b'\r\n',b'\n')
 aliases=[(b'aCOul',b'_mainl_archive_name'),(b'aMikoft_bft',b'_mainl_gaiji_font'),(b'aWin_m',b'_mainl_win_bgm'),(b'path',b'_mainl_root_op_name'),(b'aMain',b'_mainl_main_name')]
 for old,new in aliases:
  need(b'public '+new not in r,'duplicate export')
  rows=re.findall(rb'^'+re.escape(old)+rb'[ \t]+db[^\n]*$',r,re.M);need(len(rows)==1,'original string anchor')
  r=r.replace(rows[0],b'public '+new+b'\n'+new+b' label byte\n'+rows[0])
 need(r.count(b'\t.data\n')==1,'one root DATA section')
 r=r.replace(b'\t.data\n',b'extern _main:far\n\t.data\n')
 body=root_body.replace(b'\r\n',b'\n')
 need(body.count(b'public _main\n')==1 and body.count(b'_main\t\tendp')==1,'one original main')
 start=body.index(b'public _main\n');end=body.index(b'_main\t\tendp')+len(b'_main\t\tendp')
 body=body[:start]+b'; Genuine main is compiler-owned in rootdata.cpp.\n'+body[end:]
 return {'th03_mainl.asm':r.replace(b'\n',b'\r\n'),'src/mainl/root/root.asm':body.replace(b'\n',b'\r\n'),'rootdata.cpp':cpp,'rootpre.asm':rootpre,'obj/th03/mainl.@l':response}
