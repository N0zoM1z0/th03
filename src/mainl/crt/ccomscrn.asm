; Original Borland Japanese CRT ccomscrn; complete 16-bit ABI leaf.
.8086
extrn __NEC_MOVELINE:near
extrn __IBM_MOVELINE:near
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
public __MOVELINE
__MOVELINE proc near
    push bp
    mov bp,sp
    push si
    push di
    mov al,byte ptr [bp+12]
    mov dl,byte ptr [bp+10]
    mov bl,byte ptr [bp+8]
    mov cl,byte ptr [bp+6]
    cmp word ptr DGROUP:___conio_type,2
    jnz short check_ibm
    push ax
    push dx
    push bx
    push cx
    push word ptr [bp+4]
    call __NEC_MOVELINE
    jmp short after_ibm_call
check_ibm:
    cmp word ptr DGROUP:___conio_type,1
    jnz short default_done
    push ax
    push dx
    push bx
    push cx
    push word ptr [bp+4]
    call __IBM_MOVELINE
after_ibm_call:
    jmp short dispatch_done
default_done:
    xor ax,ax
dispatch_done:
    pop di
    pop si
    pop bp
    ret 10
__MOVELINE endp
_TEXT ends
end
