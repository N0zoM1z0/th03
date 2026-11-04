; Reconstructed Borland 16-bit large-model fstrcmp.
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
public __fstrcmp

__fstrcmp:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, ds
    cld
    xor ax, ax
    mov bx, ax
    les di, dword ptr [bp + 0ah]
    mov si, di
    xor al, al
    mov cx, 0ffffh
    repne scasb
    not cx
    mov di, si
    lds si, dword ptr [bp + 6]
    repe cmpsb
    mov al, byte ptr [si - 1]
    mov bl, byte ptr es:[di - 1]
    sub ax, bx
    mov ds, dx
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
