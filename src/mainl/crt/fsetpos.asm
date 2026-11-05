; Original Japanese Borland CRT member fsetpos
; Far fsetpos forwards stored long position to fseek with SEEK_SET.
; Complete 16-bit ABI and imported target relocations, no patched objects.
.8086
extrn _fseek:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _fsetpos

_fsetpos:
    push bp
    mov bp,sp
    push si
    push di
    xor ax,ax
    push ax
    les bx,[bp+10]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _fseek
    add sp,10
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
