"""Original source inputs for historical graph regressions, independent of live edits."""
from pathlib import Path
import io,os,subprocess,tarfile,tempfile

REVISION='a02fcc977422e933d10455df1fc911c37ca2ad1c'

def payload(root,stager):
    root=Path(root);names=set(stager.INPUT_HASHES)
    raw=subprocess.check_output(['git','archive',REVISION,*sorted(names)],cwd=root)
    with tempfile.TemporaryDirectory(prefix='OP-historical-test-',dir=root/'.analysis') as temp:
        view=Path(temp);found=set()
        with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
            for member in archive.getmembers():
                if not member.isfile():continue
                if member.name not in names:raise ValueError('unexpected historical fixture input')
                p=view/member.name;p.parent.mkdir(parents=True,exist_ok=True)
                p.write_bytes(archive.extractfile(member).read());found.add(member.name)
        if found!=names:raise ValueError('incomplete historical fixture inputs')
        p=view/stager.ARCHIVE;p.parent.mkdir(parents=True,exist_ok=True);os.link(root/stager.ARCHIVE,p)
        return stager.payload(view)
