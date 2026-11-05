; Original Borland streambuf base destructor. Releases an owned far buffer,
; resets ownership and optionally deletes this. Typed RTTI and virtual ABI.
.8086
extrn @$bdele$qnv:far
extrn @$bdla$qnv:far
extrn @__RefDestructorCount$qv:far
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
public @streambuf@$bdtr$qv
@streambuf@$bdtr$qv proc far
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
    mov word ptr es:[bx],offset DGROUP:streambuf_vtable_marker
    cmp word ptr es:[bx+2],0
    jz short maybe_delete_object
    push word ptr es:[bx+8]
    push word ptr es:[bx+6]
    call @$bdla$qnv
    pop cx
    pop cx
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+2],0
maybe_delete_object:
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
@streambuf@$bdtr$qv endp
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
