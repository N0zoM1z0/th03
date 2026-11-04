; Original Japanese Borland C++ ostischr full stream buffer method.
; Real 8086 far pointer arithmetic, vtable calls and original ABI.
; No executable machine-CODE byte arrays, no patched OBJ records.
.8086
extrn @ios@setstate$qi:far,@ostream@do_opfx$qv:far,@ostream@do_osfx$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostream@$blsh$qc

; Selected original C++ far entry, 597 CODE bytes.
@ostream@$blsh$qc:
    push bp
    mov bp, sp
    sub sp, 1ch
    push si
    push di
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    cmp word ptr es:[bx + 0eh], 0
    je loc_0024
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @ostream@do_opfx$qv
    pop cx
    pop cx
    jmp short loc_0027
loc_0024:
    mov ax, 1
loc_0027:
    or ax, ax
    jne loc_002e
    jmp near ptr loc_022d
loc_002e:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov ax, word ptr es:[bx + 16h]
    mov word ptr [bp - 1ch], ax
    mov word ptr es:[bx + 16h], 0
    dec ax
    mov word ptr [bp - 1ah], ax
    test byte ptr es:[bx + 10h], 0ah
    je loc_004f
    jmp near ptr loc_00e6
loc_004f:
    jmp near ptr loc_00de
loc_0052:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov cx, word ptr es:[bx + 18h]
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 2], es
    mov word ptr [bp - 4], bx
    les bx,dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 12h]
    les bx,dword ptr [bp - 4]
    les bx,dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 16h]
    jb loc_00a5
    mov al, cl
    mov ah, 0
    push ax
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 6], es
    mov word ptr [bp - 8], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx,dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 18h]
    add sp, 6
    jmp short loc_00c4
loc_00a5:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx,dword ptr es:[bx + 2]
    mov dx, word ptr es:[bx + 14h]
    mov si, word ptr es:[bx + 12h]
    inc word ptr es:[bx + 12h]
    mov al, cl
    mov es, dx
    mov byte ptr es:[si], al
    mov ah, 0
loc_00c4:
    cmp ax, 0ffffh
    jne loc_00de
    mov ax, 4
    push ax
    les bx,dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp, 6
    jmp short loc_00e6
loc_00de:
    dec word ptr [bp - 1ah]
    jl loc_00e6
    jmp near ptr loc_0052
loc_00e6:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 0ah], 86h
    je loc_00f6
    jmp near ptr loc_017c
loc_00f6:
    mov al, byte ptr [bp + 0ah]
    cbw
    mov cx, ax
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 0ah], es
    mov word ptr [bp - 0ch], bx
    les bx,dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 12h]
    les bx,dword ptr [bp - 0ch]
    les bx,dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 16h]
    jb loc_0145
    mov al, cl
    mov ah, 0
    push ax
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 0eh], es
    mov word ptr [bp - 10h], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx,dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 18h]
    add sp, 6
    jmp short loc_0164
loc_0145:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx,dword ptr es:[bx + 2]
    mov dx, word ptr es:[bx + 14h]
    mov si, word ptr es:[bx + 12h]
    inc word ptr es:[bx + 12h]
    mov al, cl
    mov es, dx
    mov byte ptr es:[si], al
    mov ah, 0
loc_0164:
    cmp ax, 0ffffh
    jne loc_017c
    mov ax, 4
    push ax
    les bx,dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp, 6
loc_017c:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 0ah], 86h
    je loc_018c
    jmp near ptr loc_022d
loc_018c:
    test byte ptr es:[bx + 10h], 2
    jne loc_0196
    jmp near ptr loc_022d
loc_0196:
    jmp near ptr loc_0225
loc_0199:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov cx, word ptr es:[bx + 18h]
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 12h], es
    mov word ptr [bp - 14h], bx
    les bx,dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 12h]
    les bx,dword ptr [bp - 14h]
    les bx,dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 16h]
    jb loc_01ec
    mov al, cl
    mov ah, 0
    push ax
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 16h], es
    mov word ptr [bp - 18h], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx,dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 18h]
    add sp, 6
    jmp short loc_020b
loc_01ec:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx,dword ptr es:[bx + 2]
    mov dx, word ptr es:[bx + 14h]
    mov si, word ptr es:[bx + 12h]
    inc word ptr es:[bx + 12h]
    mov al, cl
    mov es, dx
    mov byte ptr es:[si], al
    mov ah, 0
loc_020b:
    cmp ax, 0ffffh
    jne loc_0225
    mov ax, 4
    push ax
    les bx,dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp, 6
    jmp short loc_022d
loc_0225:
    dec word ptr [bp - 1ah]
    jl loc_022d
    jmp near ptr loc_0199
loc_022d:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 11h], 60h
    je loc_0249
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @ostream@do_osfx$qv
    pop cx
    pop cx
    jmp short loc_0249
loc_0249:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends
end
