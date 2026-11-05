; Original Japanese Borland CRT member umask
; Native DOS notUmask complement/get/set routine with original DGROUP frame.
; Complete 16-bit ABI and imported target relocations, no patched objects.
.8086
extrn __notUmask:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _umask

_umask:
    push bp
    mov bp,sp
    push si
    push di
    mov dx,word ptr DGROUP:__notUmask
    not dx
    mov ax,[bp+6]
    not ax
    mov word ptr DGROUP:__notUmask,ax
    mov ax,dx
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
