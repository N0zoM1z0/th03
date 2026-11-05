; Original Japanese Borland CRT dossetbl: native 16-bit DOS system call.
; Keep real register/flag semantics and near/far error ABI.
.8086
extrn __DOSERROR:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __dos_setblock
__dos_setblock proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    mov ah,4ah
    int 21h
    jnc short block_success
    les bx,dword ptr [bp+10]
    mov word ptr es:[bx],bx
    push ax
    call __DOSERROR
    jmp short block_done
block_success:
    xor ax,ax
block_done:
    pop di
    pop si
    pop bp
    retf
__dos_setblock endp
_TEXT ends
end
