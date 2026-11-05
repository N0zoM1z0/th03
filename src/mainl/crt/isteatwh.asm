; Complete original 16-bit Japanese Borland CRT C++ stream member isteatwh.
; Preserves original far ABI, streambuf transfer and state semantics.
; Real 8086 instructions and symbolic relocations, never executable data bytes.
.8086
extrn @ios@setstate$qi:far
extrn __ctype:byte
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @istream@eatwhite$qv

org 220
    call @ios@setstate$qi
    add sp,6

isteatwh_jump_00e4:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

org 188
    mov al,byte ptr DGROUP:__ctype[bx+1]
    mov ah,0
    and ax,1
    or ax,ax
    jz isteatwh_jump_00cc
    jmp near ptr isteatwh_jump_000a

isteatwh_jump_00cc:
    cmp dx,-1
    jnz isteatwh_jump_00e4
    mov ax,1
    push ax
    les bx,[bp+6]
    push es
    push word ptr es:[bx]

org 0

@istream@eatwhite$qv:
    push bp
    mov bp,sp
    sub sp,16
    push si
    push di
    jmp short isteatwh_jump_0062

isteatwh_jump_000a:
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-2],es
    mov [bp-4],bx
    les bx,es:[bx+2]
    mov ax,es:[bx+30]
    les bx,[bp-4]
    les bx,es:[bx+2]
    cmp ax,es:[bx+34]
    jc isteatwh_jump_004d
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
    jmp short isteatwh_jump_005b

isteatwh_jump_004d:
    les bx,[bp+6]
    mov bx,es:[bx]
    les bx,es:[bx+2]
    inc word ptr es:[bx+30]

isteatwh_jump_005b:
    les bx,[bp+6]
    inc word ptr es:[bx+4]

isteatwh_jump_0062:
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-10],es
    mov [bp-12],bx
    les bx,es:[bx+2]
    mov ax,es:[bx+30]
    les bx,[bp-12]
    les bx,es:[bx+2]
    cmp ax,es:[bx+34]
    jc isteatwh_jump_00a5
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
    jmp short isteatwh_jump_00b8

isteatwh_jump_00a5:
    les bx,[bp+6]
    mov bx,es:[bx]
    les bx,es:[bx+2]
    les bx,es:[bx+30]
    mov al,es:[bx]
    mov ah,0

isteatwh_jump_00b8:
    mov dx,ax
    mov bx,dx
_TEXTA ends
end
