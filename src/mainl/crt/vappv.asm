; Original Borland vector_applyv: type selectors and dynamic function
; descriptor invocation with 16-bit near/far pointer operations.
; 32 symbolic descriptor selectors and 32 relocatable handler entries.
; No original executable byte arrays or object patching.
.8086
extrn _abort:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __vector_applyv_
__vector_applyv_:
    push bp
    mov bp, sp
    sub sp, 0ch
    push si
    push di
    lea ax, [bp + 14h]
    mov word ptr [bp - 2], ss
    mov word ptr [bp - 4], ax
    test byte ptr [bp + 12h], 1
    je loc_002e
    add word ptr [bp - 4], 4
    les bx,dword ptr [bp - 4]
    mov dx, word ptr es:[bx - 2]
    mov ax, word ptr es:[bx - 4]
    mov word ptr [bp - 8], dx
    mov word ptr [bp - 0ah], ax
    jmp short loc_003c
loc_002e:
    add word ptr [bp - 4], 2
    les bx,dword ptr [bp - 4]
    mov ax, word ptr es:[bx - 2]
    mov word ptr [bp - 6], ax
loc_003c:
    test byte ptr [bp + 12h], 80h
    je loc_0047
    and word ptr [bp + 12h], 0feffh
loc_0047:
    mov ax, word ptr [bp + 12h]
    mov word ptr [bp - 0ch], ax
    mov cx, 20h
    mov bx,offset cs:vector_selector_words
loc_0053:
    mov ax, word ptr cs:[bx]
    cmp ax, word ptr [bp - 0ch]
    je loc_0063
    add bx, 2
    loop loc_0053
    jmp near ptr loc_02af
loc_0063:
    jmp word ptr cs:[bx + 40h]

; Entry for the original vector-descriptor selector.
op_0067:
    push word ptr [bp + 0ah]
    xor ax, ax
    push ax
    push word ptr [bp + 6]
    call word ptr word ptr [bp - 6]
    add sp, 6
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_0079:
    push word ptr [bp + 0ah]
    xor ax, ax
    push ax
    push word ptr [bp + 6]
    call dword ptr [bp - 0ah]
    add sp, 6
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_008b:
    push word ptr [bp + 6]
    xor ax, ax
    push ax
    push word ptr [bp + 0ah]
    call word ptr word ptr [bp - 6]
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_009a:
    xor ax, ax
    push ax
    push word ptr [bp + 0ah]
    push word ptr [bp + 6]
    call word ptr word ptr [bp - 6]
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_00a9:
    push word ptr [bp + 6]
    xor ax, ax
    push ax
    push word ptr [bp + 0ah]
    call dword ptr [bp - 0ah]
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_00b8:
    xor ax, ax
    push ax
    push word ptr [bp + 0ah]
    push word ptr [bp + 6]
    call dword ptr [bp - 0ah]
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_00c7:
    mov dx, word ptr [bp + 0ah]
    xor ax, ax
    mov bx, word ptr [bp + 6]
    push bx
    pop bx
    call word ptr word ptr [bp - 6]
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_00d7:
    mov dx, word ptr [bp + 6]
    mov bx, word ptr [bp + 0ah]
    xor ax, ax
    push bx
    pop bx
    call word ptr word ptr [bp - 6]
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_00e7:
    mov dx, word ptr [bp + 0ah]
    xor ax, ax
    mov bx, word ptr [bp + 6]
    push bx
    pop bx
    call dword ptr [bp - 0ah]
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_00f7:
    mov dx, word ptr [bp + 6]
    mov bx, word ptr [bp + 0ah]
    xor ax, ax
    push bx
    pop bx
    call dword ptr [bp - 0ah]
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_0107:
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    xor ax, ax
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call word ptr word ptr [bp - 6]
    jmp short loc_012d

; Entry for the original vector-descriptor selector.
op_011b:
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    xor ax, ax
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call dword ptr [bp - 0ah]
loc_012d:
    add sp, 0ah
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_0133:
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    xor ax, ax
    push ax
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    jmp short loc_0153

; Entry for the original vector-descriptor selector.
op_0144:
    xor ax, ax
    push ax
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
loc_0153:
    call word ptr word ptr [bp - 6]
    jmp short loc_017b

; Entry for the original vector-descriptor selector.
op_0158:
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    xor ax, ax
    push ax
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    jmp short loc_0178

; Entry for the original vector-descriptor selector.
op_0169:
    xor ax, ax
    push ax
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
loc_0178:
    call dword ptr [bp - 0ah]
loc_017b:
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_017e:
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    jmp short loc_0198

; Entry for the original vector-descriptor selector.
op_018c:
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
loc_0198:
    xor ax, ax
    call word ptr word ptr [bp - 6]
    jmp short loc_01be

; Entry for the original vector-descriptor selector.
op_019f:
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    jmp short loc_01b9

; Entry for the original vector-descriptor selector.
op_01ad:
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
loc_01b9:
    xor ax, ax
    call dword ptr [bp - 0ah]
loc_01be:
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_01c1:
    push si
    mov si, word ptr [bp + 6]
    push word ptr [bp + 0ah]
    xor ax, ax
    push ax
    call word ptr word ptr [bp - 6]
    pop cx
    pop cx
    pop si
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_01d4:
    push si
    mov si, word ptr [bp + 6]
    push word ptr [bp + 0ah]
    xor ax, ax
    push ax
    call dword ptr [bp - 0ah]
    pop cx
    pop cx
    pop si
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_01e7:
    push si
    mov si, word ptr [bp + 6]
    xor ax, ax
    push ax
    push word ptr [bp + 0ah]
    call word ptr word ptr [bp - 6]
    pop si
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_01f8:
    push si
    mov si, word ptr [bp + 6]
    xor ax, ax
    push ax
    push word ptr [bp + 0ah]
    call dword ptr [bp - 0ah]
    pop si
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_0209:
    push si
    mov si, word ptr [bp + 6]
    mov bx, word ptr [bp + 0ah]
    xor ax, ax
    push bx
    pop bx
    call word ptr word ptr [bp - 6]
    pop si
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_021b:
    push si
    mov si, word ptr [bp + 6]
    mov bx, word ptr [bp + 0ah]
    xor ax, ax
    push bx
    pop bx
    call dword ptr [bp - 0ah]
    pop si
    jmp near ptr loc_02b4

; Entry for the original vector-descriptor selector.
op_022d:
    push ds
    push si
    lds si,dword ptr [bp + 6]
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    xor ax, ax
    push ax
    call word ptr word ptr [bp - 6]
    add sp, 6
    pop si
    pop ds
    jmp short loc_02b4

; Entry for the original vector-descriptor selector.
op_0245:
    push ds
    push si
    lds si,dword ptr [bp + 6]
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    xor ax, ax
    push ax
    call dword ptr [bp - 0ah]
    add sp, 6
    pop si
    pop ds
    jmp short loc_02b4

; Entry for the original vector-descriptor selector.
op_025d:
    push ds
    push si
    lds si,dword ptr [bp + 6]
    xor ax, ax
    push ax
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    call word ptr word ptr [bp - 6]
    pop si
    pop ds
    jmp short loc_02b4

; Entry for the original vector-descriptor selector.
op_0272:
    push ds
    push si
    lds si,dword ptr [bp + 6]
    xor ax, ax
    push ax
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    call dword ptr [bp - 0ah]
    pop si
    pop ds
    jmp short loc_02b4

; Entry for the original vector-descriptor selector.
op_0287:
    push ds
    push si
    lds si,dword ptr [bp + 6]
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    xor ax, ax
    call word ptr word ptr [bp - 6]
    pop si
    pop ds
    jmp short loc_02b4

; Entry for the original vector-descriptor selector.
op_029b:
    push ds
    push si
    lds si,dword ptr [bp + 6]
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    xor ax, ax
    call dword ptr [bp - 0ah]
    pop si
    pop ds
    jmp short loc_02b4
loc_02af:
    call _abort
loc_02b4:
    mov ax, word ptr [bp + 0eh]
    add word ptr [bp + 6], ax
    add word ptr [bp + 0ah], ax
    dec word ptr [bp + 10h]
    mov ax, word ptr [bp + 10h]
    or ax, ax
    jbe loc_02ca
    jmp near ptr loc_0047
loc_02ca:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original 32 distinct type selectors and word-offset handler table.
vector_selector_words label word
    dw 0
    dw 1
    dw 2
    dw 3
    dw 4
    dw 5
    dw 6
    dw 7
    dw 32
    dw 33
    dw 36
    dw 37
    dw 128
    dw 129
    dw 130
    dw 131
    dw 132
    dw 133
    dw 134
    dw 135
    dw 160
    dw 161
    dw 164
    dw 165
    dw 258
    dw 259
    dw 262
    dw 263
    dw 288
    dw 289
    dw 292
    dw 293
vector_handler_words label word
    dw op_0067
    dw op_0079
    dw op_008b
    dw op_00a9
    dw op_0107
    dw op_011b
    dw op_0133
    dw op_0158
    dw op_00c7
    dw op_00e7
    dw op_017e
    dw op_019f
    dw op_01c1
    dw op_01d4
    dw op_01e7
    dw op_01f8
    dw op_022d
    dw op_0245
    dw op_025d
    dw op_0272
    dw op_0209
    dw op_021b
    dw op_0287
    dw op_029b
    dw op_009a
    dw op_00b8
    dw op_0144
    dw op_0169
    dw op_00d7
    dw op_00f7
    dw op_018c
    dw op_01ad
_TEXT ends
end
