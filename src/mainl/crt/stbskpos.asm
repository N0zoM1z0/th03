; Reconstructed Borland 16-bit large-model stbskpos.
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
public @streambuf@seekpos$qli

@streambuf@seekpos$qli:
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp + 0eh]
    xor ax, ax
    push ax
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 1ch]
    add sp, 0ch
    pop di
    pop si
    pop bp
    retf
_TEXTA ends
end
