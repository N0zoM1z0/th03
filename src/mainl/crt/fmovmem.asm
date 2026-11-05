; Original Borland FAR memmove with overlap-safe forward/backward
; byte/word copy and FAR wrapper returning the destination pointer.
.8086
extrn N_PCMP@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __fmovmem,__fmemmove

__fmovmem proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov cx,[bp+0ch]
    mov bx,[bp+0ah]
    mov dx,[bp+8]
    mov ax,[bp+6]
    call N_PCMP@
    jae short forward_copy
    std
    mov ax,1
    jmp short begin_copy
forward_copy:
    cld
    xor ax,ax
begin_copy:
    lds si,dword ptr [bp+6]
    les di,dword ptr [bp+0ah]
    mov cx,[bp+0eh]
    or ax,ax
    jz short copy_word_start
    add si,cx
    dec si
    add di,cx
    dec di
copy_word_start:
    test di,1
    je short aligned_words
    jcxz short finish_copy
    movsb
    dec cx
aligned_words:
    sub si,ax
    sub di,ax
    shr cx,1
    rep movsw
    jae short finish_copy
    add si,ax
    add di,ax
    movsb
finish_copy:
    cld
    pop ds
    pop di
    pop si
    pop bp
    retf
__fmovmem endp

__fmemmove proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+0eh]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push cs
    call near ptr __fmovmem
    add sp,0ah
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf
__fmemmove endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
