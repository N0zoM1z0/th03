; Reconstructed Borland 16-bit large-model cnecwhxy.
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
public __NEC_WHEREXY

__NEC_WHEREXY:
    push si
    push di
    xor ax, ax
    mov es, ax
    mov al, byte ptr es:[71ch]
    mov ah, byte ptr es:[710h]
    pop di
    pop si
    ret
_TEXT ends
end
