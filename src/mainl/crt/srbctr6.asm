; Complete original strstreambuf(signed char far *,int,char far *) C++ constructor.
; Real base streambuf ctor and strstreambuf::init, reference tracking,
; typed RTTI for both classes and all eleven DATA virtual-function slots.
.8086
extrn @$bnew$qui:far
extrn @__RefDestructorCount$qv:far
extrn @streambuf@$bctr$qv:far
extrn @streambuf@$bdtr$qv:far
extrn @streambuf@do_sgetn$qnci:far
extrn @streambuf@pbackfail$qi:far
extrn @streambuf@do_sputn$qnxci:far
extrn @streambuf@seekpos$qli:far
extrn @strstreambuf@$bdtr$qv:far
extrn @strstreambuf@doallocate$qv:far
extrn @strstreambuf@overflow$qi:far
extrn @strstreambuf@underflow$qv:far
extrn @strstreambuf@sync$qv:far
extrn @strstreambuf@setbuf$qnci:far
extrn @strstreambuf@seekoff$ql12ios@seek_diri:far
extrn @strstreambuf@init$qncit1:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @strstreambuf@$bctr$qncit1
@strstreambuf@$bctr$qncit1 proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short allocate_ready
    mov ax,50
    push ax
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz short retain_count
allocate_ready:
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@$bctr$qv
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],offset DGROUP:strstreambuf_vtable_marker
    push word ptr [bp+18]
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push bx
    call @strstreambuf@init$qncit1
    add sp,18
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
@strstreambuf@$bctr$qncit1 endp

; Original Borland type data at CODE+107 / CODE+179. These are typed
; metadata fields and named class strings, not embedded executable bytes.
rtti_strstreambuf:
    dw 50,3,38,0,119,52,64
    dw 0,0,0,0,0,0
    dw 2,2
    dd @strstreambuf@$bdtr$qv
    dw 5,68
    db 'strstreambuf',0,0
    dd rtti_streambuf
    dw 0,3,0,0,0,0,0,0
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
    dd rtti_strstreambuf
    dd 0
strstreambuf_vtable_marker label word
    dd @strstreambuf@$bdtr$qv
    dd @strstreambuf@setbuf$qnci
    dd @streambuf@do_sgetn$qnci
    dd @strstreambuf@underflow$qv
    dd @streambuf@pbackfail$qi
    dd @streambuf@do_sputn$qnxci
    dd @strstreambuf@overflow$qi
    dd @strstreambuf@seekoff$ql12ios@seek_diri
    dd @streambuf@seekpos$qli
    dd @strstreambuf@sync$qv
    dd @strstreambuf@doallocate$qv
_DATA ends
end
