; Original Japanese Borland CRT member: doswrite
; INT 21h AH=40h file write with DS restore and far count result.
; Full 8086 ABI and DOS carry/error behavior, no patched object bytes.
.8086
extrn __DOSERROR:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __dos_write

__dos_write:
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,40h
    mov bx,[bp+6]
    mov cx,[bp+12]
    lds dx,[bp+8]
    int 21h
    pop ds
    jc doswrite_branch_0020
    les bx,[bp+14]
    mov es:[bx],ax
    xor ax,ax
    jmp short doswrite_branch_0024

doswrite_branch_0020:
    push ax
    call __DOSERROR

doswrite_branch_0024:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
