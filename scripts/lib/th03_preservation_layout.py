"""Pure TH03 Marisa layout checks; no retained-run paths or execution."""

import re

from lib.pc98 import parse_mz

TARGET_SHA = "f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b"

ALIASES = {
"_hitcircles_enemy_add_do_not_rand":0x2881, "_marisa_gauge_y":0x2884,
"_marisa_gauge_frame":0x2888, "_marisa_chargeshots":0x288A,
"_marisa_chargeshot_p":0x28EE, "_marisa_bullet_angle":0x28F0,
"_marisa_bomb_point":0x28F2, "_kotohime_bomb_explosion_y":0x28F6,
"_gauge_pattern_timing":0x2D58, "_kotohime_exatt_pattern":0x2D58}

def require(ok, msg):
    if not ok: raise ValueError(msg)

def relocs(image, lo, hi):
    result=[]
    for r in image.relocations:
        p=r.linear
        require(not (p < lo < p+2 or p < hi < p+2), "cross-boundary relocation")
        if lo <= p < hi:
            result.append((r.segment,r.offset))
    return result

def contributions(text):
    pat=r"^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4,8})\s+C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)\s+ACBP=(\d+)\s*$"
    return [(int(a,16),int(b,16),int(c,16),d,e,f,g.replace("\\","/"),int(h))
            for a,b,c,d,e,f,g,h in re.findall(pat,text,re.M)]

def check_layout(rows, split):
    parts=[(0x900,0x5E5,"th03/cs_mari.cpp"),(0xEE5,0x1C1,"th03/bm_mari.cpp")] if split else [(0x900,0x7A6,"th03/cs_mari.cpp")]
    for off,size,module in parts+[(0x10A6,0xE7F,"th03_main.asm"),(0x1F25,0x10A,"th03/hitbox.cpp")]:
        wanted=(0x139D,off,size,"CODE","HITBOX_TEXT","MAIN_04",module,28)
        require(rows.count(wanted)==1, "MAP ownership mismatch: "+repr(wanted))
    actual=[r for r in rows if r[3]=="CODE" and r[2] and r[0]*16+r[1]<0x159FF and r[0]*16+r[1]+r[2]>0x142D0]
    require(len(actual)==len(parts)+2, "unexpected overlapping CODE contributor")
    for module in [p[2] for p in parts]:
        for kind in ["DATA","BSS"]:
            rs=[r for r in rows if r[6]==module and r[3]==kind]
            require(bool(rs) and all(r[2]==0 for r in rs), "new or missing "+kind+" contribution: "+module)

def check_aliases(text):
    for name,off in ALIASES.items():
        matches=re.findall(r"^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+"+re.escape(name)+r"\s*$",text,re.M)
        require(bool(matches) and set(matches)=={("1D56",f"{off:04X}")},"alias moved or absent: "+name)
