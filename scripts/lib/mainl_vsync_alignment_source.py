"""Bounded symbolic source composition only; no native or binary access."""
import hashlib
SOURCE='src/mainl/display_hardware/vsync_data.asm'
ORIGINAL_SHA='eb2f410ec05fec6fb257ae19daca222e7a6c3d2ce5b4bf1ebaa53708643a8e09'
def lf(b):return b.replace(b'\r\n',b'\n')
CDG_SOURCE='src/mainl/display_hardware/cdg_data.asm'
CDG_SHA='e1f482f388bd1c0f924687cf346febc6a1058a135d29a0b630bd5989a8992755'
MAINTAINED_SHA='28d8242febd00e3dc7dcf2bbf21c4e3401e920611b42f136c5ffaad6fa408854'
CDG_MAINTAINED_SHA='1192ab317a5015ece2896d397ffb2e18c7def19da752eb8acf2af3e803c184d2'
def compose(root, original, maintained, cdg, maintained_cdg):
    root=lf(root);original=lf(original);maintained=lf(maintained);maintained_cdg=lf(maintained_cdg)
    if hashlib.sha256(maintained).hexdigest()!=MAINTAINED_SHA or hashlib.sha256(maintained_cdg).hexdigest()!=CDG_MAINTAINED_SHA:raise ValueError("reviewed maintained alignment source differs")
    if hashlib.sha256(original).hexdigest()!=ORIGINAL_SHA:raise ValueError('original VSync storage differs')
    marker=b'\t.data\n';old=b'include libs/master.lib/vs[data].asm\n'
    if root.count(marker)!=1 or root.count(old)!=1 or b'mainl_data_origin' in root:raise ValueError('unique DATA/include boundary required')
    if original.count(b'\tEVEN\n')!=1:raise ValueError('unique historical alignment required')
    if b'\tEVEN\n' in maintained or maintained.count(b'mainl_vsync_storage_even mainl_data_origin')!=1:raise ValueError('named alignment invocation required')
    changed=root.replace(marker,marker+b'mainl_data_origin label byte\n').replace(old,('include '+SOURCE+'\n').encode())
    cdg=lf(cdg)
    if hashlib.sha256(cdg).hexdigest()!=CDG_SHA:raise ValueError('original CDG storage differs')
    cdg_include=b'include th03/formats/cdg[data].asm\n'
    anchor=b"_CUTSCENE_KANJI\tdb  '  ', 0\n\teven\n"
    if changed.count(cdg_include)!=1 or changed.count(anchor)!=1:raise ValueError('unique ordinary DATA alignment boundaries required')
    changed=changed.replace(cdg_include,('include '+CDG_SOURCE+'\n').encode()).replace(anchor,anchor.replace(b'\teven\n',b'\tevendata\n'))
    return {'th03_mainl.asm':changed,SOURCE:maintained,CDG_SOURCE:maintained_cdg}

