; Reconstructed Borland 16-bit large-model getfat.
; Original far ABI, semantic branches and normal assembler source.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _getfatd,_getfat,_getdfree

_getfatd:
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    mov al, 0
    push ax
    push cs
    call _getfat
    add sp, 6
    pop di
    pop si
    pop bp
    retf

_getfat:
    push bp
    mov bp, sp
    push si
    push di
    push ds
    mov ah, 1ch
    mov dl, byte ptr [bp + 6]
    int 21h
    mov ah, byte ptr [bx]
    pop ds
    les bx, dword ptr [bp + 8]
    mov word ptr es:[bx], ax
    mov word ptr es:[bx + 2], dx
    mov word ptr es:[bx + 4], cx
    pop di
    pop si
    pop bp
    retf

_getdfree:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    mov ah, 36h
    mov dl, byte ptr [bp + 6]
    int 21h
    mov word ptr [bp - 2], bx
    les bx, dword ptr [bp + 8]
    mov word ptr es:[bx + 6], ax
    mov ax, word ptr [bp - 2]
    mov word ptr es:[bx], ax
    mov word ptr es:[bx + 2], dx
    mov word ptr es:[bx + 4], cx
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
end
