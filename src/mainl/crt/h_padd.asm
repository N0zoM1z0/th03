; Normalize DX:AX +/- signed CX:BX into a 20-bit huge pointer.
; Carry/borrow across the offset word changes the segment by 1000h paragraphs.
; Negative deltas reverse the operation, sharing the opposite magnitude body.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public N_PADD@, F_PADD@, PADD@, N_PSUB@, F_PSUB@, PSUB@
N_PADD@:
    pop es
    push cs
    push es
F_PADD@ label far
PADD@ label far
    or cx,cx
    jge add_magnitude
    not bx
    not cx
    add bx,1
    adc cx,0
    jmp short subtract_magnitude
add_magnitude:
    add ax,bx
    jnc add_paragraphs
    add dx,1000h
add_paragraphs:
    mov ch,cl
    mov cl,4
    shl ch,cl
    add dh,ch
    mov ch,al
    shr ax,cl
    add dx,ax
    mov al,ch
    and ax,15
    retf
N_PSUB@:
    pop es
    push cs
    push es
F_PSUB@ label far
PSUB@ label far
    or cx,cx
    jge subtract_magnitude
    not bx
    not cx
    add bx,1
    adc cx,0
    jmp short add_magnitude
subtract_magnitude:
    sub ax,bx
    jnc subtract_paragraphs
    sub dx,1000h
subtract_paragraphs:
    mov bh,cl
    mov cl,4
    shl bh,cl
    xor bl,bl
    sub dx,bx
    mov ch,al
    shr ax,cl
    add dx,ax
    mov al,ch
    and ax,15
    retf
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
end
