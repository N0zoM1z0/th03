; Reconstructed Borland 16-bit large-model dosvuscr.
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
public _dosvupdatescreen

_dosvupdatescreen:
    push bp
    mov bp, sp
    push si
    push di
    les di, dword ptr [bp + 6]
    mov cx, word ptr [bp + 0ah]
    mov ah, 0ffh
    int 10h
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
