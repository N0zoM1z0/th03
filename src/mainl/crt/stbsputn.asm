; Complete original 16-bit Japanese Borland CRT C++ stream member stbsputn.
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
public @streambuf@sputn$qnxci

@streambuf@sputn$qnxci:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    xor ax,ax
    les bx,[bp+6]
    mov dx,es:[bx+22]
    xor cx,cx
    sub dx,es:[bx+18]
    sbb cx,0
    cmp ax,cx
    jg stbsputn_jump_0050
    jnz stbsputn_jump_0025
    cmp [bp+14],dx
    ja stbsputn_jump_0050

stbsputn_jump_0025:
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    les bx,[bp+6]
    push word ptr es:[bx+20]
    push word ptr es:[bx+18]
    call _memcpy
    add sp,10
    mov ax,[bp+14]
    mov [bp-2],ax
    les bx,[bp+6]
    add es:[bx+18],ax
    jmp short stbsputn_jump_006b

stbsputn_jump_0050:
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    les bx,[bp+6]
    mov bx,es:[bx]
    call dword ptr [bx+20]
    add sp,10

stbsputn_jump_006b:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_TEXTA ends
end
