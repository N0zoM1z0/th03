; Original Borland DOS no-echo getpass: real BSS 9-byte buffer,
; typed printf format data, 8-character limit and native CRLF output.
.8086
extrn __streams:byte
extrn _fprintf:far
extrn _bdos:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

getpass_flush proc far
    push si
    push di
    mov ax,2
    push ax
    xor ax,ax
    push ax
    mov ax,12
    push ax
    call _bdos
    add sp,6
    pop di
    pop si
    retf
getpass_flush endp

public _getpass
_getpass proc far
    push bp
    mov bp,sp
    sub sp,6
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push ds
    mov ax,offset DGROUP:getpass_format
    push ax
    push ds
    mov ax,offset DGROUP:__streams+40
    push ax
    call _fprintf
    add sp,0ch
    push cs
    call near ptr getpass_flush
    mov [bp-2],ds
    mov word ptr [bp-4],offset DGROUP:getpass_buf
    mov word ptr [bp-6],0
read_password_char:
    xor ax,ax
    push ax
    push ax
    mov ax,7
    push ax
    call _bdos
    add sp,6
    les bx,dword ptr [bp-4]
    mov byte ptr es:[bx],al
    cmp al,0dh
    je short terminate_password
    inc word ptr [bp-6]
    inc word ptr [bp-4]
    cmp word ptr [bp-6],8
    jl short read_password_char
terminate_password:
    les bx,dword ptr [bp-4]
    mov byte ptr es:[bx],0
    xor ax,ax
    push ax
    mov ax,0dh
    push ax
    mov ax,2
    push ax
    call _bdos
    xor ax,ax
    push ax
    mov ax,0ah
    push ax
    mov ax,2
    push ax
    call _bdos
    add sp,0ch
    push cs
    call near ptr getpass_flush
    mov dx,ds
    mov ax,offset DGROUP:getpass_buf
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_getpass endp
_TEXT ends
_DATA segment word public 'DATA'
getpass_format db '%s',0
_DATA ends
_BSS segment word public 'BSS'
getpass_buf db 9 dup(?)
_BSS ends
end
