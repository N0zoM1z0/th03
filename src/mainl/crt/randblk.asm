; Reconstructed Borland 16-bit large-model randblk.
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
public _randbrd,_randbwr

_randbrd:
    push bp
    mov bp, sp
    push si
    push di
    push ds
    mov ah, 27h
    mov cx, word ptr [bp + 0ah]
    lds dx, dword ptr [bp + 6]
    int 21h
    cbw
    pop ds
    pop di
    pop si
    pop bp
    retf

_randbwr:
    push bp
    mov bp, sp
    push si
    push di
    push ds
    mov ah, 28h
    mov cx, word ptr [bp + 0ah]
    lds dx, dword ptr [bp + 6]
    int 21h
    cbw
    pop ds
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
