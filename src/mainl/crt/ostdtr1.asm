; Original ostream::~ostream with flush-tie cleanup and complete typed RTTI.
.8086
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn @ios@$bdtr$qv:far
extrn @ostream@flush$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostream@$bdtr$qv
@ostream@$bdtr$qv proc far
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
    jz short destructor_done
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+2],offset DGROUP:ostream_vtable_marker
    mov bx,word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:ostream_adjusted_thunk_ptr
    mov ax,word ptr es:[bx+2]
    or ax,word ptr es:[bx+4]
    jz short check_base_delete
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @ostream@flush$qv
    pop cx
    pop cx
check_base_delete:
    test byte ptr [bp+10],2
    jz short maybe_delete
    xor ax,ax
    push ax
    mov ax,[bp+6]
    add ax,4
    push word ptr [bp+8]
    push ax
    call @ios@$bdtr$qv
    add sp,6
maybe_delete:
    test byte ptr [bp+10],1
    jz short destructor_done
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @$bdele$qnv
    pop cx
    pop cx
destructor_done:
    pop di
    pop si
    pop bp
    retf
@ostream@$bdtr$qv endp

assume cs:nothing
ostream_destructor_thunk:
    mov bx,sp
    add word ptr ss:[bx+4],-4
    jmp far ptr @ostream@$bdtr$qv

rtti_ostream:
    dw 44,3,38,2,127,46,50
    dw 0,0,0,0,0,0
    dw 2,1
    dd @ostream@$bdtr$qv
    dw 5,62
    db 'ostream',0
    dw 0,0
    dd rtti_ios
    dw 0,7,0,0,0,0
rtti_ios:
    dw 40,3,38,0,115,42,46
    dw 0,0,0,0,0,0
    dw 1,1
    dd @ios@$bdtr$qv
    dw 5,50
    db 'ios',0
    dw 0,0,0,0,0,0
_TEXTA ends

_DATA segment word public 'DATA'
    dd rtti_ostream
    dd 0
ostream_vtable_marker label word
    dd @ostream@$bdtr$qv
    dw 4,8
ostream_adjusted_thunk_ptr label word
    dd ostream_destructor_thunk
_DATA ends
end
