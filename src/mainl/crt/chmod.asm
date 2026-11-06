; Original Japanese Borland chmod: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
extrn __rtl_chmod:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _chmod
; Complete disjoint instruction chunks preserve original native field order.

org 52
    call __rtl_chmod
    add sp, 8
    mov dx, ax
    cmp dx, -1
    jne short attribute_success
return_attribute_error:
    mov ax, dx
    jmp short chmod_return
attribute_success:
    xor ax, ax
chmod_return:
    pop di
    pop si
    pop bp
    retf

org 14
    call __rtl_chmod
    add sp, 6
    mov dx, ax
    cmp dx, -1
    je short return_attribute_error
    and dx, 0fffeh
    test byte ptr [bp+0ah], 080h
    jne short write_dos_attributes
    or dx, 1
write_dos_attributes:
    push dx
    mov ax, 1
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 0
_chmod label far
    push bp
    mov bp, sp
    push si
    push di
    xor ax, ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
end
