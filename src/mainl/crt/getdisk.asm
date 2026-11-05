; Original Borland Japanese CRT getdisk; complete 16-bit ABI leaf.
.8086
extrn __dos_getdrive:far
extrn __dos_setdrive:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _getdisk,_setdisk
_getdisk proc far
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    push ss
    lea ax,[bp-2]
    push ax
    call __dos_getdrive
    pop cx
    pop cx
    mov ax,[bp-2]
    dec ax
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_getdisk endp
_setdisk proc far
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    push ss
    lea ax,[bp-2]
    push ax
    mov ax,[bp+6]
    inc ax
    push ax
    call __dos_setdrive
    add sp,6
    mov ax,[bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_setdisk endp
_TEXT ends
end
