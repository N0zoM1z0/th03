; Reconstructed Borland 16-bit large-model country.
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
public _country

_country:
    push bp
    mov bp, sp
    push si
    push di
    push ds
    lds dx, dword ptr [bp + 8]
    mov ah, 38h
    mov al, byte ptr [bp + 6]
    int 21h
    pop ds
    jb label_001b
    mov dx, word ptr [bp + 0ah]
    mov ax, word ptr [bp + 8]
    jmp short label_001f

label_001b:
    xor dx, dx
    xor ax, ax

label_001f:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
