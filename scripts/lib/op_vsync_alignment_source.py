"""Source-only historical OP VSync alignment overlay, after global-order composition."""
import hashlib
SOURCE = 'src/op/hardware/vsync_data.asm'
CDG_SOURCE = 'src/op/hardware/cdg_data.asm'
def lf(b): return b.replace(b'\r\n', b'\n')
def sha(b): return hashlib.sha256(b).hexdigest()
def compose(root, original_vs, original_cdg, maintained_vs, maintained_cdg):
    root, original_vs, original_cdg, maintained_vs, maintained_cdg = map(lf, (root, original_vs, original_cdg, maintained_vs, maintained_cdg))
    expected = {'root': '6f65388d96dd6811563227d510963be8b3815cde7603f9dd7f117f63e34170ca', 'original_vs': 'eb2f410ec05fec6fb257ae19daca222e7a6c3d2ce5b4bf1ebaa53708643a8e09', 'original_cdg': 'e1f482f388bd1c0f924687cf346febc6a1058a135d29a0b630bd5989a8992755', 'maintained_vs': 'caf01e2fbcac167df7943df64161b227233073845ca4b2fb5d8f1328b1f496c1', 'maintained_cdg': '1192ab317a5015ece2896d397ffb2e18c7def19da752eb8acf2af3e803c184d2'}
    for label, raw in [('root',root),('original_vs',original_vs),('original_cdg',original_cdg),('maintained_vs',maintained_vs),('maintained_cdg',maintained_cdg)]:
        if sha(raw) != expected[label]: raise ValueError('source drift: '+label)
    marker=b'\t.data\n'
    old=b'include libs/master.lib/vs[data].asm\n'
    cdg=b'include th03/formats/cdg[data].asm\n'
    if root.count(marker)!=1 or root.count(old)!=1 or root.count(cdg)!=1 or b'op_data_origin' in root: raise ValueError('unique source boundary required')
    result=root.replace(marker,marker+b'op_data_origin label byte\n').replace(old,('include '+SOURCE+'\n').encode()).replace(cdg,('include '+CDG_SOURCE+'\n').encode())
    return {'th03_op.asm':result,SOURCE:maintained_vs,CDG_SOURCE:maintained_cdg}
