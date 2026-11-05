; Original Japanese Borland CRT ccomwhxy: PC-98/IBM machine dispatch.
; Preserve the actual 16-bit ABI and device-type branches.
.8086
extrn __NEC_WHEREXY:near,__IBM_WHEREXY:near,___conio_type:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __WHEREXY
__WHEREXY proc near
    push si
    push di
    cmp word ptr DGROUP:___conio_type,2
    jnz short check_ibm
    call __NEC_WHEREXY
    jmp short wherexy_done
check_ibm:
    cmp word ptr DGROUP:___conio_type,1
    jnz short unsupported
    call __IBM_WHEREXY
    jmp short wherexy_done
unsupported:
    xor ax,ax
wherexy_done:
    pop di
    pop si
    ret
__WHEREXY endp
_TEXT ends
end
