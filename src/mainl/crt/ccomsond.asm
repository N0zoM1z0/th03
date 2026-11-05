; Original NEC/IBM speaker frequency and silence machine multiplexer.
.8086
extrn ___nec_sound:far,___nec_nosound:far
extrn ___ibm_sound:far,___ibm_nosound:far
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
public _sound,_nosound
_sound proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    cmp word ptr DGROUP:___conio_type,2
    jnz short test_ibm_sound
    push ax
    call ___nec_sound
    jmp short clean_sound_arg
test_ibm_sound:
    cmp word ptr DGROUP:___conio_type,1
    jnz short sound_done
    push ax
    call ___ibm_sound
clean_sound_arg:
    pop cx
sound_done:
    pop di
    pop si
    pop bp
    retf
_sound endp
_nosound proc far
    push si
    push di
    cmp word ptr DGROUP:___conio_type,2
    jnz short test_ibm_nosound
    call ___nec_nosound
    jmp short nosound_done
test_ibm_nosound:
    cmp word ptr DGROUP:___conio_type,1
    jnz short nosound_done
    call ___ibm_nosound
nosound_done:
    pop di
    pop si
    retf
_nosound endp
_TEXT ends
end
