; Original Japanese DOS wildcard argument constructor / PSP environment.
; 16-bit CS scratch, far DOS 21h helpers and owned uninitialized DATA.
; Genuine symbolic 8086 instructions, no original CODE byte arrays.
.8086
extrn __C0argc:word,__C0argv:dword,__psp:word,__envseg:word,__envLng:word
extrn __osmajor:byte,__abort:far,___path_isdbcsleadbyte:far
extrn __argc:word,__argv:dword,_sbrk:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __wildargv
; Original mutable scratch: two bytes in CODE before the abort far jump.
wild_saved_dgroup dw ?
wild_0002:
    jmp __abort

; Public wildcard startup entry after the abort trampoline.
__wildargv:
    pop word ptr DGROUP:saved_return_offset
    pop word ptr DGROUP:saved_return_segment
    pop word ptr DGROUP:saved_original_DS
    mov word ptr cs:wild_saved_dgroup, ds
    mov word ptr DGROUP:saved_original_SI, si
    mov word ptr DGROUP:saved_original_DI, di
    cld
    mov es, word ptr __psp
    mov si, 80h
    xor ah, ah
    lods byte ptr es:[si]
    inc ax
    mov bp, es
    xchg dx, si
    xchg bx, ax
    mov si, word ptr __envLng
    inc si
    inc si
    mov cx, 1
    cmp byte ptr __osmajor, 3
    jb wild_0053
    mov es, word ptr __envseg
    mov di, si
    mov cl, 7fh
    xor al, al
    repne scasb
    jcxz wild_0002
    xor cl, 7fh
wild_0053:
    push ax
    mov ax, cx
    inc ax
    and ax, 0fffeh
    mov di, sp
    sub di, ax
    jb wild_0002
    mov sp, di
    push es
    pop ds
    push ss
    pop es
    dec cx
    rep movsb
    xor al, al
    stosb
    mov cx, bp
    dec bx
    sub sp, 4ah
    mov bp, sp
    push dx
    push cx
    push bx
    mov ax, 80h
    mov word ptr [bp + 4], ax
    mov ds, word ptr cs:wild_saved_dgroup
    push ax
    call _sbrk
    pop cx
    pop cx
    pop ds
    pop si
    mov word ptr [bp], ax
    mov word ptr [bp + 2], dx
    and ax, dx
    cmp ax, 0ffffh
    je wild_00fa
    add ax, word ptr [bp + 4]
    mov word ptr [bp + 6], ax
    mov ah, 2fh
    int 21h
    mov word ptr [bp + 18h], bx
    mov word ptr [bp + 1ah], es
    push ds
    push ss
    pop ds
    lea dx, [bp + 1ch]
    mov ah, 1ah
    int 21h
    pop ds
    les di,dword ptr [bp]
    xor dx, dx
wild_00b9:
    mov word ptr [bp + 0ah], di
    xor bh, bh
    mov byte ptr [bp + 1eh], bh
wild_00c1:
    mov word ptr [bp + 8], si
    call wild_013d
    jb wild_011b
    je wild_00db
    cmp al, 20h
    je wild_00c1
    cmp al, 9
    je wild_00c1
    cmp al, 0dh
    je wild_00c1
    cmp al, 22h
    je wild_00ff
wild_00db:
    call wild_0217
    call wild_013d
    jb wild_00f5
    je wild_00db
    cmp al, 20h
    je wild_00f5
    cmp al, 9
    je wild_00f5
    cmp al, 0dh
    je wild_00f5
    cmp al, 22h
    jne wild_00db
wild_00f5:
    call wild_0251
    jmp short wild_00b9
wild_00fa:
    jmp __abort
wild_00ff:
    call wild_013d
    jb wild_0113
    je wild_010e
    cmp al, 22h
    je wild_0113
    cmp al, 0dh
    je wild_0113
wild_010e:
    call wild_0217
    jmp short wild_00ff
wild_0113:
    xor al, al
    call wild_0217
    inc dx
    jmp short wild_00b9
wild_011b:
    mov ax, di
    sub ax, word ptr [bp + 6]
    je wild_0132
    push dx
    push di
    mov ds, word ptr cs:wild_saved_dgroup
    push ax
    call _sbrk
    pop cx
    pop di
    pop dx
wild_0132:
    lds si,dword ptr [bp]
    mov cx, di
    sub cx, si
    inc dx
    jmp near ptr wild_0297
wild_013d:
    jcxz wild_0170
    lodsb
    dec cx
    call wild_0172
    cmp byte ptr [bp + 1eh], 0
    jne wild_0156
    cmp al, 5ch
    je wild_0162
    cmp al, 3fh
    je wild_015a
    cmp al, 2ah
    je wild_015a
wild_0156:
    or ah, 1
    ret
wild_015a:
    test bh, bh
    jne wild_0156
    or bh, 1
    ret
wild_0162:
    jcxz wild_0156
    cmp byte ptr [si], 22h
    jne wild_0156
    lodsb
    dec cx
    mov bh, 2
    xor ah, ah
    ret
wild_0170:
    stc
    ret
wild_0172:
    cmp byte ptr [bp + 1eh], 1
    je wild_0198
    mov byte ptr [bp + 1eh], 0
    push ax
    push bx
    push cx
    push dx
    push ds
    push es
    mov ds, word ptr cs:wild_saved_dgroup
    push ax
    call ___path_isdbcsleadbyte
    or ax, ax
    pop cx
    pop es
    pop ds
    pop dx
    pop cx
    pop bx
    pop ax
    je wild_019b
wild_0198:
    inc byte ptr [bp + 1eh]
wild_019b:
    ret
wild_019c:
    push ds
    mov word ptr [bp + 0ch], si
    mov word ptr [bp + 0eh], ds
    mov word ptr [bp + 10h], di
    mov word ptr [bp + 12h], es
    mov word ptr [bp + 16h], 0
    mov bx, si
    mov byte ptr [bp + 1eh], 0
wild_01b4:
    lodsb
    and al, al
    je wild_01d2
    call wild_0172
    cmp byte ptr [bp + 1eh], 0
    jne wild_01b4
    cmp al, 2fh
    je wild_01ce
    cmp al, 5ch
    je wild_01ce
    cmp al, 3ah
    jne wild_01b4
wild_01ce:
    mov bx, si
    jmp short wild_01b4
wild_01d2:
    sub bx, word ptr [bp + 0ch]
    mov word ptr [bp + 14h], bx
    mov ah, 4eh
    mov cx, 0
    lds dx,dword ptr [bp + 0ch]
    int 21h
    jb wild_020f
wild_01e4:
    inc word ptr [bp + 16h]
    les di,dword ptr [bp + 10h]
    mov cx, word ptr [bp + 14h]
    jcxz wild_01f8
    lds si,dword ptr [bp + 0ch]
wild_01f2:
    lodsb
    call wild_0217
    loop wild_01f2
wild_01f8:
    lea si, [bp + 3ah]
wild_01fb:
    lods byte ptr ss:[si]
    push ax
    call wild_0217
    pop ax
    and al, al
    jne wild_01fb
    mov word ptr [bp + 10h], di
    mov ah, 4fh
    int 21h
    jae wild_01e4
wild_020f:
    mov cx, word ptr [bp + 16h]
    les di,dword ptr [bp + 10h]
    pop ds
    ret
wild_0217:
    cmp di, word ptr [bp + 6]
    jae wild_021e
    stosb
    ret
wild_021e:
    push ds
    push es
    push si
    push di
    push ax
    push bx
    push cx
    push dx
    mov ds, word ptr cs:wild_saved_dgroup
    mov ax, 100h
    add word ptr [bp + 4], ax
    add word ptr [bp + 6], ax
    push ax
    call _sbrk
    pop cx
    and ax, dx
    cmp ax, 0ffffh
    je wild_024c
    pop dx
    pop cx
    pop bx
    pop ax
    pop di
    pop si
    pop es
    pop ds
    stosb
    ret
wild_024c:
    jmp __abort
wild_0251:
    push bx
    xor al, al
    call wild_0217
    pop bx
    test bh, 1
    jne wild_025f
    inc dx
    ret
wild_025f:
    push cx
    mov ax, word ptr [si - 1]
    push ax
    mov ah, 0
    cmp al, 9
    je wild_0272
    cmp al, 20h
    je wild_0272
    cmp al, 0dh
    jne wild_0274
wild_0272:
    mov al, 0
wild_0274:
    mov word ptr [si - 1], ax
    xchg word ptr [bp + 8], si
    push di
    mov di, word ptr [bp + 0ah]
    push dx
    call wild_019c
    pop dx
    pop bx
    and cx, cx
    jne wild_028d
    mov di, bx
    mov cx, 1
wild_028d:
    add dx, cx
    mov si, word ptr [bp + 8]
    pop word ptr [si - 1]
    pop cx
    ret
wild_0297:
    push ds
    push dx
    lds dx,dword ptr [bp + 18h]
    mov ah, 1ah
    int 21h
    pop dx
    pop ds
    add sp, 4ah
    mov es, word ptr cs:wild_saved_dgroup
    mov word ptr es:[DGROUP:__argc], dx
    inc dx
    shl dx, 1
    shl dx, 1
    mov bx, sp
    mov bp, sp
    sub bp, dx
    jb wild_024c
    mov sp, bp
    mov word ptr es:[DGROUP:__argv], bp
    mov word ptr es:[DGROUP:__argv]+2, ss
    mov word ptr [bp], bx
    mov word ptr [bp + 2], ss
    add bp, 4
wild_02d1:
    jcxz wild_02e3
    mov word ptr [bp], si
    mov word ptr [bp + 2], ds
    add bp, 4
wild_02dc:
    lodsb
    or al, al
    loopne wild_02dc
    je wild_02d1
wild_02e3:
    xor ax, ax
    mov word ptr [bp], ax
    mov word ptr [bp + 2], ax
    mov ds, word ptr cs:wild_saved_dgroup
    mov ds, word ptr cs:wild_saved_dgroup
    mov si, word ptr DGROUP:saved_original_SI
    mov di, word ptr DGROUP:saved_original_DI
    push word ptr DGROUP:saved_original_DS
    push word ptr DGROUP:saved_return_segment
    mov ax, word ptr DGROUP:__argc
    mov word ptr __C0argc, ax
    mov ax, word ptr DGROUP:__argv+2
    mov word ptr __C0argv+2, ax
    mov ax, word ptr DGROUP:__argv
    mov word ptr __C0argv, ax
    jmp word ptr DGROUP:saved_return_offset
_TEXT ends
_DATA segment word public 'DATA'
saved_return_offset dw ?
saved_return_segment dw ?
saved_original_DS dw ?
saved_original_SI dw ?
saved_original_DI dw ?
_DATA ends
end
