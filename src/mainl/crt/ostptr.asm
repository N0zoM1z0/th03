; Original Borland ostream insertion of a FAR pointer:
; preserve ios fmtflags, select native hexadecimal pointer style,
; emit via ulong insertion, and restore the old formatting state.
.8086
extrn @ios@basefield:dword
extrn @ios@adjustfield:dword
extrn @ios@flags$ql:far
extrn @ios@setf$qll:far
extrn @ostream@$blsh$qul:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostream@$blsh$qnv
@ostream@$blsh$qnv proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    mov dx,word ptr es:[bx+12h]
    mov ax,word ptr es:[bx+10h]
    mov [bp-2],dx
    mov [bp-4],ax
    mov dx,word ptr DGROUP:@ios@basefield+2
    mov ax,word ptr DGROUP:@ios@basefield
    or ax,word ptr DGROUP:@ios@adjustfield
    or ax,80h
    or dx,word ptr DGROUP:@ios@adjustfield+2
    push dx
    push ax
    xor ax,ax
    mov dx,0c8h
    push ax
    push dx
    les bx,dword ptr [bp+6]
    push es
    push word ptr es:[bx]
    call @ios@setf$qll
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    mov word ptr es:[bx+18h],30h
    mov word ptr es:[bx+16h],0ah
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @ostream@$blsh$qul
    push word ptr [bp-2]
    push word ptr [bp-4]
    les bx,dword ptr [bp+6]
    push es
    push word ptr es:[bx]
    call @ios@flags$ql
    add sp,1ch
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@ostream@$blsh$qnv endp
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
end
