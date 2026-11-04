; Reconstructed Borland 16-bit large-model movedata.
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
public _movedata

_movedata:
    push bp
    mov bp, sp
    push si
    push di
    cld
    mov cx, word ptr [bp + 0eh]
    mov di, word ptr [bp + 0ch]
    mov es, word ptr [bp + 0ah]
    mov si, word ptr [bp + 8]
    push ds
    mov ds, word ptr [bp + 6]
    shr cx, 1
    rep movsw
    jae label_001d
    movsb

label_001d:
    pop ds
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
