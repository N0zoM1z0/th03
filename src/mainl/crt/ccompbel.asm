; Original Japanese Borland CRT ccompbel: PC-98/IBM machine dispatch.
; Preserve the actual 16-bit ABI and device-type branches.
.8086
extrn ___nec_cputbell:far,___ibm_cputbell:far,___conio_type:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __cputbell
__cputbell proc far
    push si
    push di
    cmp word ptr DGROUP:___conio_type,2
    jnz short try_ibm
    call ___nec_cputbell
    jmp short bell_done
try_ibm:
    cmp word ptr DGROUP:___conio_type,1
    jnz short bell_done
    call ___ibm_cputbell
bell_done:
    pop di
    pop si
    retf
__cputbell endp
_TEXT ends
end
