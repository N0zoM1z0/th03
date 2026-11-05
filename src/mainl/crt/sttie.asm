; Complete original 16-bit Japanese Borland CRT C++ stream member sttie.
; Preserves original far ABI, streambuf transfer and state semantics.
; Real 8086 instructions and symbolic relocations, never executable data bytes.
.8086
extrn @ostream@flush$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ios@tie$qn7ostream

@ios@tie$qn7ostream:
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    les bx,[bp+6]
    mov dx,es:[bx+8]
    mov ax,es:[bx+6]
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,[bp-2]
    jz sttie_jump_0029
    push dx
    push word ptr [bp-4]
    call @ostream@flush$qv
    pop cx
    pop cx

sttie_jump_0029:
    les bx,[bp+6]
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov es:[bx+8],dx
    mov es:[bx+6],ax
    or ax,[bp+12]
    jz sttie_jump_004d
    or word ptr es:[bx+12],512
    or word ptr es:[bx+14],512
    jmp short sttie_jump_005c

sttie_jump_004d:
    les bx,[bp+6]
    and word ptr es:[bx+12],65023
    and word ptr es:[bx+14],65023

sttie_jump_005c:
    mov dx,[bp-2]
    mov ax,[bp-4]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_TEXTA ends
end
