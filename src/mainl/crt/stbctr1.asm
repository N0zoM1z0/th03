; Complete original Borland C++ streambuf() base constructor.
; Actual 38-byte streambuf layout, buffer pointers/flags reset,
; typed RTTI and eleven symbolic far virtual method slots.
.8086
extrn @$bnew$qui:far
extrn @__RefDestructorCount$qv:far
extrn @streambuf@$bdtr$qv:far
extrn @streambuf@setbuf$qnci:far
extrn @streambuf@do_sgetn$qnci:far
extrn @streambuf@underflow$qv:far
extrn @streambuf@pbackfail$qi:far
extrn @streambuf@do_sputn$qnxci:far
extrn @streambuf@overflow$qi:far
extrn @streambuf@seekoff$ql12ios@seek_diri:far
extrn @streambuf@seekpos$qli:far
extrn @streambuf@sync$qv:far
extrn @streambuf@doallocate$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @streambuf@$bctr$qv
@streambuf@$bctr$qv proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short allocated
    mov ax,38
    push ax
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz short retain_count
allocated:
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],offset DGROUP:streambuf_vtable_marker
    mov word ptr es:[bx+2],0
    mov word ptr es:[bx+4],0
    mov word ptr es:[bx+8],0
    mov word ptr es:[bx+6],0
    mov word ptr es:[bx+10h],0
    mov word ptr es:[bx+0eh],0
    mov word ptr es:[bx+14h],0
    mov word ptr es:[bx+12h],0
    mov word ptr es:[bx+18h],0
    mov word ptr es:[bx+16h],0
    mov word ptr es:[bx+20h],0
    mov word ptr es:[bx+1eh],0
    mov word ptr es:[bx+24h],0
    mov word ptr es:[bx+22h],0
    mov word ptr es:[bx+1ch],0
    mov word ptr es:[bx+1ah],0
    mov word ptr es:[bx+0ch],0
    mov word ptr es:[bx+0ah],0
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
@streambuf@$bctr$qv endp

; Exact streambuf C++ type descriptor and public virtual-function ABI.
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
    dd rtti_streambuf
    dd 0
streambuf_vtable_marker label word
    dd @streambuf@$bdtr$qv
    dd @streambuf@setbuf$qnci
    dd @streambuf@do_sgetn$qnci
    dd @streambuf@underflow$qv
    dd @streambuf@pbackfail$qi
    dd @streambuf@do_sputn$qnxci
    dd @streambuf@overflow$qi
    dd @streambuf@seekoff$ql12ios@seek_diri
    dd @streambuf@seekpos$qli
    dd @streambuf@sync$qv
    dd @streambuf@doallocate$qv
_DATA ends
end
