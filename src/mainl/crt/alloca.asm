; Original Japanese Borland alloca: complete platform/runtime member.
; Preserve register ABI, interrupt behavior, storage and native relocation order.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _alloca
; Complete disjoint instruction chunks follow original OMF field chronology.

org 0
_alloca label far
    pop bx
    pop es
    pop ax
    add ax, 1
    and ax, 0fffeh
    neg ax
    add ax, sp
    mov cx, ax
    sub cx, 0ah
    cmp cx, sp
    ja short alloca_overflow
    mov cx, bp
    mov bp, sp
    mov sp, ax
    push word ptr [bp+2]
    push word ptr [bp]
    mov dx, ss
    mov bp, cx
alloca_return:
    sub sp, 2
    push es
    push bx
    retf
alloca_overflow:
    xor ax, ax
    mov dx, ax
    jmp short alloca_return
_TEXT ends
end
