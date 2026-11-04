; Recovered selected original Japanese Borland vector vdelf algorithm.
; Preserve 16-bit near/far constructors, destructors and stride math.
; 16 selector words + 16 genuine symbolic relocatable handler slots.
; No original executable CODE bytes, artificial filler or OBJ patches.
.8086
extrn @$bdla$qnv:far,_abort:far,N_LXMUL@:near
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
public @_vector_delete_$qnvuiuluie
@_vector_delete_$qnvuiuluie:
    push bp
    mov bp, sp
    sub sp, 18h
    push si
    push di
    mov word ptr [bp - 0ch], 1
    mov word ptr [bp - 10h], 0
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne label_001d
    jmp near ptr label_0247
label_001d:
    lea ax, [bp + 12h]
    mov word ptr [bp - 2], ss
    mov word ptr [bp - 4], ax
    test byte ptr [bp + 10h], 1
    je label_0048
    add word ptr [bp - 4], 4
    les bx, dword ptr [bp - 4]
    mov dx, word ptr es:[bx - 2]
    mov ax, word ptr es:[bx - 4]
    mov word ptr [bp - 8], dx
    mov word ptr [bp - 0ah], ax
    or ax, word ptr [bp - 8]
    jne label_0061
    jmp short label_005c
label_0048:
    add word ptr [bp - 4], 2
    les bx, dword ptr [bp - 4]
    mov ax, word ptr es:[bx - 2]
    mov word ptr [bp - 6], ax
    cmp word ptr [bp - 6], 0
    jne label_0061
label_005c:
    mov word ptr [bp - 0ch], 0
label_0061:
    test byte ptr [bp + 10h], 10h
    je label_0078
    les bx, dword ptr [bp + 6]
    mov dx, word ptr es:[bx - 2]
    mov ax, word ptr es:[bx - 4]
    mov word ptr [bp + 0eh], dx
    mov word ptr [bp + 0ch], ax
label_0078:
    cmp word ptr [bp - 0ch], 0
    jne label_0081
    jmp near ptr label_01eb
label_0081:
    mov ax, word ptr [bp + 10h]
    and ax, 1a7h
    mov word ptr [bp - 14h], ax
    test byte ptr [bp - 14h], 80h
    je label_0095
    and word ptr [bp - 14h], 0feffh
label_0095:
    mov bx, word ptr [bp + 0ah]
    xor cx, cx
    mov dx, word ptr [bp + 0eh]
    mov ax, word ptr [bp + 0ch]
    sub ax, 1
    sbb dx, 0
    call N_LXMUL@
    add ax, word ptr [bp + 6]
    adc dx, 0
    mov cx,offset __AHSHIFT
    shl dx, cl
    add dx, word ptr [bp + 8]
    mov word ptr [bp - 16h], dx
    mov word ptr [bp - 18h], ax
    jmp near ptr label_01cd
label_00c0:
    mov ax, word ptr [bp - 14h]
    mov word ptr [bp - 12h], ax
    mov cx, 10h
    mov bx,offset cs:vector_selector_words
label_00cc:
    mov ax, word ptr cs:[bx]
    cmp ax, word ptr [bp - 12h]
    je label_00dc
    add bx, 2
    loop label_00cc
    jmp near ptr label_01b5
label_00dc:
    jmp word ptr cs:[bx + 20h]
; Original vector type case handler
case_00e0:
    mov ax, 2
    push ax
    push word ptr [bp - 16h]
    push word ptr [bp - 18h]
    call word ptr word ptr [bp - 6]
    jmp short label_00fc
; Original vector type case handler
case_00ef:
    mov ax, 2
    push ax
    push word ptr [bp - 16h]
    push word ptr [bp - 18h]
    call dword ptr [bp - 0ah]
label_00fc:
    add sp, 6
    jmp near ptr label_01ba
; Original vector type case handler
case_0102:
    push word ptr [bp - 16h]
    push word ptr [bp - 18h]
    mov ax, 2
    push ax
    jmp short label_0118
; Original vector type case handler
case_010e:
    mov ax, 2
    push ax
    push word ptr [bp - 16h]
    push word ptr [bp - 18h]
label_0118:
    call word ptr word ptr [bp - 6]
    jmp short label_0136
; Original vector type case handler
case_011d:
    push word ptr [bp - 16h]
    push word ptr [bp - 18h]
    mov ax, 2
    push ax
    jmp short label_0133
; Original vector type case handler
case_0129:
    mov ax, 2
    push ax
    push word ptr [bp - 16h]
    push word ptr [bp - 18h]
label_0133:
    call dword ptr [bp - 0ah]
label_0136:
    jmp near ptr label_01ba
; Original vector type case handler
case_0139:
    push word ptr [bp - 16h]
    push word ptr [bp - 18h]
    mov ax, 2
    call word ptr word ptr [bp - 6]
    jmp short label_0153
; Original vector type case handler
case_0147:
    push word ptr [bp - 16h]
    push word ptr [bp - 18h]
    mov ax, 2
    call dword ptr [bp - 0ah]
label_0153:
    jmp short label_01ba
; Original vector type case handler
case_0155:
    push ds
    push si
    lds si, dword ptr [bp - 18h]
    mov ax, 2
    push ax
    call word ptr word ptr [bp - 6]
    pop cx
    pop si
    pop ds
    jmp short label_01ba
; Original vector type case handler
case_0166:
    push ds
    push si
    lds si, dword ptr [bp - 18h]
    mov ax, 2
    push ax
    call dword ptr [bp - 0ah]
    pop cx
    pop si
    pop ds
    jmp short label_01ba
; Original vector type case handler
case_0177:
    push ds
    push si
    lds si, dword ptr [bp - 18h]
    mov ax, 2
    push ax
    call word ptr word ptr [bp - 6]
    pop si
    pop ds
    jmp short label_01ba
; Original vector type case handler
case_0187:
    push ds
    push si
    lds si, dword ptr [bp - 18h]
    mov ax, 2
    push ax
    call dword ptr [bp - 0ah]
    pop si
    pop ds
    jmp short label_01ba
; Original vector type case handler
case_0197:
    push ds
    push si
    lds si, dword ptr [bp - 18h]
    mov ax, 2
    call word ptr word ptr [bp - 6]
    pop si
    pop ds
    jmp short label_01ba
; Original vector type case handler
case_01a6:
    push ds
    push si
    lds si, dword ptr [bp - 18h]
    mov ax, 2
    call dword ptr [bp - 0ah]
    pop si
    pop ds
    jmp short label_01ba
label_01b5:
    call _abort
label_01ba:
    mov ax, word ptr [bp + 0ah]
    xor dx, dx
    sub word ptr [bp - 18h], ax
    sbb dx, 0
    mov cx,offset __AHSHIFT
    shl dx, cl
    add word ptr [bp - 16h], dx
label_01cd:
    mov ax, word ptr [bp + 0eh]
    mov dx, word ptr [bp + 0ch]
    sub word ptr [bp + 0ch], 1
    sbb word ptr [bp + 0eh], 0
    or ax, ax
    jbe label_01e2
    jmp near ptr label_00c0
label_01e2:
    jne label_01eb
    or dx, dx
    jbe label_01eb
    jmp near ptr label_00c0
label_01eb:
    test byte ptr [bp + 10h], 10h
    je label_01f6
    mov word ptr [bp - 10h], 4
label_01f6:
    test byte ptr [bp + 10h], 40h
    je label_021b
    add word ptr [bp - 10h], 2
    les bx, dword ptr [bp + 6]
    sub bx, word ptr [bp - 10h]
    mov al, byte ptr es:[bx]
    cbw
    mov word ptr [bp - 0eh], ax
    mov ax, word ptr [bp + 8]
    mov dx, word ptr [bp - 0eh]
    mov word ptr [bp + 8], ax
    mov word ptr [bp + 6], dx
    jmp short label_022a
label_021b:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    sub ax, word ptr [bp - 10h]
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
label_022a:
    test byte ptr [bp + 10h], 8
    je label_023f
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @$bdla$qnv
    pop cx
    pop cx
    jmp short label_0247
label_023f:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    jmp short label_024b
label_0247:
    xor dx, dx
    xor ax, ax
label_024b:
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
    dw case_00e0
    dw case_00ef
    dw case_0102
    dw case_011d
    dw case_0139
    dw case_0147
    dw case_0155
    dw case_0166
    dw case_0177
    dw case_0187
    dw case_0197
    dw case_01a6
    dw case_010e
    dw case_0129
    dw case_0139
    dw case_0147
_TEXT ends
end
