; Complete original 16-bit Japanese Borland CRT C++ stream member istpback.
; Preserves original far ABI, streambuf transfer and state semantics.
; Real 8086 instructions and symbolic relocations, never executable data bytes.
.8086
extrn @ios@clear$qi:far
extrn @ios@setstate$qi:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @istream@putback$qc

org 185
    call @ios@clear$qi

istpback_jump_00be:
    add sp,6

istpback_jump_00c1:
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

org 154
    call @ios@setstate$qi
    jmp short istpback_jump_00be

istpback_jump_00a1:
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-10],es
    mov [bp-12],bx
    mov ax,es:[bx+10]
    and ax,65534
    push ax
    push word ptr [bp-10]
    push bx

org 0

@istream@putback$qc:
    push bp
    mov bp,sp
    sub sp,12
    push si
    push di
    les bx,[bp+6]
    mov bx,es:[bx]
    test byte ptr es:[bx+10],134
    jz istpback_jump_0018
    jmp near ptr istpback_jump_00c1

istpback_jump_0018:
    mov cl,[bp+10]
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-2],es
    mov [bp-4],bx
    les bx,es:[bx+2]
    mov ax,es:[bx+30]
    les bx,[bp-4]
    les bx,es:[bx+2]
    cmp ax,es:[bx+26]
    jna istpback_jump_0065
    les bx,[bp+6]
    mov bx,es:[bx]
    les bx,es:[bx+2]
    dec word ptr es:[bx+30]
    push bx
    push es
    mov es,es:[bx+32]
    mov ax,es
    pop es
    pop bx
    mov bx,es:[bx+30]
    mov dl,cl
    mov es,ax
    mov es:[bx],dl
    mov al,dl
    mov ah,0
    jmp short istpback_jump_008a

istpback_jump_0065:
    mov al,cl
    cbw
    push ax
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-6],es
    mov [bp-8],bx
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx,es:[bx+2]
    mov bx,es:[bx]
    call dword ptr [bx+16]
    add sp,6

istpback_jump_008a:
    cmp ax,65535
    jnz istpback_jump_00a1
    mov ax,2
    push ax
    les bx,[bp+6]
    push es
    push word ptr es:[bx]
_TEXTA ends
end
