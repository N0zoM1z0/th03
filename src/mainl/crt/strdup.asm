; Original far strdup: strlen + NUL, malloc word size, copy only if allocated.
.8086
extrn _memcpy:far,_strlen:far,_malloc:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _strdup
_strdup proc far
    push bp
    mov bp,sp
    sub sp,6
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _strlen
    pop cx
    pop cx
    inc ax
    mov [bp-6],ax
    push ax
    call _malloc
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    je done_copy
    push word ptr [bp-6]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push dx
    push word ptr [bp-4]
    call _memcpy
    add sp,10
done_copy:
    mov dx,[bp-2]
    mov ax,[bp-4]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_strdup endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
