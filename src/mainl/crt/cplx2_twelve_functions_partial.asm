; PARTIAL LARGE-BOSS SOURCE: three complete FAR complex division
; implementations at original CODE offsets 0, 166, and 405, plus
; the complete acos/arg/asin/atan FAR bodies at +692/+1079/+1217/+1608.
; Native CODE through 2866 maps to original 2868. Two local FAR-call
; byte-length gaps at original CODE+799 and +984 remain unresolved.
; NOT the complete 5598-byte cplx2 CRT member, not source-linked.
; Rebuild/compare via scripts/probe_th03_cplx2_atan_partial.py.
.8086
.8087
EMUL
extrn @norm$qm7complex:far
extrn @complex@$brmul$qm7complex:far
extrn @$bmul$qm7complext1:far
extrn @$bnew$qui:far
extrn @abs$qm7complex:far
extrn _atan2:far
extrn _sqrt:far
extrn _cos:far
extrn _sin:far
extrn _log:far
extrn _exp:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @complex@$brdiv$qm7complex
@complex@$brdiv$qm7complex proc far
    push bp
    mov bp,sp
    sub sp,30h
    push si
    push di
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    call @norm$qm7complex
    fstp tbyte ptr [bp-0ah]
    push ss
    fwait
    mov dx,[bp+0ch]
    mov ax,[bp+0ah]
    mov [bp-0ch],dx
    mov [bp-0eh],ax
    les bx,dword ptr [bp-0eh]
    fld qword ptr es:[bx+8]
    fchs
    fstp qword ptr [bp-16h]
    fwait
    les bx,dword ptr [bp-0eh]
    fld qword ptr es:[bx]
    fstp qword ptr [bp-1eh]
    fld qword ptr [bp-1eh]
    fstp qword ptr [bp-30h]
    fld qword ptr [bp-16h]
    fstp qword ptr [bp-28h]
    fwait
    lea ax,[bp-30h]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @complex@$brmul$qm7complex
    add sp,0ch
    les bx,dword ptr [bp+6]
    fld qword ptr es:[bx]
    fld tbyte ptr [bp-0ah]
    fdivp st(1),st(0)
    les bx,dword ptr [bp+6]
    fstp qword ptr es:[bx]
    add bx,8
    fwait
    mov [bp-20h],bx
    fld qword ptr es:[bx]
    fld tbyte ptr [bp-0ah]
    fdivp st(1),st(0)
    mov es,[bp+8]
    mov bx,[bp-20h]
    fstp qword ptr es:[bx]
    fwait
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@complex@$brdiv$qm7complex endp


; Second complete FAR division operator; returns a constructed complex
; through the hidden return-object pointer (or original far new[] path).
public @$bdiv$qm7complext1
@$bdiv$qm7complext1 proc far
    push bp
    mov bp,sp
    sub sp,58h
    push si
    push di
    push word ptr [bp+10h]
    push word ptr [bp+0eh]
    call @norm$qm7complex
    fstp qword ptr [bp-8]
    push ss
    fwait
    mov dx,[bp+10h]
    mov ax,[bp+0eh]
    mov [bp-0ah],dx
    mov [bp-0ch],ax
    les bx,dword ptr [bp-0ch]
    fld qword ptr es:[bx+8]
    fchs
    fstp qword ptr [bp-14h]
    fwait
    les bx,dword ptr [bp-0ch]
    fld qword ptr es:[bx]
    fstp qword ptr [bp-1ch]
    fld qword ptr [bp-1ch]
    fstp qword ptr [bp-48h]
    fld qword ptr [bp-14h]
    fstp qword ptr [bp-40h]
    fwait
    lea ax,[bp-48h]
    push ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push ss
    lea ax,[bp-58h]
    push ax
    call @$bmul$qm7complext1
    add sp,10h
    lea ax,[bp-58h]
    mov [bp-1eh],ss
    mov [bp-20h],ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-22h],dx
    mov [bp-24h],ax
    les bx,dword ptr [bp-20h]
    fld qword ptr es:[bx+8]
    fdiv qword ptr [bp-8]
    fstp qword ptr [bp-2ch]
    fwait
    les bx,dword ptr [bp-20h]
    fld qword ptr es:[bx]
    fdiv qword ptr [bp-8]
    fstp qword ptr [bp-34h]
    fwait
    mov [bp-36h],dx
    mov [bp-38h],ax
    or ax,[bp-36h]
    jz short allocate_complex_result
    mov ax,[bp-38h]
    jmp short have_complex_result
allocate_complex_result:
    mov ax,16
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-36h],dx
    mov [bp-38h],ax
have_complex_result:
    or ax,dx
    jz short return_complex_result
    les bx,dword ptr [bp-38h]
    fld qword ptr [bp-34h]
    fstp qword ptr es:[bx]
    fld qword ptr [bp-2ch]
    fstp qword ptr es:[bx+8]
    fwait
return_complex_result:
    mov dx,[bp-36h]
    mov ax,[bp-38h]
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@$bdiv$qm7complext1 endp


; Third complete FAR division overload: scalar double over complex
; with real/imaginary temporaries, native x87 operations and allocation.
public @$bdiv$qdm7complex
@$bdiv$qdm7complex proc far
    push bp
    mov bp,sp
    sub sp,74h
    push si
    push di
    push word ptr [bp+14h]
    push word ptr [bp+12h]
    call @norm$qm7complex
    pop cx
    pop cx
    fstp qword ptr [bp-8]
    fwait
    mov dx,[bp+14h]
    mov ax,[bp+12h]
    mov [bp-0ah],dx
    mov [bp-0ch],ax
    les bx,dword ptr [bp-0ch]
    fld qword ptr es:[bx+8]
    fchs
    fstp qword ptr [bp-14h]
    fwait
    les bx,dword ptr [bp-0ch]
    fld qword ptr es:[bx]
    fstp qword ptr [bp-1ch]
    fld qword ptr [bp-1ch]
    fstp qword ptr [bp-64h]
    fld qword ptr [bp-14h]
    fstp qword ptr [bp-5ch]
    fwait
    lea ax,[bp-64h]
    mov [bp-1eh],ss
    mov [bp-20h],ax
    fld qword ptr [bp+0ah]
    fstp qword ptr [bp-28h]
    fwait
    les bx,dword ptr [bp-20h]
    fld qword ptr es:[bx+8]
    fmul qword ptr [bp-28h]
    fstp qword ptr [bp-30h]
    fwait
    les bx,dword ptr [bp-20h]
    fld qword ptr es:[bx]
    fmul qword ptr [bp-28h]
    fstp qword ptr [bp-38h]
    fld qword ptr [bp-38h]
    fstp qword ptr [bp-74h]
    fld qword ptr [bp-30h]
    fstp qword ptr [bp-6ch]
    fwait
    lea ax,[bp-74h]
    mov [bp-3ah],ss
    mov [bp-3ch],ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-3eh],dx
    mov [bp-40h],ax
    les bx,dword ptr [bp-3ch]
    fld qword ptr es:[bx+8]
    fdiv qword ptr [bp-8]
    fstp qword ptr [bp-48h]
    fwait
    les bx,dword ptr [bp-3ch]
    fld qword ptr es:[bx]
    fdiv qword ptr [bp-8]
    fstp qword ptr [bp-50h]
    fwait
    mov [bp-52h],dx
    mov [bp-54h],ax
    or ax,[bp-52h]
    jz short alloc_complex_division_result
    mov ax,[bp-54h]
    jmp short init_complex_division_result
alloc_complex_division_result:
    mov ax,16
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-52h],dx
    mov [bp-54h],ax
init_complex_division_result:
    or ax,dx
    jz short scalar_division_return
    les bx,dword ptr [bp-54h]
    fld qword ptr [bp-50h]
    fstp qword ptr es:[bx]
    fld qword ptr [bp-48h]
    fstp qword ptr es:[bx+8]
    fwait
scalar_division_return:
    mov dx,[bp-52h]
    mov ax,[bp-54h]
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@$bdiv$qdm7complex endp

; Fourth complete FAR complex acos overload, original CODE+692..1078.
; Uses the original double math constants -2.0 and 2.0f, local
; complex arg() at CODE+1079, real x87 operations and far result buffer.
public @acos$qm7complex
@acos$qm7complex proc far
    push bp
    mov bp,sp
    sub sp,64h
    push si
    push di
    les bx,dword ptr [bp+0ah]
    add bx,8
    mov ax,bx
    fld qword ptr es:[bx]
    les bx,dword ptr [bp+0ah]
    fld qword ptr es:[bx]
    fmul qword ptr DGROUP:complex_negative_two
    fmulp st(1),st(0)
    fstp qword ptr [bp-8]
    mov es,word ptr [bp+0ch]
    mov bx,ax
    fld qword ptr es:[bx]
    mov es,word ptr [bp+0ch]
    mov bx,ax
    fmul qword ptr es:[bx]
    mov bx,[bp+0ah]
    fld qword ptr es:[bx]
    les bx,dword ptr [bp+0ah]
    fmul qword ptr es:[bx]
    fld1
    fsubrp st(1),st(0)
    faddp st(1),st(0)
    fstp qword ptr [bp-10h]
    fld qword ptr [bp-10h]
    fstp qword ptr [bp-54h]
    fld qword ptr [bp-8]
    fstp qword ptr [bp-4ch]
    push ss
    fwait
    lea ax,[bp-54h]
    push ax
    call @arg$qm7complex
    pop cx
    pop cx
    fdiv dword ptr DGROUP:complex_two_float
    fstp qword ptr [bp-18h]
    push ss
    fwait
    lea ax,[bp-54h]
    push ax
    call @abs$qm7complex
    pop cx
    pop cx
    sub sp,8
    fstp qword ptr [bp-70h]
    fwait
    call _sqrt
    add sp,8
    fstp qword ptr [bp-20h]
    fld qword ptr [bp-18h]
    sub sp,8
    fstp qword ptr [bp-70h]
    fwait
    call _cos
    add sp,8
    fmul qword ptr [bp-20h]
    les bx,dword ptr [bp+0ah]
    fadd qword ptr es:[bx+8]
    fstp qword ptr [bp-28h]
    fld qword ptr [bp-18h]
    sub sp,8
    fstp qword ptr [bp-70h]
    fwait
    call _sin
    add sp,8
    fmul qword ptr [bp-20h]
    les bx,dword ptr [bp+0ah]
    fsubr qword ptr es:[bx]
    fstp qword ptr [bp-30h]
    fld qword ptr [bp-30h]
    fstp qword ptr [bp-64h]
    fld qword ptr [bp-28h]
    fstp qword ptr [bp-5ch]
    fwait
    push ss
    lea ax,[bp-64h]
    push ax
    call @abs$qm7complex
    pop cx
    pop cx
    sub sp,8
    fstp qword ptr [bp-70h]
    fwait
    call _log
    add sp,8
    fchs
    fstp qword ptr [bp-38h]
    push ss
    fwait
    lea ax,[bp-64h]
    push ax
    call @arg$qm7complex
    pop cx
    pop cx
    fstp qword ptr [bp-40h]
    fwait
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-42h],dx
    mov [bp-44h],ax
    or ax,[bp-42h]
    jz short acos_allocate
    mov ax,[bp-44h]
    jmp short acos_have_target
acos_allocate:
    mov ax,16
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-42h],dx
    mov [bp-44h],ax
acos_have_target:
    or ax,dx
    jz short acos_done
    les bx,dword ptr [bp-44h]
    fld qword ptr [bp-40h]
    fstp qword ptr es:[bx]
    fld qword ptr [bp-38h]
    fstp qword ptr es:[bx+8]
    fwait
acos_done:
    mov dx,[bp-42h]
    mov ax,[bp-44h]
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@acos$qm7complex endp

; Six complete original complex FAR bodies; TASM version has the
; two previously established shorter intra-segment FAR call encodings.
public @arg$qm7complex
@arg$qm7complex proc far
    push bp
    mov bp,sp
    sub sp,12h
    push si
    push di
    fld qword ptr DGROUP:complex_arg_zero_real
    fstp qword ptr [bp-12h]
    fld qword ptr DGROUP:complex_arg_zero_imag
    fstp qword ptr [bp-0ah]
    fwait
    les bx,dword ptr [bp+6]
    fld qword ptr es:[bx]
    fcomp qword ptr [bp-12h]
    fstsw word ptr [bp-2]
    fwait
    mov ax,[bp-2]
    sahf
    jnz short compute_arg_with_atan2
    les bx,dword ptr [bp+6]
    fld qword ptr es:[bx+8]
    fcomp qword ptr [bp-0ah]
    fstsw word ptr [bp-2]
    fwait
    mov ax,[bp-2]
    sahf
    jnz short compute_arg_with_atan2
    mov ax,1
    jmp short choose_arg_result
compute_arg_with_atan2:
    xor ax,ax
choose_arg_result:
    or ax,ax
    jz short call_atan2
    fldz
    jmp short arg_done
call_atan2:
    les bx,dword ptr [bp+6]
    fld qword ptr es:[bx]
    sub sp,8
    fstp qword ptr [bp-1eh]
    fwait
    les bx,dword ptr [bp+6]
    fld qword ptr es:[bx+8]
    sub sp,8
    fstp qword ptr [bp-26h]
    fwait
    call _atan2
    add sp,10h
arg_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@arg$qm7complex endp

; Native complete FAR asin(complex), original CODE+1217..1607.
public @asin$qm7complex
@asin$qm7complex proc far
    push bp
    mov bp,sp
    sub sp,64h
    push si
    push di
    les bx,dword ptr [bp+0ah]
    add bx,8
    mov ax,bx
    fld qword ptr es:[bx]
    les bx,dword ptr [bp+0ah]
    fld qword ptr es:[bx]
    fmul qword ptr DGROUP:complex_negative_two
    fmulp st(1),st(0)
    fstp qword ptr [bp-8]
    mov es,word ptr [bp+0ch]
    mov bx,ax
    fld qword ptr es:[bx]
    mov es,word ptr [bp+0ch]
    mov bx,ax
    fmul qword ptr es:[bx]
    mov bx,[bp+0ah]
    fld qword ptr es:[bx]
    les bx,dword ptr [bp+0ah]
    fmul qword ptr es:[bx]
    fld1
    fsubrp st(1),st(0)
    faddp st(1),st(0)
    fstp qword ptr [bp-10h]
    fld qword ptr [bp-10h]
    fstp qword ptr [bp-54h]
    fld qword ptr [bp-8]
    fstp qword ptr [bp-4ch]
    push ss
    fwait
    lea ax,[bp-54h]
    push ax
    call @arg$qm7complex
    pop cx
    pop cx
    fdiv dword ptr DGROUP:complex_two_float
    fstp qword ptr [bp-18h]
    push ss
    fwait
    lea ax,[bp-54h]
    push ax
    call @abs$qm7complex
    pop cx
    pop cx
    sub sp,8
    fstp qword ptr [bp-70h]
    fwait
    call _sqrt
    add sp,8
    fstp qword ptr [bp-20h]
    fld qword ptr [bp-18h]
    sub sp,8
    fstp qword ptr [bp-70h]
    fwait
    call _sin
    add sp,8
    fmul qword ptr [bp-20h]
    les bx,dword ptr [bp+0ah]
    fadd qword ptr es:[bx]
    fstp qword ptr [bp-28h]
    fld qword ptr [bp-18h]
    sub sp,8
    fstp qword ptr [bp-70h]
    fwait
    call _cos
    add sp,8
    fmul qword ptr [bp-20h]
    les bx,dword ptr [bp+0ah]
    fld qword ptr es:[bx+8]
    fchs
    faddp st(1),st(0)
    fstp qword ptr [bp-30h]
    fld qword ptr [bp-30h]
    fstp qword ptr [bp-64h]
    fld qword ptr [bp-28h]
    fstp qword ptr [bp-5ch]
    fwait
    push ss
    lea ax,[bp-64h]
    push ax
    call @abs$qm7complex
    pop cx
    pop cx
    sub sp,8
    fstp qword ptr [bp-70h]
    fwait
    call _log
    add sp,8
    fchs
    fstp qword ptr [bp-38h]
    push ss
    fwait
    lea ax,[bp-64h]
    push ax
    call @arg$qm7complex
    pop cx
    pop cx
    fstp qword ptr [bp-40h]
    fwait
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-42h],dx
    mov [bp-44h],ax
    or ax,[bp-42h]
    jz short asin_allocate
    mov ax,[bp-44h]
    jmp short asin_have_target
asin_allocate:
    mov ax,16
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-42h],dx
    mov [bp-44h],ax
asin_have_target:
    or ax,dx
    jz short asin_done
    les bx,dword ptr [bp-44h]
    fld qword ptr [bp-40h]
    fstp qword ptr es:[bx]
    fld qword ptr [bp-38h]
    fstp qword ptr es:[bx+8]
    fwait
asin_done:
    mov dx,[bp-42h]
    mov ax,[bp-44h]
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@asin$qm7complex endp


; Seventh complete original complex math FAR entry: atan(complex).
; Native x87 double arithmetic, logarithm, arg() and hidden FAR result ABI.
public @atan$qm7complex
@atan$qm7complex proc far
    push bp
    mov bp,sp
    sub sp,4eh
    push si
    push di
    les bx,dword ptr [bp+0ah]
    add bx,8
    mov [bp-3eh],bx
    fld qword ptr es:[bx]
    fld1
    faddp st(1),st(0)
    fstp qword ptr [bp-8]
    fwait
    les bx,dword ptr [bp+0ah]
    fld qword ptr es:[bx]
    les bx,dword ptr [bp+0ah]
    fmul qword ptr es:[bx]
    fstp qword ptr [bp-10h]
    fld qword ptr [bp-8]
    fmul qword ptr [bp-8]
    fadd qword ptr [bp-10h]
    fstp qword ptr [bp-18h]
    fld qword ptr es:[bx]
    fmul dword ptr DGROUP:complex_two_float
    fdiv qword ptr [bp-18h]
    fstp qword ptr [bp-20h]
    mov es,[bp+0ch]
    fwait
    mov bx,[bp-3eh]
    fld qword ptr es:[bx]
    fld1
    fsubrp st(1),st(0)
    fmul qword ptr [bp-8]
    fsub qword ptr [bp-10h]
    fdiv qword ptr [bp-18h]
    fstp qword ptr [bp-28h]
    fld qword ptr [bp-28h]
    fstp qword ptr [bp-4eh]
    fld qword ptr [bp-20h]
    fstp qword ptr [bp-46h]
    fwait
    push ss
    lea ax,[bp-4eh]
    push ax
    call @abs$qm7complex
    pop cx
    pop cx
    sub sp,8
    fstp qword ptr [bp-5ah]
    fwait
    call _log
    add sp,8
    fchs
    fdiv dword ptr DGROUP:complex_two_float
    fstp qword ptr [bp-30h]
    push ss
    fwait
    lea ax,[bp-4eh]
    push ax
    call @arg$qm7complex
    pop cx
    pop cx
    fdiv dword ptr DGROUP:complex_two_float
    fstp qword ptr [bp-38h]
    fwait
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-3ah],dx
    mov [bp-3ch],ax
    or ax,[bp-3ah]
    jz short atan_allocate
    mov ax,[bp-3ch]
    jmp short atan_have_target
atan_allocate:
    mov ax,16
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-3ah],dx
    mov [bp-3ch],ax
atan_have_target:
    or ax,dx
    jz short atan_return
    les bx,dword ptr [bp-3ch]
    fld qword ptr [bp-38h]
    fstp qword ptr es:[bx]
    fld qword ptr [bp-30h]
    fstp qword ptr es:[bx+8]
    fwait
atan_return:
    mov dx,[bp-3ah]
    mov ax,[bp-3ch]
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@atan$qm7complex endp


; Eighth complete original complex FAR procedure: cos(complex).
; Borland 80-bit intermediate exp/im-exp, 2.0f typed data and hidden result.
public @cos$qm7complex
@cos$qm7complex proc far
    push bp
    mov bp,sp
    sub sp,28h
    push si
    push di
    les bx,dword ptr [bp+0ah]
    fld qword ptr es:[bx+8]
    sub sp,8
    fstp qword ptr [bp-34h]
    fwait
    call _exp
    add sp,8
    fstp tbyte ptr [bp-0ah]
    fld1
    fld tbyte ptr [bp-0ah]
    fdivp st(1),st(0)
    fstp tbyte ptr [bp-14h]
    fwait
    les bx,dword ptr [bp+0ah]
    fld qword ptr es:[bx]
    sub sp,8
    fstp qword ptr [bp-34h]
    fwait
    call _sin
    add sp,8
    fld tbyte ptr [bp-14h]
    fld tbyte ptr [bp-0ah]
    fsubp st(1),st(0)
    fmulp st(1),st(0)
    fdiv dword ptr DGROUP:complex_two_float
    fstp qword ptr [bp-1ch]
    fwait
    les bx,dword ptr [bp+0ah]
    fld qword ptr es:[bx]
    sub sp,8
    fstp qword ptr [bp-34h]
    fwait
    call _cos
    add sp,8
    fld tbyte ptr [bp-14h]
    fld tbyte ptr [bp-0ah]
    faddp st(1),st(0)
    fmulp st(1),st(0)
    fdiv dword ptr DGROUP:complex_two_float
    fstp qword ptr [bp-24h]
    fwait
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-26h],dx
    mov [bp-28h],ax
    or ax,[bp-26h]
    jz short cos_allocate_result
    mov ax,[bp-28h]
    jmp short cos_have_target
cos_allocate_result:
    mov ax,16
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-26h],dx
    mov [bp-28h],ax
cos_have_target:
    or ax,dx
    jz short cos_done
    les bx,dword ptr [bp-28h]
    fld qword ptr [bp-24h]
    fstp qword ptr es:[bx]
    fld qword ptr [bp-1ch]
    fstp qword ptr es:[bx+8]
    fwait
cos_done:
    mov dx,[bp-26h]
    mov ax,[bp-28h]
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@cos$qm7complex endp

; Ninth complete original FAR cosh(complex).
public @cosh$qm7complex
@cosh$qm7complex proc far
    push bp
    mov bp,sp
    sub sp,28h
    push si
    push di
    les bx,dword ptr [bp+0ah]
    fld qword ptr es:[bx]
    sub sp,8
    fstp qword ptr [bp-34h]
    fwait
    call _exp
    add sp,8
    fstp tbyte ptr [bp-0ah]
    fld1
    fld tbyte ptr [bp-0ah]
    fdivp st(1),st(0)
    fstp tbyte ptr [bp-14h]
    fwait
    les bx,dword ptr [bp+0ah]
    fld qword ptr es:[bx+8]
    sub sp,8
    fstp qword ptr [bp-34h]
    fwait
    call _sin
    add sp,8
    fld tbyte ptr [bp-0ah]
    fld tbyte ptr [bp-14h]
    fsubp st(1),st(0)
    fmulp st(1),st(0)
    fdiv dword ptr DGROUP:complex_two_float
    fstp qword ptr [bp-1ch]
    fwait
    les bx,dword ptr [bp+0ah]
    fld qword ptr es:[bx+8]
    sub sp,8
    fstp qword ptr [bp-34h]
    fwait
    call _cos
    add sp,8
    fld tbyte ptr [bp-0ah]
    fld tbyte ptr [bp-14h]
    faddp st(1),st(0)
    fmulp st(1),st(0)
    fdiv dword ptr DGROUP:complex_two_float
    fstp qword ptr [bp-24h]
    fwait
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-26h],dx
    mov [bp-28h],ax
    or ax,[bp-26h]
    jz short cosh_allocate_result
    mov ax,[bp-28h]
    jmp short cosh_have_target
cosh_allocate_result:
    mov ax,16
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-26h],dx
    mov [bp-28h],ax
cosh_have_target:
    or ax,dx
    jz short cosh_done
    les bx,dword ptr [bp-28h]
    fld qword ptr [bp-24h]
    fstp qword ptr es:[bx]
    fld qword ptr [bp-1ch]
    fstp qword ptr es:[bx+8]
    fwait
cosh_done:
    mov dx,[bp-26h]
    mov ax,[bp-28h]
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@cosh$qm7complex endp


; Tenth complete FAR complex exponential, original CODE+2358..2563.
public @exp$qm7complex
@exp$qm7complex proc far
    push bp
    mov bp,sp
    sub sp,28h
    push si
    push di
    les bx,dword ptr [bp+0ah]
    fld qword ptr es:[bx+8]
    fstp qword ptr [bp-8]
    fwait
    les bx,dword ptr [bp+0ah]
    fld qword ptr es:[bx]
    sub sp,8
    fstp qword ptr [bp-34h]
    fwait
    call _exp
    add sp,8
    fstp qword ptr [bp-10h]
    fwait
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-12h],dx
    mov [bp-14h],ax
    fld qword ptr [bp-8]
    sub sp,8
    fstp qword ptr [bp-34h]
    fwait
    call _sin
    add sp,8
    fmul qword ptr [bp-10h]
    fstp qword ptr [bp-1ch]
    fld qword ptr [bp-8]
    sub sp,8
    fstp qword ptr [bp-34h]
    fwait
    call _cos
    add sp,8
    fmul qword ptr [bp-10h]
    fstp qword ptr [bp-24h]
    fwait
    mov dx,[bp-12h]
    mov ax,[bp-14h]
    mov [bp-26h],dx
    mov [bp-28h],ax
    or ax,[bp-26h]
    jz short exp_allocate
    mov ax,[bp-28h]
    jmp short exp_have_target
exp_allocate:
    mov ax,16
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-26h],dx
    mov [bp-28h],ax
exp_have_target:
    or ax,dx
    jz short exp_done
    les bx,dword ptr [bp-28h]
    fld qword ptr [bp-24h]
    fstp qword ptr es:[bx]
    fld qword ptr [bp-1ch]
    fstp qword ptr es:[bx+8]
    fwait
exp_done:
    mov dx,[bp-26h]
    mov ax,[bp-28h]
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@exp$qm7complex endp


; Eleventh original complex FAR log, using local arg + native abs/log.
public @log$qm7complex
@log$qm7complex proc far
    push bp
    mov bp,sp
    sub sp,14h
    push si
    push di
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push cs
    call near ptr @arg$qm7complex
    pop cx
    pop cx
    fstp qword ptr [bp-8]
    fwait
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    call @abs$qm7complex
    pop cx
    pop cx
    sub sp,8
    fstp qword ptr [bp-20h]
    fwait
    call _log
    add sp,8
    fstp qword ptr [bp-10h]
    fwait
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-12h],dx
    mov [bp-14h],ax
    or ax,[bp-12h]
    jz short log_allocate
    mov ax,[bp-14h]
    jmp short log_have_target
log_allocate:
    mov ax,16
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-12h],dx
    mov [bp-14h],ax
log_have_target:
    or ax,dx
    jz short log_done
    les bx,dword ptr [bp-14h]
    fld qword ptr [bp-10h]
    fstp qword ptr es:[bx]
    fld qword ptr [bp-8]
    fstp qword ptr es:[bx+8]
    fwait
log_done:
    mov dx,[bp-12h]
    mov ax,[bp-14h]
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@log$qm7complex endp


; Twelfth complete original FAR log10(complex): natural complex log,
; local FAR hidden result, base-10 factor and real new[] allocation.
public @log10$qm7complex
@log10$qm7complex proc far
    push bp
    mov bp,sp
    sub sp,2ch
    push si
    push di
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push ss
    lea ax,[bp-2ch]
    push ax
    push cs
    call near ptr @log$qm7complex
    add sp,8
    lea ax,[bp-2ch]
    mov [bp-2],ss
    mov [bp-4],ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-6],dx
    mov [bp-8],ax
    les bx,dword ptr [bp-4]
    fld qword ptr es:[bx+8]
    fmul qword ptr DGROUP:complex_log10_factor
    fstp qword ptr [bp-10h]
    fwait
    les bx,dword ptr [bp-4]
    fld qword ptr es:[bx]
    fmul qword ptr DGROUP:complex_log10_factor
    fstp qword ptr [bp-18h]
    fwait
    mov [bp-1ah],dx
    mov [bp-1ch],ax
    or ax,[bp-1ah]
    jz short log10_allocate
    mov ax,[bp-1ch]
    jmp short log10_ready
log10_allocate:
    mov ax,16
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-1ah],dx
    mov [bp-1ch],ax
log10_ready:
    or ax,dx
    jz short log10_done
    les bx,dword ptr [bp-1ch]
    fld qword ptr [bp-18h]
    fstp qword ptr es:[bx]
    fld qword ptr [bp-10h]
    fstp qword ptr es:[bx+8]
    fwait
log10_done:
    mov dx,[bp-1ah]
    mov ax,[bp-1ch]
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@log10$qm7complex endp

_TEXT ends
_DATA segment word public 'DATA'
complex_arg_zero_real label qword
    dq ? ; original DATA+0..7 unmaterialized
complex_arg_zero_imag label qword
    dq ? ; original DATA+8..15 unmaterialized
complex_negative_two label qword
    dq -2.0
complex_two_float label dword
    dd 2.0
complex_log10_factor label qword
    dq 0.434294481903251816667932416748954
_DATA ends
end
