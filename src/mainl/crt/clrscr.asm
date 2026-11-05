; Original Borland PC-98/IBM conio clear screen: scroll window then GOTOXY.
.8086
extrn __video:byte
extrn __SCROLL:near
extrn __GOTOXY:far
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
public _clrscr
_clrscr proc far
    push si
    push di
    mov al,6
    push ax
    push word ptr DGROUP:__video
    push word ptr DGROUP:__video+1
    push word ptr DGROUP:__video+2
    call ___get_windowy2
    push ax
    mov al,0
    push ax
    call __SCROLL
    push word ptr DGROUP:__video
    push word ptr DGROUP:__video+1
    call __GOTOXY
    pop di
    pop si
    retf
_clrscr endp
_TEXT ends
end
