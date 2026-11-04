; Reconstructed Borland 16-bit large-model fstrstr.
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
public __fstrstr

__fstrstr:
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp + 0ah]
    cmp byte ptr es:[bx], 0
    jne label_0016
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    jmp short label_0068

label_0016:
    push ds
    cld
    les di, dword ptr [bp + 6]
    push es
    mov bx, di
    xor ax, ax
    mov cx, 0ffffh
    repne scasb
    not cx
    xchg cx, dx
    les di, dword ptr [bp + 0ah]
    push es
    mov bp, di
    xor ax, ax
    mov cx, 0ffffh
    repne scasb
    inc cx
    not cx
    pop ds
    pop es

label_003b:
    mov si, bp
    lodsb
    xchg di, bx
    xchg cx, dx
    repne scasb
    mov bx, di
    jne label_004c
    cmp cx, dx
    jae label_0055

label_004c:
    xor bx, bx
    mov es, bx
    mov bx, 1
    jmp short label_0062

label_0055:
    xchg cx, dx
    jcxz label_0062
    mov ax, cx
    dec cx
    repe cmpsb
    mov cx, ax
    jne label_003b

label_0062:
    pop ds
    mov ax, bx
    dec ax
    mov dx, es

label_0068:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
