; Original Borland three FAR decimal/radix string formatting adapters.
; All use the native near __LONGTOA backend and retain the caller's
; 16-bit parameter order and the original signedness flags.
.8086
extrn __LONGTOA:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _itoa,_ultoa,_ltoa

_itoa proc far
    push bp
    mov bp,sp
    push si
    push di
    mov bx,[bp+6]
    mov cx,[bp+0ch]
    cmp cx,0ah
    jne short itoa_unsigned
    mov ax,bx
    cwd
    jmp short itoa_have_long
itoa_unsigned:
    mov ax,bx
    xor dx,dx
itoa_have_long:
    push dx
    push ax
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push cx
    mov al,1
    push ax
    mov al,61h
    push ax
    call __LONGTOA
    pop di
    pop si
    pop bp
    retf
_itoa endp

_ultoa proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+0eh]
    mov al,0
    push ax
    mov al,61h
    push ax
    call __LONGTOA
    pop di
    pop si
    pop bp
    retf
_ultoa endp

_ltoa proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+0eh]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push ax
    cmp ax,0ah
    jne short long_nondecimal
    mov ax,1
    jmp short long_have_sign
long_nondecimal:
    xor ax,ax
long_have_sign:
    push ax
    mov al,61h
    push ax
    call __LONGTOA
    pop di
    pop si
    pop bp
    retf
_ltoa endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
