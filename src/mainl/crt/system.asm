; Original DOS COMSPEC environment shell and command builder.
; Unchecked Borland far pointers, errno, allocation and spawn ABI.
; Real 8086 source and human-readable strings, not original CODE bytes.
.8086
extrn _errno:word,__environ:dword,_free:far,_getenv:far,_malloc:far
extrn __exitbuf:dword,__DOSENV:near,__getswitchar:far,__spawn:near
extrn _strlen:far,__stpcpy:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _system

_system:
    push bp
    mov bp, sp
    sub sp, 14h
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne loc_0031
    push ds
    mov ax,offset DGROUP:env_COMSPEC
    push ax
    call _getenv
    pop cx
    pop cx
    or ax, dx
    jne loc_002b
    mov word ptr DGROUP:_errno, 2
    xor ax, ax
    jmp near ptr loc_017b

loc_002b:
    mov ax, 1
    jmp near ptr loc_017b

loc_0031:
    push ds
    mov ax,offset DGROUP:shell_COMSPEC
    push ax
    call _getenv
    pop cx
    pop cx
    mov word ptr [bp - 10h], dx
    mov word ptr [bp - 12h], ax
    or ax, dx
    jne loc_0050
    mov word ptr DGROUP:_errno, 2
    jmp near ptr loc_0131

loc_0050:
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call _strlen
    pop cx
    pop cx
    add ax, 5
    mov word ptr [bp - 6], ax
    cmp word ptr [bp - 6], 80h
    jle loc_0073
    mov word ptr DGROUP:_errno, 14h
    jmp near ptr loc_0131

loc_0073:
    push word ptr [bp - 6]
    call _malloc
    pop cx
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or ax, dx
    jne loc_008f
    mov word ptr DGROUP:_errno, 8
    jmp near ptr loc_0131

loc_008f:
    cmp word ptr [bp - 6], 5
    jne loc_00a3
    les bx,dword ptr [bp - 4]
    mov byte ptr es:[bx], 0
    mov byte ptr es:[bx + 1], 0dh
    jmp short loc_00fe

loc_00a3:
    mov al, byte ptr [bp - 6]
    add al, 0feh
    les bx,dword ptr [bp - 4]
    mov byte ptr es:[bx], al
    inc word ptr [bp - 4]
    call __getswitchar
    les bx,dword ptr [bp - 4]
    mov byte ptr es:[bx], al
    inc word ptr [bp - 4]
    push ds
    mov ax,offset DGROUP:shell_command_flag
    push ax
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call __stpcpy
    add sp, 8
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push dx
    push ax
    call __stpcpy
    add sp, 8
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx,dword ptr [bp - 4]
    mov byte ptr es:[bx], 0dh
    inc word ptr [bp - 4]
    mov ax, word ptr [bp - 6]
    sub word ptr [bp - 4], ax

loc_00fe:
    push word ptr DGROUP:__environ+2
    push word ptr DGROUP:__environ
    push word ptr [bp - 10h]
    push word ptr [bp - 12h]
    push ss
    lea ax, [bp - 0eh]
    push ax
    call __DOSENV
    mov word ptr [bp - 8], dx
    mov word ptr [bp - 0ah], ax
    or ax, dx
    jne loc_0136
    mov word ptr DGROUP:_errno, 8
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call _free
    pop cx
    pop cx

loc_0131:
    mov ax, 0ffffh
    jmp short loc_017b

loc_0136:
    call dword ptr DGROUP:__exitbuf
    push word ptr [bp - 8]
    push word ptr [bp - 0ah]
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    push word ptr [bp - 10h]
    push word ptr [bp - 12h]
    call __spawn
    add sp, 0ch
    mov word ptr [bp - 14h], ax
    push word ptr [bp - 0ch]
    push word ptr [bp - 0eh]
    call _free
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call _free
    add sp, 8
    cmp word ptr [bp - 14h], -1
    jne loc_0179
    mov ax, 0ffffh
    jmp short loc_017b

loc_0179:
    xor ax, ax

loc_017b:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
_DATA segment word public 'DATA'
env_COMSPEC db 'COMSPEC',0
shell_COMSPEC db 'COMSPEC',0
shell_command_flag db 'c ',0
_DATA ends
end
