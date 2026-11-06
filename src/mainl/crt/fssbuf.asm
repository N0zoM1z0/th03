; Original Borland fstreambase::setbuf, real filebuf FAR virtual
; setbuf dispatch, and native ios::clear/setstate outcome.
.8086
extrn @ios@clear$qi:far
extrn @ios@setstate$qi:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @fstreambase@setbuf$qnci
@fstreambase@setbuf$qnci proc far
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    push word ptr [bp+0eh]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    mov ax,[bp+6]
    add ax,4
    mov [bp-2],ax
    push word ptr [bp+8]
    push ax
    mov es,[bp+8]
    mov bx,[bp-2]
    mov bx,word ptr es:[bx]
    call dword ptr [bx+4]
    add sp,0ah
    or ax,dx
    je short failed_setbuf
    xor ax,ax
    push ax
    les bx,dword ptr [bp+6]
    push es
    push word ptr es:[bx]
    call @ios@clear$qi
    jmp short state_complete
failed_setbuf:
    mov ax,2
    push ax
    les bx,dword ptr [bp+6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
state_complete:
    add sp,6
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@fstreambase@setbuf$qnci endp
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
end
