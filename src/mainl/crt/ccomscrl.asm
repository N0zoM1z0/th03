; Original Borland Japanese CRT ccomscrl; complete 16-bit ABI leaf.
.8086
extrn __NEC_SCROLL:near
extrn __IBM_SCROLL:near
extrn ___conio_type:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __SCROLL
__SCROLL proc near
    push bp
    mov bp,sp
    push si
    push di
    mov al,byte ptr [bp+14]
    mov dl,byte ptr [bp+12]
    mov bl,byte ptr [bp+10]
    mov cl,byte ptr [bp+8]
    cmp word ptr DGROUP:___conio_type,2
    jnz short check_ibm
    push ax
    push dx
    push bx
    push cx
    push word ptr [bp+6]
    push word ptr [bp+4]
    call __NEC_SCROLL
    jmp short dispatch_done
check_ibm:
    cmp word ptr DGROUP:___conio_type,1
    jnz short dispatch_done
    push ax
    push dx
    push bx
    push cx
    push word ptr [bp+6]
    push word ptr [bp+4]
    call __IBM_SCROLL
dispatch_done:
    pop di
    pop si
    pop bp
    ret 12
__SCROLL endp
_TEXT ends
end
