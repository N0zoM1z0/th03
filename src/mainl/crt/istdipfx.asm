; Complete original Borland C++ istream::ipfx(int) stream-prefix boss.
; Maintains original gcount reset, tied ostream flush, fast gptr/egptr
; count testing, skipws/eatwhite and complete ios error-state handling.
.8086
extrn @ios@setstate$qi:far
extrn @istream@eatwhite$qv:far
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
public @istream@ipfx$qi
@istream@ipfx$qi proc far
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+4],0
    mov bx,word ptr es:[bx]
    cmp word ptr es:[bx+0ah],0
    jz short check_tie
    mov ax,2
    push ax
    les bx,dword ptr [bp+6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp,6
    xor ax,ax
    jmp near ptr return_prefix
check_tie:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    mov ax,word ptr es:[bx+6]
    or ax,word ptr es:[bx+8]
    jz short check_skip
    cmp word ptr [bp+10],0
    jz short flush_tied
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    mov [bp-2],es
    mov [bp-4],bx
    les bx,dword ptr es:[bx+2]
    mov ax,word ptr es:[bx+22h]
    les bx,dword ptr [bp-4]
    les bx,dword ptr es:[bx+2]
    cmp ax,word ptr es:[bx+1eh]
    jna short no_get_chars
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    mov [bp-6],es
    mov [bp-8],bx
    les bx,dword ptr es:[bx+2]
    mov ax,word ptr es:[bx+22h]
    les bx,dword ptr [bp-8]
    les bx,dword ptr es:[bx+2]
    xor dx,dx
    sub ax,word ptr es:[bx+1eh]
    sbb dx,0
    jmp short compare_available
no_get_chars:
    xor ax,ax
compare_available:
    cmp ax,[bp+10]
    jnl short check_skip
flush_tied:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    push word ptr es:[bx+8]
    push word ptr es:[bx+6]
    call @ostream@flush$qv
    pop cx
    pop cx
check_skip:
    cmp word ptr [bp+10],0
    jnz short return_status
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    test byte ptr es:[bx+0dh],1
    jz short return_status
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @istream@eatwhite$qv
    pop cx
    pop cx
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    cmp word ptr es:[bx+0ah],0
    jz short return_status
    mov ax,2
    push ax
    les bx,dword ptr [bp+6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp,6
return_status:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    cmp word ptr es:[bx+0ah],0
    jnz short failed_status
    mov ax,1
    jmp short return_prefix
failed_status:
    xor ax,ax
return_prefix:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@istream@ipfx$qi endp
_TEXTA ends
end
