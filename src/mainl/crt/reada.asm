; Original Borland low-level DOS read: genuine AH=3Fh, native
; descriptor flags, IOERROR and both FAR CRT entrypoints.
.8086
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
public __rtl_read,__read
__rtl_read proc far
    push bp
    mov bp,sp
    push si
    push di
    mov bx,[bp+6]
    add bx,bx
    test byte ptr DGROUP:__openfd[bx],2
    je short perform_dos_read
    mov ax,5
    push ax
    jmp short report_dos_error
perform_dos_read:
    push ds
    mov ah,3fh
    mov bx,[bp+6]
    mov cx,[bp+0ch]
    lds dx,dword ptr [bp+8]
    int 21h
    pop ds
    jb short read_failed
    jmp short read_done
read_failed:
    push ax
report_dos_error:
    call __IOERROR
read_done:
    pop di
    pop si
    pop bp
    retf
__rtl_read endp

__read proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push cs
    call near ptr __rtl_read
    add sp,8
    pop di
    pop si
    pop bp
    retf
__read endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
