; Complete original 16-bit Japanese Borland CRT C++ stream member osttellp.
; Preserves original far ABI, streambuf transfer and state semantics.
; Real 8086 instructions and symbolic relocations, never executable data bytes.
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
public @ostream@tellp$qv

@ostream@tellp$qv:
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    mov word ptr [bp-2],65535
    mov word ptr [bp-4],65535
    les bx,[bp+6]
    mov bx,es:[bx]
    test byte ptr es:[bx+10],132
    jnz osttellp_jump_005c
    mov ax,2
    push ax
    mov ax,1
    push ax
    xor ax,ax
    push ax
    push ax
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-6],es
    mov [bp-8],bx
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx,es:[bx+2]
    mov bx,es:[bx]
    call dword ptr [bx+28]
    add sp,12
    mov [bp-2],dx
    mov [bp-4],ax
    cmp dx,-1
    jnz osttellp_jump_006f
    cmp ax,65535
    jnz osttellp_jump_006f

osttellp_jump_005c:
    mov ax,2
    push ax
    les bx,[bp+6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp,6

osttellp_jump_006f:
    mov dx,[bp-2]
    mov ax,[bp-4]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_TEXTA ends
end
