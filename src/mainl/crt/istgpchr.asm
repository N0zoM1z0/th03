; Complete original 16-bit Japanese Borland CRT C++ stream member istgpchr.
; Preserves original far ABI, streambuf transfer and state semantics.
; Real 8086 instructions and symbolic relocations, never executable data bytes.
.8086
extrn @ios@setstate$qi:far
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
public @istream@get$qmc

org 254
    call @ios@setstate$qi
    add sp,6

istgpchr_jump_0106:
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

org 228
    call @istream@do_get$qv
    pop cx
    pop cx

istgpchr_jump_00eb:
    les bx,[bp+10]
    mov es:[bx],al
    jmp short istgpchr_jump_0106

istgpchr_jump_00f3:
    mov ax,2
    push ax
    les bx,[bp+6]
    push es
    push word ptr es:[bx]

org 18
    call @istream@ipfx$qi
    add sp,6
    or ax,ax
    jnz istgpchr_jump_0021
    jmp near ptr istgpchr_jump_00f3

istgpchr_jump_0021:
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-2],es
    mov [bp-4],bx
    les bx,es:[bx+2]
    mov ax,es:[bx+34]
    les bx,[bp-4]
    les bx,es:[bx+2]
    cmp ax,es:[bx+30]
    jna istgpchr_jump_0068
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
    jmp short istgpchr_jump_006a

istgpchr_jump_0068:
    xor ax,ax

istgpchr_jump_006a:
    or ax,ax
    jz istgpchr_jump_00de
    les bx,[bp+6]
    mov word ptr es:[bx+4],1
    mov bx,es:[bx]
    mov [bp-10],es
    mov [bp-12],bx
    les bx,es:[bx+2]
    mov ax,es:[bx+30]
    les bx,[bp-12]
    les bx,es:[bx+2]
    cmp ax,es:[bx+34]
    jc istgpchr_jump_00bf
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
    jnz istgpchr_jump_00bf
    mov ax,65535
    jmp short istgpchr_jump_00dc

istgpchr_jump_00bf:
    les bx,[bp+6]
    mov bx,es:[bx]
    les bx,es:[bx+2]
    mov dx,es:[bx+32]
    mov si,es:[bx+30]
    inc word ptr es:[bx+30]
    mov es,dx
    mov al,es:[si]
    mov ah,0

istgpchr_jump_00dc:
    jmp short istgpchr_jump_00eb

istgpchr_jump_00de:
    push word ptr [bp+8]
    push word ptr [bp+6]

org 0

@istream@get$qmc:
    push bp
    mov bp,sp
    sub sp,16
    push si
    push di
    mov ax,1
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXTA ends
end
