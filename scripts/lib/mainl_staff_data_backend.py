"""Pure genuine STAFF initialized DATA ownership transfer; no binary inputs."""
import hashlib,re
PINS = {'root': '0258f0633e49ec386104e62df41644573d4ad30ad146b2b13d7d43d25e37e111', 'response': '95c115511740cad85c7ee89b1c392790529ee45eb4b8ddd74529a2bba5c57fea', 'tail': 'a49d4e747b87465f17487aa631aebff2aed0adf5a24f755c2b954863db6e9b65', 'cpp': 'a2f6e106110a0ccc8b4dae28fb2b42247614e9a6e777cf82832bedccc247aa6a'}
ALIASES = [('a@00ed_txt', '_mainl_ending_template', 3647, 2878), ('aFocab@sC_0', '_mainl_vname_0', 3647, 2901), ('aCgCv_0', '_mainl_vname_1', 3647, 2915), ('aCIjb@cvcan_0', '_mainl_vname_2', 3647, 2926), ('aB@b@gggmgu_0', '_mainl_vname_3', 3647, 2942), ('aPmuexp_0', '_mainl_vname_4', 3647, 2953), ('aGjgibegagigx_0', '_mainl_vname_5', 3647, 2964), ('aB@tisqb@canb_0', '_mainl_vname_6', 3647, 2981), ('aCkftiB@vVfvs_0', '_mainl_vname_7', 3647, 2996), ('aB@iknsb@cF_0', '_mainl_vname_8', 3647, 3012), ('aVdvbvuvs', '_mainl_vrank_0', 3647, 3026), ('aVmvpvtvnvbvm', '_mainl_vrank_1', 3647, 3038), ('aVgvbvtvd', '_mainl_vrank_2', 3647, 3052), ('aVkvxvovbvfvivg', '_mainl_vrank_3', 3647, 3064), ('aVo', '_mainl_vdigit_0', 3647, 3079), ('aVp', '_mainl_vdigit_1', 3647, 3082), ('aVq', '_mainl_vdigit_2', 3647, 3085), ('aVr', '_mainl_vdigit_3', 3647, 3088), ('aVs', '_mainl_vdigit_4', 3647, 3091), ('aVt', '_mainl_vdigit_5', 3647, 3094), ('aVu', '_mainl_vdigit_6', 3647, 3097), ('aVv', '_mainl_vdigit_7', 3647, 3100), ('aVw', '_mainl_vdigit_8', 3647, 3103), ('aVx', '_mainl_vdigit_9', 3647, 3106)]
MIGRATIONS = [('off_EE4E', '_mainl_ending_script', 'dword', 3647, 2654), ('CDG_DISSOLVE_PATTERN', '_mainl_dissolve_pattern', 'word', 3647, 2722), ('aVERDICT_PLAYCHARS', '_mainl_verdict_playchars', 'dword', 3647, 2786), ('aVERDICT_RANKS', '_mainl_verdict_ranks', 'dword', 3647, 2822), ('aVERDICT_NUMBERS', '_mainl_verdict_numbers', 'dword', 3647, 2838)]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def once(b,old,new):
 need(b.count(old)==1,'nonunique source anchor '+repr(old));return b.replace(old,new)
def generate(root,response,tail,cpp):
 for n,b in [('root',root),('response',response),('tail',tail),('cpp',cpp)]:
  need(hashlib.sha256(b).hexdigest()==PINS[n],'source drift '+n)
 r=root.replace(b'\r\n',b'\n');t=tail.replace(b'\r\n',b'\n')
 for old,new,typ,seg,off in MIGRATIONS:
  r=once(r,('extern '+old+':'+typ+'\n').encode(),b'')
 head,rest=t.split(b'\t.data\n',1)
 public_head,body=rest.split(b'public _REGI_PLAYCHAR\n',1)
 body=b'public _REGI_PLAYCHAR\n'+body
 prefix,rest=body.split(b'public _mainl_ending_script\n',1)
 removed,suffix=rest.split(b'a@00ed_txt\tdb',1)
 suffix=b'a@00ed_txt\tdb'+suffix
 need(len(re.findall(rb'^\s*dd ',removed,re.M))==23,'genuine pointer table removal')
 need(b'include th03/sprites/flake.asp' in removed and b'include th03/formats/cdg_put_dissolve[data].asm' in removed,'genuine intervening data')
 names=[]
 for line in public_head.splitlines():
  need(line.startswith(b'public '),'public preamble shape');names.extend(line[7:].split(b','))
 def assemble(part):
  selected=[]
  for name in names:
   name=name.strip()
   if re.search(rb'^'+re.escape(name)+rb'[ \t]+(?:db|dw|dd|label)\b',part,re.M):selected.append(b'public '+name+b'\n')
  return head+b'\t.data\n'+b''.join(selected)+part
 prefix=assemble(prefix)+b'\n\tend\n';suffix=assemble(suffix)
 for old,new,seg,off in ALIASES:
  anchor=re.findall(rb'^'+re.escape(old.encode())+rb'[ \t]+db[^\n]*$',suffix,re.M)
  need(len(anchor)==1,'existing string alias '+old)
  suffix=once(suffix,anchor[0],('public '+new+'\n'+new+' label byte\n').encode()+anchor[0])
 response=once(response,br'obj\th03\staffall.obj ',b'')
 response=once(response,br'obj\th03\regtail.obj ',br'obj\th03\regpre.obj obj\th03\staffdat.obj obj\th03\regtail.obj ')
 crlf=lambda b:b.replace(b'\n',b'\r\n')
 return {'th03_mainl.asm':crlf(r),'regpre.asm':crlf(prefix),'regtail.asm':crlf(suffix),'staffdat.cpp':cpp,'obj/th03/mainl.@l':response}
