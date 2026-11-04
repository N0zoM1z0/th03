; Reconstructed Borland 16-bit large-model fmemchr.
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
public __fmemchr

__fmemchr:
    push bp
    mov bp, sp
    push si
    push di
    les di, dword ptr [bp + 6]
    mov cx, word ptr [bp + 0ch]
    jcxz label_0015
    mov al, byte ptr [bp + 0ah]
    cld
    repne scasb
    je label_001c

label_0015:
    xor di, di
    mov es, di
    mov di, 1

label_001c:
    dec di
    mov ax, di
    mov dx, es
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
