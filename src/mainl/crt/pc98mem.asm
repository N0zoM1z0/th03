; Reconstructed Borland 16-bit large-model pc98mem.
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
public _pc98mem

_pc98mem:
    push si
    push di
    xor ax, ax
    mov es, ax
    mov ah, byte ptr es:[501h]
    and ah, 7
    inc ah
    shr ax, 1
    pop di
    pop si
    retf
_TEXT ends
end
