; Original Japanese Borland CRT member tell
; Return current file position by original far _lseek call with 0, SEEK_CUR.
; Complete 16-bit ABI and imported target relocations, no patched objects.
.8086
extrn _lseek:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _tell

_tell:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,1
    push ax
    xor ax,ax
    push ax
    push ax
    push word ptr [bp+6]
    call _lseek
    add sp,8
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
