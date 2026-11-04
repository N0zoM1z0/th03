; Reconstructed Borland 16-bit large-model fstrchr.
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
public __fstrchr

__fstrchr:
    push bp
    mov bp, sp
    push si
    push di
    cld
    push ds
    lds si, dword ptr [bp + 6]
    mov bl, byte ptr [bp + 0ah]
    test si, 1
    je label_001c
    lodsb
    cmp al, bl
    je label_0034
    and al, al
    je label_002d

label_001c:
    lodsw
    cmp al, bl
    je label_0035
    and al, al
    je label_002d
    cmp ah, bl
    je label_0034
    and ah, ah
    jne label_001c

label_002d:
    pop ds
    xor dx, dx
    xor ax, ax
    jmp short label_003b

label_0034:
    inc si

label_0035:
    lea ax, [si - 2]
    mov dx, ds
    pop ds

label_003b:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
