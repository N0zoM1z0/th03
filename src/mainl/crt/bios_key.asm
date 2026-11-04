; Reconstructed Borland 16-bit large-model bios_key.
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
public __ibmpc_bios_keybrd

__ibmpc_bios_keybrd:
    push bp
    mov bp, sp
    push si
    push di
    xor al, al
    mov ah, byte ptr [bp + 6]
    int 16h
    je label_001d
    test byte ptr [bp + 6], 1
    je label_0025
    or ax, ax
    jne label_0025
    mov ax, 0ffffh
    jmp short label_0025

label_001d:
    test byte ptr [bp + 6], 1
    je label_0025
    xor ax, ax

label_0025:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
