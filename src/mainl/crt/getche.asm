; Original Borland near/far getche public adapter and echo handling.
.8086
extrn _getch:far,_putch:far,__cFlag:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __Ngetche,_getche
__Ngetche:
    pop ax
    push cs
    push ax
_getche proc far
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    cmp byte ptr DGROUP:__cFlag,0
    je echo_input
    call _getch
    mov [bp-2],ax
    jmp short result
echo_input:
    call _getch
    mov [bp-2],ax
    push ax
    call _putch
    pop cx
result:
    mov ax,[bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_getche endp
_TEXT ends
end
