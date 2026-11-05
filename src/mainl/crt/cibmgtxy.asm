; IBM BIOS cursor setter: original 16-bit far ABI and near
; __IBM_VIDEOINT service (AH=2, BH=page 0, DL/DH positions).
.8086
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
public __IBM_GOTOXY
__IBM_GOTOXY:
    push bp
    mov bp,sp
    push si
    push di
    mov dl,[bp+8]
    mov dh,[bp+6]
    mov ah,2
    mov bh,0
    call __IBM_VIDEOINT
    pop di
    pop si
    pop bp
    retf 4
_TEXT ends
end
