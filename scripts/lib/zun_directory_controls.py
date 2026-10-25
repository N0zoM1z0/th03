"""Native source controls distinguish fixed directory slots from arbitrary fill."""
import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory


def run(files,parent,tasm,dos,execute,target,definitions):
    results = []
    original = files['wrapper/meta.asm']
    if original.count(b'DIRECTORY_CAPACITY equ 32') != 1:
        raise ValueError('directory capacity source declaration drift')
    for capacity in (31,33):
        with TemporaryDirectory(prefix='',dir=parent) as folder:
            work = Path(folder)
            source = original.replace(b'DIRECTORY_CAPACITY equ 32',f'DIRECTORY_CAPACITY equ {capacity}'.encode())
            (work/'meta.asm').write_bytes(source)
            (work/'meta.rsp').write_bytes(files['wrapper/meta.rsp'])
            label = f'control:directory-capacity-{capacity}'
            execute(tasm+[f'/d{k}={v}' for k,v in definitions.items()]+['meta.asm,meta.obj'],work,label+'-assemble')
            execute(dos+['tlink','@meta.rsp'],work,label+'-link')
            candidate = (work/'meta.com').read_bytes()
            if candidate == target or len(candidate) != 2+8*capacity+2*(capacity+1):
                raise ValueError('native wrong-capacity control did not change the actual directory extent')
            results.append(dict(capacity=capacity,bytes=len(candidate),byte_exact_rejected=True,
                source_sha256=hashlib.sha256(source).hexdigest(),candidate_sha256=hashlib.sha256(candidate).hexdigest(),
                object_sha256=hashlib.sha256((work/'meta.obj').read_bytes()).hexdigest(),
                changed_source_declarations=['DIRECTORY_CAPACITY'],native_definitions=definitions))
    return dict(count=2,source_only=True,object_patches=False,controls=results)
