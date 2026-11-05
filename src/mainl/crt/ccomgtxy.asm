; Original Japanese Borland CRT ccomgtxy: PC-98/IBM machine dispatch.
; Preserve the actual 16-bit ABI and device-type branches.
.8086
extrn __NEC_GOTOXY:far,__IBM_GOTOXY:far,___conio_type:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __GOTOXY
__GOTOXY proc far
    push bp
    mov bp,sp
    push si
    push di
    mov al,byte ptr [bp+8]
    mov dl,byte ptr [bp+6]
    cmp word ptr DGROUP:___conio_type,2
    jnz short choose_ibm
    push ax
    push dx
    call __NEC_GOTOXY
    jmp short gotoxy_done
choose_ibm:
    cmp word ptr DGROUP:___conio_type,1
    jnz short gotoxy_done
    push ax
    push dx
    call __IBM_GOTOXY
gotoxy_done:
    pop di
    pop si
    pop bp
    retf 4
__GOTOXY endp
_TEXT ends
end
