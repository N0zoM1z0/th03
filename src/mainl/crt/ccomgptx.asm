; Original PC-98 / IBM text region dispatchers; complete three
; FAR conio public entries, preserving original argument and ABI flow.
.8086
extrn ___nec_puttext:far
extrn ___nec_gettext:far
extrn ___nec_getputtextsize:far
extrn ___ibm_puttext:far
extrn ___ibm_gettext:far
extrn ___ibm_getputtextsize:far
extrn ___conio_type:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _gettext,_puttext,__getputtextsize
_gettext proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    mov dx,[bp+8]
    mov bx,[bp+0ah]
    mov cx,[bp+0ch]
    cmp word ptr DGROUP:___conio_type,2
    jnz short get_ibm
    push word ptr [bp+10h]
    push word ptr [bp+0eh]
    push cx
    push bx
    push dx
    push ax
    call ___nec_gettext
    jmp short get_cleanup
get_ibm:
    cmp word ptr DGROUP:___conio_type,1
    jnz short get_failed
    push word ptr [bp+10h]
    push word ptr [bp+0eh]
    push cx
    push bx
    push dx
    push ax
    call ___ibm_gettext
get_cleanup:
    add sp,0ch
    jmp short get_done
get_failed:
    xor ax,ax
get_done:
    pop di
    pop si
    pop bp
    retf
_gettext endp

_puttext proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    mov dx,[bp+8]
    mov bx,[bp+0ah]
    mov cx,[bp+0ch]
    cmp word ptr DGROUP:___conio_type,2
    jnz short put_ibm
    push word ptr [bp+10h]
    push word ptr [bp+0eh]
    push cx
    push bx
    push dx
    push ax
    call ___nec_puttext
    jmp short put_cleanup
put_ibm:
    cmp word ptr DGROUP:___conio_type,1
    jnz short put_failed
    push word ptr [bp+10h]
    push word ptr [bp+0eh]
    push cx
    push bx
    push dx
    push ax
    call ___ibm_puttext
put_cleanup:
    add sp,0ch
    jmp short put_done
put_failed:
    xor ax,ax
put_done:
    pop di
    pop si
    pop bp
    retf
_puttext endp

__getputtextsize proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    mov dx,[bp+8]
    mov bx,[bp+0ah]
    mov cx,[bp+0ch]
    cmp word ptr DGROUP:___conio_type,2
    jnz short size_ibm
    push cx
    push bx
    push dx
    push ax
    call ___nec_getputtextsize
    jmp short size_cleanup
size_ibm:
    cmp word ptr DGROUP:___conio_type,1
    jnz short size_failed
    push cx
    push bx
    push dx
    push ax
    call ___ibm_getputtextsize
size_cleanup:
    add sp,8
    jmp short size_done
size_failed:
    xor ax,ax
size_done:
    pop di
    pop si
    pop bp
    retf
__getputtextsize endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
