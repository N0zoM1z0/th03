; Original Borland istream::do_get: real streambuf/vtable underflow,
; FAR input-buffer cursor and ios state/counter side effects.
.8086
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
public @istream@do_get$qv
@istream@do_get$qv proc far
    push bp
    mov bp,sp
    sub sp,0ah
    push si
    push di
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    mov [bp-4],es
    mov [bp-6],bx
    les bx,dword ptr es:[bx+2]
    mov ax,word ptr es:[bx+1eh]
    les bx,dword ptr [bp-6]
    les bx,dword ptr es:[bx+2]
    cmp ax,word ptr es:[bx+22h]
    jb short buffered_character
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    mov [bp-8],es
    mov [bp-0ah],bx
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx,dword ptr es:[bx+2]
    mov bx,word ptr es:[bx]
    call dword ptr [bx+0ch]
    pop cx
    pop cx
    cmp ax,-1
    jne short buffered_character
    mov ax,-1
    jmp short set_result
buffered_character:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    mov dx,word ptr es:[bx+20h]
    mov si,word ptr es:[bx+1eh]
    inc word ptr es:[bx+1eh]
    mov es,dx
    mov al,byte ptr es:[si]
    mov ah,0
set_result:
    mov [bp-2],ax
    cmp word ptr [bp-2],-1
    jne short counted_character
    mov ax,3
    push ax
    les bx,dword ptr [bp+6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp,6
    jmp short return_character
counted_character:
    les bx,dword ptr [bp+6]
    inc word ptr es:[bx+4]
return_character:
    mov al,byte ptr [bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@istream@do_get$qv endp
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
end
