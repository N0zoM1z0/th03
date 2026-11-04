; Reconstructed Borland 16-bit large-model cnecsond.
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
public ___nec_sound,___nec_nosound

label_0000:
    push bp
    mov bp, sp
    push si
    push di
    pushf
    cli
    xor ax, ax
    mov es, ax
    test byte ptr es:[500h], 1
    je label_0056
    mov dx, 25h
    mov ax, 8000h
    test byte ptr es:[501h], 80h
    je label_0027
    mov dx, 1eh
    mov ax, 7800h

label_0027:
    mov bx, word ptr [bp + 8]
    shr bx, 1
    add ax, bx
    adc dx, 0
    mov bx, word ptr [bp + 8]
    cmp bx, dx
    jbe label_003b
    div bx
    xchg cx, ax

label_003b:
    mov dx, 3fdfh
    mov al, 7eh
    out dx, al
    out 5fh, al
    out 5fh, al
    mov dx, 3fdbh
    mov al, cl
    out dx, al
    out 5fh, al
    out 5fh, al
    mov al, ch
    out dx, al
    out 5fh, al
    out 5fh, al

label_0056:
    mov al, 6
    cmp byte ptr [bp + 6], 1
    adc al, 0
    out 37h, al
    out 5fh, al
    out 5fh, al
    popf
    pop di
    pop si
    pop bp
    retf 4

___nec_sound:
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp + 6]
    mov ax, 1
    push ax
    push cs
    call label_0000
    pop di
    pop si
    pop bp
    retf

___nec_nosound:
    push si
    push di
    mov al, 7
    out 37h, al
    out 5fh, al
    out 5fh, al
    mov ax, 7d0h
    push ax
    xor ax, ax
    push ax
    push cs
    call label_0000
    pop di
    pop si
    retf
_TEXT ends
end
