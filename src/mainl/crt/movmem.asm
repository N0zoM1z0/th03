; Original Borland DOS large-model overlap-safe movmem and memmove.
; The original near N_PCMP@ arithmetic helper selects direction; source
; and destination far pointers are then copied with SI/DI and CX.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
extrn N_PCMP@:near
public _movmem
public _memmove
_movmem proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov cx,[bp+12]
    mov bx,[bp+10]
    mov dx,[bp+8]
    mov ax,[bp+6]
    call N_PCMP@
    jae short forward
    std
    mov ax,1
    jmp short direction_known
forward:
    cld
    xor ax,ax
direction_known:
    lds si,dword ptr [bp+6]
    les di,dword ptr [bp+10]
    mov cx,[bp+14]
    or ax,ax
    je short at_start
    add si,cx
    dec si
    add di,cx
    dec di
at_start:
    test di,1
    je short aligned
    jcxz short copy_done
    movsb
    dec cx
aligned:
    sub si,ax
    sub di,ax
    shr cx,1
    rep movsw
    jae short copy_done
    add si,ax
    add di,ax
    movsb
copy_done:
    cld
    pop ds
    pop di
    pop si
    pop bp
    retf
_movmem endp
_memmove proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+14]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push cs
    call near ptr _movmem
    add sp,10
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf
_memmove endp
_TEXT ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
end
