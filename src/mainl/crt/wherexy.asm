; Original Japanese Borland CRT wherexy: PC-98/IBM machine dispatch.
; Preserve the actual 16-bit ABI and device-type branches.
.8086
extrn __video:byte,__WHEREXY:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _wherex,_wherey
_wherex proc far
    push si
    push di
    call __WHEREXY
    mov ah,0
    mov dl,byte ptr DGROUP:__video
    mov dh,0
    sub ax,dx
    inc ax
    pop di
    pop si
    retf
_wherex endp
_wherey proc far
    push si
    push di
    call __WHEREXY
    mov cl,8
    shr ax,cl
    mov ah,0
    mov dl,byte ptr DGROUP:__video+1
    mov dh,0
    sub ax,dx
    inc ax
    pop di
    pop si
    retf
_wherey endp
_TEXT ends
end
