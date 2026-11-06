; Own the original static 80-byte BSS result buffer and literal PATH name.
; Original Japanese Borland srchpath: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
extrn __searchenv:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
path_variable_name db 'PATH',0
_DATA ends
_BSS segment word public 'BSS'
path_buffer db 80 dup (?)
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _searchpath
; Complete disjoint instruction chunks preserve original native field order.

org 33
    call __searchenv
    add sp, 0ch
    les bx, dword ptr [bp-4]
    cmp byte ptr es:[bx], 0
    jne short return_path_buffer
    xor dx, dx
    xor ax, ax
    jmp short searchpath_return
return_path_buffer:
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
searchpath_return:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 23
    mov ax,offset DGROUP:path_variable_name
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 11
    mov word ptr [bp-4],offset DGROUP:path_buffer
    push word ptr [bp-2]
    push word ptr [bp-4]
    push ds

org 0
_searchpath label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov word ptr [bp-2], ds
_TEXT ends
end
