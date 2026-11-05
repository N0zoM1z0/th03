; Original Japanese Borland stdiostream destructor with complete typed RTTI.
; The first 98 bytes are the real far destruction path. Four RTTI class
; records, destructor pointers, inheritance and original vtable DATA are
; written as symbolic 16-bit typed source, never target instruction arrays.
.8086
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn @ios@$bdtr$qv:far
extrn @streambuf@$bdtr$qv:far
extrn @stdiobuf@$bdtr$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @stdiostream@$bdtr$qv
@stdiostream@$bdtr$qv proc far
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
    mov word ptr es:[bx],offset DGROUP:stdiostream_vtable_marker
    mov ax,2
    push ax
    mov ax,[bp+6]
    add ax,40
    push word ptr [bp+8]
    push ax
    call @stdiobuf@$bdtr$qv
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @ios@$bdtr$qv
    add sp,12
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
@stdiostream@$bdtr$qv endp

; Four original typed class records and real internal inheritance pointers.
; The local destructor pointer points to the CODE+0 exported entry, not
; to a synthetic zero dword or a separate imported descriptor.
rtti_stdiostream:
    dw 84,3,38,0,119,50,62
    dw 0,0,0,0,0,0
    dw 4,4
    dd @stdiostream@$bdtr$qv
    dw 5,66
    db 'stdiostream',0
    dd rtti_ios
    dw 0,3,0,0,0,0
    dd rtti_stdiobuf
    dw 40,0,0
rtti_stdiobuf:
    dw 44,3,38,0,119,48,60
    dw 0,0,0,0,0,0
    dw 2,2
    dd @stdiobuf@$bdtr$qv
    dw 5,64
    db 'stdiobuf',0,0
    dd rtti_streambuf
    dw 0,3,0,0,0,0,0,0
rtti_ios:
    dw 40,3,38,0,115,42,46
    dw 0,0,0,0,0,0
    dw 1,1
    dd @ios@$bdtr$qv
    dw 5,50
    db 'ios',0
    dw 0,0,0,0,0,0
rtti_streambuf:
    dw 38,3,38,0,115,48,52
    dw 0,0,0,0,0,0
    dw 1,1
    dd @streambuf@$bdtr$qv
    dw 5,56
    db 'streambuf',0
    dw 0,0,0,0,0,0
_TEXTA ends

_DATA segment word public 'DATA'
    dd rtti_stdiostream
    dd 0
stdiostream_vtable_marker label word
    dd @stdiostream@$bdtr$qv
_DATA ends
end
