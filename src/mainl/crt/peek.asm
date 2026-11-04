; Reconstructed Borland 16-bit large-model peek.
; Original far ABI, semantic branches and normal assembler source.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _peek,_peekb

_peek:
    push bp
    mov bp, sp
    push si
    push di
    mov es, word ptr [bp + 6]
    mov bx, word ptr [bp + 8]
    mov ax, word ptr es:[bx]
    pop di
    pop si
    pop bp
    retf

_peekb:
    push bp
    mov bp, sp
    push si
    push di
    mov es, word ptr [bp + 6]
    mov bx, word ptr [bp + 8]
    mov al, byte ptr es:[bx]
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
