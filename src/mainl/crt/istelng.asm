; Reconstructed Borland C++ istream long integer extraction, all 1439 bytes.
; Original four functions and near/far streambuf callbacks.
; Natural symbolic 8086 code, no embedded original machine instructions.
.8086
extrn @ios@clear$qi:far,@streambuf@do_snextc$qv:far
extrn @istream@ipfx$qi:far,__ctype:byte
extrn F_LXMUL@:far,F_LXLSH@:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @istream@$brsh$qml

; Original integer conversion entry CODE+0.
scan_signed_digits:
    push bp
    mov bp, sp
    sub sp, 0ch
    push si
    push di
    mov word ptr [bp - 2], 0
    mov word ptr [bp - 4], 0
    mov bx, word ptr [bp + 0ah]
    mov al, byte ptr DGROUP:__ctype[bx+1]
    mov ah, 0
    test al, 2
    jne loc_0062
    cmp word ptr [bp + 0ah], -1
    jne loc_003f
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 6], es
    mov word ptr [bp - 8], bx
    mov ax, word ptr es:[bx + 0ah]
    or ax, 3
    push ax
    push word ptr [bp - 6]
    push bx
    jmp short loc_0057
loc_003f:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 0ah], es
    mov word ptr [bp - 0ch], bx
    mov ax, word ptr es:[bx + 0ah]
    or ax, 2
    push ax
    push word ptr [bp - 0ah]
    push bx
loc_0057:
    call @ios@clear$qi
    add sp, 6
    jmp near ptr loc_00fa
loc_0062:
    mov cx, word ptr [bp - 2]
    mov bx, word ptr [bp - 4]
    xor dx, dx
    mov ax, 0ah
    call F_LXMUL@
    push ax
    mov ax, word ptr [bp + 0ah]
    push dx
    cwd
    pop bx
    pop cx
    add cx, ax
    adc bx, dx
    sub cx, 30h
    sbb bx, 0
    mov word ptr [bp - 2], bx
    mov word ptr [bp - 4], cx
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 1eh]
    or ax, word ptr es:[bx + 20h]
    je loc_00c0
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    inc word ptr es:[bx + 1eh]
    mov ax, word ptr es:[bx + 1eh]
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 22h]
    jb loc_00d7
loc_00c0:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    call @streambuf@do_snextc$qv
    pop cx
    pop cx
    jmp short loc_00ea
loc_00d7:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 1eh]
    mov al, byte ptr es:[bx]
    mov ah, 0
loc_00ea:
    mov word ptr [bp + 0ah], ax
    mov bx, word ptr [bp + 0ah]
    test byte ptr DGROUP:__ctype[bx+1], 2
    je loc_00fa
    jmp near ptr loc_0062
loc_00fa:
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original integer conversion entry CODE+262.
scan_unsigned_digits:
    push bp
    mov bp, sp
    sub sp, 0ch
    push si
    push di
    mov word ptr [bp - 2], 0
    mov word ptr [bp - 4], 0
    cmp word ptr [bp + 0ah], 30h
    jl loc_0124
    cmp word ptr [bp + 0ah], 37h
    jle loc_0167
loc_0124:
    cmp word ptr [bp + 0ah], -1
    jne loc_0144
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 6], es
    mov word ptr [bp - 8], bx
    mov ax, word ptr es:[bx + 0ah]
    or ax, 5
    push ax
    push word ptr [bp - 6]
    push bx
    jmp short loc_015c
loc_0144:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 0ah], es
    mov word ptr [bp - 0ch], bx
    mov ax, word ptr es:[bx + 0ah]
    or ax, 2
    push ax
    push word ptr [bp - 0ah]
    push bx
loc_015c:
    call @ios@clear$qi
    add sp, 6
    jmp near ptr loc_01fe
loc_0167:
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    mov cl, 3
    call F_LXLSH@
    push ax
    mov ax, word ptr [bp + 0ah]
    push dx
    cwd
    pop bx
    pop cx
    add cx, ax
    adc bx, dx
    sub cx, 30h
    sbb bx, 0
    mov word ptr [bp - 2], bx
    mov word ptr [bp - 4], cx
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 1eh]
    or ax, word ptr es:[bx + 20h]
    je loc_01c2
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    inc word ptr es:[bx + 1eh]
    mov ax, word ptr es:[bx + 1eh]
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 22h]
    jb loc_01d9
loc_01c2:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    call @streambuf@do_snextc$qv
    pop cx
    pop cx
    jmp short loc_01ec
loc_01d9:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 1eh]
    mov al, byte ptr es:[bx]
    mov ah, 0
loc_01ec:
    mov word ptr [bp + 0ah], ax
    cmp word ptr [bp + 0ah], 30h
    jl loc_01fe
    cmp word ptr [bp + 0ah], 37h
    jg loc_01fe
    jmp near ptr loc_0167
loc_01fe:
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original integer conversion entry CODE+522.
scan_octal_hex_digits:
    push bp
    mov bp, sp
    sub sp, 0ch
    push si
    push di
    mov word ptr [bp - 2], 0
    mov word ptr [bp - 4], 0
    mov bx, word ptr [bp + 0ah]
    mov al, byte ptr DGROUP:__ctype[bx+1]
    mov ah, 0
    test al, 10h
    jne loc_026c
    cmp word ptr [bp + 0ah], -1
    jne loc_0249
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 6], es
    mov word ptr [bp - 8], bx
    mov ax, word ptr es:[bx + 0ah]
    or ax, 5
    push ax
    push word ptr [bp - 6]
    push bx
    jmp short loc_0261
loc_0249:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 0ah], es
    mov word ptr [bp - 0ch], bx
    mov ax, word ptr es:[bx + 0ah]
    or ax, 2
    push ax
    push word ptr [bp - 0ah]
    push bx
loc_0261:
    call @ios@clear$qi
    add sp, 6
    jmp near ptr loc_031f
loc_026c:
    mov bx, word ptr [bp + 0ah]
    test byte ptr DGROUP:__ctype[bx+1], 4
    je loc_027c
    sub word ptr [bp + 0ah], 37h
    jmp short loc_0290
loc_027c:
    mov bx, word ptr [bp + 0ah]
    test byte ptr DGROUP:__ctype[bx+1], 8
    je loc_028c
    sub word ptr [bp + 0ah], 57h
    jmp short loc_0290
loc_028c:
    sub word ptr [bp + 0ah], 30h
loc_0290:
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    mov cl, 4
    call F_LXLSH@
    push ax
    mov ax, word ptr [bp + 0ah]
    push dx
    cwd
    pop bx
    pop cx
    add cx, ax
    adc bx, dx
    mov word ptr [bp - 2], bx
    mov word ptr [bp - 4], cx
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 1eh]
    or ax, word ptr es:[bx + 20h]
    je loc_02e5
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    inc word ptr es:[bx + 1eh]
    mov ax, word ptr es:[bx + 1eh]
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 22h]
    jb loc_02fc
loc_02e5:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    call @streambuf@do_snextc$qv
    pop cx
    pop cx
    jmp short loc_030f
loc_02fc:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 1eh]
    mov al, byte ptr es:[bx]
    mov ah, 0
loc_030f:
    mov word ptr [bp + 0ah], ax
    mov bx, word ptr [bp + 0ah]
    test byte ptr DGROUP:__ctype[bx+1], 10h
    je loc_031f
    jmp near ptr loc_026c
loc_031f:
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original integer conversion entry CODE+811.
@istream@$brsh$qml:
    push bp
    mov bp, sp
    sub sp, 0eh
    push si
    push di
    xor ax, ax
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @istream@ipfx$qi
    add sp, 6
    or ax, ax
    jne loc_034b
    jmp near ptr loc_0593
loc_034b:
    mov word ptr [bp - 0ah], 0
    mov word ptr [bp - 0ch], 0
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 2], es
    mov word ptr [bp - 4], bx
    les bx, dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 1eh]
    les bx, dword ptr [bp - 4]
    les bx, dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 22h]
    jb loc_0398
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 6], es
    mov word ptr [bp - 8], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 0ch]
    pop cx
    pop cx
    jmp short loc_03ab
loc_0398:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 1eh]
    mov al, byte ptr es:[bx]
    mov ah, 0
loc_03ab:
    mov dx, ax
    cmp dx, 2dh
    jne loc_03b7
    mov ax, 1
    jmp short loc_03b9
loc_03b7:
    xor ax, ax
loc_03b9:
    mov word ptr [bp - 0eh], ax
    cmp dx, 2bh
    je loc_03c7
    cmp word ptr [bp - 0eh], 0
    je loc_0429
loc_03c7:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 1eh]
    or ax, word ptr es:[bx + 20h]
    je loc_03fd
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    inc word ptr es:[bx + 1eh]
    mov ax, word ptr es:[bx + 1eh]
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 22h]
    jb loc_0414
loc_03fd:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    call @streambuf@do_snextc$qv
    pop cx
    pop cx
    jmp short loc_0427
loc_0414:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 1eh]
    mov al, byte ptr es:[bx]
    mov ah, 0
loc_0427:
    mov dx, ax
loc_0429:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 10h], 40h
    je loc_0439
    jmp near ptr loc_0537
loc_0439:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 10h], 20h
    je loc_0449
    jmp near ptr loc_0557
loc_0449:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 10h], 10h
    jne loc_045b
    cmp dx, 30h
    je loc_0469
loc_045b:
    push dx
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push cs
    call scan_signed_digits
    jmp near ptr loc_0542
loc_0469:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 1eh]
    or ax, word ptr es:[bx + 20h]
    je loc_049f
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    inc word ptr es:[bx + 1eh]
    mov ax, word ptr es:[bx + 1eh]
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 22h]
    jb loc_04b6
loc_049f:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    call @streambuf@do_snextc$qv
    pop cx
    pop cx
    jmp short loc_04c9
loc_04b6:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 1eh]
    mov al, byte ptr es:[bx]
    mov ah, 0
loc_04c9:
    mov dx, ax
    cmp dx, 78h
    je loc_04d5
    cmp dx, 58h
    jne loc_054d
loc_04d5:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 1eh]
    or ax, word ptr es:[bx + 20h]
    je loc_050b
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    inc word ptr es:[bx + 1eh]
    mov ax, word ptr es:[bx + 1eh]
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 22h]
    jb loc_0522
loc_050b:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    call @streambuf@do_snextc$qv
    pop cx
    pop cx
    jmp short loc_0535
loc_0522:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 1eh]
    mov al, byte ptr es:[bx]
    mov ah, 0
loc_0535:
    mov dx, ax
loc_0537:
    push dx
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push cs
    call scan_octal_hex_digits
loc_0542:
    add sp, 6
    mov word ptr [bp - 0ah], dx
    mov word ptr [bp - 0ch], ax
    jmp short loc_056e
loc_054d:
    cmp dx, 30h
    jl loc_0564
    cmp dx, 37h
    jg loc_0564
loc_0557:
    push dx
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push cs
    call scan_unsigned_digits
    jmp short loc_0542
loc_0564:
    mov word ptr [bp - 0ah], 0
    mov word ptr [bp - 0ch], 0
loc_056e:
    cmp word ptr [bp - 0eh], 0
    je loc_0583
    mov dx, word ptr [bp - 0ah]
    mov ax, word ptr [bp - 0ch]
    neg dx
    neg ax
    sbb dx, 0
    jmp short loc_0589
loc_0583:
    mov dx, word ptr [bp - 0ah]
    mov ax, word ptr [bp - 0ch]
loc_0589:
    les bx, dword ptr [bp + 0ah]
    mov word ptr es:[bx + 2], dx
    mov word ptr es:[bx], ax
loc_0593:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends
end
