; Reconstructed Borland 16-bit large-model stbsetg.
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
public @streambuf@setg$qnct1t1

@streambuf@setg$qnct1t1:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 0eh]
    or ax, word ptr [bp + 10h]
    je label_001d
    mov ax, word ptr [bp + 0ah]
    or ax, word ptr [bp + 0ch]
    je label_001d
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
    jmp short label_0023

label_001d:
    mov dx, word ptr [bp + 10h]
    mov ax, word ptr [bp + 0eh]

label_0023:
    les bx, dword ptr [bp + 6]
    mov word ptr es:[bx + 1ch], dx
    mov word ptr es:[bx + 1ah], ax
    mov dx, word ptr [bp + 10h]
    mov ax, word ptr [bp + 0eh]
    mov word ptr es:[bx + 20h], dx
    mov word ptr es:[bx + 1eh], ax
    or ax, word ptr [bp + 10h]
    je label_0056
    mov ax, word ptr [bp + 12h]
    or ax, word ptr [bp + 14h]
    je label_0056
    mov ax, word ptr [bp + 12h]
    cmp ax, word ptr [bp + 0eh]
    jb label_0056
    mov dx, word ptr [bp + 14h]
    jmp short label_005c

label_0056:
    mov dx, word ptr [bp + 10h]
    mov ax, word ptr [bp + 0eh]

label_005c:
    les bx, dword ptr [bp + 6]
    mov word ptr es:[bx + 24h], dx
    mov word ptr es:[bx + 22h], ax
    pop di
    pop si
    pop bp
    retf
_TEXTA ends
end
