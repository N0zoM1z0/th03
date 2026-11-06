; Original Borland istream >> float: genuine ten-byte long-double input,
; huge float bounds, ERANGE saturation, and native FPU status/waits.
.8086
.8087
EMUL
extrn @istream@$brsh$qmg:far
extrn __huge_flt:dword
extrn _errno:word
extrn FIDRQQ:far
extrn FIWRQQ:far
extrn FIERQQ:far
extrn __turboFloat:byte
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @istream@$brsh$qmf
@istream@$brsh$qmf proc far
    push bp
    mov bp,sp
    sub sp,0ch
    push si
    push di
    push ss
    lea ax,[bp-0ah]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @istream@$brsh$qmg
    add sp,8
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    test byte ptr es:[bx+0ah],86h
    jne short stream_float_done
    fld dword ptr DGROUP:__huge_flt
    fchs
    fld tbyte ptr [bp-0ah]
    fcompp
    fstsw word ptr [bp-0ch]
    fwait
    mov ax,[bp-0ch]
    sahf
    jae short check_float_positive
float_negative_overflow:
    mov word ptr DGROUP:_errno,22h
    fld dword ptr DGROUP:__huge_flt
    fchs
    jmp short float_store
check_float_positive:
    fld dword ptr DGROUP:__huge_flt
    fld tbyte ptr [bp-0ah]
    fcompp
    fstsw word ptr [bp-0ch]
    fwait
    mov ax,[bp-0ch]
    sahf
    jbe short float_from_input
    mov word ptr DGROUP:_errno,22h
    les bx,dword ptr [bp+0ah]
    mov dx,word ptr DGROUP:__huge_flt+2
    mov ax,word ptr DGROUP:__huge_flt
    mov word ptr es:[bx+2],dx
    mov word ptr es:[bx],ax
    jmp short stream_float_done
float_from_input:
    fld tbyte ptr [bp-0ah]
float_store:
    les bx,dword ptr [bp+0ah]
    fstp dword ptr es:[bx]
    fwait
stream_float_done:
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@istream@$brsh$qmf endp
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
end
