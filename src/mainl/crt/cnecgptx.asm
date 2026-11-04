; Original NEC PC-98 direct video area get/put text and text-size methods.
; Three complete native Borland far C++-style CRT APIs, symbolic 8086.
; Preserve VIDEO far memory ES:DI/DS:SI and original offset framing.
.8086
extrn __wgarbage:word,__video:byte,__VALIDATEXY:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___nec_gettext,___nec_puttext,___nec_getputtextsize

; Original NEC PC-98 text API at CODE+0.
___nec_gettext:
    push bp
    mov bp, sp
    push si
    push di
    cmp byte ptr DGROUP:__video+11, 0
    jne nec_text_001f
    push word ptr [bp + 6]
    push word ptr [bp + 8]
    push word ptr [bp + 0ah]
    push word ptr [bp + 0ch]
    call __VALIDATEXY
    or ax, ax
    jne nec_text_0024
nec_text_001f:
    xor ax, ax
    jmp short nec_text_0066
    nop
nec_text_0024:
    cld
    push ds
    dec word ptr [bp + 6]
    dec word ptr [bp + 8]
    mov al, byte ptr [bp + 8]
    mov bl, byte ptr __video+10
    mov bh, 0
    mul bl
    shl bx, 1
    add ax, word ptr [bp + 6]
    shl ax, 1
    lds si, dword ptr __video+16
    add si, ax
    les di, dword ptr [bp + 0eh]
    mov dx, word ptr [bp + 0ch]
    sub dx, word ptr [bp + 8]
nec_text_004d:
    push si
    mov cx, word ptr [bp + 0ah]
    sub cx, word ptr [bp + 6]
nec_text_0054:
    movsw
    mov ax, word ptr [si + 1ffeh]
    stosw
    loop nec_text_0054
    pop si
    add si, bx
    dec dx
    jne nec_text_004d
    mov ax, 1
    pop ds
nec_text_0066:
    pop di
    pop si
    pop bp
    retf

; Original NEC PC-98 text API at CODE+106.
___nec_puttext:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    cmp byte ptr DGROUP:__video+11, 0
    jne nec_text_008c
    push word ptr [bp + 6]
    push word ptr [bp + 8]
    push word ptr [bp + 0ah]
    push word ptr [bp + 0ch]
    call __VALIDATEXY
    or ax, ax
    jne nec_text_0091
nec_text_008c:
    xor ax, ax
    jmp near ptr nec_text_01b8
nec_text_0091:
    mov al, byte ptr DGROUP:__wgarbage
    mov byte ptr [bp - 1], al
    push ds
    cld
    dec word ptr [bp + 6]
    dec word ptr [bp + 8]
    mov bx, word ptr [bp + 0ch]
    sub bx, word ptr [bp + 8]
    je nec_text_00af
    mov cx, word ptr [bp + 0ah]
    sub cx, word ptr [bp + 6]
    jne nec_text_00b2
nec_text_00af:
    jmp near ptr nec_text_01b4
nec_text_00b2:
    mov word ptr [bp - 4], cx
    mov dl, byte ptr __video+10
    mov dh, 0
    les di, dword ptr __video+16
    mov al, byte ptr [bp + 8]
    mul dl
    add ax, word ptr [bp + 6]
    shl ax, 1
    add di, ax
    lds si, dword ptr [bp + 0eh]
nec_text_00ce:
    mov cx, word ptr [bp - 4]
    push di
    cmp byte ptr [bp - 1], 0
    je nec_text_013f
    push dx
    lodsw
    cmp word ptr [bp + 6], 0
    je nec_text_011b
    mov dx, word ptr es:[di - 2]
    or dh, dh
    je nec_text_011b
    test dx, 8080h
    jne nec_text_011b
    cmp dl, 9
    jb nec_text_00f8
    cmp dl, 0ch
    jb nec_text_011b
nec_text_00f8:
    or ah, ah
    je nec_text_0115
    test ax, 8080h
    je nec_text_0115
    and al, 7fh
    cmp al, 9
    jb nec_text_010b
    cmp al, 0ch
    jb nec_text_0115
nec_text_010b:
    or al, 80h
    xor dx, ax
    and dx, 7f7fh
    je nec_text_0131
nec_text_0115:
    mov word ptr es:[di - 2], 20h
nec_text_011b:
    or ah, ah
    je nec_text_0131
    test ax, 8080h
    je nec_text_0131
    and al, 7fh
    cmp al, 9
    jb nec_text_012e
    cmp al, 0ch
    jb nec_text_0131
nec_text_012e:
    mov ax, 20h
nec_text_0131:
    pop dx
    dec cx
    je nec_text_014f
    stosw
    lodsw
    mov word ptr es:[di + 1ffeh], ax
    dec cx
    je nec_text_014e
nec_text_013f:
    movsw
    lodsw
    mov word ptr es:[di + 1ffeh], ax
    loop nec_text_013f
    cmp byte ptr [bp - 1], 0
    je nec_text_01a9
nec_text_014e:
    lodsw
nec_text_014f:
    cmp byte ptr [bp + 0ah], dl
    jae nec_text_018e
    mov cx, word ptr es:[di + 2]
    or ch, ch
    je nec_text_018e
    test cx, 8080h
    je nec_text_018e
    and cl, 7fh
    cmp cl, 9
    jb nec_text_016f
    cmp cl, 0ch
    jb nec_text_018e
nec_text_016f:
    or ah, ah
    je nec_text_0188
    test ax, 8080h
    jne nec_text_0188
    cmp al, 9
    jb nec_text_0180
    cmp al, 0ch
    jb nec_text_0188
nec_text_0180:
    xor cx, ax
    and cx, 7f7fh
    je nec_text_01a2
nec_text_0188:
    mov word ptr es:[di + 2], 20h
nec_text_018e:
    or ah, ah
    je nec_text_01a2
    test ax, 8080h
    jne nec_text_01a2
    cmp al, 9
    jb nec_text_019f
    cmp al, 0ch
    jb nec_text_01a2
nec_text_019f:
    mov ax, 20h
nec_text_01a2:
    stosw
    lodsw
    mov word ptr es:[di + 1ffeh], ax
nec_text_01a9:
    pop di
    add di, dx
    add di, dx
    dec bx
    je nec_text_01b4
    jmp near ptr nec_text_00ce
nec_text_01b4:
    pop ds
    mov ax, 1
nec_text_01b8:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original NEC PC-98 text API at CODE+446.
___nec_getputtextsize:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 0ah]
    sub ax, word ptr [bp + 6]
    inc ax
    mov dx, word ptr [bp + 0ch]
    sub dx, word ptr [bp + 8]
    inc dx
    imul dx
    mov cl, 2
    shl ax, cl
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
