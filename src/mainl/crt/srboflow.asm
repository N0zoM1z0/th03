; Original Japanese Borland C++ srboflow full stream buffer method.
; Real 8086 far pointer arithmetic, vtable calls and original ABI.
; No executable machine-CODE byte arrays, no patched OBJ records.
.8086
extrn @$bnwa$qui:far,@$bdla$qnv:far,_memcpy:far
extrn @streambuf@setp$qnct1:far,@streambuf@setg$qnct1t1:far,@streambuf@setb$qnct1i:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @strstreambuf@overflow$qi

; Selected original C++ far entry, 512 CODE bytes.
@strstreambuf@overflow$qi:
    push bp
    mov bp, sp
    sub sp, 16h
    push si
    push di
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 2eh]
    and ax, 3
    cmp ax, 1
    jne loc_0056
    mov ax, word ptr es:[bx + 6]
    or ax, word ptr es:[bx + 8]
    jne loc_002d
    push word ptr [bp + 8]
    push bx
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 28h]
    pop cx
    pop cx
loc_002d:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 0eh]
    or ax, word ptr es:[bx + 10h]
    jne loc_0056
    push word ptr es:[bx + 0ch]
    push word ptr es:[bx + 0ah]
    push word ptr es:[bx + 8]
    push word ptr es:[bx + 6]
    push word ptr [bp + 8]
    push bx
    call @streambuf@setp$qnct1
    add sp, 0ch
loc_0056:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 0eh]
    or ax, word ptr es:[bx + 10h]
    jne loc_0066
    jmp near ptr loc_01f7
loc_0066:
    mov ax, word ptr es:[bx + 12h]
    cmp ax, word ptr es:[bx + 16h]
    jae loc_0073
    jmp near ptr loc_01b3
loc_0073:
    mov ax, word ptr es:[bx + 2eh]
    and ax, 3
    cmp ax, 1
    je loc_0082
    jmp near ptr loc_01b3
loc_0082:
    mov dx, word ptr es:[bx + 8]
    mov ax, word ptr es:[bx + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    mov ax, word ptr es:[bx + 0ah]
    xor dx, dx
    sub ax, word ptr es:[bx + 6]
    sbb dx, 0
    mov word ptr [bp - 6], ax
    add ax, 4
    push ax
    call @$bnwa$qui
    pop cx
    mov word ptr [bp - 8], dx
    mov word ptr [bp - 0ah], ax
    or ax, word ptr [bp - 8]
    jne loc_00b8
    jmp near ptr loc_01f7
loc_00b8:
    push word ptr [bp - 6]
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    push word ptr [bp - 8]
    push word ptr [bp - 0ah]
    call _memcpy
    add sp, 0ah
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 12h]
    xor dx, dx
    sub ax, word ptr [bp - 4]
    sbb dx, 0
    mov word ptr [bp - 12h], ax
    mov ax, word ptr es:[bx + 1eh]
    or ax, word ptr es:[bx + 20h]
    je loc_00f0
    mov ax, 1
    jmp short loc_00f2
loc_00f0:
    xor ax, ax
loc_00f2:
    mov word ptr [bp - 14h], ax
    cmp word ptr [bp - 14h], 0
    je loc_012b
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 1ah]
    xor dx, dx
    sub ax, word ptr [bp - 4]
    sbb dx, 0
    mov word ptr [bp - 0ch], ax
    mov ax, word ptr es:[bx + 1eh]
    xor dx, dx
    sub ax, word ptr [bp - 4]
    sbb dx, 0
    mov word ptr [bp - 0eh], ax
    mov ax, word ptr es:[bx + 22h]
    xor dx, dx
    sub ax, word ptr [bp - 4]
    sbb dx, 0
    mov word ptr [bp - 10h], ax
loc_012b:
    xor ax, ax
    push ax
    mov ax, word ptr [bp - 0ah]
    add ax, word ptr [bp - 6]
    add ax, 4
    push word ptr [bp - 8]
    push ax
    push word ptr [bp - 8]
    push word ptr [bp - 0ah]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @streambuf@setb$qnct1i
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 0ch]
    push word ptr es:[bx + 0ah]
    push word ptr [bp - 8]
    push word ptr [bp - 0ah]
    push word ptr [bp + 8]
    push bx
    call @streambuf@setp$qnct1
    add sp, 1ah
    mov ax, word ptr [bp - 12h]
    mov word ptr [bp - 16h], ax
    les bx,dword ptr [bp + 6]
    add word ptr es:[bx + 12h], ax
    cmp word ptr [bp - 14h], 0
    je loc_01a6
    mov ax, word ptr [bp - 0ah]
    add ax, word ptr [bp - 10h]
    push word ptr [bp - 8]
    push ax
    mov ax, word ptr [bp - 0ah]
    add ax, word ptr [bp - 0eh]
    push word ptr [bp - 8]
    push ax
    mov ax, word ptr [bp - 0ah]
    add ax, word ptr [bp - 0ch]
    push word ptr [bp - 8]
    push ax
    push word ptr [bp + 8]
    push bx
    call @streambuf@setg$qnct1t1
    add sp, 10h
loc_01a6:
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call @$bdla$qnv
    pop cx
    pop cx
loc_01b3:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 12h]
    cmp ax, word ptr es:[bx + 16h]
    jae loc_01f7
    mov cx, word ptr [bp + 0ah]
    cmp ax, word ptr es:[bx + 16h]
    jb loc_01dd
    mov al, cl
    mov ah, 0
    push ax
    push word ptr [bp + 8]
    push bx
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 18h]
    add sp, 6
    jmp short loc_01f5
loc_01dd:
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 14h]
    mov si, word ptr es:[bx + 12h]
    inc word ptr es:[bx + 12h]
    mov al, cl
    mov es, dx
    mov byte ptr es:[si], al
    mov ah, 0
loc_01f5:
    jmp short loc_01fa
loc_01f7:
    mov ax, 0ffffh
loc_01fa:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends
end
