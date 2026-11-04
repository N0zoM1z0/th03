; Reconstructed Borland 16-bit large-model dosvgenv.
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
public _dosvgetdosenv

_dosvgetdosenv:
    push si
    push di
    push es
    mov ax, 0c300h
    stc
    int 15h
    cmc
    mov cx, 0
    adc cx, cx
    shl cx, 1
    push ds
    mov ax, 6300h
    int 21h
    cmp word ptr [si], 0
    pop ds
    je label_0020
    or cx, 1

label_0020:
    pop es
    mov ax, cx
    pop di
    pop si
    retf
_TEXT ends
end
