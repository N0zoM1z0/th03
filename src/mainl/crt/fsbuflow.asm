; Original Japanese Borland fsbuflow complete streambuf or istream method.
; Real symbolic 8086 far C++ ABI, virtual calls and buffer controls.
; No original executable machine CODE initializer or OBJ patches.
.8086
extrn _read:far,@streambuf@setp$qnct1:far,@streambuf@setg$qnct1t1:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @filebuf@underflow$qv

@filebuf@underflow$qv:
    push bp
    mov bp, sp
    sub sp, 0eh
    push si
    push di
    les bx,dword ptr [bp + 6]
    cmp word ptr es:[bx + 2ah], 0
    jne native_0015
    jmp near ptr native_00dc

native_0015:
    mov ax, word ptr es:[bx + 28h]
    and ax, 3
    cmp ax, 2
    jne native_0024
    jmp near ptr native_00dc

native_0024:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 22h]
    cmp ax, word ptr es:[bx + 1eh]
    jbe native_003c
    xor dx, dx
    sub ax, word ptr es:[bx + 1eh]
    sbb dx, 0
    jmp short native_003e

native_003c:
    xor ax, ax

native_003e:
    or ax, ax
    je native_0051
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx + 1eh]
    mov al, byte ptr es:[bx]
    mov ah, 0
    jmp near ptr native_01b2

native_0051:
    les bx,dword ptr [bp + 6]
    cmp word ptr es:[bx + 4], 0
    je native_005e
    jmp near ptr native_013f

native_005e:
    mov ax, word ptr es:[bx + 6]
    or ax, word ptr es:[bx + 8]
    jne native_006b
    jmp near ptr native_013f

native_006b:
    push word ptr [bp + 8]
    push bx
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 24h]
    pop cx
    pop cx
    or ax, ax
    jne native_00dc
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 0ah]
    xor dx, dx
    sub ax, word ptr es:[bx + 6]
    sbb dx, 0
    cmp ax, 8
    jle native_0095
    mov ax, 4
    jmp short native_0098

native_0095:
    mov ax, 1

native_0098:
    mov word ptr [bp - 0ah], ax
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 8]
    mov ax, word ptr es:[bx + 6]
    mov word ptr [bp - 0ch], dx
    mov word ptr [bp - 0eh], ax
    mov ax, word ptr es:[bx + 0ah]
    xor dx, dx
    sub ax, word ptr es:[bx + 6]
    sbb dx, 0
    sub ax, word ptr [bp - 0ah]
    push ax
    mov ax, word ptr [bp - 0eh]
    add ax, word ptr [bp - 0ah]
    push word ptr [bp - 0ch]
    push ax
    push word ptr es:[bx + 26h]
    call _read
    add sp, 8
    mov word ptr [bp - 4], ax
    cmp word ptr [bp - 4], -1
    jne native_00e2

native_00dc:
    mov ax, 0ffffh
    jmp near ptr native_01b2

native_00e2:
    mov ax, word ptr [bp - 0eh]
    add ax, word ptr [bp - 0ah]
    mov word ptr [bp - 6], ax
    add ax, word ptr [bp - 4]
    push word ptr [bp - 0ch]
    push ax
    push word ptr [bp - 0ch]
    push word ptr [bp - 6]
    push word ptr [bp - 0ch]
    push word ptr [bp - 0eh]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @streambuf@setg$qnct1t1
    mov ax, word ptr [bp - 0eh]
    add ax, word ptr [bp - 0ah]
    mov word ptr [bp - 8], ax
    push word ptr [bp - 0ch]
    push ax
    push word ptr [bp - 0ch]
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @streambuf@setp$qnct1
    add sp, 1ch
    cmp word ptr [bp - 4], 0
    je native_01a4
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx + 1eh]
    mov al, byte ptr es:[bx]
    mov ah, 0
    mov word ptr [bp - 2], ax
    jmp short native_01a4

native_013f:
    mov ax, 1
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 34h
    push word ptr [bp + 8]
    push ax
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 26h]
    call _read
    add sp, 8
    mov word ptr [bp - 4], ax
    cmp word ptr [bp - 4], -1
    jne native_0174
    mov word ptr [bp - 2], 0ffffh
    xor ax, ax
    push ax
    push ax
    push ax
    push ax
    push ax
    push ax
    jmp short native_0196

native_0174:
    les bx,dword ptr [bp + 6]
    add bx, 34h
    mov dx, bx
    mov al, byte ptr es:[bx]
    mov ah, 0
    mov word ptr [bp - 2], ax
    mov ax, word ptr [bp + 6]
    add ax, 35h
    push word ptr [bp + 8]
    push ax
    push word ptr [bp + 8]
    push bx
    push word ptr [bp + 8]
    push bx

native_0196:
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @streambuf@setg$qnct1t1
    add sp, 10h

native_01a4:
    cmp word ptr [bp - 4], 0
    jne native_01af
    mov word ptr [bp - 2], 0ffffh

native_01af:
    mov ax, word ptr [bp - 2]

native_01b2:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends
end
