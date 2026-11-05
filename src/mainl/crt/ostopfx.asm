; Original C++ ostream prefix: state check and real tied-stream flush.
.8086
extrn @ostream@flush$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostream@do_opfx$qv
@ostream@do_opfx$qv proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    test byte ptr es:[bx+0ah],086h
    jnz short prefix_failed
    mov ax,word ptr es:[bx+6]
    or ax,word ptr es:[bx+8]
    jz short prefix_ready
    push word ptr es:[bx+8]
    push word ptr es:[bx+6]
    call @ostream@flush$qv
    pop cx
    pop cx
prefix_ready:
    mov ax,1
    jmp short return_prefix
prefix_failed:
    xor ax,ax
return_prefix:
    pop di
    pop si
    pop bp
    retf
@ostream@do_opfx$qv endp
_TEXTA ends
end
