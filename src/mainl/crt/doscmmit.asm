; Borland DOS commit wrapper: INT 21h AH=68h with original
; carry to DOSERROR path and far member ABI.
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
public __dos_commit
__dos_commit:
    push bp
    mov bp,sp
    push si
    push di
    mov ah,68h
    mov bx,[bp+6]
    int 21h
    jnc commit_ok
    push ax
    call __DOSERROR
    jmp short commit_done
commit_ok:
    xor ax,ax
commit_done:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
