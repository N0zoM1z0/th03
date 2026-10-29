#!/usr/bin/env python3
"""Build the recovered whole xx TU with DOS include-name transport only."""
from pathlib import Path
import probe_th03_mainl_xx_dispatch as native

DRIVER='scripts/probe_th03_mainl_xx_rtti.py'
SOURCE='src/mainl/crt/xx_rtti.inl'
FRONT='src/mainl/crt/xx_front.inl'
UNIT='src/mainl/crt/xx.cpp'
SUPPORT='scripts/lib/decoded_mainl_xx_rtti_probe.py'
REPORT='.analysis/work/mainl-xx-rtti-build.json'
NAMES={'xxfront.inl':FRONT,'xxeq.inl':'src/mainl/crt/xx_type_equal.inl',
    'xxtypes.inl':'src/mainl/crt/xx_type_match.inl','xxcall.inl':'src/mainl/crt/xx_calls.inl',
    'xxthrow.inl':'src/mainl/crt/xx_throw.inl','xxcatch.inl':'src/mainl/crt/xx_catch.inl',
    'xxbank.inl':'src/mainl/crt/xx_dispatch.inl','xxdtor.inl':'src/mainl/crt/xx_destroy.inl',
    'xxrtti.inl':SOURCE}


def wrapper(raw):
    unit=(native.ROOT/UNIT).read_bytes()
    for short,path in NAMES.items():
        original=Path(path).name.encode()
        native.need(unit.count(b'#include "'+original+b'"')==1,
            'one original source-order include: '+path)
        unit=unit.replace(b'#include "'+original+b'"',b'#include "'+short.encode()+b'"')
    return unit


def context(imports):
    native.need('__8086' in imports and '___JumpToCatch__' not in imports,
        'CPU byte remains imported;real register jump resolves')
    traps=native.trap_context([n for n in imports if n!='__8086'])
    return traps.removesuffix(b'end\n')+(
        b"_DATA segment word public 'DATA'\npublic __8086\n__8086 db 0\n_DATA ends\nend\n")


PROFILE=dict(stem='xx-rtti',driver=DRIVER,
    sources=dict(NAMES,**{'xxunit.cpp':UNIT}),wrapper=wrapper,context=context,
    probe_support=[SUPPORT])


if __name__=='__main__':native.main(catch=True,extension=PROFILE)
