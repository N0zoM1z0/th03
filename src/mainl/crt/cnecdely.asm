; Reconstructed Borland 16-bit large-model cnecdely.
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
public ___nec_delay

label_0000:
    push bp
    mov bp, sp
    push si
    push di
    xor ax, ax
    mov es, ax
    test byte ptr es:[501h], 8
    je label_0029
    mov ax, 0cd4h
    test byte ptr es:[54ch], 20h
    je label_0042
    test byte ptr es:[459h], 8
    je label_0042
    mov ax, 1388h
    jmp short label_0042

label_0029:
    mov ax, 0c4bh
    test byte ptr es:[54ch], 20h
    jne label_0042
    mov ax, 9b3h
    test byte ptr es:[53ch], 80h
    jne label_0042
    mov ax, 627h

label_0042:
    mov dx, word ptr [bp + 4]
    cmp dx, 1
    jb label_0075
    je label_004f
    mul dx
    inc dx

label_004f:
    dec dx
    mov bx, 64h
    xchg cx, ax
    xchg dx, ax
    xor dx, dx
    div bx
    xchg cx, ax
    div bx
    mov bx, cx
    inc bx
    mov cx, ax
    mov dx, 60h
    mov ah, 40h

label_0066:
    in al, dx
    test al, ah
    je label_0066

label_006b:
    in al, dx
    test al, ah
    jne label_006b
    loop label_0066
    dec bx
    jne label_0066

label_0075:
    pop di
    pop si
    pop bp
    ret

label_0079:
    push bp
    mov bp, sp
    push si
    push di

label_007e:
    pushf
    cli
    in ax, 5eh
    xchg cx, ax
    in ax, 5ch
    xchg bx, ax
    in ax, 5eh
    popf
    cmp cx, ax
    jne label_007e
    mov cl, ch
    xor ch, ch
    xor si, si
    mov di, 133h
    mov ax, word ptr [bp + 4]
    cmp ax, 1
    jb label_00e5
    je label_00bb
    cmp ax, 2
    jne label_00a9
    shl di, 1
    jmp short label_00bb

label_00a9:
    mov si, 0c00h
    mul si
    xchg si, ax
    xchg dx, ax
    xor dx, dx
    mov di, 0ah
    div di
    xchg si, ax
    div di
    xchg di, ax

label_00bb:
    mov dx, cx
    add bx, di
    adc cx, si

label_00c1:
    pushf
    cli
    in ax, 5eh
    xchg si, ax
    in ax, 5ch
    xchg di, ax
    in ax, 5eh
    popf
    cmp si, ax
    jne label_00c1
    mov al, ah
    mov ah, dh
    cmp al, dl
    mov dl, al
    adc dh, 0
    cmp dx, cx
    jb label_00c1
    ja label_00e5
    cmp di, bx
    jb label_00c1

label_00e5:
    pop di
    pop si
    pop bp
    ret

___nec_delay:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 6]
    xor ax, ax
    mov es, ax
    test byte ptr es:[458h], 80h
    jne label_0107
    mov es, ax
    test byte ptr es:[45bh], 4
    je label_010d

label_0107:
    push dx
    call label_0079
    jmp short label_0111

label_010d:
    push dx
    call label_0000

label_0111:
    pop cx
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
