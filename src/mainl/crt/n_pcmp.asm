; Compare huge pointers DX:AX and CX:BX. Return ordering in CPU flags.
; Segment additions wrap at 16 bits, offsets are reduced to their low nibble.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public N_PCMP@
N_PCMP@ proc near
    push cx
    mov ch,al
    mov cl,4
    shr ax,cl
    add dx,ax
    mov al,ch
    mov ah,bl
    shr bx,cl
    pop cx
    add cx,bx
    mov bl,ah
    and ax,15
    and bx,15
    cmp dx,cx
    jne compare_done
    cmp ax,bx
compare_done:
    ret
N_PCMP@ endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
end
