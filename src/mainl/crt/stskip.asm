; Reconstructed Borland 16-bit large-model stskip.
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
public @ios@skip$qi

@ios@skip$qi:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    les bx, dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 0ch]
    and ax, 100h
    mov word ptr [bp - 2], ax
    cmp word ptr [bp + 0ah], 0
    je label_0028
    or word ptr es:[bx + 0ch], 100h
    or word ptr es:[bx + 10h], 1
    jmp short label_0036

label_0028:
    les bx, dword ptr [bp + 6]
    and word ptr es:[bx + 0ch], 0feffh
    and word ptr es:[bx + 10h], 0fffeh

label_0036:
    cmp word ptr [bp - 2], 0
    je label_0041
    mov ax, 1
    jmp short label_0043

label_0041:
    xor ax, ax

label_0043:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends
end
