; Reconstructed Borland 16-bit large-model fmemcmp.
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
public __fmemcmp

__fmemcmp:
    push bp
    mov bp, sp
    push si
    push di
    push ds
    mov ax, word ptr [bp + 0eh]
    mov cx, ax
    jcxz label_0021
    lds si, dword ptr [bp + 6]
    les di, dword ptr [bp + 0ah]
    cld
    repe cmpsb
    mov al, byte ptr [si - 1]
    xor ah, ah
    mov cl, byte ptr es:[di - 1]
    xor ch, ch

label_0021:
    pop ds
    sub ax, cx
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
