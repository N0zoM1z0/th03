; Reconstructed Borland 16-bit large-model stbsync.
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
public @streambuf@sync$qv

@streambuf@sync$qv:
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 22h]
    cmp ax, word ptr es:[bx + 1eh]
    jbe label_001d
    xor dx, dx
    sub ax, word ptr es:[bx + 1eh]
    sbb dx, 0
    jmp short label_001f

label_001d:
    xor ax, ax

label_001f:
    or ax, ax
    jne label_0049
    les bx, dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 12h]
    or ax, word ptr es:[bx + 14h]
    je label_003f
    mov ax, word ptr es:[bx + 12h]
    xor dx, dx
    sub ax, word ptr es:[bx + 0eh]
    sbb dx, 0
    jmp short label_0041

label_003f:
    xor ax, ax

label_0041:
    or ax, ax
    jne label_0049
    xor ax, ax
    jmp short label_004c

label_0049:
    mov ax, 0ffffh

label_004c:
    pop di
    pop si
    pop bp
    retf
_TEXTA ends
end
