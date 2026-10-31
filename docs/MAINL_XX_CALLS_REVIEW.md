# MAINL xx DOS member-call adapters

The maintained xx.cpp links through the normal library as an unaccepted
candidate;see [current product review](MAINL_XX_PRODUCT_REVIEW.md). The current
full-TU proof is followed by the retained miniature and its separate ABI context.
Source presence stays250 extents/60,028 gross bytes;accepted MAINL is unchanged.

## Current full-TU call-bank recovery

The actual native BCC/normal893-member-library link now matches the entire
original1495-byte bank at0000:5D3C..6312,including all88 literal ordered native
fields and168 inline switch-table bytes. callCopyCtor750,callDestructor392 and
callMemberFunc185 each match complete linked bodies. Together with the earlier
type prefix,the first2822 xx object/linked bytes and92 ordered fields agree.
These are bounded exact observations inside the still-unaccepted xx candidate;
the accepted211-owner publication and28-provider library remain unchanged.

The17-byte copy-constructor gap came from six missed common call/cleanup tails.
Replacing four virtual-base near-this transfers with `_SI = FP_OFF(destination)`
keeps those SI writes visible to BCC's optimizer. The nonvirtual path retains
its actual inline ASM moves. Both forms emit the required MOV SI from the far
pointer's offset;no calling convention,argument,storage or instruction patch
is added. Source spelling is a recovery choice,not proof of original variable
names or exact historical spelling.

Focused native controls distinguish the two paths:

| SI expression change | Copy bytes | Complete object result |
| --- | ---: | --- |
| Original ASM transfers | 767 | Six unshared tails |
| All near-this transfers use register variables | 750 | One wrong JMP byte at+2BBh |
| Only nonvirtual transfers use register variables | 767 | Tail gap retained |
| Only virtual-base transfers use register variables | 750 | All750 bytes agree |

With register variables everywhere,the branch at+2BAh goes to another JMP at
+2C5h instead of the original direct epilogue at+2E7h. Its size still agrees;
complete byte comparison rejects it. The adopted four assignments recover both
the common tails and that final direct branch. The maintained product reviewer
requires the whole1495 bytes,all88 fields,and complete2822-byte prefix. Native
source-file/LINNUM records still bind all50 procedure boundaries.

Affected calls/catch/types/throw/full-TU/normal-product native pairs repeat their
complete raw outputs. The three existing real callback probes still agree in
registers,DS,stack words and cleanup. Unchanged dispatch/destruction pairs and
938 cold outputs are reused;there is no new exhaustive flag matrix or full cold
replay. Current native xx CODE12554/187 fields and EXE67308 remain different from
original12622/187 and67372. The retained S/TASM full-TU diagnostic instead has
CODE12553/181 fields. Current proof/control records are
`.analysis/work/xx-copy-tail-recovery.json` and `mainl-xx-product-review.json`.

## Retained call miniature

`src/mainl/crt/xx_calls.inl` recovers the copy-constructor,destructor and member
call adapters of the original monolithic DOS `xx.cpp`. It precedes the recovered
dispatch/destruction includes in that TU. Both destruction call edges now resolve
to real private near functions. Original bank0000:5D3C..6312 spans1495 bytes:
1327 instructions and168 actual CS switch-table bytes. Recovery added one source-present
extent. With the later [catch/type bank](MAINL_XX_CATCH_REVIEW.md) and
[type matcher](MAINL_XX_TYPES_REVIEW.md),the then-source scope was246 extents/
55,702 gross bytes. Accepted MAINL
remains211 extents/288 procedures/36,946 bytes,with zero new exact credit.

| Procedure | Original address | Instruction bytes | Following CS data |
| --- | --- | ---: | ---: |
| callCopyCtor | 5D3C | 750 | 96 |
| callDestructor | 608A | 392 | 48 |
| callMemberFunc | 6242 | 185 | 24 |

All three return near cdecl. Their caller arguments occupy14,12 and10 bytes.
The constructor's750-byte body ends at6029,followed by two24-WORD tables;
its next-function gap is846 bytes,not750 instruction bytes. The destructor's
24-WORD table begins6212; the member adapter's12-WORD table begins62FB.
6313 begins the next routine's exception metadata and is outside this owner.
Direct native decoding verifies full bodies,returns,branches and all84 table
destinations. Resolving the88 original literal ordered CODE-offset fields from
the original OMF reproduces the entire1495-byte linked bank. There are no MZ
segment words or new storage claims in this range. No database observations were
needed for this review;the fixed Japanese decoded target and original OMF/MAP
were inspected directly.

The adapters obtain callback DS from the runtime prefix reached through SS:16,
save the incoming DS and restore it before returning. They preserve the actual
SI/DI/BP frame. Mask1 selects a far function,4 a far this-pointer,2 Pascal,20
fastcall,80 SI/DS:SI this,and100 the Pascal this-last form. The copy adapter uses
1000 to add the zero virtual-base flag. Destructor flags are2 when its separate
virtual-base argument is nonzero. The compact switch kind is built with the
original conditional bit operations. Unsupported combinations retain the
original empty default; no defensive callback or validation is inserted.
The member adapter decodes only1/4/2/20; it does not inspect80/100/1000.

The16-bit fastcall signatures put this last. A virtual-base copy receives
`(0,source,destination)`: with near pointers,AX is0,BX is source and DX is
destination. A nonvirtual copy uses `(source,destination)`; a destructor uses
`(flags,destination)`. Writing ordinary this-first signatures produces wrong
register values and reverses far-pointer stack arguments. The far fastthis
paths temporarily load DS:SI from the object and restore callback DS afterward;
the outer save then restores the adapter caller's DS. Pascal paths preserve
callee cleanup and the original argument order.

Natural typed calls express near/far,cdecl,Pascal and fastcall conventions.
Symbolic inline assembly supplies the explicit DS and SI transfers required by
fastthis. An empty switch default is a normal source construct; it also retains
the original compiler's final branch shape for the two smaller helpers. No
opcode arrays,padding or object patches are used. The later Borland
[xx source](https://github.com/earthsiege2/borland-cpp-ide/blob/a0bdb214ae2a492edef4f82c91c55ec86394e7b3/SOURCE/RTL/SOURCE/EXCEPT/XX.CPP)
provided structural context; its flat calling conventions and extra type/flags
arguments are not the DOS ABI.

The same scoped BCC4.5 `-O2-pg -Os -O-i -Z- -S` / TASM5 / miniature TLINK route
builds call adapters followed by dispatch and destruction. Two rounds repeat
whole generated ASM,two-OBJ,EXE and MAP vectors. Complete timestamped TASM
listings are retained separately. All64 available SDK headers are bound; a
consumed-header subset is not inferred. The shared diagnostic driver's changes
also refreshed the affected earlier two miniatures; the original938-output
cold pair and211-owner publication/verifier inputs remain validated and unchanged.

The refreshed diagnostic call bank is1495 bytes:750,392 and185 instruction bytes
plus168 table bytes. Whole miniature CODE is5562,empty DATA and8 callback BSS
bytes;15 other runtime interfaces remain
unresolved. The original covered banks total5560 bytes in two separate ranges;
the code between6313 and72B3 is excluded from this miniature and is recovered
in later banks. The candidate
CS table operands and literal relocation stream retain their actual offsets.
Its linked bank starts at0000:0000,so its literal table addresses differ from
the original product. The separate normal native product proof above checks
complete raw bank equality at its original position. No whole-TU acceptance
follows from either diagnostic.

Three small probes execute the real target adapters and real compiled source
adapters against actual TASM-built callbacks: virtual-base fastcall copy,
far DS:SI cdecl destruction,and far Pascal member call. Each callback observes
the original register/stack arguments exactly once; both adapters return with
SPFF02 and unchanged incoming DS/SS/BP/SI/DI. Callback code occupies separate
probe memory,has no native fixups and does not alter either program image.
Unresolved runtime helpers remain traps and are never executed. This resolves
the specific register,DS and cleanup questions without an exhaustive flag matrix
or a runtime helper model; physical DOS and complete exception behavior remain open.

The later catch bank supplies exceptionHandled/initCatchArg/_CatchCleanup and
connects the real copy adapter. Its current miniature has14 unresolved interfaces.
This earlier three-bank miniature retains its15 diagnostic providers and has
been refreshed for the shared header/driver/profile. Explicit -O-i preserves
library memory calls in the later catch code; these three adapters have none.
