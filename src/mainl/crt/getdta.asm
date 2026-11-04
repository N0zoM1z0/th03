; Reconstructed Borland 16-bit large-model getdta.
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
public _getdta

_getdta:
    push si
    push di
    mov ah, 2fh
    int 21h
    mov ax, bx
    mov dx, es
    pop di
    pop si
    retf
_TEXT ends
end
