; Reconstructed Borland 16-bit large-model srbfreez.
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
public @strstreambuf@freeze$qi

@strstreambuf@freeze$qi:
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp + 6]
    test byte ptr es:[bx + 2eh], 1
    je label_0024
    cmp word ptr [bp + 0ah], 0
    je label_001c
    or word ptr es:[bx + 2eh], 2
    jmp short label_0024

label_001c:
    les bx, dword ptr [bp + 6]
    and word ptr es:[bx + 2eh], 0fffdh

label_0024:
    pop di
    pop si
    pop bp
    retf
_TEXTA ends
end
