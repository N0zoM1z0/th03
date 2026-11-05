; Complete original Japanese Borland strstreambuf(far,far) constructor.
; Native base constructor, real 52-byte virtual-function table and C++
; RTTI records are assembled symbolically, not embedded as machine bytes.
; Full original strstreambuf(char*,int,char*) C++ constructor.
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
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @strstreambuf@$bctr$qnql$nvnqnv$v
@strstreambuf@$bctr$qnql$nvnqnv$v proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short allocated
    mov ax,50
    push ax
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz short retain_count
allocated:
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@$bctr$qv
    pop cx
    pop cx
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],offset DGROUP:strstreambuf_vtable_marker
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov word ptr es:[bx+28h],dx
    mov word ptr es:[bx+26h],ax
    mov dx,[bp+16]
    mov ax,[bp+14]
    mov word ptr es:[bx+2ch],dx
    mov word ptr es:[bx+2ah],ax
    mov word ptr es:[bx+30h],0
    mov word ptr es:[bx+2eh],1
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
@strstreambuf@$bctr$qnql$nvnqnv$v endp

; Original typed strstreambuf/streambuf RTTI and 11 virtual-function slots.
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
