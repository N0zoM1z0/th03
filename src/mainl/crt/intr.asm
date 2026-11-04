; Reconstructed Borland 16-bit large-model intr.
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
public _intr

_intr:
    push bp
    mov bp, sp
    sub sp, 12h
    push si
    push di
    push bp
    push ds
    pushf
    lea cx, [bp - 12h]
    mov word ptr [bp - 4], cx
    mov word ptr [bp - 2], ss
    mov word ptr [bp - 12h], 6e8bh
    mov byte ptr [bp - 10h], 0deh
    mov byte ptr [bp - 0fh], 0cdh
    mov ax, word ptr [bp + 6]
    mov byte ptr [bp - 0eh], al
    cmp al, 25h
    jb label_0047
    cmp al, 26h
    ja label_0047
    mov byte ptr [bp - 0dh], 36h
    mov word ptr [bp - 0ch], 68fh
    mov word ptr [bp - 0ah], cx
    mov byte ptr [bp - 8], 0cah
    mov word ptr [bp - 7], 2
    jmp short label_0050

label_0046:
    iret

label_0047:
    mov byte ptr [bp - 0dh], 0cah
    mov word ptr [bp - 0ch], 2

label_0050:
    lds di, dword ptr [bp + 8]
    push ds
    push di
    mov ax, word ptr [di]
    mov bx, word ptr [di + 2]
    mov cx, word ptr [di + 4]
    mov dx, word ptr [di + 6]
    push word ptr [di + 8]
    mov si, word ptr [di + 0ah]
    mov es, word ptr [di + 10h]
    lds di, dword ptr [di + 0ch]
    call dword ptr [bp - 4]
    push ds
    push di
    push bp
    pushf
    mov bp, sp
    lds di, dword ptr [bp + 8]
    mov word ptr [di], ax
    mov word ptr [di + 2], bx
    mov word ptr [di + 4], cx
    mov word ptr [di + 6], dx
    mov word ptr [di + 0ah], si
    mov word ptr [di + 10h], es
    pop word ptr [di + 12h]
    pop word ptr [di + 8]
    pop word ptr [di + 0ch]
    pop word ptr [di + 0eh]
    add sp, 4
    push cs
    call label_0046
    pop ds
    pop bp
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
end
