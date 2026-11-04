; Reconstructed Borland 16-bit large-model srbsbuf.
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
public @strstreambuf@setbuf$qnci

@strstreambuf@setbuf$qnci:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 0eh]
    mov ax, word ptr [bp + 0ah]
    or ax, word ptr [bp + 0ch]
    je label_0016
    xor dx, dx
    xor ax, ax
    jmp short label_0028

label_0016:
    cmp dx, 4
    jle label_0022
    les bx, dword ptr [bp + 6]
    mov word ptr es:[bx + 30h], dx

label_0022:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]

label_0028:
    pop di
    pop si
    pop bp
    retf
_TEXTA ends
end
