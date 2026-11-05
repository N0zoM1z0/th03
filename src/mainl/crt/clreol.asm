; Complete original Borland Japanese CRT clreol ABI and control flow.
.8086
extrn __video:byte
extrn __SCROLL:near
extrn __WHEREXY:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _clreol
_clreol proc far
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    call __WHEREXY
    mov cl,8
    shr ax,cl
    mov ah,0
    mov [bp-2],ax
    mov al,6
    push ax
    call __WHEREXY
    push ax
    push word ptr [bp-2]
    push word ptr DGROUP:__video+2
    push word ptr [bp-2]
    mov al,0
    push ax
    call __SCROLL
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_clreol endp
_TEXT ends
end
