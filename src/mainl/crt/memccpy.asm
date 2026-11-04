; Reconstructed Borland 16-bit large-model memccpy.
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
public _memccpy

_memccpy:
    push bp
    mov bp, sp
    push si
    push di
    les di, dword ptr [bp + 0ah]
    mov cx, word ptr [bp + 10h]
    jcxz label_0032
    mov bx, cx
    mov al, byte ptr [bp + 0eh]
    cld
    repne scasb
    push ds
    sub bx, cx
    mov cx, bx
    les di, dword ptr [bp + 6]
    lds si, dword ptr [bp + 0ah]
    shr cx, 1
    rep movsw
    jae label_0027
    movsb

label_0027:
    pop ds
    mov dx, es
    cmp al, byte ptr es:[di - 1]
    mov ax, di
    je label_0035

label_0032:
    xor ax, ax
    cwd

label_0035:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
