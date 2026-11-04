; Reconstructed Borland 16-bit large-model castmptr.
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
public @_cast_memptr$qnvt1uiuiui

@_cast_memptr$qnvt1uiuiui:
    push bp
    mov bp, sp
    sub sp, 0ch
    push si
    push di
    mov cx, word ptr [bp + 0eh]
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    cmp word ptr [bp + 12h], 0
    je label_0094
    les bx, dword ptr [bp - 4]
    cmp word ptr es:[bx + 2], 0
    je label_0082
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax

label_0033:
    les bx, dword ptr [bp - 8]
    mov dx, word ptr es:[bx]
    add word ptr [bp - 8], 2
    or dx, dx
    je label_005e
    les bx, dword ptr [bp - 4]
    cmp word ptr es:[bx + 2], dx
    jne label_0058
    push es
    les si, dword ptr [bp - 8]
    mov ax, word ptr es:[si]
    pop es
    mov word ptr es:[bx + 2], ax
    jmp short label_00b0

label_0058:
    add word ptr [bp - 8], 2
    jmp short label_0033

label_005e:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    add ax, 4
    sub ax, cx
    mov word ptr [bp - 0ah], dx
    mov word ptr [bp - 0ch], ax

label_006f:
    les bx, dword ptr [bp - 0ch]
    mov byte ptr es:[bx], 0
    inc word ptr [bp - 0ch]
    dec cx
    mov ax, cx
    or ax, ax
    jne label_006f
    jmp short label_00b0

label_0082:
    les bx, dword ptr [bp - 4]
    mov ax, word ptr [bp + 10h]
    add word ptr es:[bx], ax
    mov ax, word ptr [bp + 12h]
    mov word ptr es:[bx + 2], ax
    jmp short label_00b0

label_0094:
    les bx, dword ptr [bp - 4]
    cmp word ptr es:[bx + 2], 0
    je label_00a7
    mov ax, word ptr [bp + 10h]
    add word ptr es:[bx + 2], ax
    jmp short label_00b0

label_00a7:
    les bx, dword ptr [bp - 4]
    mov ax, word ptr [bp + 10h]
    add word ptr es:[bx], ax

label_00b0:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
end
