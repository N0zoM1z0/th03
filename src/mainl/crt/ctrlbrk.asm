; Original Japanese Borland ctrlbrk: complete platform/runtime member.
; Preserve register ABI, interrupt behavior, storage and native relocation order.
.8086
extrn _setvect:far
extrn __exit:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
break_data_segment label byte
_DATA ends
_BSS segment word public 'BSS'
break_user_callback dd ?
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _ctrlbrk
; Complete disjoint instruction chunks follow original OMF field chronology.

org 71
    call _setvect
    add sp, 6
    pop di
    pop si
    pop bp
    retf

org 63
    mov ax,offset break_interrupt_entry
    push ax
    mov ax, 023h
    push ax

org 59
    mov ax,seg break_interrupt_entry
    push ax

org 56
    mov word ptr DGROUP:break_user_callback, ax

org 52
    mov word ptr DGROUP:break_user_callback+2, dx

org 25
    call __exit
    pop cx
break_restore_registers:
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
_ctrlbrk label far
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]

org 14
    call dword ptr DGROUP:break_user_callback
    or ax, ax
    jne short break_restore_registers
    xor ax, ax
    push ax

org 9
    mov bp,seg DGROUP:break_data_segment
    mov ds, bp

org 0
break_interrupt_entry:
    push ax
    push bx
    push cx
    push dx
    push es
    push ds
    push si
    push di
    push bp
_TEXT ends
end
