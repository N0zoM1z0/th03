; Complete original 16-bit Japanese Borland CRT C++ stream member stbsgetn.
; Preserves original far ABI, streambuf transfer and state semantics.
; Real 8086 instructions and symbolic relocations, never executable data bytes.
.8086
extrn _memcpy:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @streambuf@sgetn$qnci

@streambuf@sgetn$qnci:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    mov ax,[bp+14]
    cwd
    les bx,[bp+6]
    mov bx,es:[bx+34]
    mov si,[bp+6]
    xor cx,cx
    sub bx,es:[si+30]
    sbb cx,0
    cmp dx,cx
    jg stbsgetn_jump_0054
    jnz stbsgetn_jump_0029
    cmp ax,bx
    ja stbsgetn_jump_0054

stbsgetn_jump_0029:
    push word ptr [bp+14]
    les bx,[bp+6]
    push word ptr es:[bx+32]
    push word ptr es:[bx+30]
    push word ptr [bp+12]
    push word ptr [bp+10]
    call _memcpy
    add sp,10
    mov ax,[bp+14]
    mov [bp-2],ax
    les bx,[bp+6]
    add es:[bx+30],ax
    jmp short stbsgetn_jump_006f

stbsgetn_jump_0054:
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    les bx,[bp+6]
    mov bx,es:[bx]
    call dword ptr [bx+8]
    add sp,10

stbsgetn_jump_006f:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_TEXTA ends
end
