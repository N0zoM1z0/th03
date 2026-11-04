; Original Japanese Borland fsbskoff complete streambuf or istream method.
; Real symbolic 8086 far C++ ABI, virtual calls and buffer controls.
; No original executable machine CODE initializer or OBJ patches.
.8086
extrn _lseek:far,_write:far,@streambuf@setp$qnct1:far
extrn @streambuf@setg$qnct1t1:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @filebuf@seekoff$ql12ios@seek_diri

@filebuf@seekoff$ql12ios@seek_diri:
    push bp
    mov bp, sp
    sub sp, 12h
    push si
    push di
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 12h]
    or ax, word ptr es:[bx + 14h]
    je native_0030
    mov ax, word ptr es:[bx + 12h]
    xor dx, dx
    sub ax, word ptr es:[bx + 0eh]
    sbb dx, 0
    jmp short native_0032

native_0030:
    xor ax, ax

native_0032:
    mov word ptr [bp - 6], ax
    cmp word ptr [bp - 6], 0
    je native_0061
    push ax
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 10h]
    push word ptr es:[bx + 0eh]
    push word ptr es:[bx + 26h]
    call _write
    add sp, 8
    cmp ax, word ptr [bp - 6]
    je native_00d5
    mov dx, 0ffffh
    mov ax, 0ffffh
    jmp near ptr native_01ac

native_0061:
    cmp word ptr [bp + 0eh], 1
    jne native_00d5
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 22h]
    cmp ax, word ptr es:[bx + 1eh]
    jbe native_007f
    xor dx, dx
    sub ax, word ptr es:[bx + 1eh]
    sbb dx, 0
    jmp short native_0081

native_007f:
    xor ax, ax

native_0081:
    mov word ptr [bp - 6], ax
    or ax, ax
    je native_00d5
    cwd
    sub word ptr [bp - 4], ax
    sbb word ptr [bp - 2], dx
    les bx,dword ptr [bp + 6]
    test byte ptr es:[bx + 28h], 80h
    jne native_00d5
    mov dx, word ptr es:[bx + 20h]
    mov ax, word ptr es:[bx + 1eh]
    mov word ptr [bp - 0eh], dx
    mov word ptr [bp - 10h], ax
    jmp short native_00c0

native_00a9:
    les bx,dword ptr [bp - 10h]
    inc word ptr [bp - 10h]
    mov al, byte ptr es:[bx]
    cbw
    cmp ax, 0ah
    jne native_00c0
    sub word ptr [bp - 4], 1
    sbb word ptr [bp - 2], 0

native_00c0:
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 24h]
    mov ax, word ptr es:[bx + 22h]
    cmp dx, word ptr [bp - 0eh]
    jne native_00a9
    cmp ax, word ptr [bp - 10h]
    jne native_00a9

native_00d5:
    cmp word ptr [bp + 0eh], 0
    jne native_00df
    xor ax, ax
    jmp short native_00ed

native_00df:
    cmp word ptr [bp + 0eh], 1
    jne native_00ea
    mov ax, 1
    jmp short native_00ed

native_00ea:
    mov ax, 2

native_00ed:
    mov word ptr [bp - 8], ax
    push ax
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 26h]
    call _lseek
    add sp, 8
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2eh], dx
    mov word ptr es:[bx + 2ch], ax
    cmp word ptr es:[bx + 4], 0
    jne native_0188
    mov ax, word ptr es:[bx + 6]
    or ax, word ptr es:[bx + 8]
    je native_0188
    mov ax, word ptr es:[bx + 0ah]
    xor dx, dx
    sub ax, word ptr es:[bx + 6]
    sbb dx, 0
    cmp ax, 8
    jle native_0139
    mov ax, 4
    jmp short native_013c

native_0139:
    mov ax, 1

native_013c:
    mov word ptr [bp - 0eh], ax
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 8]
    mov ax, word ptr es:[bx + 6]
    mov word ptr [bp - 10h], dx
    mov word ptr [bp - 12h], ax
    add ax, word ptr [bp - 0eh]
    mov word ptr [bp - 0ah], ax
    push dx
    push ax
    push dx
    push ax
    push word ptr [bp + 8]
    push bx
    call @streambuf@setp$qnct1
    mov ax, word ptr [bp - 12h]
    add ax, word ptr [bp - 0eh]
    mov word ptr [bp - 0ch], ax
    push word ptr [bp - 10h]
    push ax
    push word ptr [bp - 10h]
    push ax
    push word ptr [bp - 10h]
    push word ptr [bp - 12h]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @streambuf@setg$qnct1t1
    add sp, 1ch

native_0188:
    les bx,dword ptr [bp + 6]
    cmp word ptr es:[bx + 2eh], -1
    jne native_01a1
    cmp word ptr es:[bx + 2ch], -1
    jne native_01a1
    mov dx, 0ffffh
    mov ax, 0ffffh
    jmp short native_01ac

native_01a1:
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 2eh]
    mov ax, word ptr es:[bx + 2ch]

native_01ac:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends
end
