; Reconstructed Borland 16-bit large-model fstrcpy.
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
public __fstrcpy

__fstrcpy:
    push bp
    mov bp, sp
    push si
    push di
    cld
    les di, dword ptr [bp + 0ah]
    mov si, di
    xor al, al
    mov cx, 0ffffh
    repne scasb
    not cx
    push ds
    mov ax, es
    mov ds, ax
    les di, dword ptr [bp + 6]
    rep movsb
    pop ds
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
