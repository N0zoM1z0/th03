; Complete original Borland Japanese CRT window ABI and control flow.
.8086
extrn __video:byte
extrn __VALIDATEXY:near
extrn __GOTOXY:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _window
_window proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+6]
    push word ptr [bp+8]
    push word ptr [bp+10]
    push word ptr [bp+12]
    call __VALIDATEXY
    or ax,ax
    jz short done
    dec word ptr [bp+6]
    dec word ptr [bp+8]
    dec word ptr [bp+10]
    dec word ptr [bp+12]
    mov al,byte ptr [bp+6]
    mov byte ptr DGROUP:__video,al
    mov al,byte ptr [bp+10]
    mov byte ptr DGROUP:__video+2,al
    mov al,byte ptr [bp+8]
    mov byte ptr DGROUP:__video+1,al
    mov al,byte ptr [bp+12]
    mov byte ptr DGROUP:__video+3,al
    push word ptr [bp+6]
    push word ptr [bp+8]
    call __GOTOXY
done:
    pop di
    pop si
    pop bp
    retf
_window endp
_TEXT ends
end
