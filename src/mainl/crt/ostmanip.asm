; Reconstructed Borland 16-bit large-model ostmanip.
; Original far ABI, semantic branches and normal assembler source.
.8086
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostream@$blsh$qnqm3ios$m3ios

@ostream@$blsh$qnqm3ios$m3ios:
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call dword ptr [bp + 0ah]
    pop cx
    pop cx
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    pop bp
    retf
_TEXTA ends
end
