; Original Japanese Borland CRT member: dosread
; INT 21h AH=3Fh file read with DS restore and far result count.
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
public __dos_read

__dos_read:
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,3fh
    mov bx,[bp+6]
    mov cx,[bp+12]
    lds dx,[bp+8]
    int 21h
    pop ds
    jc dosread_branch_0020
    les bx,[bp+14]
    mov es:[bx],ax
    xor ax,ax
    jmp short dosread_branch_0024

dosread_branch_0020:
    push ax
    call __DOSERROR

dosread_branch_0024:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
