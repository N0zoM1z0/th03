; Reconstructed Borland 16-bit large-model FMBSSET.
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
public __fmbsset

__fmbsset:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    mov ax, word ptr [bp + 0ah]
    mov cl, 8
    shr ax, cl
    mov dl, al
    or dl, dl
    je label_006a
    jmp short label_0038

label_0023:
    les bx, dword ptr [bp - 4]
    mov byte ptr es:[bx], dl
    inc word ptr [bp - 4]
    les bx, dword ptr [bp - 4]
    mov al, byte ptr [bp + 0ah]
    mov byte ptr es:[bx], al
    inc word ptr [bp - 4]

label_0038:
    les bx, dword ptr [bp - 4]
    cmp byte ptr es:[bx], 0
    je label_0048
    cmp byte ptr es:[bx + 1], 0
    jne label_0023

label_0048:
    les bx, dword ptr [bp - 4]
    cmp byte ptr es:[bx], 0
    je label_0073
    cmp byte ptr es:[bx + 1], 0
    jne label_0073
    mov byte ptr es:[bx], 20h
    jmp short label_0073

label_005e:
    les bx, dword ptr [bp - 4]
    mov al, byte ptr [bp + 0ah]
    mov byte ptr es:[bx], al
    inc word ptr [bp - 4]

label_006a:
    les bx, dword ptr [bp - 4]
    cmp byte ptr es:[bx], 0
    jne label_005e

label_0073:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
end
