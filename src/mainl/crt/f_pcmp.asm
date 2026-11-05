; Far-call form of the Borland 16:16 physical pointer comparator.
; Exports the original two names at the same offset and returns flags.
.8086
_TEXT segment byte public 'CODE'
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public F_PCMP@,PCMP@
F_PCMP@:
PCMP@:
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
    and ax,0fh
    and bx,0fh
    cmp dx,cx
    jne ptr_cmp_done
    cmp ax,bx
ptr_cmp_done:
    retf
_TEXT ends
end
