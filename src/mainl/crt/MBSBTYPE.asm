; Original Borland Japanese CRT MBSBTYPE; complete 16-bit ABI leaf.
.8086
extrn __mbbtype:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __mbsbtype
__mbsbtype proc far
    push bp
    mov bp,sp
    push si
    push di
    mov dx,0ffffh
check_byte:
    les bx,dword ptr [bp+6]
    cmp byte ptr es:[bx],0
    jnz short call_classifier
    mov ax,0ffffh
    jmp short return_type
call_classifier:
    push dx
    les bx,dword ptr [bp+6]
    mov al,byte ptr es:[bx]
    push ax
    call __mbbtype
    pop cx
    pop cx
    mov dx,ax
    cmp word ptr [bp+10],0
    jz short return_last
    inc word ptr [bp+6]
    dec word ptr [bp+10]
    jmp short check_byte
return_last:
    mov ax,dx
return_type:
    pop di
    pop si
    pop bp
    retf
__mbsbtype endp
_TEXT ends
end
