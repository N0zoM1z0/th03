; Complete original 16-bit Japanese Borland CRT C++ stream member istread.
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
public @istream@read$qnci

org 267
    call @ios@setstate$qi
    add sp,6

istread_jump_0113:
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
    jnz istread_jump_0021
    jmp near ptr istread_jump_0113

istread_jump_0021:
    mov word ptr [bp-18],0
    jmp short istread_jump_0089

istread_jump_0028:
    les bx,[bp+10]
    mov al,[bp-18]
    mov es:[bx],al
    inc word ptr [bp+10]
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
    jc istread_jump_007b
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
    jmp short istread_jump_0089

istread_jump_007b:
    les bx,[bp+6]
    mov bx,es:[bx]
    les bx,es:[bx+2]
    inc word ptr es:[bx+30]

istread_jump_0089:
    dec word ptr [bp+14]
    jl istread_jump_00ef
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-10],es
    mov [bp-12],bx
    les bx,es:[bx+2]
    mov ax,es:[bx+30]
    les bx,[bp-12]
    les bx,es:[bx+2]
    cmp ax,es:[bx+34]
    jc istread_jump_00d1
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
    jmp short istread_jump_00e4

istread_jump_00d1:
    les bx,[bp+6]
    mov bx,es:[bx]
    les bx,es:[bx+2]
    les bx,es:[bx+30]
    mov al,es:[bx]
    mov ah,0

istread_jump_00e4:
    mov [bp-18],ax
    cmp ax,65535
    jz istread_jump_00ef
    jmp near ptr istread_jump_0028

istread_jump_00ef:
    cmp word ptr [bp-18],-1
    jnz istread_jump_0113
    cmp word ptr [bp+14],0
    jl istread_jump_0100
    mov ax,3
    jmp short istread_jump_0103

istread_jump_0100:
    mov ax,1

istread_jump_0103:
    push ax
    les bx,[bp+6]
    push es
    push word ptr es:[bx]

org 0

@istream@read$qnci:
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
