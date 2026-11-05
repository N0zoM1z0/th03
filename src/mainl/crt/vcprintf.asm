; Complete original Borland Japanese CRT vcprintf ABI and control flow.
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
public _vcprintf
_vcprintf proc far
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
    push word ptr [bp+10]
    call __VPRINTER
    pop di
    pop si
    pop bp
    retf
_vcprintf endp
_TEXT ends
end
