; Reconstructed Borland 16-bit large-model segread.
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
public _segread

_segread:
    push bp
    mov bp, sp
    push si
    push di
    mov bx, es
    les si, dword ptr [bp + 6]
    mov word ptr es:[si], bx
    mov ax, word ptr [bp + 4]
    mov word ptr es:[si + 2], ax
    mov word ptr es:[si + 4], ss
    mov word ptr es:[si + 6], ds
    mov es, bx
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
