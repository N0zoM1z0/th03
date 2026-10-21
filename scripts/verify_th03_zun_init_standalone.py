"""Strict tiny-init structural verifier. No build, runtime, byte normalization."""
from pathlib import Path
import hashlib, json, re, struct, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.omf import parse_omf
from review_th03_zun_init import decode
TARGET_SHA="27fe52738878c1fa267c5dc82b0d70957d72dca5a6da375620a74d163b61e2d8"
SIZE=1390
FIXUP_SCHEMA_SHA256="86c974816bc5a076d60d5ccaf2acff04d78ca9979a1ff64fab61b3b66a00d0a7"
def exact_fixup_schema():
    raw=(ROOT/"config/th03_zun_init_fixups.json").read_bytes()
    require(hashlib.sha256(raw).hexdigest()==FIXUP_SCHEMA_SHA256,"fixup schema identity changed")
    return json.loads(raw)
def require(value,message):
    if not value: raise ValueError(message)
def idx(d,p):
    require(p<len(d),"truncated OMF index")
    n=d[p];p+=1
    if n&128:
        require(p<len(d),"truncated extended OMF index")
        n=((n&127)<<8)|d[p];p+=1
    return n,p
def word(d,p):
    require(p+2<=len(d),"truncated OMF word")
    return int.from_bytes(d[p:p+2],"little"),p+2
def string(d,p):
    require(p<len(d),"truncated OMF string")
    n=d[p];p+=1;require(p+n<=len(d),"truncated OMF string body")
    return d[p:p+n].decode("ascii"),p+n
def parse_object(raw, expected_size=SIZE):
    rs=parse_omf(raw)
    module,end=string(rs[0].data,0)
    require(end==len(rs[0].data) and module.replace("\\","/").lower()=="src/zun/init.asm",
        "THEADR maintained owner/path/trailing bytes")
    allowed={"THEADR","COMENT","LNAMES","SEGDEF","GRPDEF","PUBDEF","LPUBDEF","LEDATA","FIXUPP","MODEND"}
    require(all(r.name in allowed for r in rs),"unsupported/external/storage OMF record")
    names=[""];segments=[None];groups=[None];publics=[];dependencies=[];translator=False
    for r in rs:
        d=r.data
        if r.name=="LNAMES":
            pos=0
            while pos<len(d):
                name,pos=string(d,pos);names.append(name)
        elif r.name=="SEGDEF":
            require(len(d)>=6 and d[0]==0x48,"unsupported tiny SEGDEF attributes")
            size,pos=word(d,1);ni,pos=idx(d,pos);ci,pos=idx(d,pos);oi,pos=idx(d,pos)
            require(pos==len(d) and max(ni,ci,oi)<len(names),"SEGDEF name/index/trailing bytes")
            segments.append(dict(name=names[ni],class_name=names[ci],overlay=names[oi],size=size))
        elif r.name=="GRPDEF":
            ni,pos=idx(d,0);require(ni<len(names),"GRPDEF name")
            members=[]
            while pos<len(d):
                require(d[pos]==255,"nonsegment GRPDEF member");si,pos=idx(d,pos+1)
                require(0<si<len(segments),"GRPDEF segment");members.append(si)
            require(len(set(members))==len(members),"duplicate group member")
            groups.append(dict(name=names[ni],members=members))
        elif r.name in ("PUBDEF","LPUBDEF"):
            gi,pos=idx(d,0);si,pos=idx(d,pos)
            require(si>0,"absolute public unsupported")
            while pos<len(d):
                name,pos=string(d,pos);off,pos=word(d,pos);typ,pos=idx(d,pos)
                require(typ==0,"typed public unsupported")
                publics.append(dict(name=name,segment=si,group=gi,offset=off))
        elif r.name=="COMENT":
            require(len(d)>=2,"short COMENT")
            if d[1]==0:
                text,end=string(d,2);require(end==len(d),"translator trailing bytes")
                translator |= text=="Turbo Assembler  Version 5.0"
            elif d[1]==0xe9 and len(d)>2:
                require(len(d)>=7,"short dependency")
                name,end=string(d,6);require(end==len(d),"dependency trailing bytes")
                dependencies.append(name)
            else:
                require(d in (b"\x40\xe9",b"\x40\xa1",b"\x40\xa2\x01"),"unreviewed OMF comment")
    require(translator,"TASM translator missing")
    code=[i for i,s in enumerate(segments) if s and s["name"]=="_TEXT" and s["class_name"]=="CODE"]
    require(len(code)==1,"one _TEXT CODE required");code=code[0]
    require(segments[code]["size"]==0x100+expected_size,"unexpected logical tiny span")
    require(all(s["size"]==0 and s["name"]=="_DATA" and s["class_name"]=="DATA"
        for i,s in enumerate(segments) if s and i!=code),"unowned noncode storage")
    require(all(s["overlay"]=="" for s in segments if s),"overlay not empty")
    require(len(groups)==2 and groups[1]["name"]=="DGROUP" and
        set(groups[1]["members"])==set(range(1,len(segments))),"tiny group membership")
    require(len({p["name"] for p in publics})==len(publics),"duplicate publics")
    require(all(p["segment"]==code and p["group"]==1 and
        0x100<=p["offset"]<0x100+expected_size for p in publics),"public escapes payload")
    start=[p for p in publics if p["name"]=="start"]
    require(len(start)==1 and start[0]["offset"]==0x100,"public start origin")
    require(dependencies and all(n.replace("\\","/").lower()=="src/zun/init.asm" for n in dependencies),
        "unexpected dependency path or missing maintained path")
    image=bytearray(expected_size);covered=set();fixups=[];block=None
    for r in rs:
        d=r.data
        if r.name=="LEDATA":
            si,pos=idx(d,0);off,pos=word(d,pos);payload=d[pos:]
            require(si==code and payload,"noncode/empty LEDATA")
            require(0x100<=off and off+len(payload)<=0x100+expected_size,"LEDATA outside owned payload")
            for n in range(off,off+len(payload)):
                require(n not in covered,"overlapping LEDATA");covered.add(n)
            image[off-0x100:off-0x100+len(payload)]=payload
            block=(off,len(payload))
        elif r.name=="FIXUPP":
            require(block is not None,"FIXUPP without LEDATA");pos=0
            while pos<len(d):
                require(pos+3<=len(d),"truncated fixup")
                loc=d[pos];site=((loc&3)<<8)|d[pos+1];fd=d[pos+2];pos+=3
                require(loc&0x80 and loc&0x40 and (loc>>2)&15==1,"only segment-relative 16-bit offset fixup")
                require(fd in ((0x14,0x54) if expected_size==SIZE else (0x14,0x10)),"only reviewed exact frame forms")
                frame=None
                if fd!=0x54:frame,pos=idx(d,pos)
                target,pos=idx(d,pos);disp=0
                if not fd&4:disp,pos=word(d,pos)
                require((frame==1 or (fd==0x54 and frame is None)) and target==code,"fixup references external storage")
                require(site+2<=block[1],"fixup crosses LEDATA")
                address=block[0]+site
                require(all(abs(address-x["address"])>=2 for x in fixups),"overlapping fixup")
                value=int.from_bytes(image[address-0x100:address-0x100+2],"little")
                resolved=value+disp # CODE and DGROUP both have natural base zero.
                require(0<=resolved<=65535,"fixup overflow")
                image[address-0x100:address-0x100+2]=resolved.to_bytes(2,"little")
                fixups.append(dict(address=address,fixdat=fd,frame=frame,target=target,resolved=resolved))
        elif r.name=="MODEND":
            require(d==bytes.fromhex("c10001010001") if expected_size==SIZE else
                len(d)==6 and d[0]==0xc1 and d[1]==0x10 and d[2]==1 and d[3]==code and
                int.from_bytes(d[4:],"little")==0x100,"MODEND entry differs")
    require(covered==set(range(0x100,0x100+expected_size)),"missing/extra initialized object bytes")
    if expected_size==SIZE:
        require(fixups==exact_fixup_schema(),"exact per-address fixup schema differs")
        require(hashlib.sha256(bytes(image)).hexdigest()==TARGET_SHA,"resolved object payload differs")
    return dict(segments=segments[1:],publics=publics,fixups=fixups,dependencies=dependencies,
        entry=0x100,origin_gap=0x100,resolved=bytes(image))

def verify_map(raw,obj):
    # Exact observed TLINK -s/-t display grammar, no skipped unknown rows.
    # SEGDEF48 is paragraph-aligned when it allocates storage. The empty _DATA
    # segment allocates none: TLINK reports its position at the logical CODE end,
    # not at a synthesized padded boundary. COM equality separately forbids padding.
    require(raw.endswith(b"\r\n") and b"\r" not in raw.replace(b"\r\n",b"") and
        b"\n" not in raw.replace(b"\r\n",b""),"MAP newline grammar")
    lines=[line.strip() for line in raw.decode("ascii",errors="strict").split("\r\n") if line.strip()]
    require(len(lines)==10,"MAP exact row count")
    require(lines[0]=="Start  Stop   Length Name               Class" and
        lines[3]=="Detailed map of segments" and
        lines[6]=="Address         Publics by Name" and
        lines[8]=="Address         Publics by Value","MAP exact section ordering/headings")
    require(len(obj['segments'])==2,"MAP exact tiny segment count")
    code,data=obj['segments'];size=code['size']
    require((code['name'],code['class_name'],code['overlay'])==('_TEXT','CODE','') and
        data==dict(name='_DATA',class_name='DATA',overlay='',size=0),"MAP exact OMF segment owners")
    expected=[(0,size-1,size,'_TEXT','CODE'),(size,size,0,'_DATA','DATA')]
    allocations=[]
    for line in lines[1:3]:
        match=re.fullmatch(r"([0-9A-F]{5})H +([0-9A-F]{5})H +([0-9A-F]{5})H +(\S+) +(\S+)",line)
        require(match is not None,'MAP summary grammar')
        allocations.append((int(match[1],16),int(match[2],16),int(match[3],16),match[4],match[5]))
    require(allocations==expected,'MAP exact allocations differ')
    for line,e in zip(lines[4:6],expected):
        match=re.fullmatch(r"0000:([0-9A-F]{4}) +([0-9A-F]{4}) +C=(\S+) +S=(\S+) +G=DGROUP +M=src\\zun\\init\.asm +ACBP=48",line)
        require(match is not None,'MAP detailed grammar/owner/frame')
        require((int(match[1],16),int(match[2],16),match[3],match[4])==(e[0],e[2],e[4],e[3]),'MAP detailed allocation differs')
    require(obj['publics']==[dict(name='start',segment=1,group=1,offset=0x100)] and obj['entry']==0x100,'MAP exact OMF public contract')
    expected_public="0000:00100 idle  start"
    require(lines[7]==lines[9]==expected_public,'MAP Name/Value publics differ from OMF')
    return dict(allocations=allocations,detailed_count=2,public_tables={'by_name':[{'segment':0,'offset':0x100,'display_flag':'idle','name':'start'}],
        'by_value':[{'segment':0,'offset':0x100,'display_flag':'idle','name':'start'}]},entry_source='OMF MODEND/PUBDEF',
        empty_data_display='logical code end, zero allocated bytes')

def verify_outputs(obj_raw,com,map_raw,target):
    require(len(target)==SIZE and hashlib.sha256(target).hexdigest()==TARGET_SHA,"target identity differs")
    require(len(com)==SIZE and com==target,"complete unmodified COM differs")
    obj=parse_object(obj_raw)
    require(obj["resolved"]==com,"natural OMF resolution differs from linked COM")
    rows=decode(com);require(len(rows)==9 and sum(r["size"] for r in rows)==607,"code coverage differs")
    code=set()
    for row in rows:
        extent=set(range(row["start"]-0x100,row["start"]-0x100+row["size"]))
        require(not code&extent,"overlapping code procedures");code.update(extent)
    data=set(range(0x13d,0x313))|set(range(0x435,SIZE))
    require(len(data)==783 and not code&data and code|data==set(range(SIZE)),"complete code/data partition differs")
    require(com[0x13d:0x313]==target[0x13d:0x313] and com[0x435:]==target[0x435:],
        "783 initialized data bytes differ")
    mp=verify_map(map_raw,obj)
    return dict(raw_equal=True,object_resolution_equal=True,procedure_count=len(rows),
        code_bytes=607,data_bytes=783,procedures=rows,complete_partition=True,omf_sha256=hashlib.sha256(obj_raw).hexdigest(),
        com_sha256=hashlib.sha256(com).hexdigest(),map=mp,exact_acceptance=False)
