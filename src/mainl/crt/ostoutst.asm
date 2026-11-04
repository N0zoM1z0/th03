; Original Japanese Borland ostream::outstr, full far C++ routine.
; Handles stream sentry, padding and output-state propagation.
; Symbolic 8086 instructions and exact original stream ABI.
.8086
extrn @ios@setstate$qi:far,@streambuf@sputn$qnxci:far
extrn @ostream@do_opfx$qv:far,@ostream@do_osfx$qv:far,_strlen:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostream@outstr$qnxct1

@ostream@outstr$qnxct1:
    push bp
    mov bp, sp
    sub sp, 20h
    push si
    push di
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    cmp word ptr es:[bx + 0eh], 0
    je outstr_0024
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @ostream@do_opfx$qv
    pop cx
    pop cx
    jmp short outstr_0027

outstr_0024:
    mov ax, 1

outstr_0027:
    or ax, ax
    jne outstr_002e
    jmp near ptr outstr_030d

outstr_002e:
    mov ax, word ptr [bp + 0eh]
    or ax, word ptr [bp + 10h]
    je outstr_0045
    push word ptr [bp + 10h]
    push word ptr [bp + 0eh]
    call _strlen
    pop cx
    pop cx
    jmp short outstr_0047

outstr_0045:
    xor ax, ax

outstr_0047:
    mov word ptr [bp - 1ah], ax
    mov ax, word ptr [bp + 0ah]
    or ax, word ptr [bp + 0ch]
    je outstr_0061
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    call _strlen
    pop cx
    pop cx
    jmp short outstr_0063

outstr_0061:
    xor ax, ax

outstr_0063:
    mov word ptr [bp - 1ch], ax
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov ax, word ptr es:[bx + 16h]
    mov word ptr [bp - 20h], ax
    mov word ptr es:[bx + 16h], 0
    sub ax, word ptr [bp - 1ah]
    sub ax, word ptr [bp - 1ch]
    mov word ptr [bp - 1eh], ax
    test byte ptr es:[bx + 10h], 0ah
    je outstr_008c
    jmp near ptr outstr_0123

outstr_008c:
    jmp near ptr outstr_011b

outstr_008f:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov cx, word ptr es:[bx + 18h]
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 2], es
    mov word ptr [bp - 4], bx
    les bx, dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 12h]
    les bx, dword ptr [bp - 4]
    les bx, dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 16h]
    jb outstr_00e2
    mov al, cl
    mov ah, 0
    push ax
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 6], es
    mov word ptr [bp - 8], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 18h]
    add sp, 6
    jmp short outstr_0101

outstr_00e2:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    mov dx, word ptr es:[bx + 14h]
    mov si, word ptr es:[bx + 12h]
    inc word ptr es:[bx + 12h]
    mov al, cl
    mov es, dx
    mov byte ptr es:[si], al
    mov ah, 0

outstr_0101:
    cmp ax, 0ffffh
    jne outstr_011b
    mov ax, 4
    push ax
    les bx, dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp, 6
    jmp short outstr_0123

outstr_011b:
    dec word ptr [bp - 1eh]
    jl outstr_0123
    jmp near ptr outstr_008f

outstr_0123:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 0ah], 86h
    jne outstr_0167
    cmp word ptr [bp - 1ah], 0
    je outstr_0167
    push word ptr [bp - 1ah]
    push word ptr [bp + 10h]
    push word ptr [bp + 0eh]
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    call @streambuf@sputn$qnxci
    add sp, 0ah
    cmp ax, word ptr [bp - 1ah]
    je outstr_0167
    mov ax, 4
    push ax
    les bx, dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp, 6

outstr_0167:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 0ah], 86h
    je outstr_0177
    jmp near ptr outstr_0218

outstr_0177:
    test byte ptr es:[bx + 10h], 8
    jne outstr_0181
    jmp near ptr outstr_0218

outstr_0181:
    jmp near ptr outstr_0210

outstr_0184:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov cx, word ptr es:[bx + 18h]
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 0ah], es
    mov word ptr [bp - 0ch], bx
    les bx, dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 12h]
    les bx, dword ptr [bp - 0ch]
    les bx, dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 16h]
    jb outstr_01d7
    mov al, cl
    mov ah, 0
    push ax
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 0eh], es
    mov word ptr [bp - 10h], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 18h]
    add sp, 6
    jmp short outstr_01f6

outstr_01d7:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    mov dx, word ptr es:[bx + 14h]
    mov si, word ptr es:[bx + 12h]
    inc word ptr es:[bx + 12h]
    mov al, cl
    mov es, dx
    mov byte ptr es:[si], al
    mov ah, 0

outstr_01f6:
    cmp ax, 0ffffh
    jne outstr_0210
    mov ax, 4
    push ax
    les bx, dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp, 6
    jmp short outstr_0218

outstr_0210:
    dec word ptr [bp - 1eh]
    jl outstr_0218
    jmp near ptr outstr_0184

outstr_0218:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 0ah], 86h
    jne outstr_025c
    cmp word ptr [bp - 1ch], 0
    je outstr_025c
    push word ptr [bp - 1ch]
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    call @streambuf@sputn$qnxci
    add sp, 0ah
    cmp ax, word ptr [bp - 1ch]
    je outstr_025c
    mov ax, 4
    push ax
    les bx, dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp, 6

outstr_025c:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 0ah], 86h
    je outstr_026c
    jmp near ptr outstr_030d

outstr_026c:
    test byte ptr es:[bx + 10h], 2
    jne outstr_0276
    jmp near ptr outstr_030d

outstr_0276:
    jmp near ptr outstr_0305

outstr_0279:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov cx, word ptr es:[bx + 18h]
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 12h], es
    mov word ptr [bp - 14h], bx
    les bx, dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 12h]
    les bx, dword ptr [bp - 14h]
    les bx, dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 16h]
    jb outstr_02cc
    mov al, cl
    mov ah, 0
    push ax
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 16h], es
    mov word ptr [bp - 18h], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 18h]
    add sp, 6
    jmp short outstr_02eb

outstr_02cc:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    mov dx, word ptr es:[bx + 14h]
    mov si, word ptr es:[bx + 12h]
    inc word ptr es:[bx + 12h]
    mov al, cl
    mov es, dx
    mov byte ptr es:[si], al
    mov ah, 0

outstr_02eb:
    cmp ax, 0ffffh
    jne outstr_0305
    mov ax, 4
    push ax
    les bx, dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp, 6
    jmp short outstr_030d

outstr_0305:
    dec word ptr [bp - 1eh]
    jl outstr_030d
    jmp near ptr outstr_0279

outstr_030d:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 11h], 60h
    je outstr_0329
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @ostream@do_osfx$qv
    pop cx
    pop cx
    jmp short outstr_0329

outstr_0329:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends
end
