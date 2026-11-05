; Original Borland Japanese CRT cputs; complete 16-bit ABI leaf.
.8086
extrn _strlen:far
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
public _cputs
_cputs proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _strlen
    pop cx
    pop cx
    push ax
    xor ax,ax
    push ax
    push ax
    call __CPUTN
    pop di
    pop si
    pop bp
    retf
_cputs endp
_TEXT ends
end
