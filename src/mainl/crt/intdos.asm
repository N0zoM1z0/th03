; Original DOS intdos/intdosx 16-bit register/segment bridge.
; Native real INT 21h, FLAGS capture and near IOERROR propagation.
.8086
extrn _segread:far
extrn __IOERROR:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _intdos,_intdosx

_intdos proc far
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    push ss
    lea ax,[bp-8]
    push ax
    call _segread
    pop cx
    pop cx
    push ss
    lea ax,[bp-8]
    push ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push cs
    call near ptr _intdosx
    add sp,0ch
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_intdos endp

_intdosx proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    lds si,dword ptr [bp+0eh]
    push word ptr [si]
    push word ptr [si+6]
    lds si,dword ptr [bp+6]
    mov ax,[si]
    mov bx,[si+2]
    mov cx,[si+4]
    mov dx,[si+6]
    mov di,[si+0ah]
    mov si,[si+8]
    pop ds
    pop es
    push bp
    int 21h
    pop bp
    pushf
    pushf
    push si
    push ds
    push es
    lds si,dword ptr [bp+0eh]
    pop word ptr [si]
    pop word ptr [si+6]
    lds si,dword ptr [bp+0ah]
    pop word ptr [si+8]
    pop word ptr [si+0eh]
    pop word ptr [si+0ch]
    and word ptr [si+0ch],1
    mov word ptr [si+0ah],di
    mov word ptr [si+6],dx
    mov word ptr [si+4],cx
    mov word ptr [si+2],bx
    mov word ptr [si],ax
    pop ds
    jz short dos_return
    push ax
    push ax
    call __IOERROR
    pop ax
dos_return:
    pop di
    pop si
    pop bp
    retf
_intdosx endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
