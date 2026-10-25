"""Keep historical staging receipts immutable, then consume live source edits.

Only the explicitly listed historical bytes come from Git. Every other input
is read from the current tree and still passes the historical stagers' checks.
The temporary read view produces no native output and is removed immediately.
"""
from pathlib import Path
import hashlib,os,subprocess,tempfile
import stage_th03_op_fullcold as base
import stage_th03_op_nopcall as historical

HISTORICAL_REVISION='a02fcc977422e933d10455df1fc911c37ca2ad1c'
LIVE_SOURCES=('src/op/menu/menu_state.inl',)

def need(v,m):
    if not v:raise ValueError('current OP source overlay: '+m)

def payload(root):
    root=Path(root)
    names=subprocess.check_output(['git','ls-files','--cached','-z'],cwd=root).decode().split('\0')
    need(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names if n),'bounded tracked input paths')
    archive=root/base.ARCHIVE
    need(archive.is_file() and not archive.is_symlink(),'attested reference source archive')
    with tempfile.TemporaryDirectory(prefix='OP-source-read-',dir=root/'.analysis') as temp:
        view=Path(temp)
        for name in names:
            if not name or name in LIVE_SOURCES:continue
            p=root/name
            if not p.is_file():continue
            need(not any(q.is_symlink() for q in (p,*p.parents)),'regular live historical input: '+name)
            q=view/name;q.parent.mkdir(parents=True,exist_ok=True);os.link(p,q)
        q=view/base.ARCHIVE;q.parent.mkdir(parents=True,exist_ok=True);os.link(archive,q)
        for name in LIVE_SOURCES:
            raw=subprocess.check_output(['git','show',HISTORICAL_REVISION+':'+name],cwd=root)
            need(hashlib.sha256(raw).hexdigest()==base.INPUT_HASHES[name],'original historical source binding: '+name)
            q=view/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
        files=historical.payload(view)
    for name in LIVE_SOURCES:
        p=root/name
        need(name in files and p.is_file() and not any(q.is_symlink() for q in (p,*p.parents)),
             'explicit current maintained source: '+name)
        files[name]=p.read_bytes()
    return files
