; Original IBM-compatible text scrolling and DBCS lead/trail edge cleanup.
; It fills split double-byte glyph edges before dispatching the video
; scroll window request with the original NEC/IBM console globals.
.8086
extrn __wclrnorm:word
extrn __wgarbage:word
extrn __video:byte
extrn __IBM_CHECK_DBCS_TRAIL:near
extrn __IBM_FILL_SPACE:near
extrn __IBM_VIDEOINT:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __IBM_SCROLL
__IBM_SCROLL proc near
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    cmp word ptr DGROUP:__wgarbage,0
    jz short prepare_video
    mov al,byte ptr [bp+0ah]
    mov byte ptr [bp-1],al
    jmp short advance_column
next_column:
    mov al,byte ptr [bp+8]
    cmp al,byte ptr DGROUP:__video+0ah
    jae short check_right_border
    mov ah,0
    inc ax
    push ax
    mov al,byte ptr [bp-1]
    mov ah,0
    push ax
    call __IBM_CHECK_DBCS_TRAIL
    or ax,ax
    jz short check_right_border
    mov al,byte ptr [bp+8]
    inc al
    push ax
    push word ptr [bp-1]
    call __IBM_FILL_SPACE
    push word ptr [bp+8]
    push word ptr [bp-1]
    call __IBM_FILL_SPACE
check_right_border:
    cmp byte ptr [bp+0ch],0
    jbe short column_complete
    mov al,byte ptr [bp+0ch]
    mov ah,0
    push ax
    mov al,byte ptr [bp-1]
    mov ah,0
    push ax
    call __IBM_CHECK_DBCS_TRAIL
    or ax,ax
    jz short column_complete
    mov al,byte ptr [bp+0ch]
    add al,0ffh
    push ax
    push word ptr [bp-1]
    call __IBM_FILL_SPACE
    push word ptr [bp+0ch]
    push word ptr [bp-1]
    call __IBM_FILL_SPACE
column_complete:
    inc byte ptr [bp-1]
advance_column:
    mov al,byte ptr [bp-1]
    cmp al,byte ptr [bp+6]
    jbe short next_column
prepare_video:
    cmp byte ptr DGROUP:__video+0bh,0
    jz short select_console_color
    mov bh,0
    jmp short make_video_call
select_console_color:
    cmp word ptr DGROUP:__wclrnorm,0
    jz short normal_color
    mov bh,byte ptr DGROUP:__video+6
    jmp short make_video_call
normal_color:
    mov bh,byte ptr DGROUP:__video+4
make_video_call:
    mov ah,byte ptr [bp+0eh]
    mov al,byte ptr [bp+4]
    mov ch,byte ptr [bp+0ah]
    mov cl,byte ptr [bp+0ch]
    mov dh,byte ptr [bp+6]
    mov dl,byte ptr [bp+8]
    call __IBM_VIDEOINT
    pop di
    pop si
    mov sp,bp
    pop bp
    ret 0ch
__IBM_SCROLL endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
end
