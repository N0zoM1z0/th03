; Original Japanese Borland CRT ccomdely: PC-98/IBM machine dispatch.
; Preserve the actual 16-bit ABI and device-type branches.
.8086
extrn ___nec_delay:far,___ibm_delay:far,___conio_type:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _delay
_delay proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    cmp word ptr DGROUP:___conio_type,2
    jnz short check_ibm
    push ax
    call ___nec_delay
    jmp short clean_one_argument
check_ibm:
    cmp word ptr DGROUP:___conio_type,1
    jnz short dispatch_done
    push ax
    call ___ibm_delay
clean_one_argument:
    pop cx
dispatch_done:
    pop di
    pop si
    pop bp
    retf
_delay endp
_TEXT ends
end
