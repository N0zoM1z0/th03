; Original Japanese Borland CRT member rmdir
; DOS INT 21h AH=3Ah delete directory, same unchecked far path ABI.
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
public _rmdir

_rmdir:
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,58
    lds dx,[bp+6]
    int 21h
    pop ds
    jc rmdir_branch_0014
    xor ax,ax
    jmp short rmdir_branch_0018

rmdir_branch_0014:
    push ax
    call __IOERROR

rmdir_branch_0018:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
