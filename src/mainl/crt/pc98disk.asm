; Reconstructed Borland 16-bit large-model pc98disk.
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
public _pc98disk

_pc98disk:
    push bp
    mov bp, sp
    push si
    push di
    push ds
    lds bx, dword ptr [bp + 6]
    mov ax, word ptr [bx]
    xchg al, ah
    mov cl, al
    and cl, 0f0h
    cmp cl, 80h
    mov cx, word ptr [bx + 6]
    je label_001d
    mov ch, byte ptr [bx + 4]

label_001d:
    mov dx, word ptr [bx + 8]
    xchg dl, dh
    push bp
    les bp, dword ptr [bx + 0ah]
    mov bx, word ptr [bx + 2]
    int 1bh
    pop bp
    sbb al, al
    neg al
    xchg al, ah
    lds bx, dword ptr [bp + 6]
    push ax
    mov al, byte ptr [bx]
    and al, 0fh
    cmp al, 0ah
    pop ax
    jne label_004d
    mov byte ptr [bx + 4], ch
    xor ch, ch
    mov word ptr [bx + 6], cx
    mov byte ptr [bx + 8], dh
    mov byte ptr [bx + 9], dl

label_004d:
    pop ds
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
