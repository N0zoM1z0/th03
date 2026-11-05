; Original Borland ios::setf(long flags): three mutually exclusive
; 32-bit fmtflag groups plus ios unitbuf/status bit update.
.8086
extrn @ios@basefield:dword
extrn @ios@adjustfield:dword
extrn @ios@floatfield:dword
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ios@setf$ql
@ios@setf$ql proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    les bx,dword ptr [bp+6]
    mov dx,word ptr es:[bx+12h]
    mov ax,word ptr es:[bx+10h]
    mov [bp-2],dx
    mov [bp-4],ax
    mov dx,[bp+0ch]
    mov ax,[bp+0ah]
    and ax,word ptr DGROUP:@ios@adjustfield
    and dx,word ptr DGROUP:@ios@adjustfield+2
    or ax,dx
    jz short check_basefield
    mov dx,word ptr DGROUP:@ios@adjustfield+2
    mov ax,word ptr DGROUP:@ios@adjustfield
    not ax
    not dx
    and word ptr es:[bx+10h],ax
    and word ptr es:[bx+12h],dx
check_basefield:
    mov dx,[bp+0ch]
    mov ax,[bp+0ah]
    and ax,word ptr DGROUP:@ios@basefield
    and dx,word ptr DGROUP:@ios@basefield+2
    or ax,dx
    jz short check_floatfield
    mov dx,word ptr DGROUP:@ios@basefield+2
    mov ax,word ptr DGROUP:@ios@basefield
    not ax
    not dx
    les bx,dword ptr [bp+6]
    and word ptr es:[bx+10h],ax
    and word ptr es:[bx+12h],dx
check_floatfield:
    mov dx,[bp+0ch]
    mov ax,[bp+0ah]
    and ax,word ptr DGROUP:@ios@floatfield
    and dx,word ptr DGROUP:@ios@floatfield+2
    or ax,dx
    jz short store_new_flags
    mov dx,word ptr DGROUP:@ios@floatfield+2
    mov ax,word ptr DGROUP:@ios@floatfield
    not ax
    not dx
    les bx,dword ptr [bp+6]
    and word ptr es:[bx+10h],ax
    and word ptr es:[bx+12h],dx
store_new_flags:
    les bx,dword ptr [bp+6]
    mov dx,[bp+0ch]
    mov ax,[bp+0ah]
    or word ptr es:[bx+10h],ax
    or word ptr es:[bx+12h],dx
    test byte ptr es:[bx+10h],1
    je short clear_implicit_buffer_flag
    or word ptr es:[bx+0ch],100h
    jmp short finish_flags
clear_implicit_buffer_flag:
    les bx,dword ptr [bp+6]
    and word ptr es:[bx+0ch],0feffh
finish_flags:
    mov dx,[bp-2]
    mov ax,[bp-4]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@ios@setf$ql endp
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
end
