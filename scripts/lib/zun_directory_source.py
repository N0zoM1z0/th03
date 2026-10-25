"""Consume the linked directory as production DATA, with an independent contract.

The shared historical constructor remains a frozen MAIN scheduling input.
It supplies the format oracle here; the returned product contains the complete
native directory contribution, without selecting or patching individual bytes.
"""
from lib.zun import compose_launcher


def compose_native_launcher(stub,call,helper,names,payloads,*,directory_bytes):
    candidate = stub+directory_bytes+call+b''.join(payloads)+helper
    expected = compose_launcher(stub,call,helper,names,payloads)
    if candidate != expected:
        raise ValueError('native directory differs from the complete composition contract')
    return candidate
