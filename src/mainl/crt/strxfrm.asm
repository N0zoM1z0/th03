; Original C-locale public strxfrm, not the distinct 382-byte __strxfrm.
; Retain unchecked far source/target, size_t limit, and return length.
.8086
extrn _memcpy:far,_strlen:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _strxfrm
_strxfrm proc far
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    push word ptr [bp+12]
    push word ptr [bp+10]
    call _strlen
    pop cx
    pop cx
    mov [bp-2],ax
    mov ax,[bp+14]
    cmp ax,[bp-2]
    jbe skip_copy
    mov ax,[bp-2]
    inc ax
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _memcpy
    add sp,10
skip_copy:
    mov ax,[bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_strxfrm endp
_TEXT ends
end
