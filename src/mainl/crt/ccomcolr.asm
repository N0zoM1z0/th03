; Original Borland Japanese CRT NEC/IBM text color and attributes dispatcher.
; Six complete far APIs retain caller cleanup, machine-selection semantics,
; and the precise original DGROUP/external 16-bit relocations.
.8086
extrn ___nec_textcolor:far
extrn ___nec_textbackground:far
extrn ___nec_textattr:far
extrn ___nec_highvideo:far
extrn ___nec_lowvideo:far
extrn ___nec_normvideo:far
extrn ___ibm_textcolor:far
extrn ___ibm_textbackground:far
extrn ___ibm_textattr:far
extrn ___ibm_highvideo:far
extrn ___ibm_lowvideo:far
extrn ___ibm_normvideo:far
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

public _textcolor
_textcolor proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    cmp word ptr DGROUP:___conio_type,2
    jnz short textcolor_check_ibm
    push ax
    call ___nec_textcolor
    jmp short textcolor_clear_one_argument
textcolor_check_ibm:
    cmp word ptr DGROUP:___conio_type,1
    jnz short textcolor_done
    push ax
    call ___ibm_textcolor
textcolor_clear_one_argument:
    pop cx
textcolor_done:
    pop di
    pop si
    pop bp
    retf
_textcolor endp

public _textbackground
_textbackground proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    cmp word ptr DGROUP:___conio_type,2
    jnz short textbackground_check_ibm
    push ax
    call ___nec_textbackground
    jmp short textbackground_clear_one_argument
textbackground_check_ibm:
    cmp word ptr DGROUP:___conio_type,1
    jnz short textbackground_done
    push ax
    call ___ibm_textbackground
textbackground_clear_one_argument:
    pop cx
textbackground_done:
    pop di
    pop si
    pop bp
    retf
_textbackground endp

public _textattr
_textattr proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    cmp word ptr DGROUP:___conio_type,2
    jnz short textattr_check_ibm
    push ax
    call ___nec_textattr
    jmp short textattr_clear_one_argument
textattr_check_ibm:
    cmp word ptr DGROUP:___conio_type,1
    jnz short textattr_done
    push ax
    call ___ibm_textattr
textattr_clear_one_argument:
    pop cx
textattr_done:
    pop di
    pop si
    pop bp
    retf
_textattr endp

public _highvideo
_highvideo proc far
    push si
    push di
    cmp word ptr DGROUP:___conio_type,2
    jnz short highvideo_check_ibm
    call ___nec_highvideo
    jmp short highvideo_done
highvideo_check_ibm:
    cmp word ptr DGROUP:___conio_type,1
    jnz short highvideo_done
    call ___ibm_highvideo
highvideo_done:
    pop di
    pop si
    retf
_highvideo endp

public _lowvideo
_lowvideo proc far
    push si
    push di
    cmp word ptr DGROUP:___conio_type,2
    jnz short lowvideo_check_ibm
    call ___nec_lowvideo
    jmp short lowvideo_done
lowvideo_check_ibm:
    cmp word ptr DGROUP:___conio_type,1
    jnz short lowvideo_done
    call ___ibm_lowvideo
lowvideo_done:
    pop di
    pop si
    retf
_lowvideo endp

public _normvideo
_normvideo proc far
    push si
    push di
    cmp word ptr DGROUP:___conio_type,2
    jnz short normvideo_check_ibm
    call ___nec_normvideo
    jmp short normvideo_done
normvideo_check_ibm:
    cmp word ptr DGROUP:___conio_type,1
    jnz short normvideo_done
    call ___ibm_normvideo
normvideo_done:
    pop di
    pop si
    retf
_normvideo endp
_TEXT ends
end
