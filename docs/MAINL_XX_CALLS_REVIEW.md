# MAINL xx DOS member-call adapters

`src/mainl/crt/xx_calls.inl` recovers the copy-constructor,destructor and member
call adapters of the original monolithic DOS `xx.cpp`. It precedes the recovered
dispatch/destruction includes in that TU. Both destruction call edges now resolve
to real private near functions. Original bank0000:5D3C..6312 spans1495 bytes:
1327 instructions and168 actual CS switch-table bytes. This adds one source-present
extent; after the subsequent [catch/type bank](MAINL_XX_CATCH_REVIEW.md),current
source presence is245 extents/54,581 gross bytes. Accepted MAINL
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
needed for this turn; the fixed Japanese decoded target and original OMF/MAP
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

Candidate call bank is1512 bytes:767,392 and185 instruction bytes plus168 table
bytes. Copy-constructor tail sharing still differs by17 bytes. Whole candidate
CODE is5599,empty DATA and8 callback BSS bytes;15 other runtime interfaces remain
unresolved. The original covered banks total5560 bytes in two separate ranges;
the unrecovered code between6313 and72B3 is not silently included. The candidate
CS table operands and literal relocation stream retain their actual offsets.
Neither complete raw call-bank equality nor normal-library/whole-TU ownership
is claimed. Equal helper lengths alone do not earn exact credit.

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
