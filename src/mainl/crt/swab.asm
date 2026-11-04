; Reconstructed Borland 16-bit large-model swab.
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
public _swab

_swab:
    push bp
    mov bp, sp
    push si
    push di
    mov cx, word ptr [bp + 0eh]
    shr cx, 1
    jcxz label_001b
    push ds
    cld
    les di, dword ptr [bp + 0ah]
    lds si, dword ptr [bp + 6]

label_0014:
    lodsw
    xchg ah, al
    stosw
    loop label_0014
    pop ds

label_001b:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
