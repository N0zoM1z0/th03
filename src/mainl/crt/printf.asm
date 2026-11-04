; Original Borland large-model stdout printf / VPRINTER bridge.
.8086
extrn __streams:byte,__VPRINTER:near,__FPUTN:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _printf
_printf proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,offset __FPUTN
    push ax
    push ds
    mov ax,offset DGROUP:__streams+20
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    lea ax,[bp+10]
    push ax
    call __VPRINTER
    pop di
    pop si
    pop bp
    retf
_printf endp
_TEXT ends
end
