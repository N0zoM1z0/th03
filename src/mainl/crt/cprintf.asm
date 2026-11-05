; Complete original Borland Japanese CRT cprintf ABI and control flow.
.8086
extrn __VPRINTER:near
extrn __CPUTN:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _cprintf
_cprintf proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,offset __CPUTN
    push ax
    xor ax,ax
    push ax
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
_cprintf endp
_TEXT ends
end
