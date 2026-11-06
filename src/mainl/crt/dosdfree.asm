; Original Japanese Borland dosdfree: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
include crt_errno.inc
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
public __dos_getdiskfree
; Complete disjoint instruction chunks preserve original native field order.

org 23
    mov word ptr DGROUP:_errno, ax
    jmp short diskfree_return
store_disk_statistics:
    mov word ptr [bp-2], bx
    les bx, dword ptr [bp+8]
    mov word ptr es:[bx], dx
    mov word ptr es:[bx+4], ax
    mov word ptr es:[bx+6], cx
    mov ax, word ptr [bp-2]
    mov word ptr es:[bx+2], ax
    xor ax, ax
diskfree_return:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 0
__dos_getdiskfree label far
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    mov dl, byte ptr [bp+6]
    mov ah, 036h
    int 021h
    cmp ax, 0ffffh
    jne short store_disk_statistics
    mov ax, EINVAL
_TEXT ends
end
