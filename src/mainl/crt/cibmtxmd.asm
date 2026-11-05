; Borland IBM-compatible textmode: -1 reads current video mode,
; passes the chosen value to the near initializer, then stores __video+8.
.8086
extrn __video:byte
extrn ___ibm_crtinit:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___ibm_textmode
___ibm_textmode:
    push bp
    mov bp,sp
    push si
    push di
    cmp word ptr [bp+6],-1
    jne mode_ready
    mov al,DGROUP:__video[8]
    mov ah,0
    mov [bp+6],ax
mode_ready:
    push word ptr [bp+6]
    call ___ibm_crtinit
    pop cx
    mov al,[bp+6]
    mov DGROUP:__video[8],al
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
