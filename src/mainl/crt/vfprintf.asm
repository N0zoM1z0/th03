; Complete original Borland Japanese CRT vfprintf ABI and control flow.
.8086
extrn __VPRINTER:near
extrn __FPUTN:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _vfprintf
_vfprintf proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,offset __FPUTN
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+14]
    call __VPRINTER
    pop di
    pop si
    pop bp
    retf
_vfprintf endp
_TEXT ends
end
