; Complete original 16-bit Japanese Borland CRT C++ stream member istign.
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
public @istream@ignore$qii

org 252
    call @ios@setstate$qi
    add sp,6

istign_jump_0104:
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

org 18
    call @istream@ipfx$qi
    add sp,6
    or ax,ax
    jnz istign_jump_0021
    jmp near ptr istign_jump_0104

istign_jump_0021:
    mov word ptr [bp-18],0
    jmp short istign_jump_0085

istign_jump_0028:
    les bx,[bp+6]
    inc word ptr es:[bx+4]
    mov bx,es:[bx]
    mov [bp-2],es
    mov [bp-4],bx
    les bx,es:[bx+2]
    mov ax,es:[bx+30]
    les bx,[bp-4]
    les bx,es:[bx+2]
    cmp ax,es:[bx+34]
    jc istign_jump_006f
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
    jmp short istign_jump_007d

istign_jump_006f:
    les bx,[bp+6]
    mov bx,es:[bx]
    les bx,es:[bx+2]
    inc word ptr es:[bx+30]

istign_jump_007d:
    mov ax,[bp-18]
    cmp ax,[bp+12]
    jz istign_jump_00eb

istign_jump_0085:
    dec word ptr [bp+10]
    jl istign_jump_00eb
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-10],es
    mov [bp-12],bx
    les bx,es:[bx+2]
    mov ax,es:[bx+30]
    les bx,[bp-12]
    les bx,es:[bx+2]
    cmp ax,es:[bx+34]
    jc istign_jump_00cd
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
    jmp short istign_jump_00e0

istign_jump_00cd:
    les bx,[bp+6]
    mov bx,es:[bx]
    les bx,es:[bx+2]
    les bx,es:[bx+30]
    mov al,es:[bx]
    mov ah,0

istign_jump_00e0:
    mov [bp-18],ax
    cmp ax,65535
    jz istign_jump_00eb
    jmp near ptr istign_jump_0028

istign_jump_00eb:
    cmp word ptr [bp-18],-1
    jnz istign_jump_0104
    mov ax,1
    push ax
    les bx,[bp+6]
    push es
    push word ptr es:[bx]

org 0

@istream@ignore$qii:
    push bp
    mov bp,sp
    sub sp,18
    push si
    push di
    mov ax,1
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXTA ends
end
