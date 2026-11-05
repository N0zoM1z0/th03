; Original Japanese Borland CRT gregistr; natural 16-bit source.
.8086
extrn _registerfarbgidriver:far,_registerfarbgifont:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _registerbgidriver
_registerbgidriver proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _registerfarbgidriver
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf
_registerbgidriver endp
public _registerbgifont
_registerbgifont proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _registerfarbgifont
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf
_registerbgifont endp
_TEXT ends
end
