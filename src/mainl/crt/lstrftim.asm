; Original Japanese Borland long strftime / ordinal conversion CRT.
; Structured 16-bit assembler recovery of both entire original functions.
; CODE includes a genuinely symbolic 85-entry formatting dispatch table;
; DATA contains original human-readable fallback format strings.
.8086
extrn __UTOA:near,__tzname:byte,_strcpy:far,_strlen:far,_strncpy:far,__pLocale:dword
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __lstrftime,__getordinal

; Long locale-sensitive formatting dispatcher.

; Original CODE public at +0000
__lstrftime:
    push bp
    mov bp, sp
    sub sp, 2ch
    push si
    push di
    lea ax, [bp - 2ch]
    mov word ptr [bp - 2], ss
    mov word ptr [bp - 4], ax
    mov word ptr [bp - 0ah], 0
    mov word ptr [bp - 8], 1
    jmp near ptr loc_05e6
loc_001e:
    les bx,dword ptr [bp + 0ch]
    cmp byte ptr es:[bx], 25h
    je loc_0039
    inc word ptr [bp - 8]
    mov al, byte ptr es:[bx]
    les bx,dword ptr [bp + 6]
    mov byte ptr es:[bx], al
    inc word ptr [bp + 6]
    jmp near ptr loc_05da
loc_0039:
    push ds
    mov ax,offset DGROUP:default_00
    push ax
    push ss
    lea ax, [bp - 2ch]
    push ax
    call _strcpy
    add sp, 8
loc_004b:
    inc word ptr [bp + 0ch]
    les bx,dword ptr [bp + 0ch]
    mov al, byte ptr es:[bx]
    cbw
    sub ax, 25h
    mov bx, ax
    cmp bx, 54h
    jbe loc_0062
    jmp near ptr case_0588
loc_0062:
    add bx, bx
    jmp word ptr cs:[bx+format_dispatch]
case_0069:
    les bx,dword ptr [bp + 10h]
    mov ax, 0ah
    imul word ptr es:[bx + 0ch]
    mov dx, word ptr DGROUP:__pLocale+2
    mov bx, word ptr DGROUP:__pLocale
    add bx, ax
    add bx, 25ch
    jmp near ptr loc_031a
case_0084:
    les bx,dword ptr [bp + 10h]
    mov ax, 14h
    imul word ptr es:[bx + 0ch]
    mov dx, word ptr DGROUP:__pLocale+2
    mov bx, word ptr DGROUP:__pLocale
    add bx, ax
    add bx, 2a2h
    jmp near ptr loc_031a
case_009f:
    les bx,dword ptr [bp + 10h]
    mov ax, 0ah
    imul word ptr es:[bx + 8]
    mov dx, word ptr DGROUP:__pLocale+2
    mov bx, word ptr DGROUP:__pLocale
    add bx, ax
    add bx, 32eh
    jmp near ptr loc_031a
case_00ba:
    les bx,dword ptr [bp + 10h]
    mov ax, 14h
    imul word ptr es:[bx + 8]
    mov dx, word ptr DGROUP:__pLocale+2
    mov bx, word ptr DGROUP:__pLocale
    add bx, ax
    add bx, 3a6h
    jmp near ptr loc_031a
case_00d5:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    push word ptr [bp + 12h]
    push word ptr [bp + 10h]
    mov ax, word ptr DGROUP:__pLocale
    add ax, 4aah
    jmp near ptr loc_04f5
case_00f0:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx + 0ah]
    add ax, 76ch
    mov bx, 64h
    cwd
    idiv bx
    mov word ptr [bp - 6], ax
    push ax
    cmp word ptr [bp - 6], 0ah
    jl loc_010d
    jmp near ptr loc_0546
loc_010d:
    jmp near ptr loc_0541
case_0110:
    cmp word ptr [bp - 0ah], 0
    je loc_0132
    push ss
    lea ax, [bp - 2ch]
    push ax
    les bx,dword ptr [bp + 10h]
    push word ptr es:[bx + 6]
    assume cs:NOTHING
    call far ptr __getordinal
    assume cs:_TEXT
    add sp, 6
    cmp ax, 1
    jne loc_0132
    jmp near ptr case_0588
loc_0132:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx + 6]
    mov word ptr [bp - 0ch], ax
    push ax
    cmp word ptr [bp - 0ch], 0ah
    jl loc_0146
    jmp near ptr loc_0546
loc_0146:
    jmp near ptr loc_0541
case_0149:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    push word ptr [bp + 12h]
    push word ptr [bp + 10h]
    push ds
    mov ax,offset DGROUP:date_format
    jmp near ptr loc_04f9
case_0162:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx + 6]
    mov word ptr [bp - 6], ax
    cmp word ptr [bp - 6], 0ah
    jge loc_0176
    mov byte ptr [bp - 2ch], 20h
loc_0176:
    cmp word ptr [bp - 0ah], 0
    je loc_0194
    push ss
    lea ax, [bp - 2ch]
    push ax
    push word ptr [bp - 6]
    assume cs:NOTHING
    call far ptr __getordinal
    assume cs:_TEXT
    add sp, 6
    cmp ax, 1
    jne loc_0194
    jmp near ptr case_0588
loc_0194:
    push word ptr [bp - 6]
    cmp word ptr [bp - 6], 0ah
    jl loc_01a0
    jmp near ptr loc_0546
loc_01a0:
    jmp near ptr loc_0541
case_01a3:
    cmp word ptr [bp - 0ah], 0
    je loc_01c5
    push ss
    lea ax, [bp - 2ch]
    push ax
    les bx,dword ptr [bp + 10h]
    push word ptr es:[bx + 4]
    assume cs:NOTHING
    call far ptr __getordinal
    assume cs:_TEXT
    add sp, 6
    cmp ax, 1
    jne loc_01c5
    jmp near ptr case_0588
loc_01c5:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx + 4]
    mov word ptr [bp - 0eh], ax
    push ax
    cmp word ptr [bp - 0eh], 0ah
    jl loc_01d9
    jmp near ptr loc_0546
loc_01d9:
    jmp near ptr loc_0541
case_01dc:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx + 4]
    mov bx, 0ch
    cwd
    idiv bx
    mov word ptr [bp - 6], dx
    cmp word ptr [bp - 6], 0
    jne loc_01f7
    mov word ptr [bp - 6], 0ch
loc_01f7:
    cmp word ptr [bp - 0ah], 0
    je loc_0215
    push ss
    lea ax, [bp - 2ch]
    push ax
    push word ptr [bp - 6]
    assume cs:NOTHING
    call far ptr __getordinal
    assume cs:_TEXT
    add sp, 6
    cmp ax, 1
    jne loc_0215
    jmp near ptr case_0588
loc_0215:
    push word ptr [bp - 6]
    cmp word ptr [bp - 6], 0ah
    jl loc_0221
    jmp near ptr loc_0546
loc_0221:
    jmp near ptr loc_0541
case_0224:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx + 0eh]
    inc ax
    mov word ptr [bp - 6], ax
    cmp word ptr [bp - 0ah], 0
    je loc_024d
    push ss
    lea ax, [bp - 2ch]
    push ax
    push word ptr [bp - 6]
    assume cs:NOTHING
    call far ptr __getordinal
    assume cs:_TEXT
    add sp, 6
    cmp ax, 1
    jne loc_024d
    jmp near ptr case_0588
loc_024d:
    push word ptr [bp - 6]
    cmp word ptr [bp - 6], 0ah
    jge loc_025b
    mov ax, 1
    jmp short loc_025d
loc_025b:
    xor ax, ax
loc_025d:
    push ax
    cmp word ptr [bp - 6], 64h
    jge loc_0269
    mov ax, 1
    jmp short loc_026b
loc_0269:
    xor ax, ax
loc_026b:
    pop dx
    add dx, ax
    lea ax, [bp - 2ch]
    add dx, ax
    push ss
    push dx
    jmp near ptr loc_0560
case_0278:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx + 8]
    inc ax
    mov word ptr [bp - 6], ax
    cmp word ptr [bp - 0ah], 0
    je loc_02a1
    push ss
    lea ax, [bp - 2ch]
    push ax
    push word ptr [bp - 6]
    assume cs:NOTHING
    call far ptr __getordinal
    assume cs:_TEXT
    add sp, 6
    cmp ax, 1
    jne loc_02a1
    jmp near ptr case_0588
loc_02a1:
    push word ptr [bp - 6]
    cmp word ptr [bp - 6], 0ah
    jl loc_02ad
    jmp near ptr loc_0546
loc_02ad:
    jmp near ptr loc_0541
case_02b0:
    cmp word ptr [bp - 0ah], 0
    je loc_02d2
    push ss
    lea ax, [bp - 2ch]
    push ax
    les bx,dword ptr [bp + 10h]
    push word ptr es:[bx + 2]
    assume cs:NOTHING
    call far ptr __getordinal
    assume cs:_TEXT
    add sp, 6
    cmp ax, 1
    jne loc_02d2
    jmp near ptr case_0588
loc_02d2:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx + 2]
    mov word ptr [bp - 10h], ax
    push ax
    cmp word ptr [bp - 10h], 0ah
    jl loc_02e6
    jmp near ptr loc_0546
loc_02e6:
    jmp near ptr loc_0541
case_02e9:
    mov byte ptr [bp - 2ch], 0ah
    jmp near ptr loc_0379
case_02f0:
    mov word ptr [bp - 0ah], 1
    jmp near ptr loc_004b
case_02f8:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx + 4]
    mov bx, 0ch
    cwd
    idiv bx
    push ax
    mov ax, 0ah
    pop dx
    imul dx
    mov dx, word ptr DGROUP:__pLocale+2
    mov bx, word ptr DGROUP:__pLocale
    add bx, ax
    add bx, 496h
loc_031a:
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], bx
    jmp near ptr case_0588
case_0323:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    push word ptr [bp + 12h]
    push word ptr [bp + 10h]
    mov ax, word ptr DGROUP:__pLocale
    add ax, 4f5h
    jmp near ptr loc_04f5
case_033e:
    cmp word ptr [bp - 0ah], 0
    je loc_035f
    push ss
    lea ax, [bp - 2ch]
    push ax
    les bx,dword ptr [bp + 10h]
    push word ptr es:[bx]
    assume cs:NOTHING
    call far ptr __getordinal
    assume cs:_TEXT
    add sp, 6
    cmp ax, 1
    jne loc_035f
    jmp near ptr case_0588
loc_035f:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx]
    mov word ptr [bp - 12h], ax
    push ax
    cmp word ptr [bp - 12h], 0ah
    jl loc_0372
    jmp near ptr loc_0546
loc_0372:
    jmp near ptr loc_0541
case_0375:
    mov byte ptr [bp - 2ch], 9
loc_0379:
    mov byte ptr [bp - 2bh], 0
    jmp near ptr case_0588
case_0380:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    push word ptr [bp + 12h]
    push word ptr [bp + 10h]
    push ds
    mov ax,offset DGROUP:time_format
    jmp near ptr loc_04f9
case_0399:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx + 0ch]
    push ax
    mov ax, word ptr es:[bx + 0eh]
    mov bx, 7
    cwd
    idiv bx
    pop ax
    sub ax, dx
    mov word ptr [bp - 6], ax
    cmp word ptr [bp - 6], 0
    jge loc_03bb
    add word ptr [bp - 6], 7
loc_03bb:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx + 0eh]
    add ax, word ptr [bp - 6]
    mov bx, 7
    cwd
    idiv bx
    mov word ptr [bp - 6], ax
    cmp word ptr [bp - 0ah], 0
    je loc_03ec
    push ss
    lea ax, [bp - 2ch]
    push ax
    push word ptr [bp - 6]
    assume cs:NOTHING
    call far ptr __getordinal
    assume cs:_TEXT
    add sp, 6
    cmp ax, 1
    jne loc_03ec
    jmp near ptr case_0588
loc_03ec:
    push word ptr [bp - 6]
    cmp word ptr [bp - 6], 0ah
    jl loc_03f8
    jmp near ptr loc_0546
loc_03f8:
    jmp near ptr loc_0541
case_03fb:
    les bx,dword ptr [bp + 10h]
    cmp word ptr es:[bx + 0ch], 0
    je loc_040b
    mov ax, word ptr es:[bx + 0ch]
    jmp short loc_040e
loc_040b:
    mov ax, 7
loc_040e:
    mov word ptr [bp - 6], ax
    cmp word ptr [bp - 0ah], 0
    je loc_042f
    push ss
    lea ax, [bp - 2ch]
    push ax
    push word ptr [bp - 6]
    assume cs:NOTHING
    call far ptr __getordinal
    assume cs:_TEXT
    add sp, 6
    cmp ax, 1
    jne loc_042f
    jmp near ptr case_0588
loc_042f:
    push word ptr [bp - 6]
    jmp near ptr loc_055b
case_0435:
    cmp word ptr [bp - 0ah], 0
    je loc_0457
    push ss
    lea ax, [bp - 2ch]
    push ax
    les bx,dword ptr [bp + 10h]
    push word ptr es:[bx + 0ch]
    assume cs:NOTHING
    call far ptr __getordinal
    assume cs:_TEXT
    add sp, 6
    cmp ax, 1
    jne loc_0457
    jmp near ptr case_0588
loc_0457:
    les bx,dword ptr [bp + 10h]
    push word ptr es:[bx + 0ch]
    jmp near ptr loc_055b
case_0461:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx + 0ch]
    push ax
    mov ax, word ptr es:[bx + 0eh]
    mov bx, 7
    cwd
    idiv bx
    pop ax
    sub ax, dx
    mov word ptr [bp - 6], ax
    cmp word ptr [bp - 6], 0
    jge loc_0483
    add word ptr [bp - 6], 7
loc_0483:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx + 0eh]
    add ax, word ptr [bp - 6]
    dec ax
    mov bx, 7
    cwd
    idiv bx
    mov word ptr [bp - 6], ax
    cmp word ptr [bp - 0ah], 0
    je loc_04b5
    push ss
    lea ax, [bp - 2ch]
    push ax
    push word ptr [bp - 6]
    assume cs:NOTHING
    call far ptr __getordinal
    assume cs:_TEXT
    add sp, 6
    cmp ax, 1
    jne loc_04b5
    jmp near ptr case_0588
loc_04b5:
    push word ptr [bp - 6]
    cmp word ptr [bp - 6], 0ah
    jl loc_04c1
    jmp near ptr loc_0546
loc_04c1:
    jmp short loc_0541
case_04c3:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    push word ptr [bp + 12h]
    push word ptr [bp + 10h]
    mov ax, word ptr DGROUP:__pLocale
    add ax, 4c3h
    jmp short loc_04f5
case_04dd:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    push word ptr [bp + 12h]
    push word ptr [bp + 10h]
    mov ax, word ptr DGROUP:__pLocale
    add ax, 4dch
loc_04f5:
    push word ptr DGROUP:__pLocale+2
loc_04f9:
    push ax
    push word ptr [bp + 0ah]
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    push cs
    call __lstrftime
    add sp, 0eh
    jmp short case_0588
case_050c:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx + 0ah]
    add ax, 76ch
    mov bx, 64h
    cwd
    idiv bx
    mov word ptr [bp - 6], dx
    cmp word ptr [bp - 0ah], 0
    je loc_0538
    push ss
    lea ax, [bp - 2ch]
    push ax
    push dx
    assume cs:NOTHING
    call far ptr __getordinal
    assume cs:_TEXT
    add sp, 6
    cmp ax, 1
    je case_0588
loc_0538:
    push word ptr [bp - 6]
    cmp word ptr [bp - 6], 0ah
    jge loc_0546
loc_0541:
    mov ax, 1
    jmp short loc_0548
loc_0546:
    xor ax, ax
loc_0548:
    lea dx, [bp - 2ch]
    add ax, dx
    push ss
    jmp short loc_055f
case_0550:
    les bx,dword ptr [bp + 10h]
    mov ax, word ptr es:[bx + 0ah]
    add ax, 76ch
    push ax
loc_055b:
    push ss
    lea ax, [bp - 2ch]
loc_055f:
    push ax
loc_0560:
    call __UTOA
    jmp short case_0588
case_0565:
    les bx,dword ptr [bp + 10h]
    mov bx, word ptr es:[bx + 10h]
    mov cl, 2
    shl bx, cl
    mov dx, word ptr DGROUP:__tzname[bx+2]
    mov ax, word ptr DGROUP:__tzname[bx]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    jmp short case_0588
case_0580:
    mov word ptr [bp - 2], ds
    mov word ptr [bp - 4],offset DGROUP:literal_percent
case_0588:
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call _strlen
    pop cx
    pop cx
    mov dx, word ptr [bp + 0ah]
    sub dx, word ptr [bp - 8]
    cmp ax, dx
    jae loc_05ae
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call _strlen
    pop cx
    pop cx
    jmp short loc_05b4
loc_05ae:
    mov ax, word ptr [bp + 0ah]
    sub ax, word ptr [bp - 8]
loc_05b4:
    mov word ptr [bp - 6], ax
    push ax
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call _strncpy
    add sp, 0ah
    mov ax, word ptr [bp - 6]
    add word ptr [bp - 8], ax
    add word ptr [bp + 6], ax
    mov word ptr [bp - 0ah], 0
loc_05da:
    inc word ptr [bp + 0ch]
    lea ax, [bp - 2ch]
    mov word ptr [bp - 2], ss
    mov word ptr [bp - 4], ax
loc_05e6:
    mov ax, word ptr [bp - 8]
    cmp ax, word ptr [bp + 0ah]
    jae loc_05fa
    les bx,dword ptr [bp + 0ch]
    cmp byte ptr es:[bx], 0
    je loc_05fa
    jmp near ptr loc_001e
loc_05fa:
    les bx,dword ptr [bp + 6]
    mov byte ptr es:[bx], 0
    les bx,dword ptr [bp + 0ch]
    cmp byte ptr es:[bx], 0
    je loc_060e
    xor ax, ax
    jmp short loc_0612
loc_060e:
    mov ax, word ptr [bp - 8]
    dec ax
loc_0612:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

format_dispatch label word
    dw case_0580 ; format class 0
    dw case_0588 ; format class 1
    dw case_0588 ; format class 2
    dw case_0588 ; format class 3
    dw case_0588 ; format class 4
    dw case_0588 ; format class 5
    dw case_0588 ; format class 6
    dw case_0588 ; format class 7
    dw case_0588 ; format class 8
    dw case_0588 ; format class 9
    dw case_0588 ; format class 10
    dw case_0588 ; format class 11
    dw case_0588 ; format class 12
    dw case_0588 ; format class 13
    dw case_0588 ; format class 14
    dw case_0588 ; format class 15
    dw case_0588 ; format class 16
    dw case_0588 ; format class 17
    dw case_0588 ; format class 18
    dw case_0588 ; format class 19
    dw case_0588 ; format class 20
    dw case_0588 ; format class 21
    dw case_0588 ; format class 22
    dw case_0588 ; format class 23
    dw case_0588 ; format class 24
    dw case_0588 ; format class 25
    dw case_0588 ; format class 26
    dw case_0588 ; format class 27
    dw case_0084 ; format class 28
    dw case_00ba ; format class 29
    dw case_00f0 ; format class 30
    dw case_0149 ; format class 31
    dw case_0588 ; format class 32
    dw case_0588 ; format class 33
    dw case_0588 ; format class 34
    dw case_01a3 ; format class 35
    dw case_01dc ; format class 36
    dw case_0588 ; format class 37
    dw case_0588 ; format class 38
    dw case_0588 ; format class 39
    dw case_02b0 ; format class 40
    dw case_0588 ; format class 41
    dw case_02f0 ; format class 42
    dw case_0588 ; format class 43
    dw case_0588 ; format class 44
    dw case_0588 ; format class 45
    dw case_033e ; format class 46
    dw case_0380 ; format class 47
    dw case_0399 ; format class 48
    dw case_0588 ; format class 49
    dw case_0461 ; format class 50
    dw case_04dd ; format class 51
    dw case_0550 ; format class 52
    dw case_0565 ; format class 53
    dw case_0588 ; format class 54
    dw case_0588 ; format class 55
    dw case_0588 ; format class 56
    dw case_0588 ; format class 57
    dw case_0588 ; format class 58
    dw case_0588 ; format class 59
    dw case_0069 ; format class 60
    dw case_009f ; format class 61
    dw case_00d5 ; format class 62
    dw case_0110 ; format class 63
    dw case_0162 ; format class 64
    dw case_0588 ; format class 65
    dw case_0588 ; format class 66
    dw case_009f ; format class 67
    dw case_0588 ; format class 68
    dw case_0224 ; format class 69
    dw case_0588 ; format class 70
    dw case_0588 ; format class 71
    dw case_0278 ; format class 72
    dw case_02e9 ; format class 73
    dw case_0588 ; format class 74
    dw case_02f8 ; format class 75
    dw case_0588 ; format class 76
    dw case_0323 ; format class 77
    dw case_0588 ; format class 78
    dw case_0375 ; format class 79
    dw case_03fb ; format class 80
    dw case_0588 ; format class 81
    dw case_0435 ; format class 82
    dw case_04c3 ; format class 83
    dw case_050c ; format class 84

; Second real far entry, ordinal-string helper.

; Original CODE public at +06c2
__getordinal:
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    mov cx, word ptr [bp + 6]
    mov word ptr [bp - 2], 0
    cmp cx, 63h
    ja loc_071f
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 559h
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax
    jmp short loc_06f5
loc_06e9:
    les bx,dword ptr [bp - 6]
    inc word ptr [bp - 6]
    cmp byte ptr es:[bx], 0
    jne loc_06e9
loc_06f5:
    mov ax, word ptr [bp - 2]
    inc word ptr [bp - 2]
    cmp ax, cx
    jne loc_06e9
    les bx,dword ptr [bp - 6]
    cmp byte ptr es:[bx], 0
    je loc_071f
    push word ptr [bp - 4]
    push bx
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    call _strcpy
    add sp, 8
    mov ax, 1
    jmp short loc_0721
loc_071f:
    xor ax, ax
loc_0721:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends

_DATA segment word public 'DATA'
default_00 db '00',0
date_format db '%m/%d/%y',0
time_format db '%H:%M:%S',0
literal_percent db '%',0
_DATA ends
end
