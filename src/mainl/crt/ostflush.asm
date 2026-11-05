; Original ostream::flush invokes virtual streambuf::sync at vtable+24h.
.8086
extrn @ios@setstate$qi:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostream@flush$qv
@ostream@flush$qv proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    mov [bp-2],es
    mov [bp-4],bx
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx,dword ptr es:[bx+2]
    mov bx,word ptr es:[bx]
    call dword ptr [bx+24h]
    pop cx
    pop cx
    cmp ax,0ffffh
    jnz short return_stream
    mov ax,4
    push ax
    les bx,dword ptr [bp+6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp,6
return_stream:
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@ostream@flush$qv endp
_TEXTA ends
end
