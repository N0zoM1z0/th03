; Reconstructed Borland 16-bit large-model dosvsist.
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
public _dosvsetiasstatus

_dosvsetiasstatus:
    push bp
    mov bp, sp
    push si
    push di
    mov dl, byte ptr [bp + 6]
    mov ax, 1300h
    int 16h
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
