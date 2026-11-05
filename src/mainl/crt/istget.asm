; Complete original 16-bit Japanese Borland CRT C++ stream member istget.
; Preserves original far ABI, streambuf transfer and state semantics.
; Real 8086 instructions and symbolic relocations, never executable data bytes.
.8086
extrn @ios@setstate$qi:far
extrn @istream@ipfx$qi:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @istream@get$qv

org 157
    call @ios@setstate$qi
    add sp,6
    jmp short istget_jump_00b0

istget_jump_00a7:
    les bx,[bp+6]
    mov word ptr es:[bx+4],1

istget_jump_00b0:
    mov ax,[bp-10]
    jmp short istget_jump_00b8

istget_jump_00b5:
    mov ax,65535

istget_jump_00b8:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

org 18
    call @istream@ipfx$qi
    add sp,6
    or ax,ax
    jnz istget_jump_0021
    jmp near ptr istget_jump_00b5

istget_jump_0021:
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-2],es
    mov [bp-4],bx
    les bx,es:[bx+2]
    mov ax,es:[bx+30]
    les bx,[bp-4]
    les bx,es:[bx+2]
    cmp ax,es:[bx+34]
    jc istget_jump_006c
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-6],es
    mov [bp-8],bx
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx,es:[bx+2]
    mov bx,es:[bx]
    call dword ptr [bx+12]
    pop cx
    pop cx
    cmp ax,65535
    jnz istget_jump_006c
    mov ax,65535
    jmp short istget_jump_0089

istget_jump_006c:
    les bx,[bp+6]
    mov bx,es:[bx]
    les bx,es:[bx+2]
    mov dx,es:[bx+32]
    mov si,es:[bx+30]
    inc word ptr es:[bx+30]
    mov es,dx
    mov al,es:[si]
    mov ah,0

istget_jump_0089:
    mov [bp-10],ax
    cmp word ptr [bp-10],-1
    jnz istget_jump_00a7
    mov ax,1
    push ax
    les bx,[bp+6]
    push es
    push word ptr es:[bx]

org 0

@istream@get$qv:
    push bp
    mov bp,sp
    sub sp,10
    push si
    push di
    mov ax,1
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXTA ends
end
