; Original Japanese Borland strstreambuf destructor with typed RTTI.
; Real mode-controlled dynamic far-buffer deletion, base streambuf
; destruction and optional C++ object free. All vtable pointers symbolic.
.8086
extrn @$bdele$qnv:far
extrn @$bdla$qnv:far
extrn @__RefDestructorCount$qv:far
extrn @streambuf@$bdtr$qv:far
extrn @streambuf@do_sgetn$qnci:far
extrn @streambuf@pbackfail$qi:far
extrn @streambuf@do_sputn$qnxci:far
extrn @streambuf@seekpos$qli:far
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
public @strstreambuf@$bdtr$qv
@strstreambuf@$bdtr$qv proc far
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
    jz short done
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],offset DGROUP:strstreambuf_vtable_marker
    mov ax,word ptr es:[bx+2eh]
    and ax,3
    cmp ax,1
    jnz short destroy_base
    mov ax,word ptr es:[bx+2ah]
    or ax,word ptr es:[bx+2ch]
    jz short delete_owned_buffer
    push word ptr es:[bx+8]
    push word ptr es:[bx+6]
    call dword ptr es:[bx+2ah]
    jmp short buffer_done
delete_owned_buffer:
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+8]
    push word ptr es:[bx+6]
    call @$bdla$qnv
buffer_done:
    pop cx
    pop cx
destroy_base:
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz short done
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @$bdele$qnv
    pop cx
    pop cx
done:
    pop di
    pop si
    pop bp
    retf
@strstreambuf@$bdtr$qv endp

; Borland class RTTI at CODE+133/+205 plus original virtual slots.
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
