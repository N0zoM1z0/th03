; Original Japanese Borland istgbuf complete streambuf or istream method.
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
public @istream@get$qm9streambufc

@istream@get$qm9streambufc:
    push bp
    mov bp, sp
    sub sp, 14h
    push si
    push di
    mov ax, 1
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @istream@ipfx$qi
    add sp, 6
    or ax, ax
    jne native_0021
    jmp near ptr native_0165

native_0021:
    mov word ptr [bp - 14h], 0
    jmp near ptr native_00c7

native_0029:
    mov cx, word ptr [bp - 12h]
    les bx,dword ptr [bp + 0ah]
    mov ax, word ptr es:[bx + 12h]
    cmp ax, word ptr es:[bx + 16h]
    jb native_004d
    mov al, cl
    mov ah, 0
    push ax
    push word ptr [bp + 0ch]
    push bx
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 18h]
    add sp, 6
    jmp short native_0065

native_004d:
    les bx,dword ptr [bp + 0ah]
    mov dx, word ptr es:[bx + 14h]
    mov si, word ptr es:[bx + 12h]
    inc word ptr es:[bx + 12h]
    mov al, cl
    mov es, dx
    mov byte ptr es:[si], al
    mov ah, 0

native_0065:
    cmp ax, 0ffffh
    jne native_0072
    mov word ptr [bp - 14h], 1
    jmp near ptr native_0133

native_0072:
    les bx,dword ptr [bp + 6]
    inc word ptr es:[bx + 4]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 2], es
    mov word ptr [bp - 4], bx
    les bx,dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 1eh]
    les bx,dword ptr [bp - 4]
    les bx,dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 22h]
    jb native_00b9
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
    jmp short native_00c7

native_00b9:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx,dword ptr es:[bx + 2]
    inc word ptr es:[bx + 1eh]

native_00c7:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 0ah], es
    mov word ptr [bp - 0ch], bx
    les bx,dword ptr es:[bx + 2]
    mov ax, word ptr es:[bx + 1eh]
    les bx,dword ptr [bp - 0ch]
    les bx,dword ptr es:[bx + 2]
    cmp ax, word ptr es:[bx + 22h]
    jb native_010a
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
    jmp short native_011d

native_010a:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx,dword ptr es:[bx + 2]
    les bx,dword ptr es:[bx + 1eh]
    mov al, byte ptr es:[bx]
    mov ah, 0

native_011d:
    mov word ptr [bp - 12h], ax
    push ax
    mov al, byte ptr [bp + 0eh]
    cbw
    pop dx
    cmp dx, ax
    je native_0133
    cmp word ptr [bp - 12h], -1
    je native_0133
    jmp near ptr native_0029

native_0133:
    cmp word ptr [bp - 12h], -1
    jne native_014c
    mov ax, 1
    push ax
    les bx,dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp, 6

native_014c:
    cmp word ptr [bp - 14h], 0
    je native_0165
    mov ax, 2
    push ax
    les bx,dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp, 6

native_0165:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends
end
