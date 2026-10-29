#!/usr/bin/env python3
"""Compose the next real xx bank without changing the shared miniature recipe."""
import probe_th03_mainl_xx_dispatch as native

DRIVER='scripts/probe_th03_mainl_xx_types.py'
SOURCE='src/mainl/crt/xx_type_match.inl'
SUPPORT='scripts/lib/decoded_mainl_xx_types_probe.py'
REPORT='.analysis/work/mainl-xx-types-build.json'
TYPE_DECL=b'int near typeIDcaught(xx_type_ptr,xx_type_ptr far *,xx_type_ptr,unsigned,int);\n'


def wrapper(raw):
    native.need(raw.count(TYPE_DECL)==1 and raw.count(b'#include "xxcall.inl"')==1,'one diagnostic type forward declaration and original include position')
    return raw.replace(TYPE_DECL,b'').replace(b'#include "xxcall.inl"',b'#include "xxtypes.inl"\n#include "xxcall.inl"')


PROFILE=dict(stem='xx-types',driver=DRIVER,sources={'xxtypes.inl':SOURCE},
    wrapper=wrapper,context=native.trap_context,probe_support=[SUPPORT])


if __name__=='__main__':native.main(catch=True,extension=PROFILE)
