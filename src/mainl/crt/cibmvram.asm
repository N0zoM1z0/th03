; Original IBM text display VRAM helpers in Japanese Borland PC-98 CRT.
; All three near Pascal-cleanup entries handle physical video pages,
; bidirectional word movement and real 3DAh vertical retrace handshake.
.8086
extrn __video:byte,__IBM_VIDEOINTESDI:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _BSS,_DATA
_BSS segment word public 'BSS'
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __IBM_VPTR,__IBM_VRAM,__IBM_REFRESH_VRAM

__IBM_VPTR proc near
    push bp
    mov bp,sp
    push si
    push di
    mov al,byte ptr DGROUP:__video+10
    mov ah,0
    mov dx,[bp+4]
    dec dx
    imul dx
    add ax,[bp+6]
    dec ax
    add ax,ax
    add ax,word ptr DGROUP:__video+16
    mov dx,word ptr DGROUP:__video+18
    pop di
    pop si
    pop bp
    ret 4
__IBM_VPTR endp

__IBM_VRAM proc near
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    mov al,byte ptr DGROUP:__video+12
    mov ah,0
    mov [bp-2],ax
    push ds
    mov cx,[bp+4]
    jcxz short move_finished
    les di,dword ptr [bp+10]
    lds si,dword ptr [bp+6]
    cld
    cmp si,di
    jnc short move_direction_ready
    mov ax,cx
    dec ax
    shl ax,1
    add si,ax
    add di,ax
    std
move_direction_ready:
    cmp word ptr [bp-2],0
    jnz short sync_words
    rep movsw
    jmp short move_finished
sync_words:
    mov dx,03dah
    mov ax,es
    mov bx,ds
    cmp ax,bx
    jz short same_video_segment
next_different_word:
    cli
wait_start_different:
    in al,dx
    ror al,1
    jc short wait_start_different
wait_end_different:
    in al,dx
    ror al,1
    jnc short wait_end_different
    movsw
    sti
    loop next_different_word
    jmp short move_finished
same_video_segment:
next_same_word:
    cli
wait_start_same_source:
    in al,dx
    ror al,1
    jc short wait_start_same_source
wait_end_same_source:
    in al,dx
    ror al,1
    jnc short wait_end_same_source
    lodsw
    sti
    mov bx,ax
wait_start_same_target:
    in al,dx
    ror al,1
    jc short wait_start_same_target
wait_end_same_target:
    in al,dx
    ror al,1
    jnc short wait_end_same_target
    mov ax,bx
    stosw
    sti
    loop next_same_word
move_finished:
    cld
    pop ds
    pop di
    pop si
    mov sp,bp
    pop bp
    ret 10
__IBM_VRAM endp

__IBM_REFRESH_VRAM proc near
    push bp
    mov bp,sp
    push si
    push di
    cmp byte ptr DGROUP:__video+13,0
    jz short no_refresh
    mov ax,[bp+8]
    cmp ax,word ptr DGROUP:__video+18
    jnz short no_refresh
    mov ax,0ff00h
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+4]
    call __IBM_VIDEOINTESDI
no_refresh:
    pop di
    pop si
    pop bp
    ret 6
__IBM_REFRESH_VRAM endp
_TEXT ends
end
