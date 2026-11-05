; Original Borland Japanese CRT stdec; complete 16-bit ABI leaf.
.8086
extrn @ios@basefield:dword
extrn @ios@setf$qll:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @dec$qm3ios
@dec$qm3ios proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr DGROUP:@ios@basefield+2
    push word ptr DGROUP:@ios@basefield
    xor ax,ax
    mov dx,16
    push ax
    push dx
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @ios@setf$qll
    add sp,12
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf
@dec$qm3ios endp
_TEXTA ends
end
