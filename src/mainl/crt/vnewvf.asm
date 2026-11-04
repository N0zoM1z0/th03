; Recovered selected original Japanese Borland vector vnewvf algorithm.
; Preserve 16-bit near/far constructors, destructors and stride math.
; 16 selector words + 16 genuine symbolic relocatable handler slots.
; No original executable CODE bytes, artificial filler or OBJ patches.
.8086
extrn @$bnwa$qui:far,@$bnwa$qul:far,@__RefDestructorCount$qv:far
extrn _abort:far,N_LXMUL@:near,N_LMOD@:near
extrn __AHSHIFT:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @_vector_vnew_$qnvuiuluie
@_vector_vnew_$qnvuiuluie:
    push bp
    mov bp, sp
    sub sp, 1ch
    push si
    push di
    mov word ptr [bp - 0ch], 1
    mov word ptr [bp - 0eh], 0
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    mov dx, word ptr es:[bx + 2]
    mov ax, word ptr es:[bx]
    mov word ptr [bp - 10h], dx
    mov word ptr [bp - 12h], ax
    lea ax, [bp + 12h]
    mov word ptr [bp - 2], ss
    mov word ptr [bp - 4], ax
    test byte ptr [bp + 10h], 1
    je label_0053
    add word ptr [bp - 4], 4
    les bx, dword ptr [bp - 4]
    mov dx, word ptr es:[bx - 2]
    mov ax, word ptr es:[bx - 4]
    mov word ptr [bp - 8], dx
    mov word ptr [bp - 0ah], ax
    or ax, word ptr [bp - 8]
    jne label_006c
    jmp short label_0067
label_0053:
    add word ptr [bp - 4], 2
    les bx, dword ptr [bp - 4]
    mov ax, word ptr es:[bx - 2]
    mov word ptr [bp - 6], ax
    cmp word ptr [bp - 6], 0
    jne label_006c
label_0067:
    mov word ptr [bp - 0ch], 0
label_006c:
    test byte ptr [bp + 10h], 10h
    je label_0077
    mov word ptr [bp - 0eh], 4
label_0077:
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    je label_0082
    jmp near ptr label_0149
label_0082:
    test byte ptr [bp + 10h], 40h
    je label_0104
    add word ptr [bp - 0eh], 2
    mov bx, word ptr [bp + 0ah]
    xor cx, cx
    mov dx, word ptr [bp + 0eh]
    mov ax, word ptr [bp + 0ch]
    call N_LXMUL@
    add ax, word ptr [bp - 0eh]
    adc dx, 0
    add ax, word ptr [bp + 0ah]
    adc dx, 0
    push dx
    push ax
    call @$bnwa$qul
    pop cx
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, word ptr [bp + 8]
    jne label_00bd
    jmp near ptr label_0142
label_00bd:
    xor ax, ax
    push ax
    push word ptr [bp + 0ah]
    mov ax, 1
    xor dx, dx
    push ax
    push dx
    call N_LMOD@
    mov word ptr [bp - 18h], ax
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 16h], ax
    jmp short label_00de
label_00d8:
    mov ax, word ptr [bp + 0ah]
    add word ptr [bp - 18h], ax
label_00de:
    mov ax, word ptr [bp - 0eh]
    add ax, word ptr [bp - 16h]
    cmp ax, word ptr [bp - 18h]
    ja label_00d8
    mov ax, word ptr [bp - 18h]
    sub ax, word ptr [bp - 16h]
    sub ax, word ptr [bp - 0eh]
    add word ptr [bp + 6], ax
    les bx, dword ptr [bp + 6]
    mov ax, word ptr [bp - 16h]
    mov word ptr es:[bx], ax
    add word ptr [bp + 6], 2
    jmp short label_0149
label_0104:
    mov bx, word ptr [bp + 0ah]
    xor cx, cx
    mov dx, word ptr [bp + 0eh]
    mov ax, word ptr [bp + 0ch]
    call N_LXMUL@
    add ax, word ptr [bp - 0eh]
    adc dx, 0
    mov word ptr [bp - 1ah], dx
    mov word ptr [bp - 1ch], ax
    cmp word ptr [bp - 1ah], 0
    jb label_012e
    ja label_0142
    cmp word ptr [bp - 1ch], -1
    jbe label_012e
    jmp short label_0142
label_012e:
    push word ptr [bp - 1ch]
    call @$bnwa$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, word ptr [bp + 8]
    jne label_0149
label_0142:
    xor dx, dx
    xor ax, ax
    jmp near ptr label_02cc
label_0149:
    test byte ptr [bp + 10h], 10h
    je label_0163
    les bx, dword ptr [bp + 6]
    mov dx, word ptr [bp + 0eh]
    mov ax, word ptr [bp + 0ch]
    mov word ptr es:[bx + 2], dx
    mov word ptr es:[bx], ax
    add word ptr [bp + 6], 4
label_0163:
    cmp word ptr [bp - 0ch], 0
    jne label_016c
    jmp near ptr label_02ab
label_016c:
    mov ax, word ptr [bp + 10h]
    and ax, 1a7h
    mov word ptr [bp - 16h], ax
    test byte ptr [bp + 10h], 80h
    je label_0180
    and word ptr [bp - 16h], 0feffh
label_0180:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 18h], dx
    mov word ptr [bp - 1ah], ax
    jmp near ptr label_028d
label_018f:
    mov ax, word ptr [bp - 16h]
    mov word ptr [bp - 14h], ax
    mov cx, 10h
    mov bx,offset cs:vector_selector_words
label_019b:
    mov ax, word ptr cs:[bx]
    cmp ax, word ptr [bp - 14h]
    je label_01ab
    add bx, 2
    loop label_019b
    jmp near ptr label_0275
label_01ab:
    jmp word ptr cs:[bx + 20h]
; Original vector type case handler
case_01af:
    xor ax, ax
    push ax
    push word ptr [bp - 18h]
    push word ptr [bp - 1ah]
    call word ptr word ptr [bp - 6]
    jmp short label_01c9
; Original vector type case handler
case_01bd:
    xor ax, ax
    push ax
    push word ptr [bp - 18h]
    push word ptr [bp - 1ah]
    call dword ptr [bp - 0ah]
label_01c9:
    add sp, 6
    jmp near ptr label_027a
; Original vector type case handler
case_01cf:
    push word ptr [bp - 18h]
    push word ptr [bp - 1ah]
    xor ax, ax
    push ax
    jmp short label_01e3
; Original vector type case handler
case_01da:
    xor ax, ax
    push ax
    push word ptr [bp - 18h]
    push word ptr [bp - 1ah]
label_01e3:
    call word ptr word ptr [bp - 6]
    jmp short label_01ff
; Original vector type case handler
case_01e8:
    push word ptr [bp - 18h]
    push word ptr [bp - 1ah]
    xor ax, ax
    push ax
    jmp short label_01fc
; Original vector type case handler
case_01f3:
    xor ax, ax
    push ax
    push word ptr [bp - 18h]
    push word ptr [bp - 1ah]
label_01fc:
    call dword ptr [bp - 0ah]
label_01ff:
    jmp short label_027a
; Original vector type case handler
case_0201:
    push word ptr [bp - 18h]
    push word ptr [bp - 1ah]
    xor ax, ax
    call word ptr word ptr [bp - 6]
    jmp short label_0219
; Original vector type case handler
case_020e:
    push word ptr [bp - 18h]
    push word ptr [bp - 1ah]
    xor ax, ax
    call dword ptr [bp - 0ah]
label_0219:
    jmp short label_027a
; Original vector type case handler
case_021b:
    push ds
    push si
    lds si, dword ptr [bp - 1ah]
    xor ax, ax
    push ax
    call word ptr word ptr [bp - 6]
    pop cx
    pop si
    pop ds
    jmp short label_027a
; Original vector type case handler
case_022b:
    push ds
    push si
    lds si, dword ptr [bp - 1ah]
    xor ax, ax
    push ax
    call dword ptr [bp - 0ah]
    pop cx
    pop si
    pop ds
    jmp short label_027a
; Original vector type case handler
case_023b:
    push ds
    push si
    lds si, dword ptr [bp - 1ah]
    xor ax, ax
    push ax
    call word ptr word ptr [bp - 6]
    pop si
    pop ds
    jmp short label_027a
; Original vector type case handler
case_024a:
    push ds
    push si
    lds si, dword ptr [bp - 1ah]
    xor ax, ax
    push ax
    call dword ptr [bp - 0ah]
    pop si
    pop ds
    jmp short label_027a
; Original vector type case handler
case_0259:
    push ds
    push si
    lds si, dword ptr [bp - 1ah]
    xor ax, ax
    call word ptr word ptr [bp - 6]
    pop si
    pop ds
    jmp short label_027a
; Original vector type case handler
case_0267:
    push ds
    push si
    lds si, dword ptr [bp - 1ah]
    xor ax, ax
    call dword ptr [bp - 0ah]
    pop si
    pop ds
    jmp short label_027a
label_0275:
    call _abort
label_027a:
    mov ax, word ptr [bp + 0ah]
    xor dx, dx
    add word ptr [bp - 1ah], ax
    adc dx, 0
    mov cx,offset __AHSHIFT
    shl dx, cl
    add word ptr [bp - 18h], dx
label_028d:
    mov ax, word ptr [bp + 0eh]
    mov dx, word ptr [bp + 0ch]
    sub word ptr [bp + 0ch], 1
    sbb word ptr [bp + 0eh], 0
    or ax, ax
    jbe label_02a2
    jmp near ptr label_018f
label_02a2:
    jne label_02ab
    or dx, dx
    jbe label_02ab
    jmp near ptr label_018f
label_02ab:
    test byte ptr [bp + 11h], 2
    je label_02c6
    call @__RefDestructorCount$qv
    mov bx, word ptr [bp - 10h]
    mov cx, word ptr [bp - 12h]
    mov es, dx
    xchg bx, ax
    mov word ptr es:[bx + 2], ax
    mov word ptr es:[bx], cx
label_02c6:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
label_02cc:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Type-code selectors used by the original Borland switch.
vector_selector_words label word
    dw 4
    dw 5
    dw 6
    dw 7
    dw 36
    dw 37
    dw 132
    dw 133
    dw 134
    dw 135
    dw 164
    dw 165
    dw 262
    dw 263
    dw 292
    dw 293
vector_handler_words label word
    dw case_01af
    dw case_01bd
    dw case_01cf
    dw case_01e8
    dw case_0201
    dw case_020e
    dw case_021b
    dw case_022b
    dw case_023b
    dw case_024a
    dw case_0259
    dw case_0267
    dw case_01da
    dw case_01f3
    dw case_0201
    dw case_020e
_TEXT ends
end
