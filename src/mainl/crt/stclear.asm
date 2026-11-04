; Reconstructed Borland 16-bit large-model stclear.
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
public @ios@clear$qi

@ios@clear$qi:
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 0ah]
    and ax, 80h
    mov dx, word ptr [bp + 0ah]
    and dx, 0ffh
    or ax, dx
    mov word ptr es:[bx + 0ah], ax
    mov ax, word ptr es:[bx + 0ch]
    and ax, 0ff00h
    or ax, word ptr es:[bx + 0ah]
    mov word ptr es:[bx + 0ch], ax
    mov ax, word ptr es:[bx + 0eh]
    and ax, 0ff00h
    or ax, word ptr es:[bx + 0ah]
    mov word ptr es:[bx + 0eh], ax
    pop di
    pop si
    pop bp
    retf
_TEXTA ends
end
