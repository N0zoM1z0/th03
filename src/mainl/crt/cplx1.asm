; Original Borland complex double-precision arithmetic.
; TASM EMUL produces the genuine FIERQQ/FIDRQQ/FIWRQQ x87 fixups.
; Four native FAR entries: abs, norm, complex::operator*= and operator*.
.8086
.8087
EMUL
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @abs$qm7complex,@norm$qm7complex
public @complex@$brmul$qm7complex,@$bmul$qm7complext1

@abs$qm7complex proc far
    push bp
    mov bp,sp
    sub sp,0ah
    push si
    push di
    les bx,dword ptr [bp+6]
    fld qword ptr es:[bx]
    fmul st(0),st(0)
    fld qword ptr es:[bx+8]
    fmul st(0),st(0)
    faddp st(1),st(0)
    fsqrt
    fstp tbyte ptr [bp-0ah]
    fld tbyte ptr [bp-0ah]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@abs$qm7complex endp

@norm$qm7complex proc far
    push bp
    mov bp,sp
    sub sp,0ah
    push si
    push di
    les bx,dword ptr [bp+6]
    fld qword ptr es:[bx]
    fmul st(0),st(0)
    fld qword ptr es:[bx+8]
    fmul st(0),st(0)
    faddp st(1),st(0)
    fstp tbyte ptr [bp-0ah]
    fld tbyte ptr [bp-0ah]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@norm$qm7complex endp

@complex@$brmul$qm7complex proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+0ah]
    fld qword ptr es:[bx+8]
    fld st(0)
    fld qword ptr es:[bx]
    fld st(0)
    les bx,dword ptr [bp+6]
    fmul qword ptr es:[bx+8]
    fxch st(1)
    fmul qword ptr es:[bx]
    fxch st(2)
    fmul qword ptr es:[bx]
    fxch st(3)
    fmul qword ptr es:[bx+8]
    fsubp st(2),st(0)
    faddp st(2),st(0)
    fstp qword ptr es:[bx]
    fstp qword ptr es:[bx+8]
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf
@complex@$brmul$qm7complex endp

@$bmul$qm7complext1 label far
    push bp
    mov bp,sp
    sub sp,28h
    push si
    push di
    les bx,dword ptr [bp+0ah]
    add bx,8
    mov [bp-26h],bx
    fld qword ptr es:[bx]
    les bx,dword ptr [bp+0eh]
    add bx,8
    mov [bp-28h],bx
    fmul qword ptr es:[bx]
    les bx,dword ptr [bp+0ah]
    fld qword ptr es:[bx]
    les bx,dword ptr [bp+0eh]
    fmul qword ptr es:[bx]
    fsubrp st(1),st(0)
    fstp qword ptr [bp-8]
    mov es,word ptr [bp+0ch]
    fwait
_TEXT ends
extrn @$bnew$qui:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
    mov bx,[bp-26h]
    fld qword ptr es:[bx]
    les bx,dword ptr [bp+0eh]
    fmul qword ptr es:[bx]
    mov bx,[bp-28h]
    fld qword ptr es:[bx]
    les bx,dword ptr [bp+0ah]
    fmul qword ptr es:[bx]
    faddp st(1),st(0)
    fstp qword ptr [bp-10h]
    fwait
    fld qword ptr [bp-10h]
    fstp qword ptr [bp-18h]
    fld qword ptr [bp-8]
    fstp qword ptr [bp-20h]
    fwait
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-22h],dx
    mov [bp-24h],ax
    or ax,[bp-22h]
    jz short allocate_result
    mov ax,[bp-24h]
    jmp short store_result
allocate_result:
    mov ax,16
    push ax
    call far ptr @$bnew$qui
    pop cx
    mov [bp-22h],dx
    mov [bp-24h],ax
store_result:
    or ax,dx
    jz short return_result
    les bx,dword ptr [bp-24h]
    fld qword ptr [bp-20h]
    fstp qword ptr es:[bx]
    fld qword ptr [bp-18h]
    fstp qword ptr es:[bx+8]
    fwait
return_result:
    mov dx,[bp-22h]
    mov ax,[bp-24h]
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
