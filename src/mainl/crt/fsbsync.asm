; Original Japanese Borland fsbsync complete streambuf or istream method.
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
public @filebuf@sync$qv

@filebuf@sync$qv:
    push bp
    mov bp, sp
    sub sp, 12h
    push si
    push di
    les bx,dword ptr [bp + 6]
    cmp word ptr es:[bx + 2ah], 0
    jne native_0015
    jmp near ptr native_0192

native_0015:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 12h]
    or ax, word ptr es:[bx + 14h]
    je native_0031
    mov ax, word ptr es:[bx + 12h]
    xor dx, dx
    sub ax, word ptr es:[bx + 0eh]
    sbb dx, 0
    jmp short native_0033

native_0031:
    xor ax, ax

native_0033:
    mov word ptr [bp - 2], ax
    cmp word ptr [bp - 2], 0
    jne native_003f
    jmp near ptr native_00df

native_003f:
    push ax
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 10h]
    push word ptr es:[bx + 0eh]
    push word ptr es:[bx + 26h]
    call _write
    add sp, 8
    cmp ax, word ptr [bp - 2]
    je native_005f
    jmp near ptr native_0192

native_005f:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 0ah]
    xor dx, dx
    sub ax, word ptr es:[bx + 6]
    sbb dx, 0
    cmp ax, 8
    jle native_0079
    mov ax, 4
    jmp short native_007c

native_0079:
    mov ax, 1

native_007c:
    mov word ptr [bp - 0eh], ax
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 8]
    mov ax, word ptr es:[bx + 6]
    mov word ptr [bp - 10h], dx
    mov word ptr [bp - 12h], ax
    mov ax, word ptr es:[bx + 0ah]
    xor dx, dx
    sub ax, word ptr es:[bx + 6]
    sbb dx, 0
    add ax, word ptr [bp - 12h]
    push word ptr [bp - 10h]
    push ax
    mov ax, word ptr [bp - 12h]
    add ax, word ptr [bp - 0eh]
    push word ptr [bp - 10h]
    push ax
    push word ptr [bp + 8]
    push bx
    call @streambuf@setp$qnct1
    mov ax, word ptr [bp - 12h]
    add ax, word ptr [bp - 0eh]
    mov word ptr [bp - 4], ax
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
    jmp near ptr native_0197

native_00df:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 22h]
    cmp ax, word ptr es:[bx + 1eh]
    jbe native_00f7
    xor dx, dx
    sub ax, word ptr es:[bx + 1eh]
    sbb dx, 0
    jmp short native_00f9

native_00f7:
    xor ax, ax

native_00f9:
    or ax, ax
    jne native_0100
    jmp near ptr native_0197

native_0100:
    mov ax, 1
    push ax
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 22h]
    cmp ax, word ptr es:[bx + 1eh]
    jbe native_011c
    xor dx, dx
    sub ax, word ptr es:[bx + 1eh]
    sbb dx, 0
    jmp short native_011e

native_011c:
    xor ax, ax

native_011e:
    neg ax
    cwd
    push dx
    push ax
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 26h]
    call _lseek
    add sp, 8
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2eh], dx
    mov word ptr es:[bx + 2ch], ax
    mov dx, word ptr es:[bx + 20h]
    mov word ptr [bp - 6], dx
    mov ax, word ptr es:[bx + 1eh]
    mov word ptr [bp - 8], ax
    push dx
    push ax
    push dx
    push ax
    push word ptr es:[bx + 1ch]
    push word ptr es:[bx + 1ah]
    push word ptr [bp + 8]
    push bx
    call @streambuf@setg$qnct1t1
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 20h]
    mov word ptr [bp - 0ah], dx
    mov ax, word ptr es:[bx + 1eh]
    mov word ptr [bp - 0ch], ax
    push dx
    push ax
    push dx
    push ax
    push word ptr [bp + 8]
    push bx
    call @streambuf@setp$qnct1
    add sp, 1ch
    les bx,dword ptr [bp + 6]
    cmp word ptr es:[bx + 2eh], -1
    jne native_0197
    cmp word ptr es:[bx + 2ch], -1
    jne native_0197

native_0192:
    mov ax, 0ffffh
    jmp short native_0199

native_0197:
    xor ax, ax

native_0199:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends
end
