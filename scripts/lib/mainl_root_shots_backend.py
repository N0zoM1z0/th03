"""Pure genuine shot-pair and shot-load ownership extension from MRI02."""
import hashlib
PINS = {'root': '13f2c911f0ceb1594f21fbd959e09fe124356275989d8e53376d1ff4aad5b961', 'response': 'fc4e2a36cd41716c27e06b79d97858ee08f36e2d16318d0a3f32971f0d049141', 'root_body': '05af9587fe79580fd5367fd584f8a7dcf8dd618a5f5dabe76393982ebd1fe470', 'cpp': '4bffea2b93349f4cba2a436fc7d40247915a136fe4b89d5eb407b6a828ca247b'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def generate(root,response,root_body,cpp):
 for n,b in [('root',root),('response',response),('root_body',root_body),('cpp',cpp)]:need(hashlib.sha256(b).hexdigest()==PINS[n],'source drift '+n)
 body=root_body.replace(b'\r\n',b'\n')
 prefix,body=body.split(b'; int __cdecl main',1)
 need(prefix.count(b'proc near')==2 and prefix.count(b'endp')==2 and b'public MAINL_SHOT_LOAD' in prefix,'two complete shot helpers')
 body=b'; int __cdecl main'+body
 need(b'sub_9CB1' not in body and b'MAINL_SHOT_LOAD' not in body,'no retained shot references')
 old=br'obj\th03\rootint.obj ';new=br'obj\th03\rootshot.obj '
 need(response.count(old)==1,'response slot');response=response.replace(old,new)
 return {'th03_mainl.asm':root,'src/mainl/root/root.asm':body.replace(b'\n',b'\r\n'),'rootshot.cpp':cpp,'obj/th03/mainl.@l':response}
