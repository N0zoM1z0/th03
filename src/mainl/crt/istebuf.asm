; Original Japanese Borland istebuf complete streambuf or istream method.
; Real symbolic 8086 far C++ ABI, virtual calls and buffer controls.
; No original executable machine CODE initializer or OBJ patches.
.8086
extrn @ios@setstate$qi:far,@istream@ipfx$qi:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @istream@$brsh$qn9streambuf

@istream@$brsh$qn9streambuf:
    push bp
    mov bp, sp
    sub sp, 14h
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
    jmp near ptr native_015d

native_0020:
    mov word ptr [bp - 2], 1
    jmp near ptr native_00c7

native_0028:
    mov cx, word ptr [bp - 14h]
    les bx,dword ptr [bp + 0ah]
    mov ax, word ptr es:[bx + 12h]
    cmp ax, word ptr es:[bx + 16h]
    jb native_004c
    mov al, cl
    mov ah, 0
    push ax
    push word ptr [bp + 0ch]
    push bx
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 18h]
    add sp, 6
    jmp short native_0064

native_004c:
    les bx,dword ptr [bp + 0ah]
    mov dx, word ptr es:[bx + 14h]
    mov si, word ptr es:[bx + 12h]
    inc word ptr es:[bx + 12h]
    mov al, cl
    mov es, dx
    mov byte ptr es:[si], al
    mov ah, 0

native_0064:
    cmp ax, 0ffffh
    jne native_0071
    mov word ptr [bp - 2], 2
    jmp near ptr native_0128

native_0071:
    mov word ptr [bp - 2], 0
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 4], es
    mov word ptr [bp - 6], bx
    les bx,dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 1eh]
    les bx,dword ptr [bp - 6]
    les bx,dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 22h]
    jb native_00b9
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 8], es
    mov word ptr [bp - 0ah], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx,dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 0ch]
    pop cx
    pop cx
    jmp short native_00c7

native_00b9:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx,dword ptr es:[bx + 2]
    inc word ptr es:[bx + 1eh]

native_00c7:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 0ch], es
    mov word ptr [bp - 0eh], bx
    les bx,dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 1eh]
    les bx,dword ptr [bp - 0eh]
    les bx,dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 22h]
    jb native_010a
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 10h], es
    mov word ptr [bp - 12h], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx,dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 0ch]
    pop cx
    pop cx
    jmp short native_011d

native_010a:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx,dword ptr es:[bx + 2]
    les bx,dword ptr es:[bx + 1eh]
    mov al, byte ptr es:[bx]
    mov ah, 0

native_011d:
    mov word ptr [bp - 14h], ax
    cmp ax, 0ffffh
    je native_0128
    jmp near ptr native_0028

native_0128:
    cmp word ptr [bp - 2], 0
    jne native_0132
    xor ax, ax
    jmp short native_0135

native_0132:
    mov ax, 2

native_0135:
    mov dx, ax
    cmp word ptr [bp - 14h], -1
    jne native_0149
    or dx, 1
    cmp word ptr [bp - 2], 1
    jne native_0149
    or dx, 4

native_0149:
    or dx, dx
    je native_015d
    push dx
    les bx,dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp, 6

native_015d:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends
end
