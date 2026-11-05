; Complete Borland filebuf destructor with conditional close/virtual overflow,
; streambuf base cleanup, optional far delete and typed RTTI + vtable.
.8086
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn @streambuf@$bdtr$qv:far
extrn @streambuf@do_sgetn$qnci:far
extrn @streambuf@pbackfail$qi:far
extrn @streambuf@do_sputn$qnxci:far
extrn @streambuf@seekpos$qli:far
extrn @streambuf@doallocate$qv:far
extrn @filebuf@close$qv:far
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
public @filebuf@$bdtr$qv
@filebuf@$bdtr$qv proc far
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
    mov word ptr es:[bx],offset DGROUP:filebuf_vtable_marker
    cmp word ptr es:[bx+28h],0
    jz short flush_pending
    push word ptr [bp+8]
    push bx
    call @filebuf@close$qv
    pop cx
    pop cx
    jmp short release_streambuf
flush_pending:
    mov ax,0ffffh
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    call dword ptr [bx+18h]
    add sp,6
release_streambuf:
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@$bdtr$qv
    add sp,6
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
@filebuf@$bdtr$qv endp

; Original complete semantic Borland RTTI for filebuf and streambuf.
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
public @filebuf@openprot
@filebuf@openprot dw 0180h ; original DATA+0 class-wide open protocol flags
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
