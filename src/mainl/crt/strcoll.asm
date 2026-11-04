; Original Japanese far strcoll in C locale: forward to far strcmp.
.8086
extrn _strcmp:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _strcoll
_strcoll proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _strcmp
    add sp,8
    pop di
    pop si
    pop bp
    retf
_strcoll endp
_TEXT ends
end
