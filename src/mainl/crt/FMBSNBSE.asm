; Reconstructed Borland 16-bit large-model FMBSNBSE.
; Original far ABI, semantic branches and normal assembler source.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __fmbsnbset

__fmbsnbset:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    test byte ptr [bp + 0bh], 0ffh
    je label_0074
    jmp short label_0054

label_001c:
    dec word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ch]
    or ax, ax
    jbe label_0030
    les bx, dword ptr [bp - 4]
    cmp byte ptr es:[bx + 1], 0
    jne label_0039

label_0030:
    les bx, dword ptr [bp - 4]
    mov byte ptr es:[bx], 20h
    jmp short label_0083

label_0039:
    mov ax, word ptr [bp + 0ah]
    mov cl, 8
    shr ax, cl
    les bx, dword ptr [bp - 4]
    mov byte ptr es:[bx], al
    mov al, byte ptr [bp + 0ah]
    mov byte ptr es:[bx + 1], al
    add word ptr [bp - 4], 2
    dec word ptr [bp + 0ch]

label_0054:
    cmp word ptr [bp + 0ch], 0
    jbe label_0083
    les bx, dword ptr [bp - 4]
    cmp byte ptr es:[bx], 0
    jne label_001c
    jmp short label_0083

label_0065:
    les bx, dword ptr [bp - 4]
    mov al, byte ptr [bp + 0ah]
    mov byte ptr es:[bx], al
    inc word ptr [bp - 4]
    dec word ptr [bp + 0ch]

label_0074:
    cmp word ptr [bp + 0ch], 0
    jbe label_0083
    les bx, dword ptr [bp - 4]
    cmp byte ptr es:[bx], 0
    jne label_0065

label_0083:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
end
