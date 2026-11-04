; Reconstructed Borland 16-bit large-model fstrncmp.
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
public __fstrncmp

__fstrncmp:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, ds
    cld
    les di, dword ptr [bp + 0ah]
    mov si, di
    mov ax, word ptr [bp + 0eh]
    mov cx, ax
    jcxz label_0032
    mov bx, ax
    xor al, al
    repne scasb
    sub bx, cx
    mov cx, bx
    mov di, si
    lds si, dword ptr [bp + 6]
    repe cmpsb
    mov al, byte ptr [si - 1]
    mov bl, byte ptr es:[di - 1]
    xor ah, ah
    mov bh, ah
    sub ax, bx

label_0032:
    mov ds, dx
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
