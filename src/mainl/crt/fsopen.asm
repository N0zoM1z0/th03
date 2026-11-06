; Original Borland fstreambase::open: real filebuf open,
; mode translation and ios::clear state update.
.8086
extrn @ios@clear$qi:far
extrn @filebuf@open$qnxcii:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @fstreambase@open$qnxcii
@fstreambase@open$qnxcii proc far
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+0eh]
    test dl,8
    je short mode_check
    or dx,2
    jmp short mode_ready
mode_check:
    mov ax,dx
    and ax,0fh
    cmp ax,2
    jne short mode_ready
    or dx,10h
mode_ready:
    les bx,dword ptr [bp+6]
    cmp word ptr es:[bx+2eh],0
    je short open_new
    mov ax,2
    jmp short set_stream_state
open_new:
    push word ptr [bp+10h]
    push dx
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    mov ax,[bp+6]
    add ax,4
    push word ptr [bp+8]
    push ax
    call @filebuf@open$qnxcii
    add sp,0ch
    or ax,dx
    je short open_failed
    xor ax,ax
    jmp short set_stream_state
open_failed:
    mov ax,4
set_stream_state:
    push ax
    les bx,dword ptr [bp+6]
    push es
    push word ptr es:[bx]
    call @ios@clear$qi
    add sp,6
    pop di
    pop si
    pop bp
    retf
@fstreambase@open$qnxcii endp
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
end
