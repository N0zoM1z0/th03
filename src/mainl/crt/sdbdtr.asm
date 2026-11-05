; Original stdiobuf destructor, with real virtual overflow flush,
; base streambuf cleanup and conditional far object delete.
.8086
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn @streambuf@$bdtr$qv:far
extrn @streambuf@setbuf$qnci:far
extrn @streambuf@do_sgetn$qnci:far
extrn @streambuf@do_sputn$qnxci:far
extrn @streambuf@seekpos$qli:far
extrn @streambuf@doallocate$qv:far
extrn @stdiobuf@overflow$qi:far
extrn @stdiobuf@pbackfail$qi:far
extrn @stdiobuf@sync$qv:far
extrn @stdiobuf@seekoff$ql12ios@seek_diri:far
extrn @stdiobuf@underflow$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @stdiobuf@$bdtr$qv
@stdiobuf@$bdtr$qv proc far
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
    jz short complete
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],offset DGROUP:stdiobuf_virtual_methods
    mov ax,-1
    push ax
    push word ptr [bp+8]
    push bx
    mov bx,word ptr es:[bx]
    call dword ptr [bx+18h]
    add sp,6
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz short complete
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @$bdele$qnv
    pop cx
    pop cx
complete:
    pop di
    pop si
    pop bp
    retf
@stdiobuf@$bdtr$qv endp

stdiobuf_class_rtti:
    dw 44,3,38,0,119,48,60
    dw 0,0,0,0,0,0,2,2
    dd @stdiobuf@$bdtr$qv
    dw 5,64
    db 'stdiobuf',0
    db 0 ; Borland RTTI field alignment within the class descriptor
    dd streambuf_class_rtti
    dw 0,3,0,0,0,0,0,0
streambuf_class_rtti:
    dw 38,3,38,0,115,48,52
    dw 0,0,0,0,0,0,1,1
    dd @streambuf@$bdtr$qv
    dw 5,56
    db 'streambuf',0
    dw 0,0,0,0,0,0
_TEXTA ends

_DATA segment word public 'DATA'
assume cs:nothing
; C++ virtual table: one far class descriptor plus eleven methods.
    dd stdiobuf_class_rtti
    dw 0,0
stdiobuf_virtual_methods:
    dd @stdiobuf@$bdtr$qv
    dd @streambuf@setbuf$qnci
    dd @streambuf@do_sgetn$qnci
    dd @stdiobuf@underflow$qv
    dd @stdiobuf@pbackfail$qi
    dd @streambuf@do_sputn$qnxci
    dd @stdiobuf@overflow$qi
    dd @stdiobuf@seekoff$ql12ios@seek_diri
    dd @streambuf@seekpos$qli
    dd @stdiobuf@sync$qv
    dd @streambuf@doallocate$qv
_DATA ends
end
