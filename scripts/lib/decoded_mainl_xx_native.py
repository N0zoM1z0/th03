"""Bind native BCC procedure extents to actual source and OMF line records."""
import re
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from lib.omf import parse_omf
from build_th03_mainl_display_work import payload


def need(condition,message):
    if not condition:
        raise ValueError('MAINL native xx: '+message)


def source_definitions(sources,names):
    # Preserve line positions while excluding comments and literal contents.
    token=re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27',re.S)
    clean={path:token.sub(lambda m:re.sub(r'[^\n]',' ',m.group()),raw.decode())
        for path,raw in sources.items()}
    result=[]
    for name in names:
        found=[]
        for path,text in clean.items():
            for match in re.finditer(r'(?<![\w:])'+re.escape(name)+r'\s*\(',text):
                cursor=match.end();depth=1
                while cursor<len(text) and depth:
                    depth+=(text[cursor]=='(')-(text[cursor]==')');cursor+=1
                cursor+=len(text[cursor:])-len(text[cursor:].lstrip())
                if text[cursor:cursor+5]=='const':
                    cursor+=5;cursor+=len(text[cursor:])-len(text[cursor:].lstrip())
                if text[cursor:cursor+1]!='{':continue
                end=cursor+1;depth=1
                while end<len(text) and depth:
                    depth+=(text[end]=='{')-(text[end]=='}');end+=1
                need(depth==0,'complete source definition: '+name)
                found.append(dict(source=path,source_name=name,
                    source_line=text.count('\n',0,match.start())+1,
                    source_end_line=text.count('\n',0,end-1)+1))
        need(len(found)==1,'one actual source definition: '+name)
        result.append(found[0])
    return result


def native_bodies(obj,asm,sources,original_bodies,baseline_bodies):
    definitions=source_definitions(sources,[q['name'] for q in original_bodies])
    symbols=[(n.decode(),k.decode()) for n,k in re.findall(
        rb'^\s*(\S+)\s+proc\s+(near|far)\s*$',asm,re.M)]
    need(len(symbols)==len(definitions)==50 and symbols==[
        (q['name'],q['return_kind']) for q in baseline_bodies],
        'same50 compiler procedure names and near/far declarations')
    line_files={};current=None
    for record in parse_omf(obj):
        if record.name=='COMENT' and record.data[:2]==b'\0\xe8':
            data=record.data
            need(len(data)>=8 and len(data)==8+data[3],'complete native source-file record')
            current=data[4:4+data[3]].decode()
        if record.name=='LINNUM':
            need(current in sources and record.data[:2]==b'\0\1' and
                (len(record.data)-2)%4==0,'16-bit CODE line records for a transported source')
            line_files.setdefault(current,[]).extend(struct.iter_unpack('<HH',record.data[2:]))
    starts=[];epilogues=[]
    for definition in definitions:
        pairs=line_files.get(definition['source'],[])
        begin={at for line,at in pairs if line==definition['source_line']}
        end={at for line,at in pairs if line==definition['source_end_line']}
        need(len(begin)==len(end)==1,'one native declaration/closing-brace position: '+definition['source_name'])
        starts.append(begin.pop());epilogues.append(end.pop())
    need(starts==sorted(set(starts)) and starts[0]==0,'original source order and disjoint native starts')
    p=payload(obj);code=bytes(p[1,i] for i in range(sum(seg==1 for seg,off in p)))
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);rows=[]
    for definition,(name,kind),start,epilogue,limit in zip(
        definitions,symbols,starts,epilogues,starts[1:]+[len(code)]):
        need(start<=epilogue<limit,'source epilogue is within its native procedure')
        end=None
        for instruction in decoder.disasm(code[epilogue:limit],epilogue):
            if instruction.mnemonic in ('ret','retf'):
                need(instruction.mnemonic==('ret' if kind=='near' else 'retf'),
                    'native epilogue retains the declared return ABI')
                end=instruction.address+instruction.size;break
        need(end is not None,'actual return after the source closing-brace line')
        rows.append(dict(name=name,start=start,size=end-start,return_kind=kind,
            epilogue=epilogue,**definition))
    return rows
