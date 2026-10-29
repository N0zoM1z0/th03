; Build a DOS counted command tail. Near entry, three far arguments and RET12.
; The third pointer's presence controls argument copying; its contents are unused.
.8086
extrn _malloc:far,_strlen:far,__stpcpy:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __DOSCMD
__DOSCMD proc near
    push bp
    mov bp,sp
    sub sp,14
    push si
    push di
    ; BP-2 size, BP-6/-4 argv cursor, BP-10/-8 raw allocation,
    ; BP-14/-12 output cursor. Size arithmetic intentionally wraps16 bits.
    mov word ptr [bp-2],3
    mov ax,[bp+8]
    or ax,[bp+10]
    je count_arguments
    push word ptr [bp+10]
    push word ptr [bp+8]
    call _strlen
    pop cx
    pop cx
    add ax,[bp-2]
    inc ax
    mov [bp-2],ax
count_arguments:
    mov dx,[bp+6]
    mov ax,[bp+4]
    mov [bp-4],dx
    mov [bp-6],ax
    jmp short argument_count_test
argument_count:
    les bx,[bp-6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    call _strlen
    pop cx
    pop cx
    add ax,[bp-2]
    inc ax
    mov [bp-2],ax
    add word ptr [bp-6],4
argument_count_test:
    les bx,[bp-6]
    mov ax,es:[bx]
    or ax,es:[bx+2]
    jne argument_count
    push word ptr [bp-2]
    call _malloc
    pop cx
    mov [bp-8],dx
    mov [bp-10],ax
    or ax,dx
    jne command_allocated
    xor dx,dx
    xor ax,ax
    jmp command_done
command_allocated:
    mov dx,[bp-8]
    mov ax,[bp-10]
    inc ax
    mov [bp-12],dx
    mov [bp-14],ax
    les bx,[bp-14]
    mov byte ptr es:[bx],' '
    inc word ptr [bp-14]
    mov ax,[bp+8]
    or ax,[bp+10]
    je copy_arguments_if_requested
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp-12]
    push word ptr [bp-14]
    call __stpcpy
    add sp,8
    mov [bp-12],dx
    mov [bp-14],ax
    les bx,[bp-14]
    mov byte ptr es:[bx],' '
    inc word ptr [bp-14]
copy_arguments_if_requested:
    mov ax,[bp+12]
    or ax,[bp+14]
    je command_terminated
    mov dx,[bp+6]
    mov ax,[bp+4]
    mov [bp-4],dx
    mov [bp-6],ax
    jmp short argument_copy_test
argument_copy:
    les bx,[bp-6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    push word ptr [bp-12]
    push word ptr [bp-14]
    call __stpcpy
    add sp,8
    mov [bp-12],dx
    mov [bp-14],ax
    les bx,[bp-14]
    mov byte ptr es:[bx],' '
    inc word ptr [bp-14]
    add word ptr [bp-6],4
argument_copy_test:
    les bx,[bp-6]
    mov ax,es:[bx]
    or ax,es:[bx+2]
    jne argument_copy
command_terminated:
    les bx,[bp-14]
    mov byte ptr es:[bx-1],13
    mov byte ptr es:[bx],0
    mov ax,[bp-14]
    xor dx,dx
    sub ax,[bp-10]
    sbb dx,0
    add al,-2
    les bx,[bp-10]
    mov es:[bx],al
    mov dx,[bp-8]
    mov ax,[bp-10]
command_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    ret 12
__DOSCMD endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
