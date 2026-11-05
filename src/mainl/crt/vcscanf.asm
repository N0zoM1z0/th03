; Complete original Borland Japanese CRT vcscanf ABI and control flow.
.8086
extrn __Ngetche:near
extrn __Nungetch:near
extrn __scanner:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _vcscanf
_vcscanf proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    xor ax,ax
    push ax
    push ax
    mov ax,offset __Nungetch
    push ax
    mov ax,offset __Ngetche
    push ax
    call __scanner
    add sp,16
    pop di
    pop si
    pop bp
    retf
_vcscanf endp
_TEXT ends
end
