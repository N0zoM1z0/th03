; Original Japanese Borland sdbuflow complete streambuf or istream method.
; Real symbolic 8086 far C++ ABI, virtual calls and buffer controls.
; No original executable machine CODE initializer or OBJ patches.
.8086
extrn @streambuf@setp$qnct1:far,@streambuf@setg$qnct1t1:far,__fgetc:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @stdiobuf@underflow$qv

@stdiobuf@underflow$qv:
    push bp
    mov bp, sp
    sub sp, 0ah
    push si
    push di
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 22h]
    cmp ax, word ptr es:[bx + 1eh]
    jbe native_0020
    xor dx, dx
    sub ax, word ptr es:[bx + 1eh]
    sbb dx, 0
    jmp short native_0022

native_0020:
    xor ax, ax

native_0022:
    or ax, ax
    je native_0035
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx + 1eh]
    mov al, byte ptr es:[bx]
    mov ah, 0
    jmp near ptr native_019a

native_0035:
    les bx,dword ptr [bp + 6]
    cmp word ptr es:[bx + 4], 0
    je native_0042
    jmp near ptr native_011e

native_0042:
    mov ax, word ptr es:[bx + 6]
    or ax, word ptr es:[bx + 8]
    jne native_004f
    jmp near ptr native_011e

native_004f:
    mov ax, word ptr es:[bx + 12h]
    or ax, word ptr es:[bx + 14h]
    je native_0068
    mov ax, word ptr es:[bx + 12h]
    xor dx, dx
    sub ax, word ptr es:[bx + 0eh]
    sbb dx, 0
    jmp short native_006a

native_0068:
    xor ax, ax

native_006a:
    or ax, ax
    je native_008f
    mov ax, 0ffffh
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 18h]
    add sp, 6
    cmp ax, 0ffffh
    jne native_008f
    mov ax, 0ffffh
    jmp near ptr native_019a

native_008f:
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx + 26h]
    dec word ptr es:[bx]
    jl native_00b0
    mov dx, word ptr es:[bx + 0eh]
    mov si, word ptr es:[bx + 0ch]
    inc word ptr es:[bx + 0ch]
    mov es, dx
    mov al, byte ptr es:[si]
    mov ah, 0
    jmp short native_00c2

native_00b0:
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 28h]
    push word ptr es:[bx + 26h]
    call __fgetc
    pop cx
    pop cx

native_00c2:
    mov word ptr [bp - 2], ax
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 8]
    mov ax, word ptr es:[bx + 6]
    mov word ptr [bp - 8], dx
    mov word ptr [bp - 0ah], ax
    les bx,dword ptr [bp - 0ah]
    mov al, byte ptr [bp - 2]
    mov byte ptr es:[bx + 4], al
    mov ax, word ptr [bp - 0ah]
    add ax, 5
    push dx
    push ax
    mov ax, word ptr [bp - 0ah]
    add ax, 4
    push dx
    push ax
    push dx
    push bx
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @streambuf@setg$qnct1t1
    mov ax, word ptr [bp - 0ah]
    add ax, 4
    mov word ptr [bp - 4], ax
    push word ptr [bp - 8]
    push ax
    push word ptr [bp - 8]
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @streambuf@setp$qnct1
    add sp, 1ch
    jmp short native_0197

native_011e:
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx + 26h]
    dec word ptr es:[bx]
    jl native_013f
    mov dx, word ptr es:[bx + 0eh]
    mov si, word ptr es:[bx + 0ch]
    inc word ptr es:[bx + 0ch]
    mov es, dx
    mov al, byte ptr es:[si]
    mov ah, 0
    jmp short native_0151

native_013f:
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 28h]
    push word ptr es:[bx + 26h]
    call __fgetc
    pop cx
    pop cx

native_0151:
    mov word ptr [bp - 2], ax
    cmp word ptr [bp - 2], -1
    jne native_0164
    xor ax, ax
    push ax
    push ax
    push ax
    push ax
    push ax
    push ax
    jmp short native_0189

native_0164:
    les bx,dword ptr [bp + 6]
    mov al, byte ptr [bp - 2]
    mov byte ptr es:[bx + 2ah], al
    mov ax, word ptr [bp + 6]
    add ax, 2bh
    push word ptr [bp + 8]
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 2ah
    mov word ptr [bp - 6], ax
    push word ptr [bp + 8]
    push ax
    push word ptr [bp + 8]
    push ax

native_0189:
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @streambuf@setg$qnct1t1
    add sp, 10h

native_0197:
    mov ax, word ptr [bp - 2]

native_019a:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends
end
