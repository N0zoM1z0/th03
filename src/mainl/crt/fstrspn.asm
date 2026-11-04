; Reconstructed Borland 16-bit large-model fstrspn.
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
public __fstrspn

__fstrspn:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    xor cx, cx
    jmp short label_0041

label_000c:
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    jmp short label_002b

label_001a:
    les bx, dword ptr [bp + 6]
    mov al, byte ptr es:[bx]
    les bx, dword ptr [bp - 4]
    cmp al, byte ptr es:[bx]
    je label_0034
    inc word ptr [bp - 4]

label_002b:
    les bx, dword ptr [bp - 4]
    cmp byte ptr es:[bx], 0
    jne label_001a

label_0034:
    les bx, dword ptr [bp - 4]
    cmp byte ptr es:[bx], 0
    je label_004a
    inc word ptr [bp + 6]
    inc cx

label_0041:
    les bx, dword ptr [bp + 6]
    cmp byte ptr es:[bx], 0
    jne label_000c

label_004a:
    mov ax, cx
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
end
