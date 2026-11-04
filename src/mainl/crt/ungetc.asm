; Reconstructed Borland 16-bit large-model ungetc.
; Original far ABI, semantic branches and normal assembler source.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __Nungetc,_ungetc

__Nungetc:
    pop ax
    push cs
    push ax

_ungetc:
    push bp
    mov bp, sp
    push si
    push di
    mov cx, word ptr [bp + 6]
    cmp cx, -1
    je label_006c
    les bx, dword ptr [bp + 8]
    cmp word ptr es:[bx], 0
    jge label_001e
    mov ax, 0ffffh
    jmp short label_006e

label_001e:
    les bx, dword ptr [bp + 8]
    and word ptr es:[bx + 2], 0ffdfh
    inc word ptr es:[bx]
    mov ax, word ptr es:[bx]
    cmp ax, 1
    jle label_0050
    dec word ptr es:[bx + 0ch]
    push bx
    push es
    mov es, word ptr es:[bx + 0eh]
    mov ax, es
    pop es
    pop bx
    mov bx, word ptr es:[bx + 0ch]
    mov dl, cl
    mov es, ax
    mov byte ptr es:[bx], dl
    mov al, dl

label_004c:
    mov ah, 0
    jmp short label_006e

label_0050:
    mov dx, word ptr [bp + 0ah]
    mov ax, word ptr [bp + 8]
    add ax, 5
    les bx, dword ptr [bp + 8]
    mov word ptr es:[bx + 0eh], dx
    mov word ptr es:[bx + 0ch], ax
    mov al, cl
    mov byte ptr es:[bx + 5], al
    jmp short label_004c

label_006c:
    mov ax, cx

label_006e:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
