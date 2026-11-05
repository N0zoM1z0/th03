; Complete original Borland Japanese CRT insline ABI and control flow.
.8086
extrn __video:byte
extrn __SCROLL:near
extrn __WHEREXY:near
extrn ___get_windowy2:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _insline
_insline proc far
    push si
    push di
    mov al,7
    push ax
    push word ptr DGROUP:__video
    call __WHEREXY
    mov cl,8
    shr ax,cl
    push ax
    push word ptr DGROUP:__video+2
    call ___get_windowy2
    push ax
    mov al,1
    push ax
    call __SCROLL
    pop di
    pop si
    retf
_insline endp
public _delline
_delline proc far
    push si
    push di
    mov al,6
    push ax
    push word ptr DGROUP:__video
    call __WHEREXY
    mov cl,8
    shr ax,cl
    push ax
    push word ptr DGROUP:__video+2
    call ___get_windowy2
    push ax
    mov al,1
    push ax
    call __SCROLL
    pop di
    pop si
    retf
_delline endp
_TEXT ends
end
