; Borland large-model vscanf: stdin stream and far va_list to near scanner.
.8086
extrn __streams:byte,__Nfgetc:near,__Nungetc:near,__scanner:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _vscanf
_vscanf proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push ds
    mov ax,offset DGROUP:__streams
    push ax
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
_vscanf endp
_TEXT ends
end
