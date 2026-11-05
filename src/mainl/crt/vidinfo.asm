; Original conio gettextinfo and video-mode translation.
; Real lookup table for PC-98 display modes; no code-as-data patching.
.8086
extrn __video:byte
extrn __WHEREXY:near
extrn ___get_screen_height:far
extrn ___get_windowy2:far
extrn ___conio_type:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
video_mode_translate proc near
    push bp
    mov bp,sp
    push si
    push di
    cmp word ptr DGROUP:___conio_type,2
    jne short original_mode
    mov bx,[bp+4]
    and bx,0e0h
    mov cl,5
    shr bx,cl
    add bx,bx
    mov ax,word ptr DGROUP:video_mode_map[bx]
    mov dx,[bp+4]
    and dx,400h
    mov cl,7
    shr dx,cl
    or ax,dx
    mov dx,[bp+4]
    and dx,0f000h
    mov cl,8
    shr dx,cl
    or ax,dx
    mov dx,[bp+4]
    and dx,800h
    add dx,dx
    or ax,dx
    mov dx,[bp+4]
    and dx,1eh
    mov cl,7
    shl dx,cl
    or ax,dx
    jmp short translation_done
original_mode:
    mov ax,[bp+4]
translation_done:
    pop di
    pop si
    pop bp
    ret 2
video_mode_translate endp

public _gettextinfo
_gettextinfo proc far
    push bp
    mov bp,sp
    push si
    push di
    mov al,byte ptr DGROUP:__video
    inc al
    les bx,dword ptr [bp+6]
    mov byte ptr es:[bx],al
    mov al,byte ptr DGROUP:__video+1
    inc al
    mov byte ptr es:[bx+1],al
    mov al,byte ptr DGROUP:__video+2
    inc al
    mov byte ptr es:[bx+2],al
    call ___get_windowy2
    inc al
    les bx,dword ptr [bp+6]
    mov byte ptr es:[bx+3],al
    push word ptr DGROUP:__video+4
    call video_mode_translate
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+4],ax
    push word ptr DGROUP:__video+6
    call video_mode_translate
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+6],ax
    mov al,byte ptr DGROUP:__video+8
    mov byte ptr es:[bx+8],al
    call ___get_screen_height
    les bx,dword ptr [bp+6]
    mov byte ptr es:[bx+9],al
    mov al,byte ptr DGROUP:__video+10
    mov byte ptr es:[bx+10],al
    call __WHEREXY
    mov dx,ax
    les bx,dword ptr [bp+6]
    mov al,dl
    sub al,byte ptr DGROUP:__video
    inc al
    mov byte ptr es:[bx+11],al
    mov ax,dx
    mov cl,8
    shr ax,cl
    sub al,byte ptr DGROUP:__video+1
    inc al
    mov byte ptr es:[bx+12],al
    pop di
    pop si
    pop bp
    retf
_gettextinfo endp
_TEXT ends

_DATA segment word public 'DATA'
video_mode_map dw 0,1,4,5,2,3,6,7
_DATA ends
end
