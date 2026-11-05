; Original Japanese Borland CRT MBSNINC; natural 16-bit source.
.8086
extrn __mbsnbcnt:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __mbsninc
__mbsninc proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short nonnull
    xor dx,dx
    xor ax,ax
    jmp short return_far
nonnull:
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __mbsnbcnt
    add sp,6
    mov dx,[bp+8]
    add ax,[bp+6]
return_far:
    pop di
    pop si
    pop bp
    retf
__mbsninc endp
_TEXT ends
end
