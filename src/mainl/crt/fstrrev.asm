; Reconstructed Borland 16-bit large-model fstrrev.
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
public __fstrrev

__fstrrev:
    push bp
    mov bp, sp
    push si
    push di
    cld
    push ds
    lds si, dword ptr [bp + 6]
    mov dx, si
    mov di, si
    push ds
    pop es
    xor al, al
    mov cx, 0ffffh
    repne scasb
    cmp cx, -2
    je label_002c
    dec di
    dec di
    xchg si, di
    jmp short label_0028

label_0022:
    mov al, byte ptr [di]
    xchg byte ptr [si], al
    stosb
    dec si

label_0028:
    cmp di, si
    jb label_0022

label_002c:
    xchg dx, ax
    mov dx, ds
    pop ds
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
