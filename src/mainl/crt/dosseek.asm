; Original Japanese Borland CRT member: dosseek
; INT 21h AH=42h absolute/relative file positioning into far long.
; Full 8086 ABI and DOS carry/error behavior, no patched object bytes.
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
public __dos_seek

__dos_seek:
    push bp
    mov bp,sp
    push si
    push di
    mov bx,[bp+6]
    mov cx,[bp+10]
    mov dx,[bp+8]
    mov ah,42h
    mov al,[bp+12]
    int 21h
    jnc dosseek_branch_001d
    push ax
    call __DOSERROR
    jmp short dosseek_branch_0029

dosseek_branch_001d:
    les bx,[bp+14]
    mov es:[bx+2],dx
    mov es:[bx],ax
    xor ax,ax

dosseek_branch_0029:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
