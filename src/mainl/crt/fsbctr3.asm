; Complete original Borland C++ filebuf(int, char*, int) constructor.
; Naturally assembled 16-bit allocation, base class construction,
; original virtual setbuf call, RTTI, and eleven symbolic vtable slots.
.8086
extrn @$bnew$qui:far
extrn @__RefDestructorCount$qv:far
extrn @streambuf@$bctr$qv:far
extrn @streambuf@$bdtr$qv:far
extrn @streambuf@do_sgetn$qnci:far
extrn @streambuf@pbackfail$qi:far
extrn @streambuf@do_sputn$qnxci:far
extrn @streambuf@seekpos$qli:far
extrn @streambuf@doallocate$qv:far
extrn @filebuf@$bdtr$qv:far
extrn @filebuf@overflow$qi:far
extrn @filebuf@underflow$qv:far
extrn @filebuf@sync$qv:far
extrn @filebuf@seekoff$ql12ios@seek_diri:far
extrn @filebuf@setbuf$qnci:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @filebuf@$bctr$qinci
@filebuf@$bctr$qinci proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short allocated
    mov ax,54
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
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],offset DGROUP:filebuf_vtable_marker
    mov ax,[bp+10]
    mov word ptr es:[bx+26h],ax
    mov word ptr es:[bx+2ah],1
    mov word ptr es:[bx+28h],0
    mov word ptr es:[bx+2eh],0
    mov word ptr es:[bx+2ch],0
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+8]
    push bx
    mov bx,word ptr es:[bx]
    call dword ptr [bx+4]
    add sp,14
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
@filebuf@$bctr$qinci endp

; Original complete Borland RTTI for filebuf and streambuf.
rtti_filebuf:
    dw 54,3,38,0,119,46,58
    dw 0,0,0,0,0,0
    dw 2,2
    dd @filebuf@$bdtr$qv
    dw 5,62
    db 'filebuf',0
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
    dd rtti_filebuf
    dd 0
filebuf_vtable_marker label word
    dd @filebuf@$bdtr$qv
    dd @filebuf@setbuf$qnci
    dd @streambuf@do_sgetn$qnci
    dd @filebuf@underflow$qv
    dd @streambuf@pbackfail$qi
    dd @streambuf@do_sputn$qnxci
    dd @filebuf@overflow$qi
    dd @filebuf@seekoff$ql12ios@seek_diri
    dd @streambuf@seekpos$qli
    dd @filebuf@sync$qv
    dd @streambuf@doallocate$qv
_DATA ends
end
