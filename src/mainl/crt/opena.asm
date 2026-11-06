; Original Borland low-level DOS open with flag conversion,
; genuine int 21h/AH=3Dh and __openfd state on success.
.8086
extrn __IOERROR:near
extrn __openfd:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __rtl_open,__open
__rtl_open proc far
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    mov al,1
    mov cx,[bp+0ah]
    test cx,2
    jne short open_mode_ready
    mov al,2
    test cx,4
    jne short open_mode_ready
    mov al,0
open_mode_ready:
    push ds
    lds dx,dword ptr [bp+6]
    mov cl,0f0h
    and cl,byte ptr [bp+0ah]
    or al,cl
    mov ah,3dh
    int 21h
    pop ds
    jb short open_error
    mov [bp-2],ax
    mov ax,[bp+0ah]
    and ax,0b8ffh
    or ax,8000h
    mov bx,[bp-2]
    add bx,bx
    mov word ptr DGROUP:__openfd[bx],ax
    mov ax,[bp-2]
    jmp short open_return
open_error:
    push ax
    call __IOERROR
open_return:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
__rtl_open endp
__open proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push cs
    call near ptr __rtl_open
    add sp,6
    pop di
    pop si
    pop bp
    retf
__open endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
