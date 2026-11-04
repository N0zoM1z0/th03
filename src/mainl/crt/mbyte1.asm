; Reconstructed Borland 16-bit large-model mbyte1.
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
public _mblen,_mbtowc,_wctomb,_mbstowcs,_wcstombs

_mblen:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    je label_0016
    les bx, dword ptr [bp + 6]
    cmp byte ptr es:[bx], 0
    jne label_001a

label_0016:
    xor ax, ax
    jmp short label_0028

label_001a:
    cmp word ptr [bp + 0ah], 0
    jne label_0025
    mov ax, 0ffffh
    jmp short label_0028

label_0025:
    mov ax, 1

label_0028:
    pop di
    pop si
    pop bp
    retf

_mbtowc:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 0ah]
    or ax, word ptr [bp + 0ch]
    je label_0062
    cmp word ptr [bp + 0eh], 0
    jne label_0044
    mov ax, 0ffffh
    jmp short label_0069

label_0044:
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    je label_0059
    les bx, dword ptr [bp + 0ah]
    mov al, byte ptr es:[bx]
    cbw
    les bx, dword ptr [bp + 6]
    mov word ptr es:[bx], ax

label_0059:
    les bx, dword ptr [bp + 0ah]
    cmp byte ptr es:[bx], 0
    jne label_0066

label_0062:
    xor ax, ax
    jmp short label_0069

label_0066:
    mov ax, 1

label_0069:
    pop di
    pop si
    pop bp
    retf

_wctomb:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 0ah]
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne label_0081
    xor ax, ax
    jmp short label_0094

label_0081:
    test dh, 0ffh
    je label_008b
    mov ax, 0ffffh
    jmp short label_0094

label_008b:
    les bx, dword ptr [bp + 6]
    mov byte ptr es:[bx], dl
    mov ax, 1

label_0094:
    pop di
    pop si
    pop bp
    retf

_mbstowcs:
    push bp
    mov bp, sp
    push si
    push di
    push ds
    lds si, dword ptr [bp + 0ah]
    les di, dword ptr [bp + 6]
    mov cx, word ptr [bp + 0eh]
    mov dx, cx
    cld
    xor ah, ah

label_00ac:
    lodsb
    stosw
    test al, al
    je label_00b7
    dec cx
    test cx, cx
    jne label_00ac

label_00b7:
    mov ax, dx
    sub ax, cx
    pop ds
    pop di
    pop si
    pop bp
    retf

_wcstombs:
    push bp
    mov bp, sp
    push si
    push di
    push ds
    lds si, dword ptr [bp + 0ah]
    les di, dword ptr [bp + 6]
    mov cx, word ptr [bp + 0eh]
    mov dx, cx
    cld

label_00d2:
    lodsw
    test ah, ah
    jne label_00e8
    stosb
    test al, al
    je label_00e1
    dec cx
    test cx, cx
    jne label_00d2

label_00e1:
    mov ax, dx
    sub ax, cx
    pop ds
    jmp short label_00ec

label_00e8:
    pop ds
    mov ax, 0ffffh

label_00ec:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
