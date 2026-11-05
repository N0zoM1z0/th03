; Complete original 16-bit Japanese Borland CRT C++ stream member istws.
; Preserves original far ABI, streambuf transfer and state semantics.
; Real 8086 instructions and symbolic relocations, never executable data bytes.
.8086
extrn @ios@flags$ql:far
extrn @ios@setf$qll:far
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
public @ws$qm7istream

org 76
    call @ios@flags$ql
    add sp,26
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

org 58
    call @istream@ipfx$qi
    push word ptr [bp-2]
    push word ptr [bp-4]
    les bx,[bp+6]
    push es
    push word ptr es:[bx]

org 44
    call @ios@setf$qll
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 0

@ws$qm7istream:
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    les bx,[bp+6]
    mov bx,es:[bx]
    mov dx,es:[bx+18]
    mov ax,es:[bx+16]
    mov [bp-2],dx
    mov [bp-4],ax
    xor ax,ax
    mov dx,1
    push ax
    push dx
    push ax
    push dx
    les bx,[bp+6]
    push es
    push word ptr es:[bx]
_TEXTA ends
end
