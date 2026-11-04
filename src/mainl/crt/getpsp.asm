; Reconstructed Borland 16-bit large-model getpsp.
; Original far ABI, semantic branches and normal assembler source.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _getpsp

_getpsp:
    push si
    push di
    mov ah, 62h
    int 21h
    mov ax, bx
    pop di
    pop si
    retf
_TEXT ends
end
