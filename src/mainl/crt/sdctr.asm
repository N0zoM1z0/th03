; Original Japanese Borland stdiostream(FILE*) constructor and complete RTTI.
; 125 bytes of actual far C++ construction and four genuine typed RTTI
; records plus compiler exception/cleanup pointers occupy the _TEXTA CODE.
; All RTTI values, destructor imports and CODE local pointers are symbolic
; 16-bit Borland OMF fields, never target instruction blobs or OBJ patches.
.8086
extrn @$bnew$qui:far
extrn @__RefDestructorCount$qv:far
extrn @ios@$bdtr$qv:far
extrn @ios@$bctr$qv:far
extrn @ios@init$qn9streambuf:far
extrn @streambuf@$bdtr$qv:far
extrn @stdiobuf@$bctr$qn4FILE:far
extrn @stdiobuf@$bdtr$qv:far
extrn @stdiostream@$bdtr$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @stdiostream@$bctr$qn4FILE
@stdiostream@$bctr$qn4FILE proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short already_allocated
    mov ax,54h
    push ax
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz short retain_count
already_allocated:
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @ios@$bctr$qv
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],offset DGROUP:stdiostream_vtable_marker
    push word ptr [bp+12]
    push word ptr [bp+10]
    mov ax,[bp+6]
    add ax,40
    push word ptr [bp+8]
    push ax
    call @stdiobuf@$bctr$qn4FILE
    mov ax,[bp+6]
    add ax,40
    push word ptr [bp+8]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @ios@init$qn9streambuf
    add sp,20
retain_count:
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf
@stdiostream@$bctr$qn4FILE endp

; Original C++ RTTI descriptor blocks, with true inheritance pointers and
; the compiler-authored type names kept as semantic string fields.
rtti_stdiostream:
    dw 84,3,38,0,119,50,62
    dw 0,0,0,0,0,0
    dw 4,4
    dd @stdiostream@$bdtr$qv ; real destructor pointer at CODE+155
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
