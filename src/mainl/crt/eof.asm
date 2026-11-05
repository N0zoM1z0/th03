; Original Borland DOS _eof(handle): distinguish redirected files,
; devices, descriptor state and saved/current DOS file offsets.
.8086
extrn __nfile:word
extrn __IOERROR:near
extrn __openfd:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _eof
_eof proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    mov ax,[bp+6]
    cmp ax,word ptr DGROUP:__nfile
    jb short check_open_descriptor
    mov ax,6
    push ax
    jmp short error_handler
check_open_descriptor:
    mov bx,[bp+6]
    add bx,bx
    test byte ptr DGROUP:__openfd[bx+1],2
    jz short query_device
    mov ax,1
    jmp short done
query_device:
    mov ax,4400h
    mov bx,[bp+6]
    int 21h
    jc short propagate_dos_error
    test dl,80h
    jnz short no_eof
    mov ax,4201h
    xor cx,cx
    mov dx,cx
    int 21h
    jc short propagate_dos_error
    push dx
    push ax
    mov ax,4202h
    xor cx,cx
    mov dx,cx
    int 21h
    mov [bp-4],ax
    mov [bp-2],dx
    pop dx
    pop cx
    jc short propagate_dos_error
    mov ax,4200h
    int 21h
    jc short propagate_dos_error
    cmp dx,[bp-2]
    jb short no_eof
    ja short reached_eof
    cmp ax,[bp-4]
    jb short no_eof
reached_eof:
    mov ax,1
    jmp short done
no_eof:
    xor ax,ax
    jmp short done
propagate_dos_error:
    push ax
error_handler:
    call __IOERROR
done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_eof endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
