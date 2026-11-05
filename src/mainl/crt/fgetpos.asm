; Original Borland Japanese CRT fgetpos; complete 16-bit ABI leaf.
.8086
extrn _ftell:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _fgetpos
_fgetpos proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _ftell
    pop cx
    pop cx
    les bx,dword ptr [bp+10]
    mov word ptr es:[bx+2],dx
    mov word ptr es:[bx],ax
    cmp dx,-1
    jnz short good_position
    cmp ax,0ffffh
    jnz short good_position
    mov ax,0ffffh
    jmp short return_status
good_position:
    xor ax,ax
return_status:
    pop di
    pop si
    pop bp
    retf
_fgetpos endp
_TEXT ends
end
