; Original Japanese Borland CRT srbstr; natural 16-bit source.
.8086
extrn @strstreambuf@freeze$qi:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @strstreambuf@str$qv
@strstreambuf@str$qv proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,1
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @strstreambuf@freeze$qi
    add sp,6
    les bx,dword ptr [bp+6]
    mov dx,word ptr es:[bx+8]
    mov ax,word ptr es:[bx+6]
    pop di
    pop si
    pop bp
    retf
@strstreambuf@str$qv endp
_TEXTA ends
end
