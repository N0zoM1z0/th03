; Reconstructed Borland 16-bit large-model bion_prn.
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
public __necpc_bios_printer

__necpc_bios_printer:
    push bp
    mov bp, sp
    push si
    push di
    mov ah, byte ptr [bp + 6]
    cmp ah, 30h
    je label_002f
    cmp ah, 10h
    je label_0027
    cmp ah, 11h
    je label_0021
    cmp ah, 12h
    je label_0027
    mov ax, 0ffffh
    jmp short label_0045

label_0021:
    les bx, dword ptr [bp + 8]
    mov al, byte ptr es:[bx]

label_0027:
    int 1ah
    mov al, ah
    xor ah, ah
    jmp short label_0045

label_002f:
    les bx, dword ptr [bp + 8]
    xor cx, cx

label_0034:
    cmp byte ptr es:[bx], 0
    je label_003e
    inc cx
    inc bx
    jne label_0034

label_003e:
    les bx, dword ptr [bp + 8]
    int 1ah
    mov ax, cx

label_0045:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
