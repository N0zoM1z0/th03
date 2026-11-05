; Original DOS region locking/unlocking, two complete FAR entrypoints.
; Preserve DOS 21h AX=5C00/5C01 and genuine near IOERROR propagation.
.8086
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
public _lock,_unlock

_lock proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,5c00h
    mov bx,[bp+6]
    mov cx,[bp+0ah]
    mov dx,[bp+8]
    mov si,[bp+0eh]
    mov di,[bp+0ch]
    int 21h
    jb short lock_error
    xor ax,ax
    jmp short lock_done
lock_error:
    push ax
    call __IOERROR
lock_done:
    pop di
    pop si
    pop bp
    retf
_lock endp

_unlock proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,5c01h
    mov bx,[bp+6]
    mov cx,[bp+0ah]
    mov dx,[bp+8]
    mov si,[bp+0eh]
    mov di,[bp+0ch]
    int 21h
    jb short unlock_error
    xor ax,ax
    jmp short unlock_done
unlock_error:
    push ax
    call __IOERROR
unlock_done:
    pop di
    pop si
    pop bp
    retf
_unlock endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
