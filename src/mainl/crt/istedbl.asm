; Original Borland istream >> double. Read native long-double input,
; compare x87 +/- HUGE_VAL, set ERANGE and store real FAR double.
.8086
.8087
EMUL
extrn @istream@$brsh$qmg:far
extrn __huge_dble:qword
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
public @istream@$brsh$qmd
@istream@$brsh$qmd proc far
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
    jne short stream_double_done
    fld qword ptr DGROUP:__huge_dble
    fchs
    fld tbyte ptr [bp-0ah]
    fcompp
    fstsw word ptr [bp-0ch]
    fwait
    mov ax,[bp-0ch]
    sahf
    jae short double_check_high
double_overflow:
    mov word ptr DGROUP:_errno,22h
    jmp short double_good
double_check_high:
    fld qword ptr DGROUP:__huge_dble
    fld tbyte ptr [bp-0ah]
    fcompp
    fstsw word ptr [bp-0ch]
    fwait
    mov ax,[bp-0ch]
    sahf
    ja short double_overflow
    fld tbyte ptr [bp-0ah]
    les bx,dword ptr [bp+0ah]
    fstp qword ptr es:[bx]
double_good:
    fwait
stream_double_done:
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@istream@$brsh$qmd endp
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
end
