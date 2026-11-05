; Original NEC PC-98 character-console scrolling implementation.
; Three distinct original cases move or clear text rows by near helper
; calls, updating the original byte-sized caller arguments in place.
.8086
extrn __MOVETEXT:near,__NEC_ZAP_LINE:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __NEC_SCROLL
__NEC_SCROLL proc near
    push bp
    mov bp,sp
    push si
    push di
    cmp byte ptr [bp+4],0
    jnz short choose_scroll_direction
    mov al,[bp+6]
    sub al,[bp+10]
    inc al
    mov [bp+4],al
    jmp short check_full_clear
clear_from_top:
    push word ptr [bp+12]
    push word ptr [bp+8]
    push word ptr [bp+10]
    call __NEC_ZAP_LINE
    inc byte ptr [bp+10]
    dec byte ptr [bp+4]
check_full_clear:
    cmp byte ptr [bp+4],0
    ja short clear_from_top
    jmp short scroll_done
choose_scroll_direction:
    cmp byte ptr [bp+14],6
    jnz short scroll_forward
    push word ptr [bp+12]
    mov al,[bp+10]
    add al,[bp+4]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+12]
    push word ptr [bp+10]
    call __MOVETEXT
    jmp short check_clear_bottom
clear_from_bottom:
    push word ptr [bp+12]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __NEC_ZAP_LINE
    dec byte ptr [bp+6]
    dec byte ptr [bp+4]
check_clear_bottom:
    cmp byte ptr [bp+4],0
    ja short clear_from_bottom
    jmp short scroll_done
scroll_forward:
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    mov al,[bp+6]
    sub al,[bp+4]
    push ax
    push word ptr [bp+12]
    mov al,[bp+10]
    add al,[bp+4]
    push ax
    call __MOVETEXT
    jmp short check_clear_forward
clear_forward:
    push word ptr [bp+12]
    push word ptr [bp+8]
    push word ptr [bp+10]
    call __NEC_ZAP_LINE
    inc byte ptr [bp+10]
    dec byte ptr [bp+4]
check_clear_forward:
    cmp byte ptr [bp+4],0
    ja short clear_forward
scroll_done:
    pop di
    pop si
    pop bp
    ret 12
__NEC_SCROLL endp
_TEXT ends
end
