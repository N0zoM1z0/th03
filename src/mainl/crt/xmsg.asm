; Borland C++ original xmsg: constructor, copy constructor, destructor,
; raise and copy-assignment with complete exception-frame records and RTTI.
; Original Japanese MAINL CL.LIB CRT member 337, _TEXT 955 bytes.
; CODE pointers below are symbolic 16:16 OMF relocations, not raw CODE arrays.
; The real Borland compiler emitted its CODE fixups backwards. TASM uses
; forward emission, so the original semantic instruction and RTTI blocks
; below are written in *reverse physical offset order* using typed ORG.
; All offsets are original code-block boundaries. No filler, target CODE
; blobs, or linked-EXE/OBJ patches are inserted to manufacture equality.
; This preserves the original ordered DOS MZ relocation table, not the
; literal Borland FIXUPP record sequence.
.8086
extrn @$bnew$qui:far
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn @_ThrowException$qnvt1t1t1uiuiuinuc:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @string@$bctr$qmx6string:far
extrn @string@$bdtr$qv:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @xmsg@$bctr$qmx6string,@xmsg@$bctr$qmx4xmsg
public @xmsg@$bdtr$qv,@xmsg@raise$qv,@xmsg@$basg$qmx4xmsg



org 897
rtti_string:
    dw 4,3,38,-1,3,46,50
    dw 0,0,0,0,0,0,1,1
    dd @string@$bdtr$qv
    dw 5,54
    db 'string',0
    db 0 ; one alignment byte of the class name
    dw 0,0,0,0,0,0

org 878
rtti_string_pointer:
    dw 4,2010h,10
    dd rtti_string
    db 'string *',0

org 822
; Original typed Borland RTTI for xmsg, shared string* and string.
rtti_xmsg:
    dw 4,3,38,-1,3,44,48
    dw 0,0,0,0,0,0,1,1
    dd @xmsg@$bdtr$qv
    dw 5,52
    db 'xmsg',0
    db 0 ; one alignment byte of the class name
    dw 0,0,0,0,0,0

org 751
    call @string@$bctr$qmx6string
    add sp,8
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov word ptr [bp-22],6

branch_030e:
    mov dx,[bp-2]
    mov ax,[bp-4]
    les bx,[bp+6]
    mov es:[bx+2],dx
    mov es:[bx],ax

branch_031e:
    mov dx,[bp+8]
    mov ax,[bp+6]
    push dx
    push ax
    push word ptr [bp-34]
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf


org 704
    call @string@$bdtr$qv
    add sp,6
    mov ax,4
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    jz branch_030e
    mov word ptr [bp-22],14
    les bx,[bp+10]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    push dx
    push word ptr [bp-4]

org 645
    mov ax,seg _TEXT
    mov bx,offset _TEXT:xmsg_assign_state
    call ___InitExceptBlocks
    mov dx,[bp+8]
    mov ax,[bp+6]
    cmp dx,[bp+12]
    jnz branch_02a0
    cmp ax,[bp+10]
    jz branch_031e

branch_02a0:
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    mov ax,3
    push ax
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]

org 637
; Assignment: handle self-assignment, destruct the old string,
; allocate and construct the copy, and unwind the temporary exception frame.

@xmsg@$basg$qmx4xmsg:
    push bp
    mov bp,sp
    sub sp,34
    push si
    push di

org 601
; Exception-frame descriptor preceding operator=(const xmsg&).
xmsg_assign_frame:
    dd rtti_string_pointer
    dw 2087h,-4
    dw 0,0,0
xmsg_assign_state:
    dw 0,0
    dw -34,0,5,0,-1,6,5,0
    dw offset _TEXT:xmsg_assign_frame


org 547
    mov ax,seg _TEXT
    push ax
    mov ax,offset _TEXT:@xmsg@$bctr$qmx4xmsg
    push ax
    xor ax,ax
    push ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    push ss
    lea ax,[bp-34]
    push ax
    push cs
    call @xmsg@$bctr$qmx4xmsg
    add sp,8
    lea ax,[bp-34]
    push ss
    push ax
    push cs
    mov ax,offset _TEXT:rtti_xmsg
    push ax
    call @_ThrowException$qnvt1t1t1uiuiuinuc
    add sp,26
    pop di
    pop si
    mov sp,bp
    pop bp
    retf


org 526
    mov ax,seg _TEXT
    mov bx,offset _TEXT:xmsg_raise_scope
    call ___InitExceptBlocks
    xor ax,ax
    push ax
    push ax
    push ax
    push ax
    mov ax,5
    push ax

org 518
; Throw a typed xmsg with an on-stack copy and far Borland exception RTTI.

@xmsg@raise$qv:
    push bp
    mov bp,sp
    sub sp,34
    push si
    push di

org 512
xmsg_raise_scope:
    dd xmsg_raise_frame
    dw -30


org 504
; The raise() exception block and far destructor-table frame.
xmsg_raise_frame:
    dd rtti_xmsg
    dd 0

org 473
    call @string@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz branch_01f4
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @$bdele$qnv
    pop cx
    pop cx

branch_01f4:
    pop di
    pop si
    pop bp
    retf


org 410
; Release the referenced string, then conditionally delete the handle.

@xmsg@$bdtr$qv:
    push bp
    mov bp,sp
    push si
    push di
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov ax,[bp+6]
    or ax,[bp+8]
    jz branch_01f4
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    mov ax,3
    push ax
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]

org 325
    call @string@$bctr$qmx6string
    add sp,8
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov word ptr [bp-22],6

branch_0164:
    mov dx,[bp-2]
    mov ax,[bp-4]
    les bx,[bp+6]
    mov es:[bx+2],dx
    mov es:[bx],ax

branch_0174:
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    push word ptr [bp-34]
    call ___ExitExceptBlocks
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf


org 247
    mov ax,seg _TEXT
    mov bx,offset _TEXT:xmsg_copy_state
    call ___InitExceptBlocks
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz branch_011e
    mov ax,4
    push ax
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz branch_0174

branch_011e:
    mov ax,4
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    jz branch_0164
    mov word ptr [bp-22],14
    les bx,[bp+10]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    push dx
    push word ptr [bp-4]

org 239
; Construct xmsg from xmsg: duplicate the embedded Borland string,
; retain original heap and exception bookkeeping.

@xmsg@$bctr$qmx4xmsg:
    push bp
    mov bp,sp
    sub sp,34
    push si
    push di

org 203
; Exception-frame descriptor preceding copy construction.
xmsg_copy_frame:
    dd rtti_string_pointer
    dw 2087h,-4
    dw 0,0,0
xmsg_copy_state:
    dw 0,0
    dw -34,0,5,0,-1,6,5,0
    dw offset _TEXT:xmsg_copy_frame


org 118
    call @string@$bctr$qmx6string
    add sp,8
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov word ptr [bp-22],6

branch_0095:
    mov dx,[bp-2]
    mov ax,[bp-4]
    les bx,[bp+6]
    mov es:[bx+2],dx
    mov es:[bx],ax

branch_00a5:
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    push word ptr [bp-34]
    call ___ExitExceptBlocks
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf


org 44
    mov ax,seg _TEXT
    mov bx,offset _TEXT:xmsg_ctor_state
    call ___InitExceptBlocks
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz branch_0053
    mov ax,4
    push ax
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz branch_00a5

branch_0053:
    mov ax,4
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    jz branch_0095
    mov word ptr [bp-22],14
    push word ptr [bp+12]
    push word ptr [bp+10]
    push dx
    push word ptr [bp-4]

org 36
; Construct xmsg from string: allocate the xmsg handle and owned string,
; increment reference-destructor count, exit the exception block.

@xmsg@$bctr$qmx6string:
    push bp
    mov bp,sp
    sub sp,34
    push si
    push di

org 0
; Borland runtime exception-frame descriptor preceding xmsg(string const&).
xmsg_ctor_frame:
    dd rtti_string_pointer
    dw 2087h,-4
    dw 0,0,0
xmsg_ctor_state:
    dw 0,0
    dw -34,0,5,0,-1,6,5,0
    dw offset _TEXT:xmsg_ctor_frame


_TEXT ends
end
