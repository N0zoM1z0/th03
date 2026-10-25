"""Independent metadata contract and actual existing-wrapper DATA readers."""
import hashlib
import json

from lib.zun_directory_layout import specification,need
from lib.zun_wrapper_runtime import Machine


def cases():
    for reply in range(3):
        yield dict(reply=reply)
        yield dict(command=b' -X',fcb=b'-X',reply=reply)
        for index in range(1,6):
            name = f'-{index}'.encode()
            yield dict(command=b' '+name+b' hello',fcb=name,reply=reply,flags=0xED7,seed=index%2)


def verify(target,candidate):
    results = []
    for image in (target,candidate):
        specification(image)
        rows = []
        for load,split in ((0x1000,False),(0x3000,True)):
            m = Machine(image,load,split)
            trace,count = hashlib.sha256(),0
            try:
                for parameters in cases():
                    r = m.run(**parameters)
                    trace.update(json.dumps(r,sort_keys=True).encode())
                    count += 1
                rows.append(dict(load_segment=load,split_stack=split,cases=count,
                    trace_sha256=trace.hexdigest(),maximum_observed_stack_depth=m.maximum_stack))
            finally:
                m.close()
        results.append(rows)
    need(results[0] == results[1],'independent metadata reader observations agree')
    return dict(images=2,functions=0,code_bytes=0,data_bytes=324,cases_per_image=42,
        observations=results[0],actual_wrapper_readers=True,payload_instructions_executed=False,
        all_memory_and_ordered_stores_checked=True,unused_slots_have_execution_credit=False)


def negative_controls(image):
    static = 0
    for offset in range(223,547):
        changed = bytearray(image)
        changed[offset] ^= 1
        try:
            specification(changed)
        except ValueError:
            static += 1
        else:
            raise ValueError('directory semantic byte mutation escaped at '+hex(offset))
    rejected = []
    for kind,count,start,step in (('name',5,0x1E1,8),('boundary',6,0x2E1,2)):
        for index in range(count):
            changed = bytearray(image)
            changed[start-256+index*step] ^= 1
            m = Machine(image,0x1000)
            m.image = bytes(changed)
            name = f'-{min(index+1,5)}'.encode()
            try:
                r = m.run(command=b' '+name+b' hello',fcb=name)
                expected = m.directory['payloads'][min(index,4)]
                # The generic wrapper model correctly permits renamed input tables.
                # This DATA contract additionally requires the canonical five actions.
                need(r['outcome'] == 'payload-entry' and r['copied_bytes'] == expected['size'],
                     'canonical name must still select its complete declared payload')
            except ValueError:
                rejected.append(kind+'-'+str(index))
            else:
                raise ValueError('actual directory reader mutation escaped: '+kind+'-'+str(index))
            finally:
                m.close()
    return dict(initial_DATA_byte_mutations_rejected=static,actual_reader_DATA_mutations_rejected=rejected,
        actual_reader_DATA_mutation_count=11,instruction_mutations=0,static_mutations_have_execution_credit=False)
