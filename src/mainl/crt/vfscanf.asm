; Original Borland large-model vfscanf: use supplied far FILE and va_list.
.8086
extrn __Nfgetc:near,__Nungetc:near,__scanner:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _vfscanf
_vfscanf proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    mov ax,offset __Nungetc
    push ax
    mov ax,offset __Nfgetc
    push ax
    call __scanner
    add sp,16
    pop di
    pop si
    pop bp
    retf
_vfscanf endp
_TEXT ends
end
