; Original Japanese Borland CRT member mkdir
; DOS INT 21h AH=39h create path, with far string pointer and original I/O error.
; Complete 16-bit ABI and imported target relocations, no patched objects.
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
public _mkdir

_mkdir:
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,57
    lds dx,[bp+6]
    int 21h
    pop ds
    jc mkdir_branch_0014
    xor ax,ax
    jmp short mkdir_branch_0018

mkdir_branch_0014:
    push ax
    call __IOERROR

mkdir_branch_0018:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
