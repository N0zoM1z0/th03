; Reconstructed Borland 16-bit large-model stsetst.
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
public @ios@setstate$qi

@ios@setstate$qi:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 0ah]
    les bx, dword ptr [bp + 6]
    mov ax, dx
    and ax, 0ffh
    or word ptr es:[bx + 0ah], ax
    mov ax, dx
    and ax, 0fcffh
    or word ptr es:[bx + 0ch], ax
    mov ax, dx
    and ax, 0fdffh
    or word ptr es:[bx + 0eh], ax
    pop di
    pop si
    pop bp
    retf
_TEXTA ends
end
