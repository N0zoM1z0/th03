; Original Japanese Borland CRT member: dosfree
; INT 21h AH=49h releases one original DOS memory block segment.
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
public __dos_freemem

__dos_freemem:
    push bp
    mov bp,sp
    push si
    push di
    mov es,[bp+6]
    mov ah,49h
    int 21h
    jnc dosfree_branch_0014
    push ax
    call __DOSERROR
    jmp short dosfree_branch_0016

dosfree_branch_0014:
    xor ax,ax

dosfree_branch_0016:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
