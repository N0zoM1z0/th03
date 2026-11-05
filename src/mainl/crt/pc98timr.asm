; Original PC-98 timer callback handler and FAR timer control API.
; Retains IRQ stack image, exact INT 1Ch registration, and a
; five-byte DOS-global callback pointer / active flag state.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
timer_irq_handler proc near
    push ax
    push bx
    push cx
    push dx
    push es
    push ds
    push si
    push di
    push bp
    mov bp,seg DGROUP
    mov ds,bp
    mov bp,sp
    sub sp,4
    cld
    mov dx,word ptr DGROUP:timer_callback+2
    mov ax,word ptr DGROUP:timer_callback
    mov [bp-2],dx
    mov [bp-4],ax
    mov word ptr DGROUP:timer_callback+2,0
    mov word ptr DGROUP:timer_callback,0
    mov byte ptr DGROUP:timer_busy,0
    or ax,[bp-2]
    jz short irq_done
    call dword ptr [bp-4]
irq_done:
    mov sp,bp
    pop bp
    pop di
    pop si
    pop ds
    pop es
    pop dx
    pop cx
    pop bx
    pop ax
    iret
timer_irq_handler endp

public _pc98timer
_pc98timer proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    pushf
    cli
    mov dx,word ptr DGROUP:timer_callback+2
    mov ax,word ptr DGROUP:timer_callback
    mov [bp-2],dx
    mov [bp-4],ax
    mov dx,[bp+0ah]
    mov ax,[bp+8]
    mov word ptr DGROUP:timer_callback+2,dx
    mov word ptr DGROUP:timer_callback,ax
    mov byte ptr DGROUP:timer_busy,1
    or ax,[bp+0ah]
    jnz short register_callback
    mov word ptr [bp+6],1
register_callback:
    mov cx,[bp+6]
    push cs
    pop es
    mov bx,offset _TEXT:timer_irq_handler
    mov ah,2
    int 1ch
    mov ax,[bp+8]
    or ax,[bp+0ah]
    jnz short timer_registered
    sti
poll_timer:
    cmp byte ptr DGROUP:timer_busy,0
    jnz short poll_timer
timer_registered:
    popf
    mov dx,[bp-2]
    mov ax,[bp-4]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_pc98timer endp
_TEXT ends
_DATA segment word public 'DATA'
timer_callback dd 0
timer_busy db 0
_DATA ends
end
