; Reconstructed Borland 16-bit large-model fstrpbrk.
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
public __fstrpbrk

__fstrpbrk:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    jmp short label_003d

label_000a:
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    jmp short label_0031

label_0018:
    les bx, dword ptr [bp + 6]
    mov al, byte ptr es:[bx]
    les bx, dword ptr [bp - 4]
    cmp al, byte ptr es:[bx]
    jne label_002e
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    jmp short label_004a

label_002e:
    inc word ptr [bp - 4]

label_0031:
    les bx, dword ptr [bp - 4]
    cmp byte ptr es:[bx], 0
    jne label_0018
    inc word ptr [bp + 6]

label_003d:
    les bx, dword ptr [bp + 6]
    cmp byte ptr es:[bx], 0
    jne label_000a
    xor dx, dx
    xor ax, ax

label_004a:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
end
