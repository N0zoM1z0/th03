; Original Japanese Borland stack: complete platform/runtime member.
; Preserve register ABI, interrupt behavior, storage and native relocation order.
.8086
extrn __exit:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public F_OVERFLOW@
public N_OVERFLOW@
public OVERFLOW@
; Complete disjoint instruction chunks follow original OMF field chronology.
overflow_message db 'Stack overflow!',13,10,'$'

org 24
    mov dx,offset overflow_message
    mov ah, 9
    int 021h
    mov ds, bx

org 33
    jmp near ptr __exit

org 18
F_OVERFLOW@ label near
N_OVERFLOW@ label near
OVERFLOW@ label near
overflow_exit:
    mov bx, ds
    mov ax, cs
    mov ds, ax
_TEXT ends
end
