; Original Japanese Borland sdbsync complete streambuf or istream method.
; Real symbolic 8086 far C++ ABI, virtual calls and buffer controls.
; No original executable machine CODE initializer or OBJ patches.
.8086
extrn @streambuf@setp$qnct1:far,@streambuf@setg$qnct1t1:far,_fseek:far
extrn _ungetc:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @stdiobuf@sync$qv

@stdiobuf@sync$qv:
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 12h]
    or ax, word ptr es:[bx + 14h]
    je native_0024
    mov ax, word ptr es:[bx + 12h]
    xor dx, dx
    sub ax, word ptr es:[bx + 0eh]
    sbb dx, 0
    jmp short native_0026

native_0024:
    xor ax, ax

native_0026:
    or ax, ax
    je native_004e
    mov ax, 0ffffh
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 18h]
    add sp, 6
    cmp ax, 0ffffh
    je native_0048
    jmp near ptr native_00e8

native_0048:
    mov ax, 0ffffh
    jmp near ptr native_0118

native_004e:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 22h]
    cmp ax, word ptr es:[bx + 1eh]
    jbe native_0066
    xor dx, dx
    sub ax, word ptr es:[bx + 1eh]
    sbb dx, 0
    jmp short native_0068

native_0066:
    xor ax, ax

native_0068:
    mov word ptr [bp - 2], ax
    or ax, ax
    jle native_00e8
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 24h]
    mov ax, word ptr es:[bx + 22h]
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax

native_0080:
    dec word ptr [bp - 6]
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 28h]
    push word ptr es:[bx + 26h]
    les bx,dword ptr [bp - 6]
    mov al, byte ptr es:[bx]
    cbw
    push ax
    call _ungetc
    add sp, 6
    dec word ptr [bp - 2]
    cmp word ptr [bp - 2], 0
    jne native_0080
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 24h]
    mov ax, word ptr es:[bx + 22h]
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax
    push dx
    push ax
    push dx
    push ax
    push word ptr [bp + 8]
    push bx
    call @streambuf@setp$qnct1
    push word ptr [bp - 4]
    push word ptr [bp - 6]
    push word ptr [bp - 4]
    push word ptr [bp - 6]
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 1ch]
    push word ptr es:[bx + 1ah]
    push word ptr [bp + 8]
    push bx
    call @streambuf@setg$qnct1t1
    add sp, 1ch

native_00e8:
    mov ax, 1
    push ax
    xor ax, ax
    push ax
    push ax
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 28h]
    push word ptr es:[bx + 26h]
    call _fseek
    add sp, 0ah
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx + 26h]
    test byte ptr es:[bx + 2], 10h
    je native_0116
    mov ax, 0ffffh
    jmp short native_0118

native_0116:
    xor ax, ax

native_0118:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends
end
