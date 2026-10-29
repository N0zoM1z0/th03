#!/usr/bin/env python3
"""Compile the DOS throw/unwind bank with its recovered private dependencies."""
import probe_th03_mainl_xx_dispatch as native

DRIVER='scripts/probe_th03_mainl_xx_throw.py'
SOURCE='src/mainl/crt/xx_throw.inl'
SUPPORT='scripts/lib/decoded_mainl_xx_throw_probe.py'
REPORT='.analysis/work/mainl-xx-throw-build.json'
TYPE_DECL=b'int near typeIDcaught(xx_type_ptr,xx_type_ptr far *,xx_type_ptr,unsigned,int);\n'


def wrapper(raw):
    native.need(raw.count(TYPE_DECL)==1 and raw.count(b'#include "xxcall.inl"')==1,
        'one diagnostic type declaration and adapter include position')
    return raw.replace(TYPE_DECL,b'').replace(b'#include "xxcall.inl"',
        b'#include "xxtypes.inl"\n#include "xxcall.inl"\n#include "xxthrow.inl"')


def context(imports):
    # CPU class is DATA, not a callable trap. It is initialized by a real DOS
    # startup in the complete product; this miniature supplies only its slot.
    native.need('__8086' in imports,'DOS CPU discriminator import')
    traps=native.trap_context([n for n in imports if n!='__8086'])
    from lib.decoded_mainl_xx_throw_probe import CALLBACK
    traps=traps.replace(b'_TEXT ends',CALLBACK+b'_TEXT ends')
    return traps.removesuffix(b'end\n')+(
        b"_DATA segment word public 'DATA'\npublic __8086\n__8086 db 0\n_DATA ends\nend\n")


PROFILE=dict(stem='xx-throw',driver=DRIVER,
    sources={'xxtypes.inl':'src/mainl/crt/xx_type_match.inl','xxthrow.inl':SOURCE},
    wrapper=wrapper,context=context,probe_support=[SUPPORT])


if __name__=='__main__':native.main(catch=True,extension=PROFILE)
