; Original Japanese Borland pc98mous: complete platform/runtime member.
; Preserve register ABI, interrupt behavior, storage and native relocation order.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_BSS segment word public 'BSS'
mouse_user_callback dd ?
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _pc98mouse
assume es:DGROUP
; Complete disjoint instruction chunks follow original OMF field chronology.

org 15
    call dword ptr DGROUP:mouse_user_callback
    add sp, 8
    pop ds
    pop di
    pop si
    retf
_pc98mouse label far
    push bp
    mov bp, sp
    push si
    push di
    push ds
    push ds
    pop es
    lds si, dword ptr [bp+8]
    mov ax, ds
    or ax, si
    mov ax, word ptr [bp+6]
    je short mouse_without_register_block
    mov dx, word ptr [si+6]
    cmp ax, 0ch
    jne short mouse_check_cursor_shape
    mov dx, word ptr [si+0ch]

org 57
    mov word ptr es:mouse_user_callback, dx
    mov dx, word ptr [si+0eh]

org 65
    mov word ptr es:mouse_user_callback+2, dx
    push cs
    pop es

org 4
    mov ax,seg DGROUP
    mov ds, ax
    pop ax
    cld
    push dx
    push cx
    push bx
    push ax

org 72
    mov dx,offset mouse_callback_entry
mouse_check_cursor_shape:
    cmp ax, 9
    jne short mouse_interrupt
    les dx, dword ptr [si+8]
mouse_interrupt:
    mov bx, word ptr [si+2]
    mov cx, word ptr [si+4]
    int 033h
    lds si, dword ptr [bp+8]
    mov word ptr [si], ax
    mov word ptr [si+2], bx
    mov word ptr [si+4], cx
    mov word ptr [si+6], dx
    jmp short mouse_return
mouse_without_register_block:
    int 033h
mouse_return:
    pop ds
    pop di
    pop si
    pop bp
    retf

org 0
mouse_callback_entry:
    push si
    push di
    push ds
    push ax
_TEXT ends
end
