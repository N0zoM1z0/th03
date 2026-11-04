; Reconstructed Borland 16-bit large-model bion_key.
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
public __necpc_bios_keybrd

__necpc_bios_keybrd:
    push bp
    mov bp, sp
    push si
    push di
    mov ah, byte ptr [bp + 6]
    cmp ah, 0
    jne label_0012
    int 18h
    jmp short label_004d
    nop

label_0012:
    cmp ah, 1
    jne label_0021
    int 18h
    or bh, bh
    jne label_004d
    xor ax, ax
    jmp short label_004d

label_0021:
    cmp ah, 2
    jne label_002c
    int 18h
    xor ah, ah
    jmp short label_004d

label_002c:
    cmp ah, 3
    jne label_0035
    int 18h
    jmp short label_004d

label_0035:
    xor al, al
    mov dh, ah
    mov cx, 10h
    les bx, dword ptr [bp + 8]

label_003f:
    int 18h
    mov byte ptr es:[bx], ah
    inc bx
    mov ah, dh
    inc al
    loop label_003f
    xor al, al

label_004d:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
