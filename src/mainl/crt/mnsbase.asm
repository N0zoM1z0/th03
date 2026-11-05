; Original Borland setbase(int) manipulator: genuine ios format masks,
; far setf callback and native six-byte C++ manipulator allocation.
.8086
extrn @$bnew$qui:far
extrn @ios@basefield:dword
extrn @ios@setf$qll:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP

basefield_setter proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    mov ax,[bp+0ah]
    mov word ptr [bp-2],0
    mov word ptr [bp-4],0
    cmp ax,16
    jne short decimal_base
    mov word ptr [bp-2],0
    mov word ptr [bp-4],40h
    jmp short have_base_flags
decimal_base:
    cmp ax,10
    jne short octal_base
    mov word ptr [bp-2],0
    mov word ptr [bp-4],10h
    jmp short have_base_flags
octal_base:
    cmp ax,8
    jne short have_base_flags
    mov word ptr [bp-2],0
    mov word ptr [bp-4],20h
have_base_flags:
    push word ptr DGROUP:@ios@basefield+2
    push word ptr DGROUP:@ios@basefield
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @ios@setf$qll
    add sp,0ch
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
basefield_setter endp

public @setbase$qi
@setbase$qi proc far
    push bp
    mov bp,sp
    sub sp,6
    push si
    push di
    mov ax,[bp+0ah]
    mov [bp-2],ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-4],dx
    mov [bp-6],ax
    or ax,[bp-4]
    jz short allocate_setbase
    mov ax,[bp-6]
    jmp short init_setbase
allocate_setbase:
    mov ax,6
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-4],dx
    mov [bp-6],ax
init_setbase:
    or ax,dx
    jz short return_manipulator
    les bx,dword ptr [bp-6]
    mov word ptr es:[bx+2],seg basefield_setter
    mov word ptr es:[bx],offset basefield_setter
    mov ax,[bp-2]
    mov word ptr es:[bx+4],ax
return_manipulator:
    mov dx,[bp-4]
    mov ax,[bp-6]
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@setbase$qi endp
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
end
