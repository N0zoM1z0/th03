; Original Japanese Borland _access: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
include crt_errno.inc
extrn __rtl_chmod:far
extrn _errno:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __access
; Complete disjoint instruction chunks preserve original native field order.

org 46
access_denied:
    mov word ptr DGROUP:_errno, EACCES
    mov ax, 0ffffh
access_return:
    pop di
    pop si
    pop bp
    retf

org 14
    call __rtl_chmod
    add sp, 6
    mov dx, ax
    cmp dx, -1
    jne short check_write_access
    jmp short access_return
check_write_access:
    test byte ptr [bp+0ah], 2
    je short access_allowed
    test dl, 1
    jne short access_denied
access_allowed:
    xor ax, ax
    jmp short access_return

org 0
__access label far
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
