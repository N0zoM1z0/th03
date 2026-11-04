; Reconstructed Borland 16-bit large-model fmemset.
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
public __fsetmem,__fmemset

__fsetmem:
    push bp
    mov bp, sp
    push si
    push di
    les di, dword ptr [bp + 6]
    mov cx, word ptr [bp + 0ah]
    mov al, byte ptr [bp + 0ch]
    mov ah, al
    cld
    test di, 1
    je label_001b
    jcxz label_0022
    stosb
    dec cx

label_001b:
    shr cx, 1
    rep stosw
    jae label_0022
    stosb

label_0022:
    pop di
    pop si
    pop bp
    retf

__fmemset:
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp + 0ah]
    push word ptr [bp + 0ch]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push cs
    call __fsetmem
    add sp, 8
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
