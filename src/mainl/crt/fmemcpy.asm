; Reconstructed Borland 16-bit large-model fmemcpy.
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
public __fmemcpy

__fmemcpy:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, ds
    les di, dword ptr [bp + 6]
    lds si, dword ptr [bp + 0ah]
    mov cx, word ptr [bp + 0eh]
    shr cx, 1
    cld
    rep movsw
    jae label_0018
    movsb

label_0018:
    mov ds, dx
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
