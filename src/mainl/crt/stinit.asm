; Reconstructed Borland 16-bit large-model stinit.
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
public @ios@init$qn9streambuf

@ios@init$qn9streambuf:
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp + 6]
    mov word ptr es:[bx + 26h], 0
    xor ax, ax
    mov word ptr es:[bx + 0eh], ax
    mov word ptr es:[bx + 0ah], ax
    mov word ptr es:[bx + 0ch], 100h
    mov word ptr es:[bx + 12h], 0
    mov word ptr es:[bx + 10h], 1
    mov word ptr es:[bx + 14h], 6
    mov word ptr es:[bx + 16h], 0
    mov word ptr es:[bx + 18h], 20h
    mov word ptr es:[bx + 8], 0
    mov word ptr es:[bx + 6], 0
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
    mov word ptr es:[bx + 4], dx
    mov word ptr es:[bx + 2], ax
    pop di
    pop si
    pop bp
    retf
_TEXTA ends
end
