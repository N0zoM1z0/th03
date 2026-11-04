; Reconstructed Borland 16-bit large-model dosvgadr.
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
public _dosvgetvideoaddr

_dosvgetvideoaddr:
    push si
    push di
    mov ax, 0b800h
    mov es, ax
    mov di, 0
    mov ah, 0feh
    int 10h
    mov dx, es
    mov ax, di
    pop di
    pop si
    retf
_TEXT ends
end
