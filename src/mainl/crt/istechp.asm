; Original Japanese Borland istechp complete streambuf or istream method.
; Real symbolic 8086 far C++ ABI, virtual calls and buffer controls.
; No original executable machine CODE initializer or OBJ patches.
.8086
extrn @ios@setstate$qi:far,@istream@ipfx$qi:far,__ctype:byte
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @istream@$brsh$qnc

@istream@$brsh$qnc:
    push bp
    mov bp, sp
    sub sp, 1ah
    push si
    push di
    xor ax, ax
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @istream@ipfx$qi
    add sp, 6
    or ax, ax
    jne native_0020
    jmp near ptr native_0150

native_0020:
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 12h], dx
    mov word ptr [bp - 14h], ax
    mov word ptr [bp - 16h], 0
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov ax, word ptr es:[bx + 16h]
    mov word ptr [bp - 1ah], ax
    mov word ptr es:[bx + 16h], 0
    mov word ptr [bp - 18h], ax
    jmp short native_00a6

native_0049:
    les bx,dword ptr [bp + 0ah]
    mov al, byte ptr [bp - 16h]
    mov byte ptr es:[bx], al
    inc word ptr [bp + 0ah]
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 2], es
    mov word ptr [bp - 4], bx
    les bx,dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 1eh]
    les bx,dword ptr [bp - 4]
    les bx,dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 22h]
    jb native_0098
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 6], es
    mov word ptr [bp - 8], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx,dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 0ch]
    pop cx
    pop cx
    jmp short native_00a6

native_0098:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx,dword ptr es:[bx + 2]
    inc word ptr es:[bx + 1eh]

native_00a6:
    dec word ptr [bp - 18h]
    je native_0122
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 0ah], es
    mov word ptr [bp - 0ch], bx
    les bx,dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 1eh]
    les bx,dword ptr [bp - 0ch]
    les bx,dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 22h]
    jb native_00ee
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 0eh], es
    mov word ptr [bp - 10h], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx,dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 0ch]
    pop cx
    pop cx
    jmp short native_0101

native_00ee:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx,dword ptr es:[bx + 2]
    les bx,dword ptr es:[bx + 1eh]
    mov al, byte ptr es:[bx]
    mov ah, 0

native_0101:
    mov word ptr [bp - 16h], ax
    mov bx, word ptr [bp - 16h]
    mov al, byte ptr DGROUP:__ctype[bx+1]
    mov ah, 0
    and ax, 1
    neg ax
    sbb ax, ax
    inc ax
    or ax, ax
    je native_0122
    cmp word ptr [bp - 16h], -1
    je native_0122
    jmp near ptr native_0049

native_0122:
    cmp word ptr [bp - 16h], -1
    jne native_0150
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
    cmp dx, word ptr [bp - 12h]
    jne native_013d
    cmp ax, word ptr [bp - 14h]
    jne native_013d
    mov ax, 3
    jmp short native_0140

native_013d:
    mov ax, 1

native_0140:
    push ax
    les bx,dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp, 6

native_0150:
    les bx,dword ptr [bp + 0ah]
    mov byte ptr es:[bx], 0
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends
end
