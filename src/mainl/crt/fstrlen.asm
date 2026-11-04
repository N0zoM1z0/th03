; Reconstructed Borland 16-bit large-model fstrlen.
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
public __fstrlen

__fstrlen:
    push bp
    mov bp, sp
    push si
    push di
    les di, dword ptr [bp + 6]
    xor ax, ax
    cmp ax, word ptr [bp + 8]
    jne label_0013
    cmp ax, di
    je label_001d

label_0013:
    cld
    mov cx, 0ffffh
    repne scasb
    xchg cx, ax
    not ax
    dec ax

label_001d:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
