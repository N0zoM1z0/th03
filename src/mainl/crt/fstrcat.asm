; Reconstructed Borland 16-bit large-model fstrcat.
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
public __fstrcat

__fstrcat:
    push bp
    mov bp, sp
    push si
    push di
    cld
    push ds
    les di, dword ptr [bp + 6]
    mov dx, di
    xor al, al
    mov cx, 0ffffh
    repne scasb
    push es
    lea si, [di - 1]
    les di, dword ptr [bp + 0ah]
    mov cx, 0ffffh
    repne scasb
    not cx
    sub di, cx
    push es
    pop ds
    pop es
    xchg si, di
    test si, 1
    je label_0030
    movsb
    dec cx

label_0030:
    shr cx, 1
    rep movsw
    jae label_0037
    movsb

label_0037:
    xchg dx, ax
    mov dx, es
    pop ds
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
