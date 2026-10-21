"""Compose original symbolic root-tail providers and explicit root declarations."""
from pathlib import Path
from lib.mainl_staff_source import statements
NAMES = ('dos_keyclear', 'grcg_setcolor', 'iatan2', 'js_end', 'random', 'soundio', 'text_clear', 'text_fillca', 'respal_exist', 'respal_set_palettes', 'js_start', 'js_sense', 'pf_str_ieq')
ROOT_ANCHORS = {'root_zero_font': 'include src/mainl/resources/gdc_outpw.asm', 'joystick_prefix': 'include src/mainl/archive_io/pfint21.asm', 'joystick_suffix': 'include libs/master.lib/js_sense.asm'}
PROVIDER_PATHS = {n: 'libs/master.lib/'+n+'.asm' for n in NAMES}
def load_inputs(carrier, source_root):
    carrier, source_root = Path(carrier), Path(source_root)
    providers = {n:(carrier/p).read_bytes() for n,p in PROVIDER_PATHS.items()}
    providers.update({n:b"\t\tdb 0\n" for n in ROOT_ANCHORS})
    maintained = {n:(source_root/('src/mainl/root_tail/'+n+'.asm')).read_bytes() for n in providers}
    return providers, maintained
def compose(root_asm, providers, maintained):
    names=set(NAMES)|set(ROOT_ANCHORS)
    if set(providers)!=names or set(maintained)!=names:
        raise ValueError("complete root-tail provider set required")
    root=root_asm.replace(b"\r\n",b"\n"); generated={}
    for name in names:
        if statements(providers[name])!=statements(maintained[name]):
            raise ValueError("root-tail source statements differ: "+name)
    # Anchor replacements precede include replacement, so original context is exact.
    for name,anchor in ROOT_ANCHORS.items():
        old=anchor.encode()+b"\n\t\tdb 0\n"
        if root.count(old)!=1: raise ValueError("root declaration boundary differs: "+name)
        if statements(providers[name])!=statements(b"\t\tdb 0\n"):
            raise ValueError("root declaration differs")
        new=anchor.encode()+b"\ninclude src/mainl/root_tail/"+name.encode()+b".asm\n"
        root=root.replace(old,new,1)
    for name,path in PROVIDER_PATHS.items():
        old=("include "+path).encode()
        new=("include src/mainl/root_tail/"+name+".asm").encode()
        if root.count(old)!=1 or new in root:
            raise ValueError("root-tail include boundary differs: "+name)
        root=root.replace(old,new,1)
    for name in names:
        path='src/mainl/root_tail/'+name+'.asm'
        generated[path]=maintained[name].replace(b"\r\n",b"\n").replace(b"\n",b"\r\n")
    generated['th03_mainl.asm']=root.replace(b"\n",b"\r\n")
    return generated
def stage(destination, generated):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=False)
    for name,raw in generated.items():
        p=destination/name;p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as out:out.write(raw)
