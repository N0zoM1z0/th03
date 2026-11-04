; Reconstructed Borland 16-bit large-model stbsetp.
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
public @streambuf@setp$qnct1

@streambuf@setp$qnct1:
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp + 6]
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
    mov word ptr es:[bx + 14h], dx
    mov word ptr es:[bx + 12h], ax
    mov word ptr es:[bx + 10h], dx
    mov word ptr es:[bx + 0eh], ax
    mov ax, word ptr [bp + 0ah]
    or ax, word ptr [bp + 0ch]
    je label_003b
    mov ax, word ptr [bp + 0eh]
    or ax, word ptr [bp + 10h]
    je label_003b
    mov ax, word ptr [bp + 0eh]
    cmp ax, word ptr [bp + 0ah]
    jb label_003b
    mov dx, word ptr [bp + 10h]
    jmp short label_0041

label_003b:
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]

label_0041:
    les bx, dword ptr [bp + 6]
    mov word ptr es:[bx + 18h], dx
    mov word ptr es:[bx + 16h], ax
    pop di
    pop si
    pop bp
    retf
_TEXTA ends
end
