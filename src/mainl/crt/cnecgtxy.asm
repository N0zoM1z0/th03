; Complete original NEC PC-98 GOTOXY: BIOS/int versus direct video route.
; The original direct path updates physical 0000:071C/0710 and saves flags.
.8086
extrn __directvideo:word,__video:byte
extrn __NEC_VIDEOINT18:near,__NEC_VIDEOINTDC:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _BSS,_DATA
_BSS segment word public 'BSS'
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __NEC_GOTOXY
__NEC_GOTOXY proc far
    push bp
    mov bp,sp
    push si
    push di
    cmp word ptr DGROUP:__directvideo,0
    jz short bios_cursor
    pushf
    cli
    xor ax,ax
    mov es,ax
    mov cl,byte ptr [bp+8]
    mov byte ptr es:[071ch],cl
    mov al,byte ptr [bp+6]
    mov byte ptr es:[0710h],al
    mov ah,byte ptr __video+10
    mul ah
    add al,cl
    add ah,0
    shl ax,1
    xchg ax,dx
    mov ah,13h
    call __NEC_VIDEOINT18
    popf
    jmp short cursor_done
bios_cursor:
    mov cl,10h
    mov ah,3
    mov dl,byte ptr [bp+8]
    mov dh,byte ptr [bp+6]
    call __NEC_VIDEOINTDC
cursor_done:
    pop di
    pop si
    pop bp
    retf 4
__NEC_GOTOXY endp
_TEXT ends
end
