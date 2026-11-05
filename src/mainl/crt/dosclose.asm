; Original _dos_close: DOS INT 21h function 3Eh, carry-tested
; error forwarding to Borland's near __DOSERROR helper.
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
public __dos_close
__dos_close:
    push bp
    mov bp,sp
    push si
    push di
    mov ah,3eh
    mov bx,[bp+6]
    int 21h
    jnc close_ok
    push ax
    call __DOSERROR
    jmp short close_done
close_ok:
    xor ax,ax
close_done:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
