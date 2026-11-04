; Original Borland vector_apply: type selectors and dynamic function
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
public __vector_apply_
__vector_apply_:
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
    jmp near ptr loc_0201
loc_0063:
    jmp word ptr cs:[bx + 40h]

; Entry for the original vector-descriptor selector.
op_0067:
    push word ptr [bp + 0ah]
    push word ptr [bp + 6]
    call word ptr word ptr [bp - 6]
    jmp short loc_007b

; Entry for the original vector-descriptor selector.
op_0072:
    push word ptr [bp + 0ah]
    push word ptr [bp + 6]
    call dword ptr [bp - 0ah]
loc_007b:
    pop cx
    pop cx
    jmp near ptr loc_0206

; Entry for the original vector-descriptor selector.
op_0080:
    push word ptr [bp + 6]
    push word ptr [bp + 0ah]
    jmp short loc_008e

; Entry for the original vector-descriptor selector.
op_0088:
    push word ptr [bp + 0ah]
    push word ptr [bp + 6]
loc_008e:
    call word ptr word ptr [bp - 6]
    jmp short loc_00a4

; Entry for the original vector-descriptor selector.
op_0093:
    push word ptr [bp + 6]
    push word ptr [bp + 0ah]
    jmp short loc_00a1

; Entry for the original vector-descriptor selector.
op_009b:
    push word ptr [bp + 0ah]
    push word ptr [bp + 6]
loc_00a1:
    call dword ptr [bp - 0ah]
loc_00a4:
    jmp near ptr loc_0206

; Entry for the original vector-descriptor selector.
op_00a7:
    mov ax, word ptr [bp + 0ah]
    mov bx, word ptr [bp + 6]
    jmp short loc_00b5

; Entry for the original vector-descriptor selector.
op_00af:
    mov ax, word ptr [bp + 6]
    mov bx, word ptr [bp + 0ah]
loc_00b5:
    push bx
    pop bx
    call word ptr word ptr [bp - 6]
    jmp near ptr loc_0206

; Entry for the original vector-descriptor selector.
op_00bd:
    mov ax, word ptr [bp + 0ah]
    mov bx, word ptr [bp + 6]
    jmp short loc_00cb

; Entry for the original vector-descriptor selector.
op_00c5:
    mov ax, word ptr [bp + 6]
    mov bx, word ptr [bp + 0ah]
loc_00cb:
    push bx
    pop bx
    call dword ptr [bp - 0ah]
    jmp near ptr loc_0206

; Entry for the original vector-descriptor selector.
op_00d3:
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call word ptr word ptr [bp - 6]
    jmp short loc_00f3

; Entry for the original vector-descriptor selector.
op_00e4:
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call dword ptr [bp - 0ah]
loc_00f3:
    add sp, 8
    jmp near ptr loc_0206

; Entry for the original vector-descriptor selector.
op_00f9:
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    jmp short loc_0113

; Entry for the original vector-descriptor selector.
op_0107:
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
loc_0113:
    call word ptr word ptr [bp - 6]
    jmp short loc_0135

; Entry for the original vector-descriptor selector.
op_0118:
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    jmp short loc_0132

; Entry for the original vector-descriptor selector.
op_0126:
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
loc_0132:
    call dword ptr [bp - 0ah]
loc_0135:
    jmp near ptr loc_0206

; Entry for the original vector-descriptor selector.
op_0138:
    push si
    mov si, word ptr [bp + 6]
    push word ptr [bp + 0ah]
    call word ptr word ptr [bp - 6]
    pop cx
    pop si
    jmp near ptr loc_0206

; Entry for the original vector-descriptor selector.
op_0147:
    push si
    mov si, word ptr [bp + 6]
    push word ptr [bp + 0ah]
    call dword ptr [bp - 0ah]
    pop cx
    pop si
    jmp near ptr loc_0206

; Entry for the original vector-descriptor selector.
op_0156:
    push si
    mov si, word ptr [bp + 6]
    push word ptr [bp + 0ah]
    call word ptr word ptr [bp - 6]
    pop si
    jmp near ptr loc_0206

; Entry for the original vector-descriptor selector.
op_0164:
    push si
    mov si, word ptr [bp + 6]
    push word ptr [bp + 0ah]
    call dword ptr [bp - 0ah]
    pop si
    jmp near ptr loc_0206

; Entry for the original vector-descriptor selector.
op_0172:
    push si
    mov si, word ptr [bp + 6]
    mov bx, word ptr [bp + 0ah]
    push bx
    pop bx
    call word ptr word ptr [bp - 6]
    pop si
    jmp near ptr loc_0206

; Entry for the original vector-descriptor selector.
op_0182:
    push si
    mov si, word ptr [bp + 6]
    mov bx, word ptr [bp + 0ah]
    push bx
    pop bx
    call dword ptr [bp - 0ah]
    pop si
    jmp short loc_0206

; Entry for the original vector-descriptor selector.
op_0191:
    push ds
    push si
    lds si,dword ptr [bp + 6]
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    call word ptr word ptr [bp - 6]
    pop cx
    pop cx
    pop si
    pop ds
    jmp short loc_0206

; Entry for the original vector-descriptor selector.
op_01a5:
    push ds
    push si
    lds si,dword ptr [bp + 6]
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    call dword ptr [bp - 0ah]
    pop cx
    pop cx
    pop si
    pop ds
    jmp short loc_0206

; Entry for the original vector-descriptor selector.
op_01b9:
    push ds
    push si
    lds si,dword ptr [bp + 6]
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    call word ptr word ptr [bp - 6]
    pop si
    pop ds
    jmp short loc_0206

; Entry for the original vector-descriptor selector.
op_01cb:
    push ds
    push si
    lds si,dword ptr [bp + 6]
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    call dword ptr [bp - 0ah]
    pop si
    pop ds
    jmp short loc_0206

; Entry for the original vector-descriptor selector.
op_01dd:
    push ds
    push si
    lds si,dword ptr [bp + 6]
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    call word ptr word ptr [bp - 6]
    pop si
    pop ds
    jmp short loc_0206

; Entry for the original vector-descriptor selector.
op_01ef:
    push ds
    push si
    lds si,dword ptr [bp + 6]
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    call dword ptr [bp - 0ah]
    pop si
    pop ds
    jmp short loc_0206
loc_0201:
    call _abort
loc_0206:
    mov ax, word ptr [bp + 0eh]
    add word ptr [bp + 6], ax
    add word ptr [bp + 0ah], ax
    dec word ptr [bp + 10h]
    mov ax, word ptr [bp + 10h]
    or ax, ax
    jbe loc_021c
    jmp near ptr loc_0047
loc_021c:
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
    dw op_0072
    dw op_0080
    dw op_0093
    dw op_00d3
    dw op_00e4
    dw op_00f9
    dw op_0118
    dw op_00a7
    dw op_00bd
    dw op_00f9
    dw op_0118
    dw op_0138
    dw op_0147
    dw op_0156
    dw op_0164
    dw op_0191
    dw op_01a5
    dw op_01b9
    dw op_01cb
    dw op_0172
    dw op_0182
    dw op_01dd
    dw op_01ef
    dw op_0088
    dw op_009b
    dw op_0107
    dw op_0126
    dw op_00af
    dw op_00c5
    dw op_0107
    dw op_0126
_TEXT ends
end
