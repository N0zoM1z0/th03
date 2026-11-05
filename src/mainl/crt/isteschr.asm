; Complete original 16-bit Japanese Borland CRT C++ stream member isteschr.
; Preserves original far ABI, streambuf transfer and state semantics.
; Real 8086 instructions and symbolic relocations, never executable data bytes.
.8086
extrn @istream@ipfx$qi:far
extrn @istream@do_get$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @istream@$brsh$qmzc

org 221
    call @istream@do_get$qv
    pop cx
    pop cx

isteschr_jump_00e4:
    les bx,[bp+10]
    mov es:[bx],al

isteschr_jump_00ea:
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

org 17
    call @istream@ipfx$qi
    add sp,6
    or ax,ax
    jnz isteschr_jump_0020
    jmp near ptr isteschr_jump_00ea

isteschr_jump_0020:
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-2],es
    mov [bp-4],bx
    les bx,es:[bx+2]
    mov ax,es:[bx+34]
    les bx,[bp-4]
    les bx,es:[bx+2]
    cmp ax,es:[bx+30]
    jna isteschr_jump_0067
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-6],es
    mov [bp-8],bx
    les bx,es:[bx+2]
    mov ax,es:[bx+34]
    les bx,[bp-8]
    les bx,es:[bx+2]
    xor dx,dx
    sub ax,es:[bx+30]
    sbb dx,0
    jmp short isteschr_jump_0069

isteschr_jump_0067:
    xor ax,ax

isteschr_jump_0069:
    or ax,ax
    jz isteschr_jump_00d7
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-10],es
    mov [bp-12],bx
    les bx,es:[bx+2]
    mov ax,es:[bx+30]
    les bx,[bp-12]
    les bx,es:[bx+2]
    cmp ax,es:[bx+34]
    jc isteschr_jump_00b8
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-14],es
    mov [bp-16],bx
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx,es:[bx+2]
    mov bx,es:[bx]
    call dword ptr [bx+12]
    pop cx
    pop cx
    cmp ax,65535
    jnz isteschr_jump_00b8
    mov ax,65535
    jmp short isteschr_jump_00d5

isteschr_jump_00b8:
    les bx,[bp+6]
    mov bx,es:[bx]
    les bx,es:[bx+2]
    mov dx,es:[bx+32]
    mov si,es:[bx+30]
    inc word ptr es:[bx+30]
    mov es,dx
    mov al,es:[si]
    mov ah,0

isteschr_jump_00d5:
    jmp short isteschr_jump_00e4

isteschr_jump_00d7:
    push word ptr [bp+8]
    push word ptr [bp+6]

org 0

@istream@$brsh$qmzc:
    push bp
    mov bp,sp
    sub sp,16
    push si
    push di
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXTA ends
end
